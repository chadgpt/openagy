# Local RE run — agy 1.3.4 (macOS/arm64)

> Target: `~/.local/bin/agy` — Mach-O 64-bit arm64, 181,130,800 B
> SHA-256: `9da414c0624c27aa2969a86030a070b5341c0657700512eba70b21725ce253f5`
> Go toolchain: `go1.28-20260921-RC02 cl/985595000 +644cd61a4a X:fieldtrack,boringcrypto,simd`
> (Google internal monorepo, package root `google3/third_party/jetski/…`)
>
> This is the **macOS case**. The committed `out/*.md` reports are the Linux/ELF case from
> the `/workspace/agy` sandbox. Addresses are not comparable between the two — only the
> `.text` base (`0x1000011c0` here) is shared in form.

## Result

| Metric | Value |
|---|---|
| Functions recovered from pclntab | **154,525** |
| Ghidra functions created from seeds | **154,506** (19 already existed, **0 failed**) |
| Priority functions decompiled | **2,101 / 2,101 (100%)** |
| Decompiled pseudocode | 307,357 LOC in `dec/` |
| Import wall time | 11 min |
| Decompile wall time | 56 s (1,959 funcs) + 13 s (142 more, resume) |

## Evidence grading

Per the repo convention: 【一手】 first-hand from the binary · 【反编译】 decompiled at a
confirmed address · 【strings】 string-table hit only · 【推测】 hypothesis.

---

## 1. Pipeline

Fully configured and run end-to-end on this machine. Commands are in `AGENTS.md`;
helpers in this directory:

| File | Purpose |
|---|---|
| `env.sh` | `JAVA_HOME` / `GHIDRA_INSTALL_DIR` / `REA_GHIDRA_SEED_FILE` |
| `build_priority.py` | seeds.txt → `priority-funcs.txt` (2,101 auth/CLI functions) |
| `build_plan.py` | name→address resolution → REA MCP plan JSONL |
| `build_reports.py` | `decompile-summary.md` + 93 per-package reports |
| `resolve_strings.py` | turn Ghidra `&UNK_<vaddr>,<len>` refs back into real strings |
| `ghidra-scripts/DecompilePriority.java` | the decompile postScript (paths rewritten) |

**`-noanalysis` is what makes this work.** The Linux/ELF pass in `out/` imported *with*
Ghidra's analyzers and got 860/1498 = 57 %, with 637 functions skipped because Go thunks
share an address with their target and Ghidra reported *"function X inside instruction
at Y"*. Importing with `-noanalysis` means no disassembly pass has run when the seeds are
applied, so there are no instruction boundaries to collide with — **0 failures, 100 %
decompile rate**. That is the single most useful thing learned from this run.

## 2. Hidden CLI flags【一手 + 反编译】

`main.hideFlagsForExternal` at `0x1028dd2f0` (`dec/1028dd2f0_hideFlagsForExternal.c`) is
13 identical blocks of the form:

```c
piVar1 = runtime_mapaccess1_faststr(…, &UNK_<vaddr>, <len>);
*(undefined1 *)(*piVar1 + 0x50) = 1;   /* 1 = Hidden */
```

Resolving each `UNK_` by `file_offset = vaddr − 0x100000000` and slicing by the emitted
length (Go's linker concatenates all short strings into one blob, so the length is
authoritative — reading to the next NUL returns neighbouring garbage):

| # | Flag | State |
|---|---|---|
| 1 | `app_data_dir` | hidden |
| 2 | `gemini_dir` | hidden |
| 3 | `bg-updater` | hidden |
| 4 | `cdp_port` | hidden |
| 5 | `local_chrome_user_data_dir` | hidden |
| 6 | `local_chrome_headless` | hidden |
| 7 | `use_local_chrome` | hidden |
| 8 | `release_base_url` | hidden |
| 9 | `csrf_token` | hidden |
| 10 | `host_bridge_url` | hidden |
| 11 | `read_host_bridge_token_from_stdin` | hidden |
| 12 | `use_host_auth` | hidden |
| 13 | `remote-control` | **explicitly made visible** (`= 0`) |

**Delta vs the older build in `docs/TUTORIAL.md` §6.3:** that one listed 11 hidden flags.
1.3.4 hides 12 — **`release_base_url` is new**. The last entry being set to `0` rather
than `1` is the documented "flip `remote-control` back to visible" behaviour.

These cluster into three capabilities: local-Chrome CDP control (4–7), host-bridge auth
(9–12), and path/URL overrides (1–2, 8).

## 3. Auth / eligibility【strings】

Every string the tutorial reported for the older build is still present, character for
character:

```
Your account is blocked due to a Terms of Service violation.
Verification required. Please complete verification in your browser to continue.
Unable to verify account eligibility.
Timed out waiting for the account-eligibility verdict; sending anyway
Print mode: eligibility verdict did not settle within %s; proceeding; the %s tool(s) instead require approval that settings cannot grant
```

New in 1.3.4:

```
Eligibility check failed: %w. Please log out (/logout) and log back in (/login).
The daily voice transcription limit for this account is used up; it resets in %s
There was a network issue connecting to the server, please try again.
```

Keyring circuit-breaker【strings】 — unchanged, still present:

```
Keyring SaveUserTier timed out after %v, falling back to file storage
failed to write keyring marker: %v
keyring-marker-*
Android (no OS keyring)
```

Confirmed at the code level: `codeassistclient.shouldBypassKeyring` (`0x1018c28f0`),
`codeassistclient.keyringRecentlyUnavailable` (`0x1018c2880`),
`(*compositeTokenStorage).memoizeKeyringTimeout` (`0x1018b2ae0`),
`(*compositeTokenStorage).LoadToken` (`0x1018b33c0`).

## 4. Endpoints【strings】

| Endpoint | Note |
|---|---|
| `https://cloudcode-pa.googleapis.com` | prod |
| `https://daily-cloudcode-pa.googleapis.com` | daily — **the CLI's default** |
| `https://autopush-cloudcode-pa.sandbox.googleapis.com` | autopush |
| `https://preprod-daily-cloudcode-pa.sandbox.googleapis.com` | **new in 1.3.4** |
| `https://aicode.googleapis.com` | AI Code / license management |
| `https://autopush-aicode.sandbox.googleapis.com` | **new in 1.3.4** |
| `https://antigravity-unleash.goog/api/` | feature flags |
| `https://antigravity-cli-auto-updater-974169037036.us-central1.run.app` | auto-updater |

The tutorial reported "4 environments"; 1.3.4 ships **6** distinct hosts, with a
`preprod` tier that did not exist before. Project number `974169037036` on the updater is
unchanged.

New LLM-gateway env vars【strings】, not in the older build:

```
AGY_LLM_GATEWAY_API_KEY
AGY_LLM_GATEWAY_HEADERS
AGY_LLM_GATEWAY_CA_CERT
```

Model strings present: `gemini-3.5-flash`, `gemini-3.6-flash`, `gemini-3.7-flash`,
`gemini-3.8-flash`, `chat-gemini-3.1-pro-low`, plus `claude-opus-4-6/4-8/5-5` and
`gemini-2_5-flash-lite`.

## 5. gRPC surface

The binary exposes a large `/exa.language_server_pb.LanguageServerService/` surface —
~60 methods including `GetUnleashData`, `GetMendelFlags`, `StreamAgentStateUpdates`,
`StartNarration`, `CreateWorktree`, `GetSkillMarketplaceLink`, `ListPluginAuthProviders`.
Plus `google.internal.cloud.code.v1internal.CloudCode/OnboardUser` and
`google.gca.aicode.v1main.PredictionService/FetchQuotaStatus`.

## 6. Where the REA wrapper still fails

- `rea analyze` — killed by the documented ~5.5 min internal timeout (`provider_timeout`,
  `timeout_ms: 330000`). No flag raises it.
- `rea --mcp` — `open_binary` succeeds in ~1 s (it only registers the artifact), then
  `binary_overview` triggers the Ghidra launch. At the default 2 G heap this fails fast
  with `Ghidra headless launch failed`. Raising the heap to 10 G gets much further — the
  run survived **621 s** (the seeds alone take ~10 min) — but the MCP server then exits
  `rc=0` without answering, leaving nothing behind. Measured across three attempts; not
  a usable path for this binary.
- REA defaults Ghidra's heap to `-Xmx2G` (`dist/ghidra/GhidraJavaLaunch.js:53`); override
  with `GHIDRA_HEADLESS_MAXMEM`. Even at 10 G the wrapper budget does not cover a
  154,525-seed import.

The direct `analyzeHeadless` path has none of these problems and is ~2 orders of
magnitude cheaper (11 min + 56 s, no re-analysis per query).

## 7. Hard constraints honoured

- The binary was never modified. SHA-256 above is of the on-disk file.
- `rea-go-seeds` still has **zero third-party dependencies** (stdlib only).
- All generated tooling is stdlib-only Python; the Ghidra script is Ghidra-API-only.
- Nothing outside `out/local-macos/` was touched; no credentials were read.

## 8. Open / unverified

- **30 s / 60 s eligibility timeouts** — still not readable from `strings` (the messages
  are `%s`-parameterized). Confirming them needs the immediates in the disassembly, as
  the older pass did (`0x2faf080` = 50 ms poll). Not re-done here.
- **Proto enum values** (`IneligibleTierReasonCodes`, `Mode`, `AuthMode`) — not attempted.
  Remember Google's modified `FieldDescriptorProto` puts the field number in wire field
  **3**, not 2.
- **No full auto-analysis was run.** `-noanalysis` is what produced the 100 % hit rate;
  a second pass *with* analyzers would give call-graph/fixup data but would reintroduce
  the thunk collisions.
- **Strings inside decompiled functions are mostly unresolved.** `resolve_strings.py`
  recovers 1,892 references, but only short literals emitted as `&UNK_…,len`. Long
  user-facing strings reach the code through Go's `concatstring` call path and are only
  visible to `strings(1)`.
