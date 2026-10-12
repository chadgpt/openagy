# Decompile report — `google3/third_party/jetski/cli/backend/backend`

> 48 priority functions in this Go package

**Decompiled:** 27/48

## `<package>`

_27 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x86b0ce0` | `google3/third_party/jetski/cli/backend/backend.ParsePresetContextWindow` |  | |
| `0x86b1960` | `google3/third_party/jetski/cli/backend/backend.searchSummaries` |  | |
| `0x86b1fe0` | `google3/third_party/jetski/cli/backend/backend.IsValidEffort` |  | |
| `0x86b20a0` | `google3/third_party/jetski/cli/backend/backend.effortIndex` |  | |
| `0x86b2300` | `google3/third_party/jetski/cli/backend/backend.findModelBySlug` |  | |
| `0x86b2560` | `google3/third_party/jetski/cli/backend/backend.CurrentBaseEffort` |  | |
| `0x86b26c0` | `google3/third_party/jetski/cli/backend/backend.EffortsForBase` |  | |
| `0x86b2e60` | `google3/third_party/jetski/cli/backend/backend.ResolveEffort` |  | |
| `0x86b3ac0` | `google3/third_party/jetski/cli/backend/backend.ApplyPassThroughEffort` |  | |
| `0x86b47a0` | `google3/third_party/jetski/cli/backend/backend.ResolveModel` |  | |
| `0x86b5160` | `google3/third_party/jetski/cli/backend/backend.ResolveCustomModelLabel` |  | |
| `0x86b5400` | `google3/third_party/jetski/cli/backend/backend.extractAPIProvider` |  | |
| `0x86b5ae0` | `google3/third_party/jetski/cli/backend/backend.constructCustomModelInfo` |  | |
| `0x86b6ac0` | `google3/third_party/jetski/cli/backend/backend.buildVersion` |  | |
| `0x86b6ba0` | `google3/third_party/jetski/cli/backend/backend.NewServerBackend` |  | |
| `0x86c1880` | `google3/third_party/jetski/cli/backend/backend.applyModelAPIMaxRetriesOverride` |  | |
| `0x86c1b20` | `google3/third_party/jetski/cli/backend/backend.applyDisableSafetyFilteringOverride` |  | |
| `0x86c7ec0` | `google3/third_party/jetski/cli/backend/backend.buildToolInteraction` |  | |
| `0x86cae40` | `google3/third_party/jetski/cli/backend/backend.recordSummaryStoreEvent` |  | |
| `0x86d04c0` | `google3/third_party/jetski/cli/backend/backend.mapQuotaSummary` |  | |
| `0x86d0ba0` | `google3/third_party/jetski/cli/backend/backend.trajectoryLastStepTime` |  | |
| `0x86d15c0` | `google3/third_party/jetski/cli/backend/backend.startTranscriptionWithTimeout` |  | |
| `0x86d2000` | `google3/third_party/jetski/cli/backend/backend.wrapTranscriptionErrs` |  | |
| `0x86d2400` | `google3/third_party/jetski/cli/backend/backend.isInsufficientScopeErr` |  | |
| `0x86d2680` | `google3/third_party/jetski/cli/backend/backend.transcriptionQuotaInfo` |  | |
| `0x86d9e60` | `google3/third_party/jetski/cli/backend/backend.newUpdateQueue` |  | |
| `0x86da440` | `google3/third_party/jetski/cli/backend/backend.subscribeWithRetry` |  | |

## Pending / errors (21)

Functions that did not decompile (likely thunks, glue, or out-of-spec):

- `0x86b1ba0` — `google3/third_party/jetski/cli/backend/backend.summaryToTrajectorySummary`
- `0x86b2900` — `google3/third_party/jetski/cli/backend/backend.ModelForBaseEffort`
- `0x86b2b40` — `google3/third_party/jetski/cli/backend/backend.CurrentEffortSelection`
- `0x86b2ca0` — `google3/third_party/jetski/cli/backend/backend.availableEfforts`
- `0x86b3960` — `google3/third_party/jetski/cli/backend/backend.EffortUnsupportedError`
- `0x86b3a20` — `google3/third_party/jetski/cli/backend/backend.effortToThinkingLevel`
- `0x86b3f40` — `google3/third_party/jetski/cli/backend/backend.IneligibilityFromResult`
- `0x86b4100` — `google3/third_party/jetski/cli/backend/backend.applyIneligibilityURLs`
- `0x86b4b20` — `google3/third_party/jetski/cli/backend/backend.LogModelRewrite`
- `0x86b55a0` — `google3/third_party/jetski/cli/backend/backend.constructFromCustomModelConfig`
- `0x86b5ba0` — `google3/third_party/jetski/cli/backend/backend.resolveCustomAgentModels`
- `0x86b61e0` — `google3/third_party/jetski/cli/backend/backend.buildCustomAgentModel`
- `0x86b63e0` — `google3/third_party/jetski/cli/backend/backend.buildCustomModelDescription`
- `0x86b64e0` — `google3/third_party/jetski/cli/backend/backend.extractFeaturesFromProto`
- `0x86b6660` — `google3/third_party/jetski/cli/backend/backend.slugFor`
- `0x86b6700` — `google3/third_party/jetski/cli/backend/backend.parseModelSlug`
- `0x86b6880` — `google3/third_party/jetski/cli/backend/backend.UserFacingSlug`
- `0x86cafc0` — `google3/third_party/jetski/cli/backend/backend.isInternalTrajectory`
- `0x86d24a0` — `google3/third_party/jetski/cli/backend/backend.describeTranscriptionErr`
- `0x86da980` — `google3/third_party/jetski/cli/backend/backend.conversationIDFromFileName`
- `0x86db500` — `google3/third_party/jetski/cli/backend/backend.isHiddenRecord`

See `/workspace/agy/out/decompile/dec/_errors.txt` for details.
