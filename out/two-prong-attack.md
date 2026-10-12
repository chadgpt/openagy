# antigravity RE — 两头夹击最终报告

> **任务**:在 plan_d03b0152 4 任务全部 PASS 之后,继续推进,
> 一边用最新 Go 重新构建 rea-go-seeds 验证种子可重现,一边派两路 subagent
> 并行深挖 auth/eligibility 流程的真实代码。

## 1. 三件事的最终状态

| 子任务 | 结果 | 关键证据 |
| --- | --- | --- |
| Go 1.26.2 装 + 重新构建 rea-go-seeds | ✅ DONE | `/workspace/agy/go126/bin/go version` = `go1.26.2`;`go build .` 退出 0;新 binary 跑 antigravity 出 seeds.txt **SHA-256 一致** |
| Subagent A: Ghidra analyzeHeadless 绕开 rea 5.5min | ✅ DONE | 220 秒 跑完 decompile 阶段;**860 / 1498** priority funcs 真实反编译,14 MB `.c` 文件 |
| Subagent B: 静态调用图 + proto schema + 流程叙述 | ✅ DONE | call-graph.json 2,625 nodes / 2,422 edges;proto-schema.md 还原 14 个 message;auth-flow.md 273 行 |

## 2. Go 1.26.2 安装与回归验证

| 步骤 | 命令 | 结果 |
| --- | --- | --- |
| 下载 | `curl -fsSL https://mirrors.aliyun.com/golang/go1.26.2.linux-amd64.tar.gz` | 66.8 MB,exit 0 |
| 解压到本地 tmpfs | `tar -xzf → /tmp/go_installs/go` | 27.8 s,go version = go1.26.2 |
| 复制到 NAS | `cp -a /tmp/go_installs/go /workspace/agy/go126` | 后台跑约 5 min,253 MB(不含 git,.gitignore 已 exclude) |
| 还原 go.mod | `go 1.26.2`(原值) | 不再降级 |
| 编译 | `go build -o /tmp/pclnseeds-126 .` | 27.8 s,exit 0,3.1 MB binary |
| 跑 antigravity | `pclnseeds-126 /workspace/agy/install/antigravity /tmp/seeds-126/` | recovered **155,184 function names** |
| **SHA-256 一致性** | `sha256sum /tmp/seeds-126/seeds.txt /workspace/agy/out/seeds/seeds.txt` | 两者都是 `e1504128b7661974855e2f4009a4c6c26ee53e2f64ba587bb7b8cf7b8ba8aa3a` |

> 唯一源码修改保留:`.lrodata` ELF 分支回退补丁(让 Google 内部 Go toolchain
> 把 pclntab 折到 `.lrodata` 时也能找到)。

## 3. 两头夹击:Subagent A (Ghidra 反编译)

### 3.1 关键决策

| 问题 | 决策 | 原因 |
| --- | --- | --- |
| rea 5.5min 内部 timeout | **绕过 rea**,直接调 `$GHIDRA/support/analyzeHeadless` | rea-agents 6.4.0 在 5.5 min 处硬切,沙箱跑 17 个 analyzer 需 20-40 min |
| Ghidra Decompiler Switch Analyzer 慢 | `-noanalysis` | 该 analyzer 90% 时间花在 Go 的 switch-jump 推导,得 30+ 个 "Unable to resolve constructor" 警告才能 decompile 一个函数 |
| 函数边界 | preScript `ReaGhidraApplySeeds.java` 一次性种 155K funcs | seeds.txt 给我们完整 function start 表 |
| 反编译哪些 | postScript `DecompilePriority.java` 只跑 1498 个 priority funcs | 60 sec/func timeout,只对 auth/eligibility 相关的下功夫 |

### 3.2 跑出来的数字

| Metric | Value |
| --- | --- |
| 种子 preScript 处理 | ~5 min(155,184 funcs + 1485 thunk 冲突) |
| Decompile phase | **220 s (3 min)** |
| Total processed | 1,498 |
| Decompiled OK | **860 (57%)** |
| Skipped (no func at addr) | 637 (43%) |
| Errors (low-level) | 1 |
| Total LOC decompiled | 297,104 |
| Go packages covered | 26 |
| Output dir size | 14 MB |

### 3.3 关键文件

```
/workspace/agy/out/decompile/
├── dec/                              # 860 .c files (14 MB)
│   ├── 899cd40_waitForEligibility.c
│   ├── 899cf80_StartOAuthProcess.c
│   ├── 899d3a0_StartGCPAuthProcess.c
│   ├── 899cc00_commitAuth.c
│   ├── 86d8d40_StartOAuthProcess.c  (ServerBackend version)
│   ├── 86a66a0_Authenticate.c       (ChainedAuth)
│   ├── 86a6aa0_StartGCPAuthProcess.c (ChainedAuth)
│   ├── 86aa0c0_TryAuth.c            (keyringAuth)
│   ├── 899db00_ResetAuthState.c
│   ├── 899de20_Logout.c
│   ├── 6f468a0_StartOAuthSignIn.c   (cortex sandboxproxy)
│   └── ... (849 more)
├── dec/_summary.txt
├── dec/_errors.txt                   # 638 行 (637 SKIP, 1 ERR)
├── DecompilePriority.java            # Ghidra postScript (~165 lines)
├── decompile-summary.md              # 106 行
├── decompile-<package>.md            # 26 个 per-package 报告
└── logs/analyzeHeadless2.log         # 1.5 MB 完整日志
```

## 4. 两头夹击:Subagent B (静态分析)

### 4.1 关键决策

| 问题 | 决策 | 原因 |
| --- | --- | --- |
| 怎么找 caller/callee | `objdump -d` + 用 seeds.txt 做 function boundary 表 | 剥符号 binary 里 objdump header 只剩 global symbols;bisect seeds 找 containing function |
| 怎么解 field number | 直接 parse binary 里的 `FileDescriptorProto` blob | 发现 Google 用 modified wire layout:field 3 = number(标准是 field 2) |
| 怎么理解 50ms polling | 反汇编里硬编码立即数 `0x2faf080` = 50×10⁶ ns | 这就是 `time.Sleep(50 * time.Millisecond)` |

### 4.2 跑出来的数字

| Metric | Value |
| --- | --- |
| `objdump -d` 文件大小 | 498 MB (`/tmp/agy.text.asm`) |
| 总指令数 | 14,808,346 |
| `call` 指令数 | 753,461 |
| `jmp` 指令数 | 354,338 |
| 全 binary 唯一边数 | 665,551 |
| Priority funcs 覆盖 | 2,559 / 2,559 (100%) |
| 1-hop 图节点 | 2,625 |
| 1-hop 图边 | 2,422 |
| Proto messages 还原 | 14(v1internal + language_server + codeassistclient) |

### 4.3 关键文件

```
/workspace/agy/out/decompile/
├── call-graph.json                   # 891 KB — 节点 + 边 + 元数据
├── call-graph.dot                    # 395 KB — Graphviz DOT
├── xrefs.txt                         # 2.1 MB — 17,275 行 raw xref (from<TAB>to<TAB>count)
├── auth-flow.md                      # 273 行 — 流程叙述
├── proto-schema.md                   # 230 行 — 还原的 .proto
└── build_reports.py                  # 14 KB
```

## 5. 关键发现(两端互证)

### 5.1 `waitForEligibility` 的真实实现

| 段 | Subagent A 看到的 (反编译) | Subagent B 看到的 (反汇编) | 一致性 |
| --- | --- | --- | --- |
| Timeout | `context.WithTimeoutCause(parent, 30*time.Minute, …)`(推断) | `0x6fc23ac00 ns = 30*60*1e9` 立即数 | ✅ |
| Polling | `time.Sleep(50 * time.Millisecond)` | `0x2faf080 = 50*1e6` 立即数 | ✅ |
| 阻塞 | `runtime.chanrecv` 间接调用 | `call *%rcx`(interface dispatch) | ✅ |
| Eligibility flag | offset `0x79` 的 bool | `cmpb $0x0,0x79(%rax)` | ✅ |
| 失败路径 | `backend.IneligibilityFromResult` | `call 86b3da0`(=IneligibilityFromResult 0x86b3da0)| ✅ |

### 5.2 Auth chain 拓扑

```
cli (store.Manager)                   ← auth state coordinator
   ↓ initAuth
   ├→ TrySilentAuth (0x899d9c0)        ← 0 static callers (goroutine)
   ├→ StartOAuthProcess (0x899cf80)    ← 0 static callers (goroutine)
   ├→ StartGCPAuthProcess (0x899d3a0)  ← 0 static callers (goroutine)
   └→ waitForEligibility (0x899cd40)   ← channel receive + 30 min timeout
        ↓ (on success)
        commitAuth (0x899cc00)         ← writes to keyring
   ↓
cli/backend (ServerBackend)            ← gRPC client
   ↓ ValidateAndOnboardAccount
   ↓ SelectLicense / SelfAssignLicense / FetchLicenses
   ↓
language_server/code_assist_client (CodeAssistClient)
   ↓ SelectLicense / SelfAssignLicense / FetchLicenses
   ↓
language_server_go_grpc (Connect/gRPC stub)
   ↓
cloudaicompanion.googleapis.com:443   ← server side, NOT in binary
```

### 5.3 Keyring fallback(D-Bus 不可用时)

```c
// 86aa0c0 keyringAuth.TryAuth
// step 1: dbus.SessionBus()  ← 失败时设 codeassistclient.keyringRecentlyUnavailable = true
// step 2: secret-service lookup
// step 3: nacl/secretbox 解密 token
// step 4: 返给 ChainedAuth

// 86a6aa0 ChainedAuth.StartGCPAuthProcess
//   检查 keyringRecentlyUnavailable
//   跳过 keyringAuth, 试 adcAuth
//   失败就试 oauthAuth
```

### 5.4 Proto schema 关键发现

**Google modified `FieldDescriptorProto` layout**:
- field 3 (varint) = **field number** ← 标准 proto 是 field 2
- field 5 (varint) = type
- field 10 (LEN) = json_name

这影响所有 Google 内部 proto 的 binary 解析。**用标准 protobuf 库
直接 parse Google 内部产物的 FileDescriptorProto 会拿错 field number**。

## 6. Git 提交历史(本次推进)

```
$ git log --oneline | head -10
7d15b51 subagent A (decompile-auth-funcs) decompile phase DONE
dff37a6 subagent A (decompile-auth-funcs) string analysis pass
76df0a9 subagent B (call-graph-auth-flow) initial pass
702ce07 two-prong attack prep
ae960ac baseline: PASS artifacts from plan_d03b0152
```

## 7. 完整交付物清单

### 7.1 本次新增(本任务)

| 路径 | 大小 | 说明 |
| --- | --- | --- |
| `/workspace/agy/go126/` | ~253 MB | Go 1.26.2(.gitignore 已 exclude runtime) |
| `/workspace/agy/rea-go-seeds/go.mod` | 4 lines | 还原为 `go 1.26.2`(原值) |
| `/workspace/agy/out/decompile/dec/` | 14 MB,860 .c | Ghidra 反编译产物 |
| `/workspace/agy/out/decompile/dec/_summary.txt` | 9 lines | decompile run stats |
| `/workspace/agy/out/decompile/dec/_errors.txt` | 638 lines | error log |
| `/workspace/agy/out/decompile/DecompilePriority.java` | 165 lines | Ghidra postScript |
| `/workspace/agy/out/decompile/decompile-summary.md` | 106 lines | per-package stats |
| `/workspace/agy/out/decompile/decompile-*.md` | 26 files,150 KB | per-package reports |
| `/workspace/agy/out/decompile/call-graph.json` | 891 KB | 节点+边+元数据 |
| `/workspace/agy/out/decompile/call-graph.dot` | 395 KB | Graphviz DOT |
| `/workspace/agy/out/decompile/xrefs.txt` | 2.1 MB | 17,275 xref 边 |
| `/workspace/agy/out/decompile/auth-flow.md` | 273 lines | 流程叙述 |
| `/workspace/agy/out/decompile/proto-schema.md` | 230 lines | 还原的 .proto |
| `/workspace/agy/out/blackbox/changelog.txt` | 141 KB | antigravity 1.3.x release notes |
| `/workspace/agy/out/grpc-paths.txt` | — | gRPC service paths |
| `/workspace/agy/out/models-gemini.txt` | — | 44 个 model identifiers |
| `/workspace/agy/out/urls-google.txt` | — | 27 个 Google API endpoint |
| `/workspace/agy/out/supplement-deep-dive.md` | — | 补充深挖 |
| `/workspace/agy/out/two-prong-attack.md` | 本文件 | 最终报告 |

### 7.2 plan_d03b0152 已 PASS 产物(基线)

| 路径 | 来源 |
| --- | --- |
| `out/seeds/seeds.txt` | restore-symbols (155,184 funcs, SHA-256 e1504128...) |
| `out/seeds/funcs.txt` | restore-symbols |
| `out/inspect-agy.md` | inspect-agy (25 KB, 426 lines) |
| `out/ghidra-analyze.md` | ghidra-analyze (29 KB) + fallback-functions.txt (115 lines) |
| `out/qa-report.md` | qa (14 KB) |
| `out/prep-env.md` | prep-env |
| `out/restore-symbols.md` | restore-symbols |

## 8. 下一步可做(本次未做)

1. **Ghidra decompiler post-processor** — 把 `func_0x05xxxxxx` 这类 raw call target
   用 seeds.txt 替换成真实函数名。当前 860 个 .c 文件里大量间接调用
   (call *%rax) 无法静态解析,需要 binary 跑起来做 dynamic trace。
2. **reconstruct .proto enum values** — 14 个 messages 已还原,enum 值
   (IneligibleTierReasonCodes, Mode, AuthMode, UpgradeSubscriptionType,
   ReleaseChannel, CreditType) 需要再 parse `EnumDescriptorProto` blob。
3. **Ghidra GUI 验证** — 当前 decompile 是 headless 跑的,无人工 review。
   高价值函数 (waitForEligibility, commitAuth) 应该用 Ghidra GUI 看一遍
   修正 Ghidra 误判的 control flow。
4. **render call-graph.png** — 沙箱无 graphviz,DOT 文件需要在本地 render。
5. **dynamic trace** — 用 `gdb` 或 `rr` 跑一次 antigravity 的 OAuth 流程,
   抓真实 runtime call stack,跟静态图对比。
6. **server-side analysis** — cloudaicompanion.googleapis.com 是 server,
   不在 binary 里。要分析它需要走 GCP 的公开 API 文档 + gRPC reflection。

## 9. 硬约束验证

| 约束 | 状态 |
| --- | --- |
| 二进制不被修改 | ✅ `sha256sum` 前后一致(基线 9.4 KB 文件已存档) |
| `out/seeds/seeds.txt` 不变 | ✅ SHA-256 e1504128... 在 Go 1.22.10 和 1.26.2 下都生成同样产物 |
| Go 1.22.10 仍可用 | ✅ `/workspace/agy/go/bin/go version` = 1.22.10 |
| Git 追踪 | ✅ 5 个 commit,从 baseline 到本次完成 |
| 反编译 sandbox 内存 < 3 GB | ✅ Ghidra 用了 1.2 GB(2G heap 限制) |
| 反编译 sandbox CPU 2 cores | ✅ 96% CPU 单进程,留 1 core 给 subagent B |
| 不引入新外部依赖 | ✅ rea-go-seeds 仍只依赖 Go stdlib(debug/elf, debug/gosym) |
