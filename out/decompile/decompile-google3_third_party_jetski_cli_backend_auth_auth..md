# Decompile report — `google3/third_party/jetski/cli/backend/auth/auth.`

> 58 priority functions in this Go package

**Decompiled:** 40/58

## `google3/third_party/jetski/cli/backend/auth/auth.(*ChainedAuth)`

_2 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x86a66a0` | `google3/third_party/jetski/cli/backend/auth/auth.(*ChainedAuth).Authenticate` | **yes** | |
| `0x86a71a0` | `google3/third_party/jetski/cli/backend/auth/auth.(*ChainedAuth).IsMethodSupported` | **yes** | |

## `google3/third_party/jetski/cli/backend/auth/auth.(*adcAuth)`

_4 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x86a5aa0` | `google3/third_party/jetski/cli/backend/auth/auth.(*adcAuth).TryAuth` | **yes** | |
| `0x86a5b00` | `google3/third_party/jetski/cli/backend/auth/auth.(*adcAuth).Authenticate` | **yes** | |
| `0x86a6280` | `google3/third_party/jetski/cli/backend/auth/auth.(*adcAuth).Logout` | **yes** | |
| `0x86a62a0` | `google3/third_party/jetski/cli/backend/auth/auth.(*adcAuth).Name` | **yes** | |

## `google3/third_party/jetski/cli/backend/auth/auth.(*adcTokenStorage)`

_1 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x86aabc0` | `google3/third_party/jetski/cli/backend/auth/auth.(*adcTokenStorage).LoadCredentials` | **yes** | |

## `google3/third_party/jetski/cli/backend/auth/auth.(*cliFileTokenStorage)`

_5 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x86aa780` | `google3/third_party/jetski/cli/backend/auth/auth.(*cliFileTokenStorage).updateStoredToken` | **yes** | |
| `0x86aaaa0` | `google3/third_party/jetski/cli/backend/auth/auth.(*cliFileTokenStorage).SaveToken` | **yes** | |
| `0x86aae40` | `google3/third_party/jetski/cli/backend/auth/auth.(*cliFileTokenStorage).LoadStoredToken` | **yes** | |
| `0x86ab5e0` | `google3/third_party/jetski/cli/backend/auth/auth.(*cliFileTokenStorage).RemoveToken` | **yes** | |
| `0x86ab6c0` | `google3/third_party/jetski/cli/backend/auth/auth.(*cliFileTokenStorage).SaveProjectAndRegion` | **yes** | |

## `google3/third_party/jetski/cli/backend/auth/auth.(*externalCorpLoginAuth)`

_1 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x86a9be0` | `google3/third_party/jetski/cli/backend/auth/auth.(*externalCorpLoginAuth).StartInteractive` | **yes** | |

## `google3/third_party/jetski/cli/backend/auth/auth.(*gatewayAuth)`

_4 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x86a9c60` | `google3/third_party/jetski/cli/backend/auth/auth.(*gatewayAuth).TryAuth` | **yes** | |
| `0x86a9d60` | `google3/third_party/jetski/cli/backend/auth/auth.(*gatewayAuth).StartInteractive` | **yes** | |
| `0x86a9e60` | `google3/third_party/jetski/cli/backend/auth/auth.(*gatewayAuth).Logout` | **yes** | |
| `0x86a9e80` | `google3/third_party/jetski/cli/backend/auth/auth.(*gatewayAuth).Name` | **yes** | |

## `google3/third_party/jetski/cli/backend/auth/auth.(*geminiAPIKeyAuth)`

_3 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x86a9ea0` | `google3/third_party/jetski/cli/backend/auth/auth.(*geminiAPIKeyAuth).TryAuth` | **yes** | |
| `0x86a9f80` | `google3/third_party/jetski/cli/backend/auth/auth.(*geminiAPIKeyAuth).StartInteractive` | **yes** | |
| `0x86aa0a0` | `google3/third_party/jetski/cli/backend/auth/auth.(*geminiAPIKeyAuth).Name` | **yes** | |

## `google3/third_party/jetski/cli/backend/auth/auth.(*keyringAuth)`

_4 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x86aa0c0` | `google3/third_party/jetski/cli/backend/auth/auth.(*keyringAuth).TryAuth` | **yes** | |
| `0x86aa360` | `google3/third_party/jetski/cli/backend/auth/auth.(*keyringAuth).StartInteractive` | **yes** | |
| `0x86aa380` | `google3/third_party/jetski/cli/backend/auth/auth.(*keyringAuth).Logout` | **yes** | |
| `0x86aa480` | `google3/third_party/jetski/cli/backend/auth/auth.(*keyringAuth).Name` | **yes** | |

## `google3/third_party/jetski/cli/backend/auth/auth.(*keyringAuth).TryAuth.func1`

_1 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x86ae4e0` | `google3/third_party/jetski/cli/backend/auth/auth.(*keyringAuth).TryAuth.func1.1` | **yes** | |

## `google3/third_party/jetski/cli/backend/auth/auth.(*oauthMethod)`

_6 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x86a7380` | `google3/third_party/jetski/cli/backend/auth/auth.(*oauthMethod).StartInteractive` | **yes** | |
| `0x86a77e0` | `google3/third_party/jetski/cli/backend/auth/auth.(*oauthMethod).SubmitAuthorizationCode` | **yes** | |
| `0x86a7900` | `google3/third_party/jetski/cli/backend/auth/auth.(*oauthMethod).completeOAuth` | **yes** | |
| `0x86a7b80` | `google3/third_party/jetski/cli/backend/auth/auth.(*oauthMethod).Logout` | **yes** | |
| `0x86a7cc0` | `google3/third_party/jetski/cli/backend/auth/auth.(*oauthMethod).Name` | **yes** | |
| `0x86a83c0` | `google3/third_party/jetski/cli/backend/auth/auth.(*oauthMethod).getOAuthConfig` | **yes** | |

## `google3/third_party/jetski/cli/backend/auth/auth.(*oauthMethod).StartInteractive`

_1 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x86aca00` | `google3/third_party/jetski/cli/backend/auth/auth.(*oauthMethod).StartInteractive.gowrap1` | **yes** | |

## `google3/third_party/jetski/cli/backend/auth/auth.(*oauthMethod).completeOAuth.func1`

_1 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x86acc60` | `google3/third_party/jetski/cli/backend/auth/auth.(*oauthMethod).completeOAuth.func1.1` | **yes** | |

## `google3/third_party/jetski/cli/backend/auth/auth.(*oauthMethod).completeOAuth.func1.1`

_1 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x86ad720` | `google3/third_party/jetski/cli/backend/auth/auth.(*oauthMethod).completeOAuth.func1.1.1` | **yes** | |

## `google3/third_party/jetski/cli/backend/auth/auth.(*savingTokenSource)`

_1 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x86a8500` | `google3/third_party/jetski/cli/backend/auth/auth.(*savingTokenSource).Token` | **yes** | |

## `google3/third_party/jetski/cli/backend/auth/auth.(*wifOAuthMethod)`

_2 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x86abe40` | `google3/third_party/jetski/cli/backend/auth/auth.(*wifOAuthMethod).SetWIFProvider` | **yes** | |
| `0x86ac680` | `google3/third_party/jetski/cli/backend/auth/auth.(*wifOAuthMethod).completeOAuth` | **yes** | |

## `google3/third_party/jetski/cli/backend/auth/auth.(*wifOAuthMethod).StartInteractive`

_1 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x86ae8c0` | `google3/third_party/jetski/cli/backend/auth/auth.(*wifOAuthMethod).StartInteractive.gowrap1` | **yes** | |

## `google3/third_party/jetski/cli/backend/auth/auth.(*wifOAuthMethod).completeOAuth.func1`

_1 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x86aeb60` | `google3/third_party/jetski/cli/backend/auth/auth.(*wifOAuthMethod).completeOAuth.func1.1` | **yes** | |

## `google3/third_party/jetski/cli/backend/auth/auth.(*wifOAuthMethod).completeOAuth.func1.1`

_1 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x86af640` | `google3/third_party/jetski/cli/backend/auth/auth.(*wifOAuthMethod).completeOAuth.func1.1.1` | **yes** | |

## Pending / errors (18)

Functions that did not decompile (likely thunks, glue, or out-of-spec):

- `0x86a6200` — `google3/third_party/jetski/cli/backend/auth/auth.(*adcAuth).StartInteractive`
- `0x86a6900` — `google3/third_party/jetski/cli/backend/auth/auth.(*ChainedAuth).StartInteractive`
- `0x86a6aa0` — `google3/third_party/jetski/cli/backend/auth/auth.(*ChainedAuth).StartGCPAuthProcess`
- `0x86a6e20` — `google3/third_party/jetski/cli/backend/auth/auth.(*ChainedAuth).Logout`
- `0x86a6ec0` — `google3/third_party/jetski/cli/backend/auth/auth.(*ChainedAuth).Active`
- `0x86a6ee0` — `google3/third_party/jetski/cli/backend/auth/auth.(*ChainedAuth).Cancel`
- `0x86a6fc0` — `google3/third_party/jetski/cli/backend/auth/auth.(*ChainedAuth).SubmitAuthorizationCode`
- `0x86a7360` — `google3/third_party/jetski/cli/backend/auth/auth.(*oauthMethod).TryAuth`
- `0x86a7ac0` — `google3/third_party/jetski/cli/backend/auth/auth.(*oauthMethod).Cancel`
- `0x86a9bc0` — `google3/third_party/jetski/cli/backend/auth/auth.(*externalCorpLoginAuth).TryAuth`
- `0x86a9c00` — `google3/third_party/jetski/cli/backend/auth/auth.(*externalCorpLoginAuth).Logout`
- `0x86a9c20` — `google3/third_party/jetski/cli/backend/auth/auth.(*externalCorpLoginAuth).Name`
- `0x86a9c40` — `google3/third_party/jetski/cli/backend/auth/auth.(*externalCorpLoginAuth).IsSupported`
- `0x86aa080` — `google3/third_party/jetski/cli/backend/auth/auth.(*geminiAPIKeyAuth).Logout`
- `0x86ab1a0` — `google3/third_party/jetski/cli/backend/auth/auth.(*cliFileTokenStorage).LoadToken`
- `0x86ab220` — `google3/third_party/jetski/cli/backend/auth/auth.(*cliFileTokenStorage).SaveUserTier`
- `0x86abf40` — `google3/third_party/jetski/cli/backend/auth/auth.(*wifOAuthMethod).StartInteractive`
- `0x86ac560` — `google3/third_party/jetski/cli/backend/auth/auth.(*wifOAuthMethod).SubmitAuthorizationCode`

See `/workspace/agy/out/decompile/dec/_errors.txt` for details.
