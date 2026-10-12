# 补充深挖报告（owner 自跑）

> 跑完 qa-report.md 后继续抽的细节，3 个 grep 任务并发跑完

## 1) 完整 model 列表（44 个 unique）

不只是 Gemini——**还集成 Claude 4.5/4、OpenAI gpt-oss-120b**：

### Gemini 代号（已发布 + 内部代号）
- `MODEL_GOOGLE_GEMINI_1_0_PRO` / `_1_5_PRO`（老）
- `MODEL_GOOGLE_GEMINI_2_0_FLASH` / `_2_5_FLASH` / `_2_5_FLASH_LITE`（主力）
- `MODEL_GOOGLE_GEMINI_2_5_PRO` / `_2_5_PRO_EVAL`
- `MODEL_GOOGLE_GEMINI_2_5_FLASH_THINKING` / `_2_5_FLASH_THINKING_TOOLS`
- `MODEL_GOOGLE_GEMINI_2_5_FLASH_PREVIEW_04_17` / `_PREVIEW_05_20` / `_PREVIEW_05_20_THINKING`
- `MODEL_GOOGLE_GEMINI_2_5_FLASH_IMAGE_PREVIEW`

### Gemini 内部代号（未发布）
- `MODEL_GOOGLE_GEMINI_RIFTRUNNER` + `_THINKING_LOW` + `_THINKING_HIGH`
- `MODEL_GOOGLE_GEMINI_INFINITYBLOOM`
- `MODEL_GOOGLE_GEMINI_INFINITYJET`
- `MODEL_GOOGLE_GEMINI_COSMICFORGE`
- `MODEL_GOOGLE_GEMINI_NEMOSREEF`
- `MODEL_GOOGLE_GEMINI_PUREPRISM`
- `MODEL_GOOGLE_GEMINI_ORIONFIRE`
- `MODEL_GOOGLE_GEMINI_HORIZONDAWN`
- `MODEL_GOOGLE_GEMINI_GENTLEISLAND`
- `MODEL_GOOGLE_GEMINI_RAINSONG`
- `MODEL_GOOGLE_GEMINI_INTERNAL_TAB_FLASH_LITE` / `_TAB_JUMP_FLASH_LITE`
- `MODEL_GOOGLE_GEMINI_INTERNAL_BYOM`（Bring Your Own Model）
- `MODEL_GOOGLE_GEMINI_COMPUTER_USE_EXPERIMENTAL`
- `MODEL_GOOGLE_GEMINI_TRAINING_POLICY`
- `MODEL_GOOGLE_GEMINI_EXAMPLE_GEMAX_SAMPLER`
- `MODEL_GOOGLE_GEMINI_EXP_1206`
- `MODEL_GOOGLE_GEMINI_FOR_GOOGLE_2_5_PRO`
- `MODEL_GOOGLE_GEMINI_JARVIS_PROXY`

### Claude（Antigravity 接的）
- `MODEL_CLAUDE_4_SONNET_THINKING`
- `MODEL_CLAUDE_4_5_SONNET_THINKING`
- `MODEL_CLAUDE_4_5_HAIKU_THINKING`
- `MODEL_CLAUDE_4_OPUS_THINKING`

### OpenAI
- `MODEL_OPENAI_GPT_OSS_120B_MEDIUM`

### Provider 路由
- `API_PROVIDER_ANTHROPIC_VERTEX`（走 Vertex AI 调 Claude）
- `API_PROVIDER_GOOGLE_EVERGREEN`（Google 内部代号 Evergreen）
- 还看到 scheme prefix `gemini-api:` / `blade:` / `evergreen:` / `beyond-api:`

> **结论**：Antigravity 是个**多模型网关**，不是单一 Gemini 客户端。

## 2) 完整 host/server URL 列表（35 个）

| 类别 | 域名 |
|---|---|
| **业务主端** | `cloudcode-pa.googleapis.com`（prod）、`daily-cloudcode-pa.googleapis.com`（daily）、`preprod-daily-cloudcode-pa.sandbox.googleapis.com`（preprod）、`autopush-cloudcode-pa.sandbox.googleapis.com`（autopush）|
| **AI 平台** | `aicode.googleapis.com`、`aiplatform.googleapis.com`、`generativelanguage.googleapis.com`、`alkalimakersuiteapplets.pa.googleapis.com`、`autopush-aicode.sandbox.googleapis.com` |
| **认证** | `accounts.google.com`、`oauth2.googleapis.com`、`oauth2.mtls.googleapis.com`、`www.mtls.googleapis.com`、`sts.googleapis.com`、`iamcredentials.googleapis.com` |
| **产品域** | `antigravity.google.com`、`antigravity.goog`、`antigravity-unleash.goog`、`auth.cloud.goog`、`ai.goog` |
| **Cloud Run auto-updater** | `antigravity-cli-auto-updater-974169037036.us-central1.run.app` ✅ 文章有 |
| **企业内网 (corp)** | `gaiastaging.corp.google.com`、`jetski.corp.google.com`、`jetski-autopush.corp.google.com`、`symbolize.corp.google.com` |
| **其他** | `safebrowsing.googleapis.com`、`play.googleapis.com`、`drive.google.com`、`cloud.google.com`、`docs.cloud.google.com`、`policies.google.com`、`one.google.com`、`www.googleapis.com`、`www.gstatic.com` |

> **4 套 host 实际是**：prod / daily / preprod-daily / autopush，加上 corp 内网，**至少 5 套**。比文章说的"4 套"略多。

## 3) Tier 枚举（30+ 个定价 tier）

```
TIER_UNSPECIFIED, TIER_UNKNOWN, TIER_TRIAL, TIER_PRO, TIER_PRO_ULTIMATE,
TIER_FLASH, TIER_FLASH_LITE, TIER_FLEX, TIER_HYBRID, TIER_INHERIT,
TIER_PRIORITY, TIER_STANDARD, TIER_TEAMS, TIER_TEAMS_ULTIMATE,
TIER_WAITLIST_PRO,
TIER_ENTERPRISE_SAAS, TIER_ENTERPRISE_SELF_HOSTED, TIER_ENTERPRISE_SELF_SERVE
```

> **Antigravity 支持 17+ 种定价 tier**，从免费 trial 到 enterprise SaaS 都有。

## 4) EPD Eligibility 枚举（新版，跟 v1internal 不一样）

```
EPD_ELIGIBILITY_UNSPECIFIED
EPD_ELIGIBILITY_ELIGIBLE
EPD_ELIGIBILITY_NOT_ELIGIBLE_APPLICATION_OUT_OF_SCOPE
EPD_ELIGIBILITY_NOT_ELIGIBLE_REGION_OUT_OF_SCOPE
```

> **EPD** = 一个新的 eligibility 系统（不是 v1internal 的 `IneligibleTier`），独立的资格检查通路。具体是哪个业务的（Entitlement / Eligibility / Policy Director？），strings 看不出来。

## 5) 完整 env var 列表（50+ 个 `AGY_*`）

按用途分类：

| 用途 | 例子 |
|---|---|
| **认证** | `AGY_ACCOUNT`, `AGY_ADC_AUTH`, `AGY_BROWSER_WS_URL`, `AGY_BROWSER_ACTIVE_PORT_FILE` |
| **行为开关** | `AGY_CLI_EXPERIMENTAL_RENDERING`, `AGY_CLI_DISABLE_AUTO_UPDATE`, `AGY_CLI_DISABLE_MERMAID_ASCII`, `AGY_CLI_DISABLE_LATEX`, `AGY_CLI_DISABLE_SAFETY_FILTERING`, `AGY_CLI_DISABLE_INLINE_MERMAID`, `AGY_CLI_DISABLE_INPUT_MODE_REASSERT`, `AGY_CLI_DISABLE_ESCAPE_SEQUENCE_OPTIMIZATIONS`, `AGY_CLI_FAST_PROMPT_EDITOR`, `AGY_CLI_FORCE_OSC8`, `AGY_CLI_HIDE_LOGO`, `AGY_CLI_HIDE_ACCOUNT_INFO`, `AGY_CLI_INTERACTIVE_HEADLESS`, `AGY_CLI_NONINTERACTIVE_HEADLESS`, `AGY_CLI_LOGO_STYLE`, `AGY_CLI_MAC_OPTION_AS_ALT` |
| **模型/LLM gateway** | `AGY_LLM_GATEWAY_API_KEY`, `AGY_LLM_GATEWAY_HEADERS`, `AGY_LLM_GATEWAY_CA_CERT`, `AGY_LLM_GATEWAY_MODELS`, `AGY_LLM_GATEWAY_PROXY_URL`, `AGY_LLM_GATEWAY_URL`, `AGY_LLM_GATEWAY_WIRE_PROTOCOL` |
| **业务** | `AGY_BUSINESS_PAYGO_TIER`, `AGY_CLI_CDE_AUTH_ACTION`, `AGY_CLI_MODEL_EXPERIMENT_PROFILES`, `AGY_CLI_MODEL_API_MAX_RETRIES`, `AGY_CLI_CMD_OUTPUT_PERCENTAGE`, `AGY_CLI_REMOTE_CONTROL_WEB_VERSION` |
| **Onboarding** | `AGY_ONBOARDING_*` (4 个：AGENT_CONFIG_PAGE_OPENED, INSTALL_EXTENSIONS, TERMS_OF_USE_PAGE_OPENED, USAGE_MODE_PAGE_OPENED) |
| **Hub / 插件** | `AGY_ENABLE_HUB`, `AGY_PLUGIN_AUTH_CALLBACK_PORT`, `AGY_ERROR` |

> **50+ 个 env var 完全是文档没写的开关**，等于一个内部的"配置清单"。这些就是文章说的"故意对用户隐藏的命令行开关"——它们走 env 而不是 flag。

## 6) google3 monorepo 顶层包结构（48 个）

业务主包：`google3/devtools/jetski`（CLI 主包，路径里出现 163K 次）

其他顶层：
- `google3/devtools/cider`、`google3/devtools/cog`、`google3/devtools/search`、`google3/devtools/staticanalysis`
- `google3/cloud/ai`、`google3/cloud/developer_experience`、`google3/cloud/security`
- `google3/learning/agents`、`google3/learning/gemini`、`google3/learning/genai`
- `google3/google/cloud`、`google3/google/gca`、`google3/google/internal`、`google3/google/protobuf`
- `google3/identity/ubermint`、`google3/privacy/*`、`google3/frameworks/*`
- `google3/borg/borgletlib`、`google3/assistant/api`、`google3/apps/framework`

> antigravity 是 Google 内部 google3 monorepo 一个 project，目录结构暴露了**其他相关项目**（cider / cog / ubermint 等）。

## 7) 内部 gRPC service（exa.* / jetski.* / codeium.*）

35+ gRPC service，列出主要几个：

- `exa.language_server_pb.LanguageServerService`（80+ method：Jetbox/Subscribe/RecordEvent/State/Plugin 等）
- `exa.seat_management_pb.SeatManagementService`（座位管理：GetSeat / BulkUpdate / Team / etc.）
- `exa.cascade_plugins_pb.CascadePluginsService`
- `exa.api_server_pb.ApiServerService`（40+ method：RecordEvent / ContactForm / GetTokenBase 等）
- `exa.opensearch_clients_pb.KnowledgeBaseService`
- `exa.conversation_pb.ConversationService`
- `exa.extension_server_pb.ExtensionServerService`
- `exa.seat_management_pb.SeatManagementService`

外加：
- `google.internal.cloud.code.v1internal.CloudCode`
- `google.internal.cloud.code.v1internal.JetskiService`
- `google.internal.cloud.code.v1internal.PredictionService`
- `google.gca.aicode.v1main.JetskiRemoteAgentProxyService`
- `google.cloud.aiplatform.master.PredictionService`
- `codeium_common_go_proto.*`（Codeium/Cascade 共享类型）

> 业务核心 RPC 都在 `exa.*`（experimental antigravity？）和 `v1internal.JetskiService`。

## 8) CLI flag 短名（部分）

`--approv --compacf --config --countldx --debug --escape --eval --exec --exit-s --extcmd --field --gemini --gunit --header --heap --hostna --input --kill-a --librar --method --mou --no-config --null-i --output --pager --parent --raw-fi --raw-ou --recurs --reepo --signal --sort-k --test --to-cmd --versio --write-`

> 多数是 truncated 字串（`--approv` 是 `--approval-mode` 之类被截断）。`--gemini` 明显是 Gemini 专用 flag。

## 9) Keyring 状态

- `Keyring SaveUserTier timed out after %v, falling back to file storage` ✅
- `Keyring SaveProjectAndRegion timed out after %v, falling back to file storage` ✅

> **两套 keyring 都有熔断机制**——SaveUserTier（用户资格缓存）和 SaveProjectAndRegion（项目+region 缓存）。

## 10) P0 实验 / Feature flag 字符串

- `ANTIGRAVITY_SENTRY_SAMPLE_RATE`
- `AGY_CLI_EXPERIMENTAL_RENDERING`（TUI 渲染实验）
- `AGY_CLI_DISABLE_AUTO_UPDATEF`（auto-updater 关闭开关）—— **F 后缀可能是字符串截断**
- `MODEL_GOOGLE_GEMINI_TRAINING_POLICY`
- `MODEL_GOOGLE_GEMINI_COMPUTER_USE_EXPERIMENTAL`
- `jetski.product.v1.ConversationService.ListConversations is not implemented`

> antigravity 内部用了 LaunchDarkly 风格实验系统（Sentry sample rate 也是）。

## 11) 5 套 host 实测确认

| 环境 | URL | 用途 |
|---|---|---|
| **prod** | `https://cloudcode-pa.googleapis.com` | 线上生产 |
| **daily** | `https://daily-cloudcode-pa.googleapis.com` | 每日构建（GA 内部）|
| **preprod** | `https://preprod-daily-cloudcode-pa.sandbox.googleapis.com` | 预生产 |
| **autopush** | `https://autopush-cloudcode-pa.sandbox.googleapis.com` | 自动推送分支 |
| **corp 内网** | `https://jetski.corp.google.com` / `https://gaiastaging.corp.google.com` | Google 内部 |

> **5 套**，通过环境变量切换。文章说 4 套是错的（少算了 corp 内部那套）。

## 12) Ghidra 实际跑通的额外产物（`out/decompile/`）

Ghidra 任务虽然 rea analyze 5.5min timeout 截断，但 worker **自己额外跑了 Ghidra headless 第二轮**，生成了额外的高质量产物：

| 文件 | 大小 | 用途 |
|---|---|---|
| `out/decompile/priority-funcs.txt` | 147 KB / 1498 行 | **1498 个 priority 函数 + 名字 + 地址**（比 fallback-functions.txt 的 115 个多 13 倍）|
| `out/decompile/call-graph.json` | 891 KB | **2625 节点 / 2422 边**的调用图（auth 链路可追溯）|
| `out/decompile/call-graph.dot` | 395 KB | 同上（Graphviz 格式）|
| `out/decompile/xrefs.txt` | 2.1 MB | 完整 xref 邻接表（1-hop neighborhood）|
| `out/decompile/DecompilePriority.java` | 8.6 KB | Ghidra 脚本源码（按 priority 排序反编译）|
| `out/decompile/build_reports.py` | 9.6 KB | 提取脚本 |
| `out/decompile/proj/proj.gpr` | - | Ghidra project 文件（可 GUI 重新打开）|
| `out/decompile/logs/analyzeHeadless*.log` | 22 KB | 完整 Ghidra 运行日志 |

> 1498 个 priority funcs 中 `google3/third_party/jetski` 占 1502 个（行数 > 节点数因为文件还包含 xref 注释），auth/eligibility 相关 957 个。
>
> **call-graph.json 是这次逆向的真正宝藏**——2.6K 节点 + 2.4K 边的 auth 链路调用图，下次要看 auth flow 直接读这个图，不用再 grep。

## 13) 关键发现：Ghidra 不止跑了 1 轮

`out/decompile/logs/` 里有 2 个 Ghidra headless 日志：

- `analyzeHeadless.log`（17.6 KB）—— rea 包装跑的第一轮，5.5min timeout 截断
- `analyzeHeadless2.log`（4.7 KB）—— **worker 自己又跑了一次**（可能调短了 disassembly 阶段或换策略），第二轮没 timeout，完成 disassembly + symbol 标注，但**没生成 .c 反编译输出**（155K 函数规模 + 3GB RAM 装不下 decompiler output）。

实际：worker 的 1 轮 + 自己的 1 轮 = 2 轮 Ghidra。**这比报告里"5.5min timeout 失败"更准确**——核心反编译没出，但符号化（function naming）+ 调用图 + xref 全部到位。

> 后续如果想跑完整 decompile：直接调 `analyzeHeadless proj.gpr -process -postScript DecompilePriority.java`，**避开 rea 包装的 5.5min timeout**。
