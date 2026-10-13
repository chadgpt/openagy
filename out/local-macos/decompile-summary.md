# Decompile summary — agy (macOS/arm64, local run)

> Target: `/Users/gear/.local/bin/agy` (Mach-O arm64, agy 1.3.4)
> SHA-256: `9da414c0624c27aa2969a86030a070b5341c0657700512eba70b21725ce253f5`
> Go toolchain: `go1.28-20260921-RC02` (Google internal, tags `fieldtrack,boringcrypto,simd`)
> Decompiler: Ghidra 12.1.4, imported with `-noanalysis`, native decompiler built for mac_arm_64
> Priority list: `/Users/gear/Documents/GitHub/openagy/out/local-macos/priority-funcs.txt` (2101 funcs across 93 Go packages)
> Output: `/Users/gear/Documents/GitHub/openagy/out/local-macos/dec/<HEX>_<shortname>.c`

## Headline numbers

| Metric | Value |
|---|---|
| Functions recovered from pclntab | 154,525 |
| Ghidra functions created from seeds | 154,506 (19 already existed, **0 failed**) |
| Priority funcs decompiled | 2101/2101 |
| Decompiled LOC | 307,357 |
| Decompile wall time | 56 s |

## All packages

| Functions | Decompiled | LOC | Package |
|---:|---:|---:|---|
| 661 | 661 | 117,096 | `google3/third_party/jetski/cli/store/store.` |
| 334 | 334 | 38,574 | `google3/third_party/jetski/language_server/code_assist_client/codeassistclient.` |
| 195 | 195 | 31,480 | `google3/third_party/jetski/cli/backend/backend.` |
| 190 | 190 | 10,365 | `google3/third_party/jetski/cli/commands/commands.` |
| 131 | 131 | 24,539 | `google3/third_party/jetski/cli/store/store` |
| 90 | 90 | 17,222 | `google3/third_party/jetski/language_server/code_assist_client/codeassistclient` |
| 70 | 70 | 9,880 | `main` |
| 69 | 69 | 15,768 | `google3/third_party/jetski/cli/printmode/printmode` |
| 63 | 63 | 6,751 | `google3/third_party/jetski/cli/backend/auth/auth.` |
| 54 | 54 | 8,309 | `google3/third_party/jetski/cli/backend/backend` |
| 36 | 36 | 3,076 | `google3/third_party/jetski/cli/printmode/printmode.` |
| 26 | 26 | 4,877 | `google3/third_party/jetski/cli/commands/commands` |
| 16 | 16 | 4,340 | `google3/third_party/jetski/cli/updater/updater` |
| 13 | 13 | 2,052 | `google3/third_party/jetski/cli/backend/auth/auth` |
| 11 | 11 | 957 | `main.` |
| 11 | 11 | 2,188 | `main.setupSubcommandUsage` |
| 10 | 10 | 1,135 | `main.init` |
| 9 | 9 | 723 | `google3/third_party/jetski/cli/backend/backend.NewServerBackend` |
| 5 | 5 | 170 | `google3/third_party/jetski/cli/store/store.init` |
| 5 | 5 | 378 | `main.main` |
| 4 | 4 | 206 | `google3/third_party/jetski/cli/backend/auth/auth..embed.1.0.google3/third_party/jetski/cli/backend/auth/auth.` |
| 3 | 3 | 617 | `google3/third_party/jetski/language_server/code_assist_client/codeassistclient.map.init` |
| 3 | 3 | 102 | `google3/third_party/jetski/language_server/code_assist_client/codeassistclient.shouldBypassKeyring` |
| 3 | 3 | 123 | `google3/third_party/jetski/cli/backend/backend.ContextWindow` |
| 3 | 3 | 197 | `google3/third_party/jetski/cli/store/store.OSC52Clipboard` |
| 2 | 2 | 79 | `google3/third_party/jetski/language_server/code_assist_client/codeassistclient.containerDetector` |
| 2 | 2 | 30 | `google3/third_party/jetski/language_server/code_assist_client/codeassistclient.dbusDetector` |
| 2 | 2 | 59 | `google3/third_party/jetski/language_server/code_assist_client/codeassistclient.sshDetector` |
| 2 | 2 | 37 | `google3/third_party/jetski/language_server/code_assist_client/codeassistclient.androidDetector` |
| 2 | 2 | 70 | `google3/third_party/jetski/language_server/code_assist_client/codeassistclient.wslDetector` |
| 2 | 2 | 82 | `google3/third_party/jetski/language_server/code_assist_client/codeassistclient.WithWIFProvider` |
| 2 | 2 | 78 | `google3/third_party/jetski/cli/backend/backend.startTranscriptionWithTimeout` |
| 2 | 2 | 125 | `google3/third_party/jetski/cli/backend/backend.subscribeWithRetry` |
| 2 | 2 | 140 | `google3/third_party/jetski/cli/store/store.map.init` |
| 2 | 2 | 86 | `google3/third_party/jetski/cli/store/store.FileClipboard` |
| 2 | 2 | 41 | `google3/third_party/jetski/cli/store/store.ExitState` |
| 2 | 2 | 313 | `google3/third_party/jetski/cli/store/store.NewManager` |
| 2 | 2 | 105 | `google3/third_party/jetski/cli/store/store.FetchCLIFeatureProvider` |
| 2 | 2 | 62 | `google3/third_party/jetski/cli/store/store.pendingNuxes` |
| 2 | 2 | 107 | `google3/third_party/jetski/cli/store/store.RegisterCLIFeatureProviderLoader` |
| 2 | 2 | 86 | `google3/third_party/jetski/cli/printmode/printmode.applyAgentMode` |
| 2 | 2 | 48 | `main.stderrLogSink` |
| 2 | 2 | 117 | `main.setupSubcommandUsage.func1` |
| 1 | 1 | 349 | `google3/third_party/jetski/language_server/code_assist_client/codeassistclient.ShadowDiffSummary` |
| 1 | 1 | 18 | `google3/third_party/jetski/language_server/code_assist_client/codeassistclient.RemoteAgentConversationConfigPatch` |
| 1 | 1 | 64 | `google3/third_party/jetski/language_server/code_assist_client/codeassistclient.init` |
| 1 | 1 | 32 | `google3/third_party/jetski/language_server/code_assist_client/codeassistclient.yieldErrorAndEndIterator[go.shape.f690ba7eaf8c87d6496d6384116d7da54226a8cdb211422aa9284808d6827add]` |
| 1 | 1 | 36 | `google3/third_party/jetski/language_server/code_assist_client/codeassistclient.yieldAndWrapUserFacingError[go.shape.f690ba7eaf8c87d6496d6384116d7da54226a8cdb211422aa9284808d6827add]` |
| 1 | 1 | 94 | `google3/third_party/jetski/language_server/code_assist_client/codeassistclient.newFastpushTransport` |
| 1 | 1 | 58 | `google3/third_party/jetski/language_server/code_assist_client/codeassistclient.remoteAgentFastpushClient` |
| 1 | 1 | 32 | `google3/third_party/jetski/language_server/code_assist_client/codeassistclient.yieldErrorAndEndIterator[go.shape.8d6ed42d28611fae4dd5ef8cc0ff70b1a4fa3bd7f8b6bcea93f9d9e7b39ac65f]` |
| 1 | 1 | 32 | `google3/third_party/jetski/language_server/code_assist_client/codeassistclient.filterModelSortGroups` |
| 1 | 1 | 45 | `google3/third_party/jetski/language_server/code_assist_client/codeassistclient.getSummaryWithCitations` |
| 1 | 1 | 63 | `google3/third_party/jetski/language_server/code_assist_client/codeassistclient.doJetskiRequestAndUnmarshal[go.shape` |
| 1 | 1 | 312 | `google3/third_party/jetski/language_server/code_assist_client/codeassistclient.doPostAndUnmarshal[go.shape` |
| 1 | 1 | 266 | `google3/third_party/jetski/language_server/code_assist_client/codeassistclient.doGetAndUnmarshal[go.shape` |
| 1 | 1 | 63 | `google3/third_party/jetski/language_server/code_assist_client/codeassistclient.doRequestAndUnmarshal[go.shape` |
| 1 | 1 | 173 | `google3/third_party/jetski/cli/backend/auth/auth.RunLogin` |
| 1 | 1 | 118 | `google3/third_party/jetski/cli/backend/backend.map.init` |
| 1 | 1 | 17 | `google3/third_party/jetski/cli/backend/backend.AgentModel` |
| 1 | 1 | 97 | `google3/third_party/jetski/cli/backend/backend.sortByLabelOrder` |
| 1 | 1 | 71 | `google3/third_party/jetski/cli/backend/backend.sortConversationSummaries` |
| 1 | 1 | 11 | `google3/third_party/jetski/cli/backend/backend.newRetry` |
| 1 | 1 | 507 | `google3/third_party/jetski/cli/store/store.Store` |
| 1 | 1 | 11 | `google3/third_party/jetski/cli/store/store.HintMask` |
| 1 | 1 | 70 | `google3/third_party/jetski/cli/store/store.ActiveAgentTaskStepIndices` |
| 1 | 1 | 109 | `google3/third_party/jetski/cli/store/store.activeAgentTaskStepIndicesByDaemon` |
| 1 | 1 | 54 | `google3/third_party/jetski/cli/store/store.splitTextAndMentions` |
| 1 | 1 | 48 | `google3/third_party/jetski/cli/store/store.featureProvider` |
| 1 | 1 | 42 | `google3/third_party/jetski/cli/store/store.init.0` |
| 1 | 1 | 84 | `google3/third_party/jetski/cli/store/store.RegisterCLIFeatureProviderLoader.func1` |
| 1 | 1 | 34 | `google3/third_party/jetski/cli/store/store.RegisterCLIRPCInit` |
| 1 | 1 | 178 | `google3/third_party/jetski/cli/printmode/printmode.map.init` |
| 1 | 1 | 11 | `google3/third_party/jetski/cli/printmode/printmode.init` |
| 1 | 1 | 71 | `google3/third_party/jetski/cli/printmode/printmode.helpReport` |
| 1 | 1 | 131 | `google3/third_party/jetski/cli/printmode/printmode.waitForAuth` |
| 1 | 1 | 127 | `google3/third_party/jetski/cli/printmode/printmode.DecodeStreamInput` |
| 1 | 1 | 26 | `google3/third_party/jetski/cli/printmode/printmode.runStreamInput` |
| 1 | 1 | 55 | `google3/third_party/jetski/cli/updater/updater.init` |
| 1 | 1 | 61 | `google3/third_party/jetski/cli/updater/updater.runUpdateShared` |
| 1 | 1 | 27 | `main.init.func3` |
| 1 | 1 | 83 | `main.ApplyBoolOverrides` |
| 1 | 1 | 94 | `main.swallowedPromptFlag` |
| 1 | 1 | 81 | `main.deleteAgentMessageFn` |
| 1 | 1 | 215 | `main.setupProfiling` |
| 1 | 1 | 26 | `main.handleMCPAdd` |
| 1 | 1 | 142 | `main.handlePluginCommand` |
| 1 | 1 | 79 | `main.recordPluginSubcommandEvents` |
| 1 | 1 | 63 | `main.redirectStderrToPluginLog` |
| 1 | 1 | 24 | `main.recordPluginSubcommandEvents.func1` |
| 1 | 1 | 124 | `main.main.func2` |
| 1 | 1 | 28 | `main.main.func4` |
| 1 | 1 | 11 | `main.maybeSetupIsolatedEnv` |

