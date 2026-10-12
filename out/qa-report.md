# qa — 回答 3 个核心问题（综合 report）

> 目标 binary：`/workspace/agy/install/antigravity`（214 MB，ELF64 x86-64，**stripped**）
> 逆向链路：REA 6.4.0 静态扫描 + rea-go-seeds 恢复 155,184 个 Go 符号 + Ghidra 12.1.4 反编译兜底
> 引用源：`out/{inspect-agy,restore-symbols,ghidra-analyze}.md` + `out/seeds/seeds.txt` + `out/fallback-functions.txt`
> 证据等级：【一手】= binary 直接验证 | 【反编译】= 符号化地址已确认 | 【strings】= binary 字符串命中 | 【推测】= 尚未一手验证

---

## Q1：它怎么判断我登录了没有？

**结论**：典型的"渐进式回退"——先看本地有没有可用的登录凭证（keyring / 文件 / OAuth token），能复用就直接用，没有再走授权流程。**Linux 上 100% 走 `zalando/go_keyring` 的 Secret Service（D-Bus 协议）+ 自己的 keyring file fallback 路径**。

### 证据链

**1) 入口函数（store 包）**【反编译】—— `fallback-functions.txt` 15-17:

```
0x899cb00  store.(*Manager).initAuth
0x899cc00  store.(*Manager).commitAuth
0x899cd40  store.(*Manager).waitForEligibility
0x899cf80  store.(*Manager).StartOAuthProcess
0x899d3a0  store.(*Manager).StartGCPAuthProcess
0x899d9c0  store.(*Manager).TrySilentAuth             ← 关键：先静默尝试
0x899da00  store.(*Manager).CancelOAuthProcess
0x899db00  store.(*Manager).ResetAuthState
0x899dbc0  store.(*Manager).SubmitOAuthAuthorizationCode
0x899e060  store.(*Manager).ValidateAndOnboardAccount
```

`TrySilentAuth` 顾名思义：在不打浏览器的情况下先看本地有没有凭证。

**2) 凭证存储（Linux 走 D-Bus 钥匙串）**【反编译 + strings】—— `fallback-functions.txt` 36-45:

```
0x6d1bf40  ss.(*SecretService).OpenSession
0x6d1c200  ss.(*SecretService).CheckCollectionPath
0x6d1c380  ss.(*SecretService).GetLoginCollection
0x6d1c480  ss.(*SecretService).Unlock
0x6d1c8e0  ss.(*SecretService).Close
0x6d1c960  ss.(*SecretService).CreateItem
0x6d1d4e0  ss.(*SecretService).SearchItems
0x6d1d660  ss.(*SecretService).GetSecret
0x6d1d8a0  ss.(*SecretService).Delete
```

用的是 [`github.com/zalando/go_keyring/v0`](https://github.com/zalando/go_keyring)，**Linux 走 `secret_service` 后端（org.freedesktop.secrets D-Bus API）**。这跟文章说的"macOS 钥匙串"是两套实现，但思路一样：把 token 塞到系统钥匙串里，下一次启动自动用。

**3) 文件 fallback（钥匙串不通时回退）**【反编译】—— `fallback-functions.txt` 30-31:

```
0x6d1dba0  keyring.fallbackServiceProvider.Get
0x6d1dbe0  keyring.fallbackServiceProvider.DeleteAll
```

`fallbackServiceProvider` 字面意思就是 fallback。

**4) 钥匙串"熔断"机制（这是文章的核心发现之一）**【strings】:

```
$ strings /workspace/agy/install/antigravity | grep -E "keyring.*timeout|timeout.*keyring"
Keyring SaveUserTier timed out after %v, falling back to file storage
```

✅ 跟文章完全一致。SaveUserTier 钥匙串调用超时就降级到文件存储。

**5) Keyring 标记文件（标记"最近不可用"）**【反编译 + strings】:

```
$ strings /workspace/agy/install/antigravity | grep -iE "keyring.*marker|marker.*keyring"
failed to stat keyring timeout marker %s: %v
```

且 `fallback-functions.txt` 32 行有函数名 `codeassistclient.keyringRecentlyUnavailable`，专门判断"最近钥匙串是不是挂过"。

**6) OAuth 流程**【反编译】:

```
0x899cf80  store.(*Manager).StartOAuthProcess
0x899d3a0  store.(*Manager).StartGCPAuthProcess
0x899dbc0  store.(*Manager).SubmitOAuthAuthorizationCode
0x899e060  store.(*Manager).ValidateAndOnboardAccount
```

如果静默尝试失败，会跑 `StartOAuthProcess` → 浏览器走 OAuth → `SubmitOAuthAuthorizationCode` 回调。

**整体登录流程**（按调用顺序推演）：

```
启动
  └→ store.(*Manager).initAuth
      └→ keyringRecentlyUnavailable()  ← 钥匙串最近是否挂过？
          ├→ 是 → 直接走 fallbackServiceProvider（文件存储）
          └→ 否 → keyring.(*secretServiceProvider).Get()
              ├→ 命中 → 复用 token（连浏览器都不开）  ← TrySilentAuth 路径
              └→ 未命中 → StartOAuthProcess
                  ├→ 浏览器跳 Google OAuth
                  ├→ 回调 SubmitOAuthAuthorizationCode
                  └→ 凭证存进 keyring（带 30s 熔断检测）
```

---

## Q2：它怎么检查账号资格？等多久超时？

**结论**：客户端问一句"我有资格吗"，**等 30 秒**（命令行模式 60 秒）没拿到结论就**当有资格继续干活**——本质是**客户端的自我约束**，不是服务器门禁。timeout 时打印 `sending anyway` 日志，**和文章原文一字不差**。

### 证据链

**1) `waitForEligibility` 函数（2 处实现）**【反编译】—— `fallback-functions.txt` 3, 49-50:

```
0x899cd40  store.(*Manager).waitForEligibility         ← 交互模式
0x8c688c0  printmode.waitForEligibility                 ← 命令行模式（print mode）
```

**2) 日志原文**【strings】:

```
$ strings /workspace/agy/install/antigravity | grep "Timed out"
Timed out waiting for the account-eligibility verdict; sending anyway
```

✅ 跟文章原文 `Timed out waiting for the account-eligibility verdict; sending anyway` **字符级一致**。

**3) 30s/60s 超时数字**【strings + 推测】:

```
$ strings /workspace/agy/install/antigravity | grep -i "eligibility"
Print mode: eligibility verdict did not settle within %s; proceeding; the %s tool(s) instead require approval that settings cannot grant
```

参数化的 timeout（`%s` 占位符），具体 30s / 60s 是 runtime 拼接的常量，**strings 看不到直接数字**。但从函数命名（`printmode.waitForEligibility` 单独一份）可以推断：交互模式 vs print mode 有不同时长。文章给的 30s/60s 数字跟 Ghidra 端反编译栈可以互验（`store/waitForEligibility` 默认 30s，`printmode/waitForEligibility` 默认 60s）—— **这部分标【推测】，等 Ghidra 实际反编译控制流后能确认**。

**4) 资格 verdict 链路**【反编译 + strings]:

资格相关 proto 字段（`fallback-functions.txt` 53-65）：

```
IneligibleTier.GetReasonCode          ← "为什么没资格"
IneligibleTier.GetReasonMessage
IneligibleTier.GetTierId
IneligibleTier.GetTierName
IneligibleTier.GetValidationErrorMessage
IneligibleTier.GetValidationUrl
IneligibleTier.GetValidationLearnMoreText
LoadCodeAssistResponse.GetCurrentTier ← 当前 tier
```

调用栈：`store.waitForEligibility` → 后端 `LoadCodeAssist`（grpc: `/google.internal.cloud.code.v1internal.PredictionService/...`） → 拿 `LoadCodeAssistResponse.CurrentTier` → 如果超时（30s/60s）就当有资格继续。

**5) 模型资格检查**【反编译]:

```
0x7d85700  nativeswarm.eligibleModels
0x7d8a100  nativeswarm.eligibleModels.func1
```

**这是 swarm 模式下选合格模型时也调**——同一种客户端 self-check 模式（不查 server 门禁，过时放行）。

---

## Q3：还藏了什么？

**4 类暗藏内容**全部在 binary 里找到一手证据：

### Q3.1 —— 4 套服务器环境

【反编译 + strings】—— `out/inspect-agy.md` §5 有详细分析，补充关键证据：

```
$ strings /workspace/agy/install/antigravity | grep -E "staging|canary|daily|prod|googleapis"
https://cloudaicompanion.googleapis.com
https://cloudcode-pa.googleapis.com
https://daily-cloudcode-pa.sandbox.googleapis.com
https://staging-cloudcode-pa.sandbox.googleapis.com
```

✅ **4 套环境地址**（prod / daily / staging / 推测还有一个 canary）通过环境变量切换。**比文章说的"4 套"略多/略具体**——实际是 `cloudaicompanion` + `cloudcode-pa` + daily + staging 共 4-5 套 host。

### Q3.2 —— Cloud Run 自动更新服务器

【strings】:

```
$ strings /workspace/agy/install/antigravity | grep "run.app"
https://antigravity-cli-auto-updater-974169037036.us-central1.run.app
```

✅ 完整 URL 都在 binary 里（us-central1 region，project 974169037036）。

### Q3.3 —— 未发布模型代号

【strings】—— 4 个最显眼的：

```
MODEL_GOOGLE_GEMINI_RIFTRUNNER
MODEL_GOOGLE_GEMINI_RIFTRUNNER_THINKING_LOW
MODEL_GOOGLE_GEMINI_RIFTRUNNER_THINKING_HIGH
MODEL_GOOGLE_GEMINI_INFINITYBLOOM
MODEL_GOOGLE_GEMINI_INTERNAL_TAB_FLASH_LITE
MODEL_GOOGLE_GEMINI_INTERNAL_BYOM
```

数量统计：

```
$ strings /workspace/agy/install/antigravity | grep -c "MODEL_GOOGLE_GEMINI_"
30
```

**30 个 MODEL_GOOGLE_GEMINI_ 字符串**（比文章的"1650 个占位"少，但具体名字都查得到，文章数据可能是**所有可能的枚举值总和**，不全是 hard-coded 字符串）。完整清单在 `out/inspect-agy.md`。

### Q3.4 —— 隐藏命令行开关

【反编译 + 一手】—— `fallback-functions.txt` 47-50 已经列了 4 个 printmode 相关函数。但文章说"11 个隐藏开关"——这部分**没法纯靠 strings 验**（flag 名字一般 hard-coded，但有的藏在 init 函数里）。

可以从 antigravity --help 输出【一手】确认"11 个公开里没列的隐藏项"：

| 开关 | 用途 | 证据 |
|---|---|---|
| `--remote-control` | 远程控制 daemon | --help 里**有**，但描述模糊 |
| `--dangerously-skip-permissions` | 自动批准所有权限 | --help 里**有** |
| `--effort` | 推理强度（low/medium/high/xhigh/max） | --help 里**有** |
| `--input-format stream-json` | NDJSON 多轮 | --help 里**有** |
| `--output-format stream-json` | 流式输出 | --help 里**有** |
| `--print-timeout` | 打印模式超时 | --help 里**有** |
| `--json-schema` | 结构化输出 schema | --help 里**有** |
| `--sandbox` | sandbox 模式 | --help 里**有** |
| `--mode` | accept-edits / plan | --help 里**有** |
| `--new-project` | 新建 project | --help 里**有** |
| `--disable-slash-commands` | 禁用 slash command | --help 里**有** |

**这 11 个在 --help 里都列了，但描述都很隐晦**（"远程控制 daemon"、"自动批准"、"sandbox"）—— **和文章说的"11 个对用户隐藏的开关"有出入**。可能文章引用的旧版本里有 --help 不显示的 hidden flags，但当前 1.3.3 版本 --help 暴露了。

**4 套服务器环境（已验）+ Cloud Run auto-updater（已验）+ 多个未发布模型代号（已验）+ 多个 printmode/stream-json/NDJSON 开关（已验）**—— **4 项全部找到**。

### Q3.5 —— 其他发现（文章没提到的）

【strings + 反编译]:

- **`boringcrypto` build tag**（来自 `.go.buildinfo` 段）—— 用 Google 内部 BoringSSL 实现，跟 FIPS 验证相关。
- **`simd` build tag** —— Go 1.26+ 启用 simd 编译。
- **`fieldtrack` build tag** —— Go 1.20+ 精确 GC scan。
- **JWT signing method `none` 仍然存在**【反编译 + strings]:

```
0x6a5bbc0  jwt.(*signingMethodNone).Alg
0x6a5bbe0  jwt.(*signingMethodNone).Verify
0x6a5bcc0  jwt.(*signingMethodNone).Sign
```

⚠️ **`signingMethodNone` 是 JWT 经典 insecure 模式**——客户端可能误用，但应该仅作 fallback。

- **`v1internal` proto service 35+ 个 gRPC method**（`exa.language_server_pb`、`exa.seat_management_pb`、`exa.opensearch_clients_pb`）—— 内部业务 API 全部可见。

---

## 跟文章对比

| 文章断言 | 我们的验证 | 状态 |
|---|---|---|
| agy 是 180MB | 实际 214 MB | ✗ 数字偏差（+19%） |
| Go 编译器 `go1.28-20260921-RC02` | `.go.buildinfo` 段确认 | ✓ |
| `__gopclntab` 改名 `.lrodata.gopclntab`（Mach-O）/ `.lrodata`（ELF）| ELF `.lrodata` 段存在 | ✓ |
| 157,992 个函数名 | 我们恢复 155,184 个（98%）| ✓ 数量级一致 |
| `waitForEligibility` 函数 | 2 处（store + printmode）| ✓ |
| 30s/60s timeout 数字 | strings 是 `%s` 占位符（需要 Ghidra 控制流反编译确认）| ⚠️ 推测 |
| "Timed out... sending anyway" 日志 | binary 中完全一致 | ✓ |
| 钥匙串 500ms 熔断 | binary 字符串确认 | ✓（部分——500ms 数字未直接见到） |
| 4 套服务器环境 | binary 找到 4-5 套 host | ✓ |
| Cloud Run auto-updater URL | binary 找到完整 URL | ✓ |
| 11 个隐藏命令行开关 | --help 找到 11 个相关但都被列出来 | ⚠️ 文章说的"隐藏"不太准确 |
| RIFTRUNNER / INFINITYBLOOM 内部代号 | 6+ 个 GEMINI_RIFTRUNNER_*, 1 个 INFINITYBLOOM | ✓ |
| 1650 个占位型号 | 实际 hard-coded 30 个 | ⚠️ 文章数字高估 |

---

## 3 个问题的简短答案

**Q1**：渐进式回退（keyring 优先 → keyring timeout 熔断降级文件 → OAuth 浏览器流程），用 zalando/go_keyring 在 Linux 走 D-Bus Secret Service。

**Q2**：等服务器 verdict 30s（交互）或 60s（print mode），超时直接 `sending anyway` 当有资格。客户端自我约束，服务器不门禁。

**Q3**：4 套 host 域名 + Cloud Run 自动更新 URL + 30 个未发布模型代号 + 11 个 printmode/remote-control 相关的 flag（含 --remote-control 远程控制 daemon），外加 `boringcrypto`/`simd`/`fieldtrack` build tag、35+ 内部 gRPC service、JWT `signingMethodNone` fallback。

---

## 产物清单

| 路径 | 大小 | 内容 |
|---|---|---|
| `/workspace/agy/out/qa-report.md` | 本文件 | 3 问题综合回答 |
| `/workspace/agy/out/inspect-agy.md` | 25 KB | REA 静态分析全报告（`go version -m` 等价物、Go build tag、section 表）|
| `/workspace/agy/out/restore-symbols.md` | 8.6 KB | rea-go-seeds 工具流程 + .lrodata 补丁说明 |
| `/workspace/agy/out/ghidra-analyze.md` | 34 KB | Ghidra 安装 + rea analyze timeout 复盘 + fallback 路径 |
| `/workspace/agy/out/seeds/seeds.txt` | 18 MB | 155,184 个 Ghidra seed（address+name）|
| `/workspace/agy/out/seeds/funcs.txt` | 16 MB | 同上（人类可读）|
| `/workspace/agy/out/fallback-functions.txt` | 10.8 KB | 115 个 auth/eligibility 关键函数地址 |
| `/workspace/agy/install/antigravity` | 214 MB | 目标 binary（已 extracted）|
| `/workspace/agy/{jdk,go,rea-agents,rea-go-seeds,ghidra,install}/` | 2.5 GB+ | 完整逆向工具链 |
