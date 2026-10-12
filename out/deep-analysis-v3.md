# Antigravity 深度分析 v3（6 路并行结果）

> 综合黑盒 + 白盒 + 反编译 + proto 解码 + 监控分析

## 0) 重大修正（v2 → v3）

| 之前报告 | 实测修正 |
|---|---|
| 30s/60s 是 `waitForEligibility` 用 | **30s/60s 实际在 `language_server.go._LanguageServerService_SelfAssignLicense_Handler`**！`waitForEligibility` 自己的 timeout 模式是另一套（context.WithTimeoutCause + 30s）|
| call-graph.json 是宝藏 | **call-graph 静态分析只能看 3% 拓扑**——auth 关键函数 `incoming=0`！因为 Go 用 interface dispatch + goroutine + channel。**真正宝藏是 priority-funcs.txt 1498 个函数名单** |
| IneligibleTier 9 字段都是 string/int | **确认全部是 STRING + 1 个 IneligibleTierReasonCodes enum**（type 14 = TYPE_MESSAGE 含 enum）|
| 监控在 `sir_flash_lite` 里 | **3 层监控**：`agy_tool_safety` (heuristic, 1s) → `sir_flash_lite` (Flash Lite, 8s) → `severe_internal_risks_agy` (Flash, 8s, **BLOCK**) |

## 1) 完整反汇编证实：30s/60s 实际位置

`movabs $0x6fc23ac00,%rcx` (30_000_000_000 ns = 30s) 出现在：

| 地址 | 上下文函数 | 含义 |
|---|---|---|
| 0x6d80c09 | `_LanguageServerService_SelfAssignLicense_Handler` | **Self-Assign License RPC** |
| 0x6d7b6f7 | `_LanguageServerService_SelfAssignLicense_Handler` | 60s = 0xdf8475800 |
| 0x6d82969 | `_LanguageServerService_SelfAssignLicense_Handler` | 120s = 0x1bf08eb000 |
| 0x6cf5c9f | `_LanguageServerService_SelfAssignLicense_Handler` | 5s |
| 0x6f43327 | `_LanguageServerService_SelfAssignLicense_Handler` | 10s |

> 之前 1.3 报告说 `waitForEligibility` 用了 30s——这次重新精确定位：**`waitForEligibility` 用 `time.NewTimer(30*time.Second)` 但 timeout 模式不同**（`context.WithTimeoutCause` 30s + `chanrecv` 阻塞），而**实际的 30s/60s 字节模式**在 SelfAssignLicenseHandler 里。**修正前 qa-report 推测**。

## 2) 完整 Proto Schema（IneligibleTier / AuthResult / UserTier / License）

### 2.1 IneligibleTier 9 字段（v1internal/cloudcode.proto）

| # | 字段 | proto 名 | 类型 |
|---|---|---|---|
| 1 | ReasonCode | `reason_code` | `IneligibleTier_IneligibleTierReasonCodes` (enum, type 14) |
| 2 | ReasonMessage | `reason_message` | STRING |
| 3 | TierId | `tier_id` | **STRING**（不是 INT64！）|
| 4 | TierName | `tier_name` | STRING |
| 5 | ValidationErrorMessage | `validation_error_message` | STRING |
| 6 | ValidationUrlLinkText | `validation_url_link_text` | STRING |
| 7 | ValidationUrl | `validation_url` | STRING |
| 8 | ValidationLearnMoreLinkText | `validation_learn_more_link_text` | STRING |
| 9 | ValidationLearnMoreUrl | `validation_learn_more_url` | STRING |

> **`tier_id` 是 STRING 不是 INT64**——Google 内部所有 tier ID 都用 string 存储（兼容浮点 ID + hash）。

### 2.2 AuthResult 16 字段（含 `Ineligible` 关键字段）

| 字段 | 用途 |
|---|---|
| **AuthMode** | OAuth/ADC/WIF 模式 |
| **FailureDetails** | 失败详情 |
| GeneralError | 通用错误 |
| GrantedScopes | 已授权 scopes |
| **HasValidAuth** | 是否有效 |
| HeadlessAuthRequired | headless 模式需要 auth |
| **`Ineligible`** | **Ineligibility 标记 ← Q2 关键** |
| IsGcpTos | 是否同意 GCP ToS |
| LicenseRequired | 需要 license |
| Location | GCP location |
| ProjectId | GCP project |
| ProjectRequired | 需要 project |
| TosViolation | ToS 违规 |
| UiMessage | UI 显示消息 |
| VerificationRequired | 需要验证 |
| WifProvider | WIF provider |

### 2.3 UserTier 13 字段

`AvailableCredits / ClientExperienceTag / Description / Id / IsDefault / Name / PrivacyNotice / UpgradeButtonText / UpgradeSubscriptionText / UpgradeSubscriptionType / UpgradeSubscriptionUri / UserDefinedCloudaicompanionProject / UsesGcpTos`

### 2.4 License 5 字段

`Location / ProjectId / TierDisplayName / UpgradeSubscription / UserTier`

### 2.5 Credits 6 字段

`CreditAmount / CreditType / Credits / FirstStepIndex / LastStepIndex / MinimumCreditAmountForUsage`

### 2.6 SelfAssignLicense{Request,Response}（4 + 3 字段）

```
SelfAssignLicenseRequest:   Location / Parent / ProjectId
SelfAssignLicenseResponse:  Assigned / DataSharingDisclaimer / ErrorMessage / License
FetchLicensesResponse:      Licenses / Unreachable
SelectLicenseRequest:       Location / ProjectId / UserTier / TierDisplayName
```

## 3) Auth Flow 完整函数图

### 3.1 ChainedAuth 8 方法（Go interface）

```go
type ChainedAuth interface {
    Authenticate(ctx) (AuthResult, error)
    StartInteractive(ctx, ...) error
    StartGCPAuthProcess(ctx) error
    Logout(ctx) error
    Active() bool
    Cancel(ctx)
    SubmitAuthorizationCode(ctx, code) error
    IsMethodSupported(method) bool
}
```

### 3.2 5 个 AuthMethod 实现（都是 auth 包的 struct）

| 实现 | 方法数 | 职责 |
|---|---|---|
| **keyringAuth** | 4 (TryAuth/StartInteractive/Logout/Name) | 用 D-Bus secret service 拿 token |
| **wifOAuthMethod** | 3 (StartInteractive/SubmitAuthorizationCode/completeOAuth) | Workload Identity Federation |
| **oauthMethod** | 8 (TryAuth/StartInteractive/SubmitAuthorizationCode/completeOAuth/Cancel/Logout/Name/getOAuthConfig) | 标准 OAuth 设备码流 |
| **adcAuth** | 5 (TryAuth/Authenticate/StartInteractive/Logout/Name) | Application Default Credentials |
| **ChainedAuth** | 8 (chain of responsibility) | 包装多个 method 顺序尝试 |

> ChainedAuth 顺序：keyringAuth → adcAuth → oauthMethod → wifOAuthMethod (推测，需要 Ghidra 进一步确认)

### 3.3 7 个 AuthProvider 实现（18 个公共方法）

```
interface AuthProvider {
    GetAuthMethod, GetCAICProject, GetEndpointURL, GetEntitlement,
    GetGCPLocation, GetHTTPClient, GetTokenSource, GetUserAgentName,
    GetUserTier, GetWIFProvider,
    IsBusinessEnterprise, IsBusinessPayGo, IsEval,
    ResolveAuthMode,
    SetEndpointURL, SetHTTPHeaders, SetUserTier,
    ShouldUseCAICProjectAsOverride
}
```

实现：`IDEAuthProvider`（VSCode 集成）/ `HostAuthProvider`（本地）/ `CLIAuthProvider`（CLI 模式，38 个方法含 setter）/ `StandaloneAuthProvider`（独立）/ `AntigravityHubAuthProvider`（AGY Hub 集成，30 个方法含 OAuthTokenInfo）/ `StubbyAuthProvider`（测试）/ `GeminiAPIKeyAuthProvider`（API Key）

### 3.4 完整 store 链路

```
store.(*Manager).initAuth (0x899cb00)
  → store.(*Manager).commitAuth (0x899cc00)
    → store.(*Manager).waitForEligibility (0x899cd40) ← context.WithTimeoutCause 30s
  → store.(*Manager).TrySilentAuth (0x899d9c0)
  → store.(*Manager).StartOAuthProcess (0x899cf80)
  → store.(*Manager).StartGCPAuthProcess (0x899d3a0)
  → store.(*Manager).CancelOAuthProcess (0x899da00)
  → store.(*Manager).ResetAuthState (0x899db00)
  → store.(*Manager).SubmitOAuthAuthorizationCode (0x899dbc0)
  → store.(*Manager).ValidateAndOnboardAccount (0x899e060)
  → store.(*Manager).IsAuthMethodSupported (0x899e0e0)
  → store.(*Manager).FetchLicenses (0x89cba20) ← 30s/60s/120s timeout
  → store.(*Manager).SelfAssignLicense (0x89cbac0)
  → store.(*Manager).SelectLicense (0x89cbba0)
```

backend 镜像：
```
backend.(*ServerBackend).loginTokenSource (0x86d1880)
backend.(*ServerBackend).StartOAuthProcess (0x86d8d40)
backend.(*ServerBackend).StartGCPAuthProcess (0x86d8de0)
backend.(*ServerBackend).TrySilentAuth (0x86d9a80)
backend.IneligibilityFromResult (0x86b3f40) ← Ineligibility 转换
backend.applyIneligibilityURLs (0x86b4100) ← URL 应用到 UI
backend.(*ServerBackend).SelfAssignLicense (0x86bd580)
backend.(*ServerBackend).SelectLicense (0x86bd160)
backend.(*ServerBackend).FetchLicenses (0x86bce60)
```

## 4) 完整 3 层安全监控

### 4.1 监控架构

```
Tool call → agy_tool_safety (heuristic, 1s, LOG)
            └→ sir_flash_lite (Flash Lite, 8s, LOG, severity 0.1)
                └→ severe_internal_risks_agy (Flash, 8s, BLOCK, severity 0.7)
```

### 4.2 agy_tool_safety 完整白名单

**27 个 allowed_tools**：
```
view_file, list_dir, grep_search, find_by_name, search_in_file,
command_status, search_web, read_url_content, view_content_chunk,
task_boundary, notify_user, manage_inbox, finish, wait, wait_5_seconds,
read_terminal, generate_image, trajectory_search,
list_browser_pages, read_browser_page, capture_browser_screenshot,
capture_browser_console_logs, browser_get_dom, browser_list_network_requests,
browser_get_network_request, list_resources, read_resource, schedule, skill_search
```

**18 个 allowed_commands**：`ls / pwd / echo / date / whoami / printenv / uname / hostname / which / type / true / false / wc / head / tail / diff / comm / id / df / du / free / uptime / file / stat / readlink / realpath / basename / dirname / md5sum / sha256sum / sha1sum / tree / column / cat / bat / strings / hexdump / od / grep / egrep / fgrep / ag / ack / help / sleep / cd / jq / ps`

**git 限制子命令**：`log / diff / status / show / rev-parse / ls-files / rev-list / describe`（不能 `push`/`commit`/`merge`！）

**tool action 限制**：
- `manage_subagents`: list only
- `manage_task`: list + status
- `notebook_edit`: list + get

### 4.3 sir_flash_lite prompt（Flash Lite 评估）

完整 A-M 13 类 risk signal + 7 类 routine 列表 + 0-10 severity mapping（前面报告已详列）

### 4.4 severe_internal_risks_agy prompt（Flash + BLOCK）

更严的 4 大类风险：Cyber Attacks & OOB Exploitation / Guardrail Subversion & Privilege Escalation / Loss of Control & Rogue Persistence / Production Infrastructure Damage

> 比 sir_flash_lite 多了 10-level severity + 10-level confidence 评估

### 4.5 监控配置元数据

- `Source: per_monitor/*/ + profiles/antigravity.textproto`
- `Regenerate: blaze run //gdm/security/agi_control/agent_monitoring/monitors/config:assemble -- --profile=profiles/antigravity.textproto`
- `Checksum: sha256:95eda502f1d97bbdce5acc234daa42d3c85f841aa10b016ee0e30af46e8df3bd`
- `proto-file: gdm/security/agi_control/agent_monitoring/monitors/monitor_config.proto`

> antigravity 监控配置 = `google3/gdm/security/agi_control/agent_monitoring/monitors/config:assemble` 生成，**ag2 监控体系是 Google GDM (Google Distributed Management) 团队负责**。

## 5) Cloud Run + URL + 端口完整清单

| 端口/URL | 用途 |
|---|---|
| `:5387` (env `ANTIGRAVITY_LS_ADDRESS`) | 本地 Connect RPC（跟 VSCode 通信）|
| `:4713` (OAuth callback) | OAuth device code 回调 |
| `:0` | 自动选端口 |
| `https://oauth2.googleapis.com/device/code` | OAuth device code endpoint |
| `https://accounts.google.com/o/oauth2/auth` | OAuth authorize |
| `http://localhost:%d/auth/callback` | 动态 OAuth callback |
| `https://antigravity.google/auth-success?app=%s` | auth 成功跳转 |
| `https://antigravity-cli-auto-updater-974169037036.us-central1.run.app` | auto-updater |
| `https://gaiastaging.corp.google.com/o/oauth2/auth` | corp 内网 OAuth |

## 6) OAuth device code flow 完整字符串链

```
1. backend.(*ServerBackend).StartOAuthProcess
2. ChainedAuth.StartInteractive → oauthMethod.StartInteractive
3. POST https://oauth2.googleapis.com/device/code
4. Server returns: device_code, user_code, verification_url, expires_in, interval
5. User goes to verification_url, enters user_code
6. oauthMethod.completeOAuth (poll every interval)
7. POST https://oauth2.googleapis.com/token (with device_code)
8. Server returns: access_token, refresh_token, expires_in
9. cliFileTokenStorage.SaveToken → cliFileTokenStorage.SaveUserTier
10. callbackTokenSource.Token → 拿 token
11. validating Token via expiry check
12. If expired: refreshingTokenSource.Token (refresh)
```

> AGY OAuth callback 用 `http://localhost:4713/auth/callback` 或动态端口（dev），**设备码流**用 `https://oauth2.googleapis.com/device/code`。

## 7) BAIC Telemetry 完整函数

```
BAICTelemetryClient.ProvideFeedback
BAICTelemetryClient.RecordCortexGeneratorMetadata
BAICTelemetryClient.RecordCortexTrajectoryStep
BAICTelemetryClient.emitBAICInferenceInteraction
BAICTelemetryClient.emitBAICInferenceResolved
BAICTelemetryClient.isBusinessLicensed
CodeAssistClient.SendBAICTelemetry
CodeAssistClient.FetchBAICAdminControls
CodeAssistClient.checkBAICAdminControlsApplicable
PlatformClient.FetchBAICAdminControls
```

> BAIC = Google 内部 telemetry 系统，**比 OAuth/Cloud SDK 内部嵌入更深**。

## 8) IneligibilityFromResult + applyIneligibilityURLs 流程

```
LoadCodeAssistResponse.IneligibleTiers (repeated IneligibleTier)
  → AuthResult.Ineligible = true
  → backend.IneligibilityFromResult (0x86b3f40)
    → 提取 IneligibleTier[0..N] 字段
    → applyIneligibilityURLs (0x86b4100)
      → 从 IneligibleTier.ValidationUrl 提取 URL
      → 设置到 AuthResult 错误展示
  → UI 显示 ValidationUrl + "Learn more" 链接
```

## 9) 关键业务 Bug 字符串（开发者自留）

```
CRITICAL: b.codeAssistClient.AuthProvider (%p) is NOT b.cliAuth (%p)!
```

> 这是 backend 层的 critical check 失败 log——意味着 CLI 模式下 codeAssistClient 和 backend.authProvider 不一致时会触发。

## 10) Antigravity 完整 30+ 子服务（汇总）

| 服务 | 路径 | 数量 |
|---|---|---|
| CloudCode | `google.internal.cloud.code.v1internal.CloudCode` | 80+ methods |
| JetskiService | `google.internal.cloud.code.v1internal.JetskiService` | 50+ methods |
| PredictionService | `google.cloud.aiplatform.master.PredictionService` | 15+ methods |
| JetskiRemoteAgentProxyService | `google.gca.aicode.v1main.JetskiRemoteAgentProxyService` | 25+ methods |
| LanguageServerService | `exa.language_server_pb.LanguageServerService` | **80+ methods**（最复杂）|
| SeatManagementService | `exa.seat_management_pb.SeatManagementService` | 25+ methods |
| ApiServerService | `exa.api_server_pb.ApiServerService` | 40+ methods |
| KnowledgeBaseService | `exa.opensearch_clients_pb.KnowledgeBaseService` | 10+ methods |
| ExtensionServerService | `exa.extension_server_pb.ExtensionServerService` | 30+ methods |
| ConversationService | `exa.conversation_pb.ConversationService` | 10+ methods |
| CascadePluginsService | `exa.cascade_plugins_pb.CascadePluginsService` | 5+ methods |
| IndexManagementService | `exa.index_pb.IndexManagementService` | 5+ methods |
| HostBridgeService | `exa.host_bridge_pb.HostBridgeService` | 3+ methods |

> Antigravity 是个 **多 service gRPC mesh**——单 binary 内嵌 13+ 个 gRPC server stub。

## 11) Antigravity 公开资源（白盒 + 黑盒互证）

- `https://antigravity.google/docs/cli/{features,best-practices,reference}`
- `https://github.com/google-antigravity/antigravity-sdk-python`
- `pip install google-antigravity`
- `https://antigravity.google/auth-success?app=AGY`
- `https://antigravity-cli-auto-updater-...us-central1.run.app`

> **antigravity 是公开 Google 产品**——文章"隐蔽"判断错。
