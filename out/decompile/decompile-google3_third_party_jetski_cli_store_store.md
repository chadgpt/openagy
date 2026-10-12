# Decompile report — `google3/third_party/jetski/cli/store/store`

> 120 priority functions in this Go package

**Decompiled:** 61/120

## `<package>`

_61 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x899e220` | `google3/third_party/jetski/cli/store/store.IsBackgroundTaskStep` |  | |
| `0x899e280` | `google3/third_party/jetski/cli/store/store.LiveAgentTaskSteps` |  | |
| `0x899e380` | `google3/third_party/jetski/cli/store/store.forEachActiveBackgroundTask` |  | |
| `0x899e460` | `google3/third_party/jetski/cli/store/store.ActiveAgentTaskStepIndices` |  | |
| `0x899ed00` | `google3/third_party/jetski/cli/store/store.deriveSideQuestionError` |  | |
| `0x89a2b40` | `google3/third_party/jetski/cli/store/store.isValidUnifiedRule` |  | |
| `0x89a9000` | `google3/third_party/jetski/cli/store/store.tmuxLoadBuffer` |  | |
| `0x89a9320` | `google3/third_party/jetski/cli/store/store.nativeCopy` |  | |
| `0x89b1dc0` | `google3/third_party/jetski/cli/store/store.reconcileSendingMessages` |  | |
| `0x89bb480` | `google3/third_party/jetski/cli/store/store.ComputeRebuiltIndices` |  | |
| `0x89bc000` | `google3/third_party/jetski/cli/store/store.canUpgradeTrailingThoughtToToolGroup` |  | |
| `0x89bc1c0` | `google3/third_party/jetski/cli/store/store.canMergeConsecutiveThoughts` |  | |
| `0x89bc3c0` | `google3/third_party/jetski/cli/store/store.groupSteps` |  | |
| `0x89be6a0` | `google3/third_party/jetski/cli/store/store.denialsFromTrajectory` |  | |
| `0x89c7a60` | `google3/third_party/jetski/cli/store/store.getPermissionIndices` |  | |
| `0x89c7ae0` | `google3/third_party/jetski/cli/store/store.scanStep` |  | |
| `0x89cb8a0` | `google3/third_party/jetski/cli/store/store.isFileInsideWorkspace` |  | |
| `0x89cc3a0` | `google3/third_party/jetski/cli/store/store.NewManager` |  | |
| `0x89d5bc0` | `google3/third_party/jetski/cli/store/store.splitTextAndMentions` |  | |
| `0x89d6aa0` | `google3/third_party/jetski/cli/store/store.isWordChar` |  | |
| `0x89df8a0` | `google3/third_party/jetski/cli/store/store.removeFromList` |  | |
| `0x89e0040` | `google3/third_party/jetski/cli/store/store.BuildUnsandboxedPermissionsWarning` |  | |
| `0x89e1b00` | `google3/third_party/jetski/cli/store/store.featureProvider` |  | |
| `0x89e1c00` | `google3/third_party/jetski/cli/store/store.thirdPartyMarketplaces` |  | |
| `0x89e1ce0` | `google3/third_party/jetski/cli/store/store.pluginCommandAvailable` |  | |
| `0x89e3da0` | `google3/third_party/jetski/cli/store/store.enrichInstalledFromCatalog` |  | |
| `0x89e4420` | `google3/third_party/jetski/cli/store/store.listManagedPlugins` |  | |
| `0x89e4640` | `google3/third_party/jetski/cli/store/store.pluginSummaryFor` |  | |
| `0x89e4e00` | `google3/third_party/jetski/cli/store/store.ruleNames` |  | |
| `0x89e4fa0` | `google3/third_party/jetski/cli/store/store.builtinPluginsRoot` |  | |
| `0x89e7360` | `google3/third_party/jetski/cli/store/store.FindInstalledPlugin` |  | |
| `0x89e7820` | `google3/third_party/jetski/cli/store/store.PluginAlreadyInstalled` |  | |
| `0x89e7980` | `google3/third_party/jetski/cli/store/store.ResolvePluginPath` |  | |
| `0x89e8220` | `google3/third_party/jetski/cli/store/store.stripPathQuotes` |  | |
| `0x89e82a0` | `google3/third_party/jetski/cli/store/store.IsPathLikePrefix` |  | |
| `0x89e8460` | `google3/third_party/jetski/cli/store/store.matchedPrefixLen` |  | |
| `0x89e85c0` | `google3/third_party/jetski/cli/store/store.CompleteLocalPluginPath` |  | |
| `0x89e8e40` | `google3/third_party/jetski/cli/store/store.externalMarketplaceIndex` |  | |
| `0x89e9040` | `google3/third_party/jetski/cli/store/store.fetchExternalMarketplacePlugins` | **yes** | |
| `0x89e96c0` | `google3/third_party/jetski/cli/store/store.installExternalMarketplacePluginImpl` |  | |
| `0x89ea560` | `google3/third_party/jetski/cli/store/store.isSafeInstallDirName` |  | |
| `0x89ebf40` | `google3/third_party/jetski/cli/store/store.fetchAgentMarketplacePluginsImpl` | **yes** | |
| `0x89ec360` | `google3/third_party/jetski/cli/store/store.classifyInstalledPlugin` |  | |
| `0x89eea00` | `google3/third_party/jetski/cli/store/store.expandedCommands` |  | |
| `0x89effe0` | `google3/third_party/jetski/cli/store/store.allNonTaskStepsPrinted` |  | |
| `0x89f6080` | `google3/third_party/jetski/cli/store/store.BuildStatusLineData` |  | |
| `0x8a05880` | `google3/third_party/jetski/cli/store/store.skillSlashCommandScopeItem` |  | |
| `0x8a05ae0` | `google3/third_party/jetski/cli/store/store.splitSlashToken` | **yes** | |
| `0x8a05cc0` | `google3/third_party/jetski/cli/store/store.LeadingSlashCommandName` |  | |
| `0x8a09120` | `google3/third_party/jetski/cli/store/store.resolveShell` |  | |
| `0x8a09260` | `google3/third_party/jetski/cli/store/store.detectOSC8Support` |  | |
| `0x8a097e0` | `google3/third_party/jetski/cli/store/store.getTerminalName` |  | |
| `0x8a09a40` | `google3/third_party/jetski/cli/store/store.detectRemoteSession` |  | |
| `0x8a09ac0` | `google3/third_party/jetski/cli/store/store.detectTermSupportsAltScreen` |  | |
| `0x8a09fa0` | `google3/third_party/jetski/cli/store/store.detectInitialOSC8Support` |  | |
| `0x8a0a080` | `google3/third_party/jetski/cli/store/store.queryAppleTerminalDA2` |  | |
| `0x8a0f500` | `google3/third_party/jetski/cli/store/store.toolNameFromStep` |  | |
| `0x8a106a0` | `google3/third_party/jetski/cli/store/store.canAutoApproveWrite` |  | |
| `0x8a11380` | `google3/third_party/jetski/cli/store/store.lastStepShowsError` |  | |
| `0x8a11cc0` | `google3/third_party/jetski/cli/store/store.validateTransition` | **yes** | |
| `0x8a14e20` | `google3/third_party/jetski/cli/store/store.hasWorkspaceDir` |  | |

## Pending / errors (59)

Functions that did not decompile (likely thunks, glue, or out-of-spec):

- `0x899e180` — `google3/third_party/jetski/cli/store/store.IsAgentCommandStep`
- `0x89ac0c0` — `google3/third_party/jetski/cli/store/store.NormalizeGroupName`
- `0x89b5200` — `google3/third_party/jetski/cli/store/store.isFirstTokenStep`
- `0x89ba380` — `google3/third_party/jetski/cli/store/store.findLastToolGroupAbsIdx`
- `0x89bbd60` — `google3/third_party/jetski/cli/store/store.lastToolStepInGroup`
- `0x89bbe20` — `google3/third_party/jetski/cli/store/store.isThoughtOnlyGroup`
- `0x89be5c0` — `google3/third_party/jetski/cli/store/store.isDeniedInteraction`
- `0x89c82a0` — `google3/third_party/jetski/cli/store/store.toItems`
- `0x89d5640` — `google3/third_party/jetski/cli/store/store.specBelongsToPlugin`
- `0x89d69e0` — `google3/third_party/jetski/cli/store/store.isPathChar`
- `0x89d7fe0` — `google3/third_party/jetski/cli/store/store.availableModelsHint`
- `0x89d91c0` — `google3/third_party/jetski/cli/store/store.showableNux`
- `0x89d9280` — `google3/third_party/jetski/cli/store/store.pendingNuxes`
- `0x89d9fe0` — `google3/third_party/jetski/cli/store/store.readNuxFile`
- `0x89ded20` — `google3/third_party/jetski/cli/store/store.addToList`
- `0x89e0de0` — `google3/third_party/jetski/cli/store/store.FetchCLIFeatureProvider`
- `0x89e7280` — `google3/third_party/jetski/cli/store/store.normalizePluginTarget`
- `0x89e7660` — `google3/third_party/jetski/cli/store/store.marketplaceEntryMatches`
- `0x89e7700` — `google3/third_party/jetski/cli/store/store.FindMarketplacePlugin`
- `0x89e7be0` — `google3/third_party/jetski/cli/store/store.LocalPluginDir`
- `0x89e7c60` — `google3/third_party/jetski/cli/store/store.InspectLocalPluginDir`
- `0x89e8d20` — `google3/third_party/jetski/cli/store/store.installExternalMarketplacePlugin`
- `0x89e95e0` — `google3/third_party/jetski/cli/store/store.isMarketplaceEntryID`
- `0x89ea5e0` — `google3/third_party/jetski/cli/store/store.checkInstallDirFree`
- `0x89ea900` — `google3/third_party/jetski/cli/store/store.installedFromEntry`
- `0x89eab80` — `google3/third_party/jetski/cli/store/store.marketplacePluginComponentsImpl`
- `0x89eaf20` — `google3/third_party/jetski/cli/store/store.pluginComponentKinds`
- `0x89eb220` — `google3/third_party/jetski/cli/store/store.installMarketplacePluginFromCLI`
- `0x89ece00` — `google3/third_party/jetski/cli/store/store.RecordPluginAction`
- `0x89f0100` — `google3/third_party/jetski/cli/store/store.storePlannerText`
- `0x89f02a0` — `google3/third_party/jetski/cli/store/store.StripThoughts`
- `0x89f03c0` — `google3/third_party/jetski/cli/store/store.sampleProactiveTargetTurn`
- `0x89f3820` — `google3/third_party/jetski/cli/store/store.isReservedCommandName`
- `0x89f5280` — `google3/third_party/jetski/cli/store/store.skillsReloadSummary`
- `0x89f7840` — `google3/third_party/jetski/cli/store/store.detectVCSOnDisk`
- `0x89f7a40` — `google3/third_party/jetski/cli/store/store.ModelEffortDisplay`
- `0x89f7d00` — `google3/third_party/jetski/cli/store/store.stripEffortSuffix`
- `0x89f9e60` — `google3/third_party/jetski/cli/store/store.expandTilde`
- `0x89f9f20` — `google3/third_party/jetski/cli/store/store.cleanAndTruncateError`
- `0x89fae20` — `google3/third_party/jetski/cli/store/store.NewStore`
- `0x89fbba0` — `google3/third_party/jetski/cli/store/store.Deserialize`
- `0x8a011c0` — `google3/third_party/jetski/cli/store/store.deriveTriggerInput`
- `0x8a09420` — `google3/third_party/jetski/cli/store/store.isLocalAppleTerminal`
- `0x8a09540` — `google3/third_party/jetski/cli/store/store.queryTmuxTermFeatures`
- `0x8a096a0` — `google3/third_party/jetski/cli/store/store.tmuxSupportsHyperlinks`
- `0x8a098e0` — `google3/third_party/jetski/cli/store/store.detectOSC52Support`
- `0x8a0a420` — `google3/third_party/jetski/cli/store/store.readAppleTerminalDA2`
- `0x8a0a840` — `google3/third_party/jetski/cli/store/store.cutAtRuneBoundary`
- `0x8a0ba40` — `google3/third_party/jetski/cli/store/store.pruneCoveredEntries`
- `0x8a0e480` — `google3/third_party/jetski/cli/store/store.softDenialFromStep`

... and 9 more.

See `/workspace/agy/out/decompile/dec/_errors.txt` for details.
