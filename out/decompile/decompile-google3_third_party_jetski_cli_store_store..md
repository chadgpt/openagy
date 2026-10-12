# Decompile report — `google3/third_party/jetski/cli/store/store.`

> 600 priority functions in this Go package

**Decompiled:** 324/600

## `google3/third_party/jetski/cli/store/store.(*HintMask)`

_1 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x8a27d20` | `google3/third_party/jetski/cli/store/store.(*HintMask).Has` |  | |

## `google3/third_party/jetski/cli/store/store.(*Manager)`

_250 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x8998fc0` | `google3/third_party/jetski/cli/store/store.(*Manager).applyAdminControlsOverridesUnlocked` |  | |
| `0x89993e0` | `google3/third_party/jetski/cli/store/store.(*Manager).applyToolPermissionOverride` |  | |
| `0x89997a0` | `google3/third_party/jetski/cli/store/store.(*Manager).applyNonWorkspaceAccessOverride` |  | |
| `0x8999940` | `google3/third_party/jetski/cli/store/store.(*Manager).GetAgentCustomizations` |  | |
| `0x8999980` | `google3/third_party/jetski/cli/store/store.(*Manager).GetAgentsCreatePath` |  | |
| `0x8999a00` | `google3/third_party/jetski/cli/store/store.(*Manager).SelectAgentByName` | **yes** | |
| `0x8999cc0` | `google3/third_party/jetski/cli/store/store.(*Manager).resolvePendingAgentSelection` | **yes** | |
| `0x8999dc0` | `google3/third_party/jetski/cli/store/store.(*Manager).SetSelectedAgent` | **yes** | |
| `0x899a2a0` | `google3/third_party/jetski/cli/store/store.(*Manager).SelectedAgentCustomization` | **yes** | |
| `0x899a3c0` | `google3/third_party/jetski/cli/store/store.(*Manager).ClearSelectedAgent` | **yes** | |
| `0x899a600` | `google3/third_party/jetski/cli/store/store.(*Manager).StartTransitionToAgent` |  | |
| `0x899a8e0` | `google3/third_party/jetski/cli/store/store.(*Manager).startTransitionWorker` |  | |
| `0x899aae0` | `google3/third_party/jetski/cli/store/store.(*Manager).handleTransition` |  | |
| `0x899b560` | `google3/third_party/jetski/cli/store/store.(*Manager).CancelTransition` |  | |
| `0x899b740` | `google3/third_party/jetski/cli/store/store.(*Manager).resetTransitionState` |  | |
| `0x899b880` | `google3/third_party/jetski/cli/store/store.(*Manager).resolveAgent` |  | |
| `0x899b980` | `google3/third_party/jetski/cli/store/store.(*Manager).forkOrStartConversation` |  | |
| `0x899bce0` | `google3/third_party/jetski/cli/store/store.(*Manager).DismissArtifactReview` |  | |
| `0x899be00` | `google3/third_party/jetski/cli/store/store.(*Manager).ResetArtifactReview` |  | |
| `0x899bf40` | `google3/third_party/jetski/cli/store/store.(*Manager).refreshArtifactReviewLocked` | **yes** | |
| `0x899c300` | `google3/third_party/jetski/cli/store/store.(*Manager).commitPendingAskQuestion` |  | |
| `0x899c440` | `google3/third_party/jetski/cli/store/store.(*Manager).handleAskQuestion` |  | |
| `0x899c740` | `google3/third_party/jetski/cli/store/store.(*Manager).RespondToAskQuestion` |  | |
| `0x899c800` | `google3/third_party/jetski/cli/store/store.(*Manager).scanAskQuestion` |  | |
| `0x899cc00` | `google3/third_party/jetski/cli/store/store.(*Manager).commitAuth` | **yes** | |
| `0x899cd40` | `google3/third_party/jetski/cli/store/store.(*Manager).waitForEligibility` | **yes** | |
| `0x899cf80` | `google3/third_party/jetski/cli/store/store.(*Manager).StartOAuthProcess` | **yes** | |
| `0x899d3a0` | `google3/third_party/jetski/cli/store/store.(*Manager).StartGCPAuthProcess` | **yes** | |
| `0x899d8a0` | `google3/third_party/jetski/cli/store/store.(*Manager).CompleteGCPSetup` | **yes** | |
| `0x899d9c0` | `google3/third_party/jetski/cli/store/store.(*Manager).TrySilentAuth` | **yes** | |
| `0x899da00` | `google3/third_party/jetski/cli/store/store.(*Manager).CancelOAuthProcess` | **yes** | |
| `0x899db00` | `google3/third_party/jetski/cli/store/store.(*Manager).ResetAuthState` | **yes** | |
| `0x899dbc0` | `google3/third_party/jetski/cli/store/store.(*Manager).SubmitOAuthAuthorizationCode` | **yes** | |
| `0x899dc20` | `google3/third_party/jetski/cli/store/store.(*Manager).SubmitVertexAPIKey` |  | |
| `0x899de20` | `google3/third_party/jetski/cli/store/store.(*Manager).Logout` |  | |
| `0x899e0c0` | `google3/third_party/jetski/cli/store/store.(*Manager).IsBusinessLoginEnabled` | **yes** | |
| `0x899e140` | `google3/third_party/jetski/cli/store/store.(*Manager).RememberedWIFProvider` |  | |
| `0x899e4c0` | `google3/third_party/jetski/cli/store/store.(*Manager).ActiveAgentTaskStepIndices` |  | |
| `0x899e5e0` | `google3/third_party/jetski/cli/store/store.(*Manager).ActiveAgentTaskStepIndicesByDaemon` |  | |
| `0x899e8a0` | `google3/third_party/jetski/cli/store/store.(*Manager).SendBtwQuestion` |  | |
| `0x899ede0` | `google3/third_party/jetski/cli/store/store.(*Manager).DismissBtwResponse` |  | |
| `0x899f100` | `google3/third_party/jetski/cli/store/store.(*Manager).ToggleBtwExpanded` |  | |
| `0x899f420` | `google3/third_party/jetski/cli/store/store.(*Manager).NavigateBtw` |  | |
| `0x899f5c0` | `google3/third_party/jetski/cli/store/store.(*Manager).ShowBtwHistory` |  | |
| `0x899f780` | `google3/third_party/jetski/cli/store/store.(*Manager).IsBtwActive` |  | |
| `0x899f880` | `google3/third_party/jetski/cli/store/store.(*Manager).PersistLastConversation` |  | |
| `0x899fa60` | `google3/third_party/jetski/cli/store/store.(*Manager).persistLastConversationAsync` |  | |
| `0x899fc40` | `google3/third_party/jetski/cli/store/store.(*Manager).initCliSettings` |  | |
| `0x89a0580` | `google3/third_party/jetski/cli/store/store.(*Manager).applyUserSettings` | **yes** | |
| `0x89a0d80` | `google3/third_party/jetski/cli/store/store.(*Manager).ApplyProjectPermissionGrants` |  | |
| `0x89a1280` | `google3/third_party/jetski/cli/store/store.(*Manager).ReloadPermissions` |  | |
| `0x89a2040` | `google3/third_party/jetski/cli/store/store.(*Manager).commitCliSetting` |  | |
| `0x89a2260` | `google3/third_party/jetski/cli/store/store.(*Manager).SetDefaultModel` |  | |
| `0x89a2660` | `google3/third_party/jetski/cli/store/store.(*Manager).ReadCliSettings` |  | |
| `0x89a3fa0` | `google3/third_party/jetski/cli/store/store.(*Manager).applySettingsSideEffects` |  | |
| `0x89a40a0` | `google3/third_party/jetski/cli/store/store.(*Manager).ResetSettingsToDefaults` |  | |
| `0x89a4600` | `google3/third_party/jetski/cli/store/store.(*Manager).propagateBackendSettings` |  | |
| `0x89a4e80` | `google3/third_party/jetski/cli/store/store.(*Manager).SetPermissionMode` |  | |
| `0x89a53e0` | `google3/third_party/jetski/cli/store/store.(*Manager).EffectivePermissionMode` |  | |
| `0x89a5500` | `google3/third_party/jetski/cli/store/store.(*Manager).SetArtifactReviewPolicy` |  | |
| `0x89a5d40` | `google3/third_party/jetski/cli/store/store.(*Manager).validateCliSettings` | **yes** | |
| `0x89a6620` | `google3/third_party/jetski/cli/store/store.(*Manager).parseDiskSettings` |  | |
| `0x89a6a60` | `google3/third_party/jetski/cli/store/store.(*Manager).SetToolPermission` |  | |
| `0x89a6e60` | `google3/third_party/jetski/cli/store/store.(*Manager).SetAllowNonWorkspaceAccess` |  | |
| `0x89a7240` | `google3/third_party/jetski/cli/store/store.(*Manager).SetStatusLineConfig` |  | |
| `0x89a7940` | `google3/third_party/jetski/cli/store/store.(*Manager).syncTelemetryFromServer` |  | |
| `0x89a7e80` | `google3/third_party/jetski/cli/store/store.(*Manager).SetTelemetryEnabled` |  | |
| `0x89a7f80` | `google3/third_party/jetski/cli/store/store.(*Manager).propagateTelemetry` |  | |
| `0x89a8200` | `google3/third_party/jetski/cli/store/store.(*Manager).persistProjectPermissions` |  | |
| `0x89a8900` | `google3/third_party/jetski/cli/store/store.(*Manager).persistSharedConfigPermissions` |  | |
| `0x89a8ce0` | `google3/third_party/jetski/cli/store/store.(*Manager).SetIncludeDefaultCustomizationsOverride` |  | |
| `0x89a9720` | `google3/third_party/jetski/cli/store/store.(*Manager).AddCommandOutput` |  | |
| `0x89a98c0` | `google3/third_party/jetski/cli/store/store.(*Manager).addRunningCommandOutput` |  | |
| `0x89a9a80` | `google3/third_party/jetski/cli/store/store.(*Manager).UpdateCommandOutputFinished` |  | |
| `0x89a9b00` | `google3/third_party/jetski/cli/store/store.(*Manager).UpdateCommandOutputResult` |  | |
| `0x89a9b80` | `google3/third_party/jetski/cli/store/store.(*Manager).updateCommandOutput` |  | |
| `0x89a9ee0` | `google3/third_party/jetski/cli/store/store.(*Manager).AddErrorCommandOutput` |  | |
| `0x89aa000` | `google3/third_party/jetski/cli/store/store.(*Manager).AddErrorAlert` |  | |
| `0x89aa1c0` | `google3/third_party/jetski/cli/store/store.(*Manager).addAlert` |  | |
| `0x89aa960` | `google3/third_party/jetski/cli/store/store.(*Manager).AddCommandOutputAtEnd` |  | |
| `0x89aa9e0` | `google3/third_party/jetski/cli/store/store.(*Manager).AddErrorAlertAtEnd` |  | |
| `0x89aaa60` | `google3/third_party/jetski/cli/store/store.(*Manager).AddWarningAlertAtEnd` |  | |
| `0x89aaae0` | `google3/third_party/jetski/cli/store/store.(*Manager).addCommandOutputAtEnd` |  | |
| `0x89aaea0` | `google3/third_party/jetski/cli/store/store.(*Manager).addAlertAtEnd` |  | |
| `0x89ab200` | `google3/third_party/jetski/cli/store/store.(*Manager).addCommandOutputWith` |  | |
| `0x89aba40` | `google3/third_party/jetski/cli/store/store.(*Manager).flushDeferredOutputs` |  | |
| `0x89abfe0` | `google3/third_party/jetski/cli/store/store.(*Manager).syncContextWindow` |  | |
| `0x89ac520` | `google3/third_party/jetski/cli/store/store.(*Manager).CreateConversationGroup` |  | |
| `0x89acf80` | `google3/third_party/jetski/cli/store/store.(*Manager).RenameConversationGroup` |  | |
| `0x89ad8e0` | `google3/third_party/jetski/cli/store/store.(*Manager).DeleteConversationGroup` |  | |
| `0x89adf00` | `google3/third_party/jetski/cli/store/store.(*Manager).MoveConversationToGroup` |  | |
| `0x89ae0e0` | `google3/third_party/jetski/cli/store/store.(*Manager).applyGeneratorMetadata` |  | |
| `0x89ae320` | `google3/third_party/jetski/cli/store/store.(*Manager).applyExecutorMetadata` |  | |
| `0x89ae520` | `google3/third_party/jetski/cli/store/store.(*Manager).applyCostSummary` |  | |
| `0x89ae720` | `google3/third_party/jetski/cli/store/store.(*Manager).applyCompactionInfo` |  | |
| `0x89ae9c0` | `google3/third_party/jetski/cli/store/store.(*Manager).applyBackgroundTasks` |  | |
| `0x89aecc0` | `google3/third_party/jetski/cli/store/store.(*Manager).updateInterpolationStates` |  | |
| `0x89af080` | `google3/third_party/jetski/cli/store/store.(*Manager).commitPendingSteps` |  | |
| `0x89af2e0` | `google3/third_party/jetski/cli/store/store.(*Manager).commitAbsoluteIndices` |  | |
| `0x89af9c0` | `google3/third_party/jetski/cli/store/store.(*Manager).GetAbsoluteIndex` |  | |
| `0x89afc80` | `google3/third_party/jetski/cli/store/store.(*Manager).RerenderAbsoluteIndex` |  | |
| `0x89b06a0` | `google3/third_party/jetski/cli/store/store.(*Manager).SetAbsoluteIndex` |  | |
| `0x89b0b80` | `google3/third_party/jetski/cli/store/store.(*Manager).rerenderAt` |  | |
| `0x89b2000` | `google3/third_party/jetski/cli/store/store.(*Manager).AddStep` |  | |
| `0x89b2320` | `google3/third_party/jetski/cli/store/store.(*Manager).AppendStepAndIndex` |  | |
| `0x89b2740` | `google3/third_party/jetski/cli/store/store.(*Manager).ConversationStepCount` |  | |
| `0x89b2840` | `google3/third_party/jetski/cli/store/store.(*Manager).ConversationSteps` |  | |
| `0x89b29e0` | `google3/third_party/jetski/cli/store/store.(*Manager).commitNewConversation` |  | |
| `0x89b2b60` | `google3/third_party/jetski/cli/store/store.(*Manager).commitInitState` |  | |
| `0x89b2dc0` | `google3/third_party/jetski/cli/store/store.(*Manager).commitTrajectoryID` |  | |
| `0x89b2fe0` | `google3/third_party/jetski/cli/store/store.(*Manager).commitStreamState` |  | |
| `0x89b3420` | `google3/third_party/jetski/cli/store/store.(*Manager).snapshotPendingSteps` |  | |
| `0x89b3720` | `google3/third_party/jetski/cli/store/store.(*Manager).NewConversation` |  | |
| `0x89b3760` | `google3/third_party/jetski/cli/store/store.(*Manager).startNewConversationInternal` |  | |
| `0x89b39a0` | `google3/third_party/jetski/cli/store/store.(*Manager).SwitchToConversation` |  | |
| `0x89b46e0` | `google3/third_party/jetski/cli/store/store.(*Manager).SendUserMessage` | **yes** | |
| `0x89b5800` | `google3/third_party/jetski/cli/store/store.(*Manager).StopStreamingConversation` |  | |
| `0x89b6140` | `google3/third_party/jetski/cli/store/store.(*Manager).StreamConversation` |  | |
| `0x89b6a80` | `google3/third_party/jetski/cli/store/store.(*Manager).LoadBugStore` |  | |
| `0x89b6b80` | `google3/third_party/jetski/cli/store/store.(*Manager).startStreaming` |  | |
| `0x89b7460` | `google3/third_party/jetski/cli/store/store.(*Manager).applyPendingAgentMessages` |  | |
| `0x89b7fe0` | `google3/third_party/jetski/cli/store/store.(*Manager).StreamSubagentUpdates` |  | |
| `0x89b81e0` | `google3/third_party/jetski/cli/store/store.(*Manager).ListenToSubagentStream` |  | |
| `0x89b85a0` | `google3/third_party/jetski/cli/store/store.(*Manager).CancelInit` |  | |
| `0x89b86e0` | `google3/third_party/jetski/cli/store/store.(*Manager).stopCurrentStream` |  | |
| `0x89b8ba0` | `google3/third_party/jetski/cli/store/store.(*Manager).MarkConversationCanceled` |  | |
| `0x89b9080` | `google3/third_party/jetski/cli/store/store.(*Manager).CancelConversation` |  | |
| `0x89b9280` | `google3/third_party/jetski/cli/store/store.(*Manager).RewindConversation` |  | |
| `0x89b95c0` | `google3/third_party/jetski/cli/store/store.(*Manager).ForkConversation` |  | |
| `0x89ba100` | `google3/third_party/jetski/cli/store/store.(*Manager).CancelSteps` |  | |
| `0x89ba720` | `google3/third_party/jetski/cli/store/store.(*Manager).findAbsIdxForStep` |  | |
| `0x89bd020` | `google3/third_party/jetski/cli/store/store.(*Manager).SubmitFeedback` |  | |
| `0x89bd8e0` | `google3/third_party/jetski/cli/store/store.(*Manager).doRefreshG1Credits` | **yes** | |
| `0x89bdd40` | `google3/third_party/jetski/cli/store/store.(*Manager).WaitForExperiments` |  | |
| `0x89bdfa0` | `google3/third_party/jetski/cli/store/store.(*Manager).waitForExperiments` |  | |
| `0x89be060` | `google3/third_party/jetski/cli/store/store.(*Manager).refreshExperiments` | **yes** | |
| `0x89befe0` | `google3/third_party/jetski/cli/store/store.(*Manager).ReloadHooks` |  | |
| `0x89bf7c0` | `google3/third_party/jetski/cli/store/store.(*Manager).SaveHooks` |  | |
| `0x89bffc0` | `google3/third_party/jetski/cli/store/store.(*Manager).GetHookSourceMap` |  | |
| `0x89c0220` | `google3/third_party/jetski/cli/store/store.(*Manager).GetGlobalPermissionGrants` |  | |
| `0x89c0400` | `google3/third_party/jetski/cli/store/store.(*Manager).AddGlobalPermissionGrants` |  | |
| `0x89c0a40` | `google3/third_party/jetski/cli/store/store.(*Manager).GetAllowNonWorkspaceAccess` |  | |
| `0x89c0b40` | `google3/third_party/jetski/cli/store/store.(*Manager).GetEnableTerminalSandbox` |  | |
| `0x89c0c60` | `google3/third_party/jetski/cli/store/store.(*Manager).GetSandboxProxy` |  | |
| `0x89c0e40` | `google3/third_party/jetski/cli/store/store.(*Manager).GetAutoExecutionPolicy` |  | |
| `0x89c0f00` | `google3/third_party/jetski/cli/store/store.(*Manager).autoExecutionPolicyUnlocked` |  | |
| `0x89c1120` | `google3/third_party/jetski/cli/store/store.(*Manager).GetPermissionPreset` |  | |
| `0x89c1300` | `google3/third_party/jetski/cli/store/store.(*Manager).GetArtifactReviewMode` |  | |
| `0x89c15a0` | `google3/third_party/jetski/cli/store/store.(*Manager).PermissionGrants` |  | |
| `0x89c2400` | `google3/third_party/jetski/cli/store/store.(*Manager).PopPendingInputs` |  | |
| `0x89c24e0` | `google3/third_party/jetski/cli/store/store.(*Manager).commitPendingInputs` |  | |
| `0x89c2740` | `google3/third_party/jetski/cli/store/store.(*Manager).commitOptimisticMessage` |  | |
| `0x89c2920` | `google3/third_party/jetski/cli/store/store.(*Manager).userInputLoop` | **yes** | |
| `0x89c76a0` | `google3/third_party/jetski/cli/store/store.(*Manager).scanToolConfirmation` |  | |
| `0x89c8800` | `google3/third_party/jetski/cli/store/store.(*Manager).commitOptimisticUserStep` | **yes** | |
| `0x89c90a0` | `google3/third_party/jetski/cli/store/store.(*Manager).sendMessageOrSteer` |  | |
| `0x89c9d20` | `google3/third_party/jetski/cli/store/store.(*Manager).addSendingMessage` |  | |
| `0x89ca740` | `google3/third_party/jetski/cli/store/store.(*Manager).recallSendingMessages` |  | |
| `0x89cae60` | `google3/third_party/jetski/cli/store/store.(*Manager).sendImmediateMidTurn` |  | |
| `0x89cbac0` | `google3/third_party/jetski/cli/store/store.(*Manager).SelfAssignLicense` | **yes** | |
| `0x89cbba0` | `google3/third_party/jetski/cli/store/store.(*Manager).SelectLicense` | **yes** | |
| `0x89cc020` | `google3/third_party/jetski/cli/store/store.(*Manager).SetRequestedModel` |  | |
| `0x89cc120` | `google3/third_party/jetski/cli/store/store.(*Manager).SetRequestedEffort` |  | |
| `0x89cc220` | `google3/third_party/jetski/cli/store/store.(*Manager).SetPrintMode` |  | |
| `0x89cdac0` | `google3/third_party/jetski/cli/store/store.(*Manager).interpolationLoop` |  | |
| `0x89cdec0` | `google3/third_party/jetski/cli/store/store.(*Manager).markInterpolationsCompleted` |  | |
| `0x89ceee0` | `google3/third_party/jetski/cli/store/store.(*Manager).WorkspaceFileSystem` |  | |
| `0x89cef00` | `google3/third_party/jetski/cli/store/store.(*Manager).Close` |  | |
| `0x89cf2a0` | `google3/third_party/jetski/cli/store/store.(*Manager).ListConversations` |  | |
| `0x89cf660` | `google3/third_party/jetski/cli/store/store.(*Manager).ImportConversation` |  | |
| `0x89cf780` | `google3/third_party/jetski/cli/store/store.(*Manager).drainRerenders` |  | |
| `0x89cfae0` | `google3/third_party/jetski/cli/store/store.(*Manager).commitFullRedraw` |  | |
| `0x89d0740` | `google3/third_party/jetski/cli/store/store.(*Manager).notify` |  | |
| `0x89d0e60` | `google3/third_party/jetski/cli/store/store.(*Manager).SetMcpAuthSuccess` | **yes** | |
| `0x89d1340` | `google3/third_party/jetski/cli/store/store.(*Manager).SetMigrationProgress` |  | |
| `0x89d1600` | `google3/third_party/jetski/cli/store/store.(*Manager).SetSuggestionsVisible` |  | |
| `0x89d1a00` | `google3/third_party/jetski/cli/store/store.(*Manager).SetSearchMode` |  | |
| `0x89d1cc0` | `google3/third_party/jetski/cli/store/store.(*Manager).SetBugReportConfig` |  | |
| `0x89d2400` | `google3/third_party/jetski/cli/store/store.(*Manager).GetMcpManager` |  | |
| `0x89d2a80` | `google3/third_party/jetski/cli/store/store.(*Manager).SetScrollOffsets` |  | |
| `0x89d2c80` | `google3/third_party/jetski/cli/store/store.(*Manager).ScrollOffsets` |  | |
| `0x89d2d60` | `google3/third_party/jetski/cli/store/store.(*Manager).Layout` |  | |
| `0x89d30e0` | `google3/third_party/jetski/cli/store/store.(*Manager).SetPreviousBashResponse` |  | |
| `0x89d32e0` | `google3/third_party/jetski/cli/store/store.(*Manager).StreamError` |  | |
| `0x89d33c0` | `google3/third_party/jetski/cli/store/store.(*Manager).runAsyncBackendCall` |  | |
| `0x89d37a0` | `google3/third_party/jetski/cli/store/store.(*Manager).ReloadSlashCommandsAndSkillsSync` |  | |
| `0x89d38c0` | `google3/third_party/jetski/cli/store/store.(*Manager).ReloadSystemSlashCommandsSync` |  | |
| `0x89d3980` | `google3/third_party/jetski/cli/store/store.(*Manager).SetCycleMode` |  | |
| `0x89d4640` | `google3/third_party/jetski/cli/store/store.(*Manager).StartPluginMcpServers` |  | |
| `0x89d4d00` | `google3/third_party/jetski/cli/store/store.(*Manager).stopPluginMcpServers` |  | |
| `0x89d6b60` | `google3/third_party/jetski/cli/store/store.(*Manager).initModelConfig` |  | |
| `0x89d7c00` | `google3/third_party/jetski/cli/store/store.(*Manager).warnFlagErrorOnce` |  | |
| `0x89d84c0` | `google3/third_party/jetski/cli/store/store.(*Manager).applySavedModel` |  | |
| `0x89da260` | `google3/third_party/jetski/cli/store/store.(*Manager).beginOneShotModel` |  | |
| `0x89da4e0` | `google3/third_party/jetski/cli/store/store.(*Manager).currentModelLabel` |  | |
| `0x89da620` | `google3/third_party/jetski/cli/store/store.(*Manager).restoreOneShotModelAsync` |  | |
| `0x89dbbe0` | `google3/third_party/jetski/cli/store/store.(*Manager).LookupPermission` |  | |
| `0x89dcaa0` | `google3/third_party/jetski/cli/store/store.(*Manager).AddConversationDenyRule` |  | |
| `0x89dd300` | `google3/third_party/jetski/cli/store/store.(*Manager).GetConversationPermissions` |  | |
| `0x89dd400` | `google3/third_party/jetski/cli/store/store.(*Manager).SetProjectPermissions` |  | |
| `0x89dd6c0` | `google3/third_party/jetski/cli/store/store.(*Manager).AddPermissionRule` |  | |
| `0x89de1e0` | `google3/third_party/jetski/cli/store/store.(*Manager).RemovePermissionRule` |  | |
| `0x89e0560` | `google3/third_party/jetski/cli/store/store.(*Manager).HasUnsandboxedPermissionRules` |  | |
| `0x89e0620` | `google3/third_party/jetski/cli/store/store.(*Manager).unsandboxedRuleSourcesUnlocked` |  | |
| `0x89e0b00` | `google3/third_party/jetski/cli/store/store.(*Manager).UnsandboxedRuleSources` |  | |
| `0x89e0be0` | `google3/third_party/jetski/cli/store/store.(*Manager).WarnUnsandboxedPermissions` |  | |
| `0x89ee1c0` | `google3/third_party/jetski/cli/store/store.(*Manager).acquireConversationPresence` |  | |
| `0x89eed80` | `google3/third_party/jetski/cli/store/store.(*Manager).PollPrintmode` |  | |
| `0x89f0880` | `google3/third_party/jetski/cli/store/store.(*Manager).ProactivePromptMetadata` |  | |
| `0x89f09e0` | `google3/third_party/jetski/cli/store/store.(*Manager).SetFeedbackDraft` |  | |
| `0x89f0ba0` | `google3/third_party/jetski/cli/store/store.(*Manager).ResetProactivePromptState` |  | |
| `0x89f1160` | `google3/third_party/jetski/cli/store/store.(*Manager).TriggerProactiveFeedback` |  | |
| `0x89f1a80` | `google3/third_party/jetski/cli/store/store.(*Manager).RemoteControlStatus` |  | |
| `0x89f2f00` | `google3/third_party/jetski/cli/store/store.(*Manager).commitWindow` |  | |
| `0x89f81c0` | `google3/third_party/jetski/cli/store/store.(*Manager).triggerStatusLineUpdate` |  | |
| `0x89fde40` | `google3/third_party/jetski/cli/store/store.(*Manager).SetBackendForTest` |  | |
| `0x89fdea0` | `google3/third_party/jetski/cli/store/store.(*Manager).ToolResponsesForTest` |  | |
| `0x89ff260` | `google3/third_party/jetski/cli/store/store.(*Manager).UpdateSubagentSteps` |  | |
| `0x8a006c0` | `google3/third_party/jetski/cli/store/store.(*Manager).RespondToSubagentToolConfirmation` |  | |
| `0x8a01400` | `google3/third_party/jetski/cli/store/store.(*Manager).updatePendingApprovalsQueue` |  | |
| `0x8a05e00` | `google3/third_party/jetski/cli/store/store.(*Manager).resolveSkill` |  | |
| `0x8a05e80` | `google3/third_party/jetski/cli/store/store.(*Manager).parseLeadingSlashCommands` |  | |
| `0x8a062c0` | `google3/third_party/jetski/cli/store/store.(*Manager).parseSystemSlashCommand` |  | |
| `0x8a06880` | `google3/third_party/jetski/cli/store/store.(*Manager).parseSuffixSlashCommand` |  | |
| `0x8a09b80` | `google3/third_party/jetski/cli/store/store.(*Manager).ensureTerminalDetected` |  | |
| `0x8a09be0` | `google3/third_party/jetski/cli/store/store.(*Manager).DetectTerminalCapabilities` |  | |
| `0x8a09c40` | `google3/third_party/jetski/cli/store/store.(*Manager).IsAppleTerminalSSH` |  | |
| `0x8a09c80` | `google3/third_party/jetski/cli/store/store.(*Manager).SetTerminalInfo` |  | |
| `0x8a0a5a0` | `google3/third_party/jetski/cli/store/store.(*Manager).SetTerminalBackground` |  | |
| `0x8a0a700` | `google3/third_party/jetski/cli/store/store.(*Manager).commitTerminalInfo` |  | |
| `0x8a0c5e0` | `google3/third_party/jetski/cli/store/store.(*Manager).advanceDrip` |  | |
| `0x8a0d500` | `google3/third_party/jetski/cli/store/store.(*Manager).GetTip` |  | |
| `0x8a0dfe0` | `google3/third_party/jetski/cli/store/store.(*Manager).TitleRunner` |  | |
| `0x8a0e160` | `google3/third_party/jetski/cli/store/store.(*Manager).TitleEnabled` |  | |
| `0x8a0e520` | `google3/third_party/jetski/cli/store/store.(*Manager).recordHeadlessSoftDeny` |  | |
| `0x8a0f380` | `google3/third_party/jetski/cli/store/store.(*Manager).autoModeExperiment` |  | |
| `0x8a0f3a0` | `google3/third_party/jetski/cli/store/store.(*Manager).autoModeArm` |  | |
| `0x8a108c0` | `google3/third_party/jetski/cli/store/store.(*Manager).clearRemotelyResolvedInteractions` |  | |
| `0x8a10d40` | `google3/third_party/jetski/cli/store/store.(*Manager).noteTurnStreamLocked` |  | |
| `0x8a110c0` | `google3/third_party/jetski/cli/store/store.(*Manager).turnStepsLocked` |  | |
| `0x8a12420` | `google3/third_party/jetski/cli/store/store.(*Manager).commitVersionInfo` |  | |
| `0x8a12660` | `google3/third_party/jetski/cli/store/store.(*Manager).syncWorkflowAgents` |  | |
| `0x8a15660` | `google3/third_party/jetski/cli/store/store.(*Manager).initWorkspaceDirs` |  | |
| `0x8a15760` | `google3/third_party/jetski/cli/store/store.(*Manager).ReadWorkspaceDirs` |  | |
| `0x8a15d20` | `google3/third_party/jetski/cli/store/store.(*Manager).AddWorkspaceDir` |  | |
| `0x8a28220` | `google3/third_party/jetski/cli/store/store.(*Manager).loadCascadeNux-fm` |  | |
| `0x8a28280` | `google3/third_party/jetski/cli/store/store.(*Manager).doFetchAdminControls-fm` | **yes** | |
| `0x8a282e0` | `google3/third_party/jetski/cli/store/store.(*Manager).doRefreshVCS-fm` | **yes** | |
| `0x8a28340` | `google3/third_party/jetski/cli/store/store.(*Manager).doRefreshG1Credits-fm` | **yes** | |
| `0x8a284c0` | `google3/third_party/jetski/cli/store/store.(*Manager).refreshExperiments-fm` | **yes** | |

## `google3/third_party/jetski/cli/store/store.(*Manager).ReloadSlashCommandsAndSkills`

_1 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x8a1eb40` | `google3/third_party/jetski/cli/store/store.(*Manager).ReloadSlashCommandsAndSkills.gowrap1` |  | |

## `google3/third_party/jetski/cli/store/store.(*Manager).SendBtwQuestion.func1`

_1 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x8a188a0` | `google3/third_party/jetski/cli/store/store.(*Manager).SendBtwQuestion.func1.1` |  | |

## `google3/third_party/jetski/cli/store/store.(*Manager).SetCycleMode`

_1 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x8a1ebc0` | `google3/third_party/jetski/cli/store/store.(*Manager).SetCycleMode.gowrap1` |  | |

## `google3/third_party/jetski/cli/store/store.(*Manager).userInputLoop.func10`

_1 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x8a1b7a0` | `google3/third_party/jetski/cli/store/store.(*Manager).userInputLoop.func10.1` | **yes** | |

## `google3/third_party/jetski/cli/store/store.(*OSC52Clipboard)`

_1 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x8a28060` | `google3/third_party/jetski/cli/store/store.(*OSC52Clipboard).ReadAll` |  | |

## `google3/third_party/jetski/cli/store/store.(*PluginsManager)`

_22 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x89e1d40` | `google3/third_party/jetski/cli/store/store.(*PluginsManager).stopPluginProcesses` |  | |
| `0x89e1de0` | `google3/third_party/jetski/cli/store/store.(*PluginsManager).resolveConfigDir` |  | |
| `0x89e1ec0` | `google3/third_party/jetski/cli/store/store.(*PluginsManager).GetCachedPlugins` |  | |
| `0x89e2000` | `google3/third_party/jetski/cli/store/store.(*PluginsManager).InvalidateMarketplaceCache` | **yes** | |
| `0x89e20e0` | `google3/third_party/jetski/cli/store/store.(*PluginsManager).installedInventory` |  | |
| `0x89e23c0` | `google3/third_party/jetski/cli/store/store.(*PluginsManager).cacheInventory` |  | |
| `0x89e25c0` | `google3/third_party/jetski/cli/store/store.(*PluginsManager).GetPlugins` |  | |
| `0x89e2e60` | `google3/third_party/jetski/cli/store/store.(*PluginsManager).fetchMarketplaceCatalog` | **yes** | |
| `0x89e40a0` | `google3/third_party/jetski/cli/store/store.(*PluginsManager).listInstalled` |  | |
| `0x89e58e0` | `google3/third_party/jetski/cli/store/store.(*PluginsManager).CachedInstalledPlugin` |  | |
| `0x89e5c00` | `google3/third_party/jetski/cli/store/store.(*PluginsManager).NeedsMcpSetup` |  | |
| `0x89e5c60` | `google3/third_party/jetski/cli/store/store.(*PluginsManager).SavePluginMcpVariables` |  | |
| `0x89e6060` | `google3/third_party/jetski/cli/store/store.(*PluginsManager).InstallPlugin` |  | |
| `0x89e64e0` | `google3/third_party/jetski/cli/store/store.(*PluginsManager).afterPluginInstalled` |  | |
| `0x89e6d60` | `google3/third_party/jetski/cli/store/store.(*PluginsManager).UninstallPlugin` |  | |
| `0x89e8860` | `google3/third_party/jetski/cli/store/store.(*PluginsManager).FindInstalledPluginWithRefresh` | **yes** | |
| `0x89e8980` | `google3/third_party/jetski/cli/store/store.(*PluginsManager).FindMarketplacePluginWithRefresh` | **yes** | |
| `0x89e8da0` | `google3/third_party/jetski/cli/store/store.(*PluginsManager).MarketplacePluginComponents` |  | |
| `0x89ebfa0` | `google3/third_party/jetski/cli/store/store.(*PluginsManager).InstalledPluginEvent` |  | |
| `0x89ec960` | `google3/third_party/jetski/cli/store/store.(*PluginsManager).KnownMarketplace` |  | |
| `0x89ed0c0` | `google3/third_party/jetski/cli/store/store.(*PluginsManager).Preload` |  | |
| `0x89ed860` | `google3/third_party/jetski/cli/store/store.(*PluginsManager).markInstalledStale` |  | |

## `google3/third_party/jetski/cli/store/store.(*PluginsManager).GetPlugins.func1`

_1 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x8a202e0` | `google3/third_party/jetski/cli/store/store.(*PluginsManager).GetPlugins.func1.1` |  | |

## `google3/third_party/jetski/cli/store/store.(*SkillsManager)`

_2 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x89f3720` | `google3/third_party/jetski/cli/store/store.(*SkillsManager).GetCachedSkills` |  | |
| `0x89f4680` | `google3/third_party/jetski/cli/store/store.(*SkillsManager).InitSkills` |  | |

## `google3/third_party/jetski/cli/store/store.(*StatusLineRunner)`

_2 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x89f8980` | `google3/third_party/jetski/cli/store/store.(*StatusLineRunner).Run` |  | |
| `0x89f8cc0` | `google3/third_party/jetski/cli/store/store.(*StatusLineRunner).ErrorHint` |  | |

## `google3/third_party/jetski/cli/store/store.(*Store)`

_22 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x8998b60` | `google3/third_party/jetski/cli/store/store.(*Store).AdminControls` |  | |
| `0x8998b80` | `google3/third_party/jetski/cli/store/store.(*Store).IsOptionDisallowed` |  | |
| `0x8998de0` | `google3/third_party/jetski/cli/store/store.(*Store).GetAllowedFallbackValue` |  | |
| `0x89a9500` | `google3/third_party/jetski/cli/store/store.(*Store).EffectiveColorScheme` |  | |
| `0x89a95e0` | `google3/third_party/jetski/cli/store/store.(*Store).EffectiveBackground` |  | |
| `0x89abd20` | `google3/third_party/jetski/cli/store/store.(*Store).appliedContextWindow` |  | |
| `0x89fa3c0` | `google3/third_party/jetski/cli/store/store.(*Store).SetConversation` |  | |
| `0x89fa480` | `google3/third_party/jetski/cli/store/store.(*Store).ProjectPermissions` |  | |
| `0x89fa4a0` | `google3/third_party/jetski/cli/store/store.(*Store).SharedConfigPermissions` |  | |
| `0x89fa4c0` | `google3/third_party/jetski/cli/store/store.(*Store).SetCliSetting` |  | |
| `0x89fa5a0` | `google3/third_party/jetski/cli/store/store.(*Store).OnboardingStatus` | **yes** | |
| `0x89fa620` | `google3/third_party/jetski/cli/store/store.(*Store).TerminalInfo` |  | |
| `0x89fa640` | `google3/third_party/jetski/cli/store/store.(*Store).RenderedWidth` |  | |
| `0x89fa660` | `google3/third_party/jetski/cli/store/store.(*Store).SetTerminalInfo` |  | |
| `0x89fa900` | `google3/third_party/jetski/cli/store/store.(*Store).AuthPlanTier` | **yes** | |
| `0x89fa9e0` | `google3/third_party/jetski/cli/store/store.(*Store).LogoOverride` |  | |
| `0x89faa00` | `google3/third_party/jetski/cli/store/store.(*Store).ProjectInfo` |  | |
| `0x89faa20` | `google3/third_party/jetski/cli/store/store.(*Store).ProjectName` |  | |
| `0x89faa40` | `google3/third_party/jetski/cli/store/store.(*Store).AnnouncementMessage` |  | |
| `0x89faa60` | `google3/third_party/jetski/cli/store/store.(*Store).ActiveNux` |  | |
| `0x89fab40` | `google3/third_party/jetski/cli/store/store.(*Store).AutoModePreset` |  | |
| `0x8c563a0` | `google3/third_party/jetski/cli/store/store.(*Store).SubagentAwaitsApproval-fm` |  | |

## `google3/third_party/jetski/cli/store/store.(*TaskManager)`

_6 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x8a07340` | `google3/third_party/jetski/cli/store/store.(*TaskManager).UpdateShellCommandOutput` |  | |
| `0x8a07ce0` | `google3/third_party/jetski/cli/store/store.(*TaskManager).StartHiddenBackgroundTask` |  | |
| `0x8a07dc0` | `google3/third_party/jetski/cli/store/store.(*TaskManager).RemoveBackgroundTask` |  | |
| `0x8a08100` | `google3/third_party/jetski/cli/store/store.(*TaskManager).backgroundTaskLoop` |  | |
| `0x8a08d60` | `google3/third_party/jetski/cli/store/store.(*TaskManager).GetBackgroundTasks` |  | |
| `0x8a28400` | `google3/third_party/jetski/cli/store/store.(*TaskManager).backgroundTaskLoop-fm` |  | |

## `google3/third_party/jetski/cli/store/store.(*fullRedraw)`

_2 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x89f1f40` | `google3/third_party/jetski/cli/store/store.(*fullRedraw).run` |  | |
| `0x89f2500` | `google3/third_party/jetski/cli/store/store.(*fullRedraw).poll` |  | |

## `google3/third_party/jetski/cli/store/store.(*pendingBatch)`

_2 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x89da9a0` | `google3/third_party/jetski/cli/store/store.(*pendingBatch).takeThrough` |  | |
| `0x89db020` | `google3/third_party/jetski/cli/store/store.(*pendingBatch).prepend` |  | |

## `google3/third_party/jetski/cli/store/store.(*pluginsWatcher)`

_2 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x89ed8e0` | `google3/third_party/jetski/cli/store/store.(*pluginsWatcher).syncPluginDirs` |  | |
| `0x89edd00` | `google3/third_party/jetski/cli/store/store.(*pluginsWatcher).relevant` |  | |

## `google3/third_party/jetski/cli/store/store.(*textDrip)`

_6 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x8a0abc0` | `google3/third_party/jetski/cli/store/store.(*textDrip).flush` |  | |
| `0x8a0b260` | `google3/third_party/jetski/cli/store/store.(*textDrip).start` |  | |
| `0x8a0b3c0` | `google3/third_party/jetski/cli/store/store.(*textDrip).stop` |  | |
| `0x8a0b480` | `google3/third_party/jetski/cli/store/store.(*textDrip).reset` |  | |
| `0x8a0b540` | `google3/third_party/jetski/cli/store/store.(*textDrip).prime` |  | |
| `0x8a0b720` | `google3/third_party/jetski/cli/store/store.(*textDrip).pendingTail` |  | |

## `google3/third_party/jetski/cli/store/store.(*workflowAgents)`

_1 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x8a12560` | `google3/third_party/jetski/cli/store/store.(*workflowAgents).stopUnlocked` |  | |

## Pending / errors (276)

Functions that did not decompile (likely thunks, glue, or out-of-spec):

- `0x8998760` — `google3/third_party/jetski/cli/store/store.(*Manager).FetchAdminControls`
- `0x89987c0` — `google3/third_party/jetski/cli/store/store.(*Manager).enableAdminControls`
- `0x89988c0` — `google3/third_party/jetski/cli/store/store.(*Manager).doFetchAdminControls`
- `0x8999660` — `google3/third_party/jetski/cli/store/store.(*Manager).applySandboxModeOverride`
- `0x89999c0` — `google3/third_party/jetski/cli/store/store.(*Manager).GetGlobalAgentsCreatePath`
- `0x899a180` — `google3/third_party/jetski/cli/store/store.(*Manager).SelectedAgent`
- `0x899c900` — `google3/third_party/jetski/cli/store/store.(*Manager).checkStepForAskQuestion`
- `0x899ca20` — `google3/third_party/jetski/cli/store/store.(*Manager).StartTranscription`
- `0x899e060` — `google3/third_party/jetski/cli/store/store.(*Manager).ValidateAndOnboardAccount`
- `0x899e0e0` — `google3/third_party/jetski/cli/store/store.(*Manager).IsAuthMethodSupported`
- `0x899e800` — `google3/third_party/jetski/cli/store/store.(*Manager).StartBattleSession`
- `0x899e880` — `google3/third_party/jetski/cli/store/store.(*Manager).CancelBattleSession`
- `0x89a2180` — `google3/third_party/jetski/cli/store/store.(*Manager).SetModelOverride`
- `0x89a2420` — `google3/third_party/jetski/cli/store/store.(*Manager).setModelInMemory`
- `0x89a2640` — `google3/third_party/jetski/cli/store/store.(*Manager).GetCliSettings`
- `0x89a29a0` — `google3/third_party/jetski/cli/store/store.(*Manager).ReadCliSettingsFromDisk`
- `0x89a2bc0` — `google3/third_party/jetski/cli/store/store.(*Manager).WriteCliSettings`
- `0x89a5860` — `google3/third_party/jetski/cli/store/store.(*Manager).SetTerminalSandboxOverride`
- `0x89a5b00` — `google3/third_party/jetski/cli/store/store.(*Manager).SetShowFeedbackSurveyOverride`
- `0x89a7620` — `google3/third_party/jetski/cli/store/store.(*Manager).ReadOnboardingStatus`
- `0x89a77a0` — `google3/third_party/jetski/cli/store/store.(*Manager).WriteOnboardingStatus`
- `0x89a7c80` — `google3/third_party/jetski/cli/store/store.(*Manager).SetOnTelemetrySynced`
- `0x89a7d80` — `google3/third_party/jetski/cli/store/store.(*Manager).notifyTelemetrySynced`
- `0x89a97c0` — `google3/third_party/jetski/cli/store/store.(*Manager).AddCommandOutputRunning`
- `0x89a9840` — `google3/third_party/jetski/cli/store/store.(*Manager).AddCommandOutputInProgress`
- `0x89aa080` — `google3/third_party/jetski/cli/store/store.(*Manager).AddWarningAlert`
- `0x89aa120` — `google3/third_party/jetski/cli/store/store.(*Manager).AddWarning`
- `0x89abca0` — `google3/third_party/jetski/cli/store/store.(*Store).ContextWindowChoice`
- `0x89abce0` — `google3/third_party/jetski/cli/store/store.(*Store).ContextWindow`
- `0x89abe60` — `google3/third_party/jetski/cli/store/store.(*Manager).SetContextWindow`
- `0x89ac180` — `google3/third_party/jetski/cli/store/store.(*Manager).GetConversationGroups`
- `0x89af640` — `google3/third_party/jetski/cli/store/store.(*Manager).AddAbsoluteIndex`
- `0x89b5280` — `google3/third_party/jetski/cli/store/store.(*Manager).maybeReportFirstToken`
- `0x89b54a0` — `google3/third_party/jetski/cli/store/store.(*Manager).RenameConversation`
- `0x89b5600` — `google3/third_party/jetski/cli/store/store.(*Manager).RenameConversationByID`
- `0x89b72a0` — `google3/third_party/jetski/cli/store/store.(*Manager).reviveDeadStream`
- `0x89b8860` — `google3/third_party/jetski/cli/store/store.(*Manager).resetConversationSteps`
- `0x89ba340` — `google3/third_party/jetski/cli/store/store.(*Manager).SetMessageListLineCap`
- `0x89ba360` — `google3/third_party/jetski/cli/store/store.(*Manager).GetMessageListLineCap`
- `0x89bab80` — `google3/third_party/jetski/cli/store/store.(*Manager).RebuildIndices`
- `0x89bd160` — `google3/third_party/jetski/cli/store/store.(*Manager).EnsureProjectCreated`
- `0x89bd660` — `google3/third_party/jetski/cli/store/store.(*Manager).updateConversationByIDUnlocked`
- `0x89bd880` — `google3/third_party/jetski/cli/store/store.(*Manager).RefreshG1Credits`
- `0x89bdbe0` — `google3/third_party/jetski/cli/store/store.(*ExitState).Press`
- `0x89bde80` — `google3/third_party/jetski/cli/store/store.(*Manager).OnExperimentsReady`
- `0x89be5a0` — `google3/third_party/jetski/cli/store/store.(*Store).GcertStatus`
- `0x89beca0` — `google3/third_party/jetski/cli/store/store.(*Manager).HeadlessDenials`
- `0x89c0060` — `google3/third_party/jetski/cli/store/store.(*Manager).GetDefaultHooksPath`
- `0x89c00a0` — `google3/third_party/jetski/cli/store/store.(*Manager).updateStoreHooks`
- `0x89c1ea0` — `google3/third_party/jetski/cli/store/store.(*Manager).InMemoryCLISettingsProvider`

... and 226 more.

See `/workspace/agy/out/decompile/dec/_errors.txt` for details.
