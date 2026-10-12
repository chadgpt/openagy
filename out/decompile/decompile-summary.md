# Decompile summary — antigravity (Go 1.28-20260921-RC02)

> Source: `/workspace/agy/install/antigravity` (214 MB ELF64 x86-64 PIE stripped)
> Decompiler: Ghidra 12.1.4 (DecompInterface, 60s/func timeout)
> Priority list: `/workspace/agy/out/decompile/priority-funcs.txt` (1498 funcs across 26 Go packages)
> Decompiled output: `/workspace/agy/out/decompile/dec/<HEX>_<safename>.c`
> Per-package reports: `decompile-<slug>.md`
> Run logs: `logs/analyzeHeadless2.log`, `dec/_summary.txt`, `dec/_errors.txt`

## Headline numbers

| Metric | Value |
|---|---|
| Total priority funcs | 1498 |
| Decompiled OK | 860 (57%) |
| Skipped/errored | 638 (42%) |
| Go packages covered | 26 |
| Total decompiled LOC | 297,104 |
| Run time (decompile only) | ~3 min (220s) |
| Run time (seeds preScript) | ~5 min (155K funcs apply) |

## Auth/eligibility flow packages

| Functions | Decompiled | LOC | Package |
|---:|---:|---:|---|
| 731 | 391 | 201,733 | `google3/third_party/jetski/cli/store` |
| 321 | 215 | 38,314 | `google3/third_party/jetski/cli/backend` |
| 104 | 63 | 20,847 | `google3/third_party/jetski/cli/printmode` |
| 166 | 81 | 16,305 | `google3/third_party/jetski/cli/commands` |
| 170 | 107 | 18,489 | `google3/third_party/jetski/language_server/code_assist_client` |

## All packages

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

## Key auth/eligibility findings (1-2 line summary each)

- **`waitForEligibility`** (`cli/store/Manager`): Blocks session start until backend reports eligibility (license tier, business flag, etc.). Polls the LSP server's GetStatus RPC.
- **`StartOAuthProcess`** (`cli/store/Manager`): Initiates OAuth device-code flow: requests device code from `oauth2.googleapis.com/device/code`, opens browser for user to authorize, then polls token endpoint.
- **`StartGCPAuthProcess`** (`cli/store/Manager`): Alternative auth path: Application Default Credentials (ADC) via gcloud auth or service account key file. Calls into `iamcredentials.googleapis.com` for token exchange.
- **`CompleteGCPSetup`** (`cli/store/Manager`): Wraps up ADC: sets quota project, region, ADC environment, persists to `~/.config/gcloud/application_default_credentials.json`.
- **`TrySilentAuth`** (`cli/store/Manager`): Re-uses cached refresh token without user interaction. Reads from `~/.config/antigravity/auth.json` (or similar) and silently refreshes via OAuth2 refresh_token grant.
- **`SubmitOAuthAuthorizationCode`** (`cli/store/Manager`): Exchanges user-supplied OAuth code (PKCE) for access+refresh tokens, stores them in OS keyring (Linux: libsecret/Secret Service, macOS: Keychain).
- **`SubmitVertexAPIKey`** (`cli/store/Manager`): Alternative auth: user supplies a Vertex AI API key directly; stored in keyring, no OAuth flow needed.
- **`Logout`** (`cli/store/Manager`): Clears stored credentials (keyring + cached file), resets auth state, notifies LSP server to drop entitlement cache.
- **`commitAuth`** (`cli/store/Manager`): Commits the auth state transactionally into the Manager (used by the auth state machine).
- **`CLIAuthProvider.GetTokenSource`** (`codeassistclient`): Default auth provider when running as CLI: returns a `RefreshingTokenSource` that auto-refreshes OAuth access tokens using stored refresh token.
- **`AntigravityHubAuthProvider.GetTokenSource`** (`codeassistclient`): Auth provider when running inside the Antigravity IDE (Hub): pulls tokens from a local IPC socket/Unix domain socket set up by the IDE.
- **`HostAuthProvider.GetTokenSource`** (`codeassistclient`): Auth provider for the host (server/headless) mode: reads tokens from a shared file location like `/var/run/antigravity/auth.json`.
- **`IDEAuthProvider.GetTokenSource`** (`codeassistclient`): Legacy IDE auth provider: reads from environment variables or a config file specific to the calling IDE.
- **`StandaloneAuthProvider.GetTokenSource`** (`codeassistclient`): Standalone (no IDE) auth provider: identical behavior to CLI but used in different contexts.
- **`StubbyAuthProvider.GetTokenSource`** (`codeassistclient`): Google-internal: gets tokens via Stubby (Google's internal RPC proxy) when running inside Google.
- **`GeminiAPIKeyAuthProvider.GetTokenSource`** (`codeassistclient`): API-key-only path: uses a raw Gemini API key for `generativelanguage.googleapis.com` calls, no OAuth flow.
- **`RefreshingTokenSource`** (`codeassistclient`): Token source wrapper that wraps a base token source and auto-refreshes on 401/expiry.
- **`FetchLicensesFromAICode`** (`codeassistclient`): Calls the `aicode.googleapis.com` ManagementService.FetchLicenses RPC to discover which licenses the user has (free/standard/pro/enterprise).
- **`SelfAssignLicense`** (`codeassistclient`): Calls `SelectLicense`/`SelfAssignLicense` RPC to attach a license to the current user/session.
- **`parseIDToken`** (`codeassistclient`): Decodes the JWT `id_token` from the OAuth response to extract user email, picture, tier claims without signature verification.

## Auth endpoints / OAuth client IDs found in binary

- OAuth2 device code: `https://oauth2.googleapis.com/device/code`
- OAuth2 token: `https://oauth2.googleapis.com/token` and `https://oauth2.mtls.googleapis.com/token` (mTLS variant)
- Service account impersonation: `https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/...`
- Main backend: `https://cloudcode-pa.googleapis.com` (Cloud Code Public API)
- License/management: `https://aicode.googleapis.com` (AI Code API) and `https://daily-cloudcode-pa.googleapis.com`
- Auth staging: `https://autopush-cloudcode-pa.sandbox.googleapis.com`
- Gemini: `https://generativelanguage.googleapis.com`
- **OAuth Client ID 1** (CLI/Antigravity public): `1071006060591-tmhssin2h21lcre235vtolojh4g403ep.apps.googleusercontent.com`
- **OAuth Client ID 2** (IDE/internal): `884354919052-36trc1jjb3tguiac32ov6cod268c5blh.apps.googleusercontent.com`
- OAuth scopes: `https://www.googleapis.com/auth/cloud-platform`, `.../auth/cclog`, `.../auth/aicode`, `.../auth/drive.*`

## Files

- This summary: `decompile-summary.md`
- Per-package reports: `decompile-<slug>.md`
- Decompiled C pseudocode: `/workspace/agy/out/decompile/dec/<HEX>_<short>.c`
- Errors / skips: `/workspace/agy/out/decompile/dec/_errors.txt`
- Decompile run summary: `/workspace/agy/out/decompile/dec/_summary.txt`
- Original task: `/workspace/.mavis/plans/plan_d03b0152/plan.yaml`
