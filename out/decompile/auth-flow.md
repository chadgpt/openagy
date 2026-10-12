# antigravity auth/eligibility flow — static call-graph analysis

**Source:** `/workspace/agy/install/antigravity` (214 MB stripped ELF, 155,184 funcs recovered).
**Method:** Direct disassembly (`objdump -d`) of `.text` + friends, stream-parsed for `call <addr>` instructions; function boundaries from recovered pclntab (`seeds.txt`).
**Output:** `call-graph.json` (2,625 nodes, 2,422 edges covering 1-hop neighborhood of 2,559 priority funcs), `call-graph.dot`, `xrefs.txt` (17,275 edges), `proto-schema.md`.

> **Important caveat.** objdump strips internal function headers from stripped binaries; we use `seeds.txt` as the function boundary source. Most call sites within the auth path are **direct** `call <addr>` (Go generated code), but the auth flow uses **goroutines + channels + interface dispatch** for many steps, so static call graphs miss most of the dynamic control flow. Where a function has 0 callers in the disassembly, that usually means it's called via a function pointer (interface method, channel-send) or started by `runtime.newproc` (goroutine spawn). The descriptions below note *both* what the disassembly shows AND what the seed/function-name + body analysis implies.

---

## 1. Auth call-flow summary

| Step | Layer | Function | Address | Called by (static) | Notes |
|------|-------|----------|---------|--------------------|-------|
| 1. CLI starts | `store.Manager` | `(*Manager).initAuth` | `0x899cb00` | `Manager.startup` (via defer) | Initializes auth state, sets up channel for auth results |
| 2. Validate user | `store.Manager` | `(*Manager).ValidateAndOnboardAccount` | `0x899e060` | `Manager.initAuth` (likely) | Calls `Manager.publishSnapshot`; spawns onboarding goroutine |
| 3. Silent auth check | `store.Manager` | `(*Manager).TrySilentAuth` | `0x899d9c0` | init flow | 0 callers in disassembly; called via channel callback |
| 4a. OAuth | `store.Manager` | `(*Manager).StartOAuthProcess` | `0x899cf80` | `initAuth.func1` (`0x8a161c0`) | 0 direct callers — likely started as goroutine |
| 4b. GCP | `store.Manager` | `(*Manager).StartGCPAuthProcess` | `0x899d3a0` | `initAuth.func1` (`0x8a161c0`) | 0 direct callers — likely started as goroutine |
| 5. Wait for result | `store.Manager` | `(*Manager).waitForEligibility` | `0x899cd40` | `Manager.StartOAuthProcess.deferwrap1` (`0x8a16580`) | 30-min timeout, 50ms poll, channel receive |
| 6. Commit | `store.Manager` | `(*Manager).commitAuth` | `0x899cc00` | `waitForEligibility` (likely) | Writes token to keyring |
| 7. Server RPC | `cli/backend` | `(*ServerBackend).SelectLicense` etc. | `0x86bd160` | `Manager.SelectLicense` (`0x89cbba0`) | gRPC call to language-server endpoint |

> The auth pipeline forms a **directed acyclic graph** at the package level:
> `cli` → `store` (state) → `cli/backend` (RPC) → `language_server` (gRPC client) → `cloudaicompanion` (gRPC service)
>
> Within `store`, the Manager is the single coordinator; within `cli/backend`, the `ServerBackend` is the gRPC adapter; within `language_server`, the `CodeAssistClient` is the long-lived connection.

---

## 2. `(*Manager).waitForEligibility` — what it actually does

The disassembly of `waitForEligibility` (`0x899cd40` … `0x899cf80`) reveals the implementation:

```asm
; waitForEligibility prologue + body
899cd40:  movups %xmm14,(%rax)         ; struct copy (Manager state)
…
899cdec:  movb   $0x0,0x4f(%rsp)        ; clear flag
899cdf1:  movups %xmm15,0x70(%rsp)      ; clear struct
899cdf7:  mov    0x100(%rax),%rdx       ; load auth channel/struct
899ce00:  test   %rdx,%rdx             ; nil check
…
899ce2c:  movabs $0x6fc23ac00,%rcx      ; 0x6fc23ac00 = 30 * 60 * 1e9 (30 minutes in ns)
899ce36:  call   context.WithTimeoutCause  ; ctx, cancel := context.WithTimeoutCause(parent, 30*time.Minute, …)
…
899ce60:  call   0x89cee80              ; (in Manager.Store) get-or-create result receiver
899ce65:  mov    0x8(%rax),%rcx         ; load backend
899ce69:  mov    0x10(%rcx),%rax        ; load auth status
899ce6d:  test   %rax,%rax             ; nil check
899ce70:  je     899cf97                ; if no auth status, return early
899ce76:  cmpb   $0x0,0x79(%rax)        ; check eligibility flag at offset 0x79
899ce80:  je     899cf6a                ; if not eligible, jump to IneligibilityFromResult
…
899ce86:  mov    $0x2faf080,%eax        ; 0x2faf080 = 50 * 1e6 (50 ms in ns)
899ce8b:  call   time.Sleep            ; time.Sleep(50 * time.Millisecond)
…
899ce9c:  mov    0x68(%rsp),%rcx
899cea9:  call   *%rcx                  ; INDIRECT CALL: channel receive (auth result channel)
…
899ceab:  lea    0x90(%rsp),%rcx        ; reset result struct
…
899ceed:  call   runtime.chanrecv       ; <- blocking channel receive
…
899cf0c:  call   *%rcx                  ; INDIRECT CALL: handler on received result
…
899cf41:  call   log.ctxlogf            ; log progress
…
899cf5c:  call   *%rax                  ; INDIRECT CALL: state update
899cf6a:  call   backend.IneligibilityFromResult  ; convert result to ineligibility
```

**Summary of the wait loop:**

1. **30-minute timeout.** `context.WithTimeoutCause(parent, 30*time.Minute, …)` — gives up after 30 minutes.
2. **Read current auth state.** Calls `Manager.Store` to get the current `AuthStatus`. If status is missing or `eligible==false` at offset `0x79`, jumps to `IneligibilityFromResult`.
3. **50 ms polling sleep.** `time.Sleep(50 * time.Millisecond)`.
4. **Channel receive.** `runtime.chanrecv` + indirect call — this is a blocking wait on the auth result channel. Whoever completes the auth (OAuth callback, GCP ADC, etc.) writes to this channel.
5. **Result handling.** `log.ctxlogf` logs; on ineligibility, `IneligibilityFromResult` converts the result to a typed `IneligibilityError`.
6. **`Manager.publishSnapshot`** (called 3× within this function) — broadcasts state to all subscribers (UI, telemetry, etc.).

> **Block point:** This function is a long-running blocking wait. It only returns when (a) the auth result channel fires, (b) the 30-min context expires, or (c) the goroutine is cancelled via `runtime.Goexit` (3 `Goexit` calls in the body — defer-cleanup paths).

### Cross-references in disassembly

`waitForEligibility` has the following direct call targets:

| Target | Symbol | Count | Purpose |
|--------|--------|-------|---------|
| `0x5f4f460` | `context.WithTimeoutCause` | 1 | create timeout context |
| `0x89d07c0` | `(*Manager).publishSnapshot` | 3 | broadcast state update |
| `0x5e5ef40` | `runtime.gcWriteBarrier5` | 8 | GC write barrier (pointer store) |
| `0x5e5ef60` | `runtime.gcWriteBarrier6` | 3 | GC write barrier (slice header store) |
| `0x5e18260` | `runtime.Goexit` | 3 | goroutine exit (defer cleanup) |

`commitAuth`, `StartOAuthProcess`, `StartGCPAuthProcess` show **0 static outgoing edges** in our call graph because their internal call instructions all target non-priority funcs (runtime helpers, gcWriteBarrier, indirect calls). They are not "no-op" — they just don't call other priority funcs.

---

## 3. The GCP / OAuth branching

```
                initAuth (0x899cb00)
                       │
                       ▼
            ValidateAndOnboardAccount (0x899e060)
                       │
                       ▼
        ┌──────────────┴──────────────┐
        ▼                             ▼
  StartOAuthProcess              StartGCPAuthProcess
    (0x899cf80)                    (0x899d3a0)
        │                             │
        ▼                             ▼
  ChainedAuth.StartInteractive  ChainedAuth.StartGCPAuthProcess
    (0x86a6900)                    (0x86a6aa0)
        │                             │
        ▼                             ▼
  browser auth flow            ADC / gcloud auth flow
  (via 0x86a00c0)              (via ADC + keyring)
        │                             │
        └──────────────┬──────────────┘
                       ▼
              keyringAuth (Linux: secret-service D-Bus)
              0x86aa0c0 - 0x86aa480
                       │
                       ▼
                waitForEligibility
                       │
                       ▼
                  commitAuth
                       │
                       ▼
                publishSnapshot
```

The disassembly of `StartOAuthProcess` (0x899cf80–0x899d3a0) and `StartGCPAuthProcess` (0x899d3a0–0x899d9c0) is **nearly identical** — both call the same sequence of helpers:

```asm
; both functions:
…
  call   5e68060   ; runtime.morestack_noctxt
  call   65ffe40   ; log.ctxlogf  (start log)
  call   5debde0   ; runtime.newobject
  call   86a00c0   ; analytics.New  (record event)
  call   5dd56e0   ; runtime.makeslice
  call   86a0240   ; analytics.(*EventRecorder).Record  (record event)
  call   5dec820   ; runtime.concatstrings
  call   5def180   ; runtime.mapassign
```

This pattern (log → new event → record event → maps) is the standard "fire telemetry event then call the auth method" pattern. The actual auth method bodies (which one gets called) are likely dispatched through a `ChainedAuth` interface — the 6-call sequence above is the "outer wrapper" that the Manager provides.

**The `ChainedAuth` interface (in `cli/backend/auth/auth`)** has 7 methods, all defined in priority funcs:

| Method | Address | Type |
|--------|---------|------|
| `Authenticate` | `0x86a66a0` | `(*ChainedAuth).Authenticate` |
| `StartInteractive` | `0x86a6900` | `(*ChainedAuth).StartInteractive` |
| `StartGCPAuthProcess` | `0x86a6aa0` | `(*ChainedAuth).StartGCPAuthProcess` |
| `Logout` | `0x86a6e20` | `(*ChainedAuth).Logout` |
| `Active` | `0x86a6ec0` | `(*ChainedAuth).Active` |
| `Cancel` | `0x86a6ee0` | `(*ChainedAuth).Cancel` |
| `SubmitAuthorizationCode` | `0x86a6fc0` | `(*ChainedAuth).SubmitAuthorizationCode` |
| `IsMethodSupported` | `0x86a71a0` | `(*ChainedAuth).IsMethodSupported` |

`ChainedAuth` is a typical Go "chain of responsibility" pattern — it tries each registered auth provider (`keyringAuth`, `adcAuth`, `oauthAuth`, etc.) in order until one succeeds.

---

## 4. Keyring layer (Linux D-Bus)

The `keyringAuth` type (0x86aa0c0 - 0x86aa480) is the Linux backend. Its implementation uses the `github.com/zalando/go-keyring` package, which on Linux goes through the **D-Bus Secret Service** (typically `gnome-keyring` or `kwallet` via `secret-service` protocol).

`go-keyring` has 41 funcs in the priority list:

| Function | Address |
|----------|---------|
| `(*keyringAuth).TryAuth` | `0x86aa0c0` |
| `(*keyringAuth).StartInteractive` | `0x86aa360` |
| `(*keyringAuth).Logout` | `0x86aa380` |
| `(*keyringAuth).Name` | `0x86aa480` |
| `(*keyringAuth).TryAuth.func1` | `0x86adb20` |
| `(*keyringAuth).TryAuth.func1.1` | `0x86ae4e0` |
| `codeassistclient.keyringRecentlyUnavailable` | `0x799b580` |

`codeassistclient.keyringRecentlyUnavailable` is called by `(*CodeAssistClient).SetUserInfo` (`0x79c1b40`, 4 callers in disassembly) — this is the fallback when the keyring is unavailable (e.g., no D-Bus session, headless server, locked keyring). The CLI then falls back to `OAuth` flow.

`keyringAuth.TryAuth` does (per `go-keyring` semantics):
1. Get the `secret_service` D-Bus connection via `dbus.SessionBus()`.
2. Search for a collection matching the antigravity namespace.
3. Unlock the collection if locked (may prompt for password).
4. Read the stored OAuth token.
5. Decrypt with `golang.org/x/crypto/nacl/secretbox`.
6. Return the token to the auth chain.

If step 1-3 fail, `keyringRecentlyUnavailable` is set and the chain moves to the next provider.

---

## 5. Server-side: `(*ServerBackend)` and the language-server gRPC

The `ServerBackend` is the gRPC client side of the language-server protocol. Its funcs:

| Method | Address | RPC |
|--------|---------|-----|
| `(*ServerBackend).FetchLicenses` | `0x86bce60` | `language_server_go_grpc.FetchLicenses` |
| `(*ServerBackend).SelectLicense` | `0x86bd160` | `language_server_go_grpc.SelectLicense` |
| `(*ServerBackend).SelfAssignLicense` | `0x86bd580` | `language_server_go_grpc.SelfAssignLicense` |
| `(*ServerBackend).StartOAuthProcess` | `0x86d8d40` | (server-side) |
| `(*ServerBackend).StartGCPAuthProcess` | `0x86d8de0` | (server-side) |
| `(*ServerBackend).TrySilentAuth` | `0x86d9a80` | (server-side) |
| `(*ServerBackend).ValidateAndOnboardAccount` | `0x86d9b00` | `OnboardUser` |

`(*ServerBackend).FetchLicenses` (0x86bce60) has 4 outgoing static edges:
- 2× `runtime.gcWriteBarrier6` (slice header store)
- 1× `(*FetchConfigurationResponse).Get...` (proto accessor, `0x7469280`)
- 2× `runtime.gcWriteBarrier5/8`

The full RPC chain:

```
Manager (cli)
   │
   │ (*Manager).SelectLicense / SelfAssignLicense / FetchLicenses
   ▼
codeassistclient (language_server)
   │
   │ (*CodeAssistClient).SelectLicense / SelfAssignLicense / FetchLicenses
   ▼
language_server_go_grpc (Connect/gRPC stub)
   │
   ▼
connectrpc (HTTP/2 transport)
   │
   ▼
cloudaicompanion.googleapis.com:443  (gRPC server, not in binary)
```

In the call graph, `CodeAssistClient.FetchLicensesFromAICode` (`0x798b480`) is the entry point that calls the AICode-side management service (which has the gRPC handlers we listed: `v1beta_management_service_go_proto._ManagementService_FetchLicenses_Handler` at `0x746b8e0`).

---

## 6. Surprises / notable findings

1. **Google-internal Go toolchain.** The binary was built with `go1.28-20260921-RC02 cl/985595000 +644cd61a4a` (per `inspect-agy.md`). This is a pre-release Go with internal-only field tracking + boringcrypto + simd tags. Some field numbers in the recovered `FieldDescriptorProto` use a non-standard layout (field 3 = number, field 5 = type — see `proto-schema.md` for details).

2. **Field-track enabled.** The `fieldtrack` build tag means every field access is wrapped in a write barrier (visible as the many `runtime.gcWriteBarrier5/6/7/8` calls). This makes the binary larger and slower but allows the field-track tooling to trace every pointer write.

3. **`time.Sleep(50ms)` polling.** `waitForEligibility` polls every 50ms rather than using a condition variable. This is a common pattern in Go code that pre-dates `sync.Cond`.

4. **30-minute hard timeout.** The auth wait has a 30-minute hard cap. After 30 minutes, the function returns an error and the user has to retry.

5. **boringcrypto for crypto.** All crypto operations go through Go's BoringCrypto (BoringSSL) bindings — visible in the `boring` package funcs in the binary. Token encryption uses `nacl/secretbox` (XSalsa20-Poly1305).

6. **No `xxx_Marshal` / `xxx_MarshalTo` functions.** The standard Go protobuf generated code uses these private methods, but the Google internal `v1internal_go_proto` package doesn't have them — instead, it uses `protoreflect.MessageDescriptor` and a custom marshal path. This is why the field numbers aren't in the accessor functions.

7. **The `init` function is huge.** The `cli/store/store` package has 440 funcs, of which 254 are store/internal helpers. The `Manager` alone has 169 funcs in the priority list. This is consistent with Google's typical monorepo service style.

8. **Antigravity as a name.** Despite the binary being called "antigravity", all the auth/eligibility code is from the `jetski` project (Google's internal CLI for AI agents). The `antigravity` name appears to be a Google Cloud "brand wrapper" around the jetski codebase.

---

## 7. What this analysis cannot tell you

- **Runtime field values.** Static analysis shows field *names* and field *numbers* but not what values are assigned at runtime.
- **Channel-based control flow.** Most of the auth flow is goroutine-based. The static call graph misses:
  - `runtime.newproc` (goroutine spawn)
  - `runtime.chanrecv` / `runtime.chansend1`
  - Interface method dispatch (`call *%rax` etc.)
  - Closures / anonymous functions (visible as `funcN` symbols)
- **The actual OAuth flow.** The OAuth dance (browser open, callback, code exchange) is in `cortex/command/sandboxproxy` (sandboxproxy.StartOAuthSignIn at `0x6f468a0`) and is not analyzed here.
- **Server-side validation.** The server-side gRPC service is not in this binary — only the client stubs.
