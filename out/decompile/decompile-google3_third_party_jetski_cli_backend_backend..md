# Decompile report — `google3/third_party/jetski/cli/backend/backend.`

> 193 priority functions in this Go package

**Decompiled:** 129/193

## `google3/third_party/jetski/cli/backend/backend.(*AgentModel)`

_1 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x86e4120` | `google3/third_party/jetski/cli/backend/backend.(*AgentModel).PreferredID` |  | |

## `google3/third_party/jetski/cli/backend/backend.(*ServerBackend)`

_120 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x86b0f40` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).startConversationSearchIndex` |  | |
| `0x86b12c0` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).projectNames` |  | |
| `0x86b1780` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).closeConversationSearchIndex` |  | |
| `0x86b1860` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).notifyConversationSearch` |  | |
| `0x86b1a80` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).notifyConversationSearchDelete` |  | |
| `0x86b1e40` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).SearchConversations` |  | |
| `0x86b8380` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).startSummaryStoreReconcile` |  | |
| `0x86b84e0` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).BindInMemoryCLISettingsProvider` |  | |
| `0x86b8540` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).Close` |  | |
| `0x86b9520` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).VersionInfo` |  | |
| `0x86b95a0` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).GetSlashCommands` |  | |
| `0x86b95e0` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).activeCascadeConfig` |  | |
| `0x86b97a0` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).getActiveModelOrAlias` |  | |
| `0x86b98c0` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).GetShellCommandTracker` |  | |
| `0x86b98e0` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).GetOnShellCommandFinished` |  | |
| `0x86b9900` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).GetModelConfig` |  | |
| `0x86babe0` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).ReadCliSettings` |  | |
| `0x86baea0` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).WriteCliSettings` |  | |
| `0x86bb200` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).QuarantineCliSettings` |  | |
| `0x86bb800` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).ReadKeybindings` |  | |
| `0x86bbb20` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).WriteKeybindings` |  | |
| `0x86bbe20` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).KeybindingsFilePath` |  | |
| `0x86bbe80` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).ReadAllHooks` |  | |
| `0x86bcae0` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).GetWorkspaceDirs` |  | |
| `0x86bcdc0` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).FetchAdminControls` | **yes** | |
| `0x86bce60` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).FetchLicenses` | **yes** | |
| `0x86bd160` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).SelectLicense` | **yes** | |
| `0x86bd580` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).SelfAssignLicense` | **yes** | |
| `0x86bd760` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).AddWorkspaceDir` |  | |
| `0x86bda20` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).RemoveWorkspaceDir` |  | |
| `0x86bdd20` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).newCustomizationManagerWithOptions` |  | |
| `0x86be740` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).StartConversation` |  | |
| `0x86bf060` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).StreamConversationUpdates` |  | |
| `0x86bf6c0` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).SetStreamCreatedHook` |  | |
| `0x86c0200` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).buildCascadeConfigAndAgentSpec` |  | |
| `0x86c0380` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).buildCustomAgentSpec` |  | |
| `0x86c06a0` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).buildCascadeConfigInternal` |  | |
| `0x86c1be0` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).hasCustomAgentPlanner` |  | |
| `0x86c1de0` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).SendUserMessage` | **yes** | |
| `0x86c2360` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).DeletePendingAgentMessage` |  | |
| `0x86c2400` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).populatePermissionConfig` |  | |
| `0x86c32e0` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).resolveModelLabel` |  | |
| `0x86c3400` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).RenameConversation` |  | |
| `0x86c35c0` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).MoveConversationToGroup` |  | |
| `0x86c3ce0` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).SetFinishToolSchema` |  | |
| `0x86c3ec0` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).SetConversationPermissions` |  | |
| `0x86c40e0` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).GetAllowNonWorkspaceAccess` |  | |
| `0x86c41a0` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).SetIncludeDefaultCustomizations` |  | |
| `0x86c4260` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).GetIncludeDefaultCustomizations` |  | |
| `0x86c4320` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).SetAutoExecutionPolicy` |  | |
| `0x86c43c0` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).SetToolPermissionMode` |  | |
| `0x86c44c0` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).SetProjectID` |  | |
| `0x86c4660` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).GetProjectID` |  | |
| `0x86c4740` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).SetTerminalSandboxSettings` |  | |
| `0x86c4800` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).SetSandboxOverrideForNextConfirmation` |  | |
| `0x86c48c0` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).GetTelemetryEnabled` |  | |
| `0x86c49c0` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).SetTelemetryEnabled` |  | |
| `0x86c4ae0` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).SetSelectedModelOverride` | **yes** | |
| `0x86c4ba0` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).SetContextWindow` |  | |
| `0x86c4c80` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).ContextWindow` |  | |
| `0x86c4d40` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).SetCustomModelInfoOverride` |  | |
| `0x86c4ea0` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).GetCustomModelInfoOverride` |  | |
| `0x86c4f60` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).SetCustomModels` |  | |
| `0x86c5020` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).CustomModelsEnabled` |  | |
| `0x86c5060` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).appendCustomModels` |  | |
| `0x86c5220` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).GetSelectedModelOverride` | **yes** | |
| `0x86c52e0` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).SetOnRunStatusChange` |  | |
| `0x86c53c0` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).NumSteps` |  | |
| `0x86c5460` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).cancelConversation` |  | |
| `0x86c56e0` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).Cancel` |  | |
| `0x86c5740` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).CancelSubagent` |  | |
| `0x86c57a0` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).CancelSteps` |  | |
| `0x86c59a0` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).RecordFeedback` |  | |
| `0x86c6060` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).RevertToStep` |  | |
| `0x86c6400` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).ForkConversation` |  | |
| `0x86c6f20` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).WarmUpAgentSync` |  | |
| `0x86c7060` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).RespondToToolConfirmation` |  | |
| `0x86c7960` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).RespondToAskQuestion` |  | |
| `0x86c8220` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).handleCodeAcknowledgement` |  | |
| `0x86c8640` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).GetSkills` |  | |
| `0x86c8820` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).GetSkillsCreatePath` |  | |
| `0x86c89e0` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).GetGlobalSkillsCreatePath` |  | |
| `0x86c8b80` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).ListConversations` |  | |
| `0x86c9120` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).activeInMemorySummaries` |  | |
| `0x86c9ba0` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).scanConversations` |  | |
| `0x86cab20` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).syncSummariesToStore` |  | |
| `0x86cb0c0` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).listConversationsFromDir` |  | |
| `0x86cbf80` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).GetConversationDetail` |  | |
| `0x86ccba0` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).fallbackGetConversationDetail` |  | |
| `0x86ce220` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).ImportConversation` |  | |
| `0x86cf400` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).GetAgentCustomizations` |  | |
| `0x86cf9c0` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).GetGlobalAgentsCreatePath` |  | |
| `0x86cfb00` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).SearchFiles` |  | |
| `0x86cfc20` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).SearchCode` |  | |
| `0x86cfe60` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).StreamSearchCode` |  | |
| `0x86d00a0` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).GetChangelog` |  | |
| `0x86d00c0` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).GetG1Credits` |  | |
| `0x86d03c0` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).RetrieveUserQuotaSummary` | **yes** | |
| `0x86d0c60` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).SendSideQuestion` |  | |
| `0x86d14c0` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).StartTranscription` |  | |
| `0x86d1880` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).loginTokenSource` | **yes** | |
| `0x86d19c0` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).startTranscription` |  | |
| `0x86d2a20` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).StartSideQuestion` |  | |
| `0x86d3260` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).buildBtwCascadeConfig` |  | |
| `0x86d3a20` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).ReadLastConversations` |  | |
| `0x86d3f80` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).SetLastConversation` |  | |
| `0x86d53a0` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).WriteOnboardingStatus` | **yes** | |
| `0x86d57e0` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).fillSummaryCacheInBackground` |  | |
| `0x86d5920` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).fillSummaryCacheChunk` |  | |
| `0x86d5f60` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).waitForSummaryFill` |  | |
| `0x86d60c0` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).loadConversationCache` |  | |
| `0x86d6540` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).saveConversationCache` |  | |
| `0x86d69c0` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).clearConversationCache` |  | |
| `0x86d8320` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).ListCascadeNuxes` |  | |
| `0x86d8480` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).ReadNuxState` |  | |
| `0x86d8560` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).WriteNuxState` |  | |
| `0x86d8800` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).authStatusFor` | **yes** | |
| `0x86d8d40` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).StartOAuthProcess` | **yes** | |
| `0x86d9ce0` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).IsAuthMethodSupported` | **yes** | |
| `0x86e4220` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).loginTokenSource-fm` | **yes** | |

## `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).StreamConversationUpdates.func3`

_1 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x86dcb40` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).StreamConversationUpdates.func3.2` |  | |

## `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).handleAuthResult.func1`

_2 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x86df980` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).handleAuthResult.func1.2` | **yes** | |
| `0x86dfa40` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).handleAuthResult.func1.1` | **yes** | |

## `google3/third_party/jetski/cli/backend/backend.(*ServerBackendConfig)`

_1 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x86b89c0` | `google3/third_party/jetski/cli/backend/backend.(*ServerBackendConfig).chainedAuthOrDefault` | **yes** | |

## `google3/third_party/jetski/cli/backend/backend.(*retry)`

_1 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x86b68e0` | `google3/third_party/jetski/cli/backend/backend.(*retry).Run` |  | |

## `google3/third_party/jetski/cli/backend/backend.(*standardModelResolver)`

_1 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x86b42c0` | `google3/third_party/jetski/cli/backend/backend.(*standardModelResolver).resolve` |  | |

## `google3/third_party/jetski/cli/backend/backend.(*updateQueue)`

_2 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x86d9fc0` | `google3/third_party/jetski/cli/backend/backend.(*updateQueue).Send` |  | |
| `0x86da260` | `google3/third_party/jetski/cli/backend/backend.(*updateQueue).run` |  | |

## Pending / errors (64)

Functions that did not decompile (likely thunks, glue, or out-of-spec):

- `0x86b1040` — `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).initConversationSearchIndex`
- `0x86b3d20` — `google3/third_party/jetski/cli/backend/backend.(*AuthStatus).EligibilityError`
- `0x86b4260` — `google3/third_party/jetski/cli/backend/backend.(*OnboardingStatus).IsComplete`
- `0x86b4c80` — `google3/third_party/jetski/cli/backend/backend.(*adHocCustomModelResolver).resolve`
- `0x86b4d80` — `google3/third_party/jetski/cli/backend/backend.(*customModelsResolver).resolve`
- `0x86bab60` — `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).WaitForConversationFullyIdle`
- `0x86bb1a0` — `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).CliSettingsFilePath`
- `0x86bc5e0` — `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).WriteHooksTo`
- `0x86bca80` — `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).DefaultHooksPath`
- `0x86bf7a0` — `google3/third_party/jetski/cli/backend/backend.(*callbackStreamer).Send`
- `0x86c02e0` — `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).resolveIsInteractive`
- `0x86c0620` — `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).buildCascadeConfig`
- `0x86c3160` — `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).getWorkspaceURIs`
- `0x86c37a0` — `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).RefreshExperiments`
- `0x86c38c0` — `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).FeatureProvider`
- `0x86c3940` — `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).kindGateChecker`
- `0x86c3aa0` — `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).DeleteConversation`
- `0x86c3de0` — `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).FinishToolSchema`
- `0x86c4020` — `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).SetAllowNonWorkspaceAccess`
- `0x86cf580` — `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).GetPluginMCPSpecs`
- `0x86cf6a0` — `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).GetInstalledPlugins`
- `0x86cf7e0` — `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).GetAgentsCreatePath`
- `0x86d0a20` — `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).SetUseG1Credits`
- `0x86d0ae0` — `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).GetUseG1Credits`
- `0x86d2860` — `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).SetRemoteControlSession`
- `0x86d28e0` — `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).RemoteControlStatus`
- `0x86d47c0` — `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).ReadOnboardingStatus`
- `0x86d6ae0` — `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).loadSummaryFromFile`
- `0x86d7900` — `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).parallelLoadSummaries`
- `0x86d8160` — `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).fallbackConvImportDirs`
- `0x86d82e0` — `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).StartBattleMode`
- `0x86d8300` — `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).EndBattleMode`
- `0x86d8700` — `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).nuxStatePath`
- `0x86d8980` — `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).StreamOAuthStatus`
- `0x86d8b40` — `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).handleAuthResult`
- `0x86d8de0` — `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).StartGCPAuthProcess`
- `0x86d8ea0` — `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).CancelOAuthProcess`
- `0x86d8f80` — `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).SubmitOAuthAuthorizationCode`
- `0x86d8fe0` — `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).Logout`
- `0x86d9200` — `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).applyAuthResult`
- `0x86d9920` — `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).fetchPlanTierAndAntigravityUsage`
- `0x86d9a80` — `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).TrySilentAuth`
- `0x86d9b00` — `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).ValidateAndOnboardAccount`
- `0x86d9d40` — `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).RememberedWIFProvider`
- `0x86da1a0` — `google3/third_party/jetski/cli/backend/backend.(*updateQueue).close`
- `0x86da760` — `google3/third_party/jetski/cli/backend/backend.(*deliveryTracker).Send`
- `0x86da7c0` — `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).SubscribeToSummaries`
- `0x86daa20` — `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).conversationDirs`
- `0x86dac00` — `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).conversationIDsOnDisk`
- `0x86dade0` — `google3/third_party/jetski/cli/backend/backend.(*ServerBackend).summaryStoreReadsEnabled`

... and 14 more.

See `/workspace/agy/out/decompile/dec/_errors.txt` for details.
