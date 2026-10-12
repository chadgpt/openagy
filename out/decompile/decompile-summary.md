# Decompile summary — antigravity (Go 1.28-20260921-RC02)

> Source: `/workspace/agy/install/antigravity` (214 MB ELF64 x86-64 PIE stripped)
> Decompiler: Ghidra 12.1.4 (DecompInterface, 60s/func timeout)
> Priority list: `/workspace/agy/out/decompile/priority-funcs.txt` (1498 funcs across 26 Go packages)
> Decompiled output: `/workspace/agy/out/decompile/dec/<HEX>_<safename>.c`

## Headline numbers

| Metric | Value |
|---|---|
| Total priority funcs | 1498 |
| Decompiled OK | 860 (57%) |
| Skipped/errored | 638 (42%) |
| Go packages covered | 26 |
| Total decompiled LOC | 297,104 |

## Per-package breakdown

| Functions | Decompiled | LOC | Package |
|---:|---:|---:|---|
| 600 | 324 | 157,083 | `google3/third_party/jetski/cli/store/store.` |
| 193 | 129 | 19,772 | `google3/third_party/jetski/cli/backend/backend.` |
| 167 | 104 | 18,188 | `google3/third_party/jetski/language_server/code_assist_client/codeassistclient.` |
| 140 | 69 | 12,896 | `google3/third_party/jetski/cli/commands/commands.` |
| 120 | 61 | 43,997 | `google3/third_party/jetski/cli/store/store` |
| 67 | 42 | 7,828 | `google3/third_party/jetski/cli/printmode/printmode` |
| 58 | 40 | 9,144 | `google3/third_party/jetski/cli/backend/auth/auth.` |
| 48 | 27 | 3,171 | `google3/third_party/jetski/cli/backend/backend` |
| 36 | 20 | 12,988 | `google3/third_party/jetski/cli/printmode/printmode.` |
| 26 | 12 | 3,409 | `google3/third_party/jetski/cli/commands/commands` |
| 13 | 13 | 1,992 | `google3/third_party/jetski/cli/backend/auth/auth` |
| 4 | 2 | 676 | `google3/third_party/jetski/cli/backend/auth/auth..embed.1.0.google3/third_party/jetski/cli/backend/auth/auth.` |
| 4 | 1 | 1,297 | `google3/third_party/jetski/language_server_pb/language_server_go_grpc.` |
| 3 | 3 | 350 | `google3/third_party/jetski/cli/backend/backend.ContextWindow` |
| 3 | 3 | 117 | `google3/third_party/jetski/cli/store/store.OSC52Clipboard` |
| 3 | 3 | 301 | `google3/third_party/jetski/language_server/code_assist_client/codeassistclient` |
| 2 | 1 | 331 | `google3/third_party/jetski/cli/store/store.ExitState` |
| 2 | 1 | 14 | `google3/third_party/jetski/cli/store/store.FileClipboard` |
| 2 | 2 | 119 | `google3/third_party/jetski/language_server_pb/language_server_go_proto` |
| 1 | 0 | 0 | `google3/third_party/jetski/cli/backend/backend.AgentModel` |
| 1 | 1 | 3,209 | `google3/third_party/jetski/cli/backend/backend.newUpdateQueue` |
| 1 | 1 | 31 | `google3/third_party/jetski/cli/printmode/printmode.pollResponse` |
| 1 | 1 | 191 | `google3/third_party/jetski/cli/store/store.HintMask` |
| 1 | 0 | 0 | `google3/third_party/jetski/cli/store/store.OSC52Clipboard.WriteAll` |
| 1 | 0 | 0 | `google3/third_party/jetski/cli/store/store.RegisterCLIFeatureProviderLoader.func1` |
| 1 | 0 | 0 | `google3/third_party/jetski/cli/store/store.Store` |

## Top auth-flow packages


## Files

- This summary: `decompile-summary.md`
- Per-package reports: `decompile-<package-slug>.md`
- Decompiled C pseudocode: `/workspace/agy/out/decompile/dec/<HEX>_<short>.c`
- Errors / skips: `/workspace/agy/out/decompile/dec/_errors.txt`
- Decompile run summary: `/workspace/agy/out/decompile/dec/_summary.txt`
