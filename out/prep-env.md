# prep-env 报告 — JDK 21 / Go 1.22+ / rea-agents 三套工具链就位

> 沙箱：Debian 12 (bookworm) x86_64 · 时间：2026-10-12 18:00–18:20 UTC
> 出口带宽实测：~20 MB/s（远好于任务提示的 50 KB/s），275 MB 全部 5 秒内下完。
> 布局：JDK 和 Go 已经把版本化子目录扁平化到 `<tool>/` 根目录，**contract 路径直接生效**。
> 修复（attempt 4）：Go stdlib `src/` 在前几轮被 30s bash timeout 截断（只有 7/72 个包），已用完整 tarball 重灌。

## 0. 目录布局（重要 — 验证 contract）

```
/workspace/agy/
├── install/
│   ├── agy → /workspace/agy/install/antigravity  (214 MB ELF)
│   └── antigravity                              (目标 binary，前置已就位)
├── jdk/                       ← JDK 21 安装根（直接可访问）
│   ├── bin/java, bin/javac, bin/jshell, ...    ← contract 路径
│   ├── conf/, include/, jmods/, legal/, lib/, man/, release
│   └── NOTICE
├── go/                        ← Go 1.22.10 安装根（直接可访问）
│   ├── bin/go, bin/gofmt                      ← contract 路径
│   ├── go.env                                  ← GOPROXY/GOSUMDB 配置
│   ├── src/                                    ← 完整 stdlib（72 个包，122 MB）
│   ├── pkg/, lib/, api/, doc/, misc/
│   └── CONTRIBUTING.md, LICENSE, ...
└── out/prep-env.md             ← 本文件
```

## 1. 总览

| 工具 | 版本 | Contract 路径 | 大小 | 验证 | 状态 |
|---|---|---|---|---|---|
| JDK 21 (Temurin LTS) | 21.0.12.1+1 | `/workspace/agy/jdk/bin/java` | 345 MB | `java -version` | ✅ |
| Go (linux amd64) | 1.22.10 | `/workspace/agy/go/bin/go` | 247 MB（含 122 MB src） | `go version` + `go test fmt` | ✅ |
| rea-agents (npm) | 6.4.0 | `/usr/local/bin/rea` | 96 MB | `rea --version` | ✅ |
| antigravity (前置) | 1.0 | `/workspace/agy/install/agy` | 214 MB | `readelf -h` ELF64 | ✅（前置已就位） |

`readlink -f` 全部解析到 NAS 实际挂载点 `/run/csi/mount-root/nas/.../agy/...`（正常 sandbox 行为，路径合法）。

## 2. 每个工具的来源、安装、验证

### 2.1 JDK 21 — Temurin LTS

- **源 URL**：`https://mirrors.tuna.tsinghua.edu.cn/Adoptium/21/jdk/x64/linux/OpenJDK21U-jdk_x64_linux_hotspot_21.0.12.1_1.tar.gz`
- **源文件大小**：207,473,347 B（≈198 MB），HTTP 200，Tuna 镜像 `x-tuna-mirror-id: nanomirrors`
- **备选 URL**：`https://mirrors.huaweicloud.com/openjdk/21/`（HTTP 200，未触发；Tuna 一次成功）
- **未使用**：`https://mirrors.aliyun.com/Adoptium/...`（HTTP 404，Aliyun 没同步 Adoptium 目录）
- **下载实测**：`curl` 单连接 207 MB 在 5 秒内下完
- **解压**：`tar -xzf jdk21.tar.gz -C jdk_extract` → 得到 `jdk-21.0.12.1+1/`
- **安装**（v1）：`mv jdk_extract/jdk-21.0.12.1+1 /workspace/agy/jdk/jdk-21` + `ln -sfn jdk-21 current`
- **重布局**（v2，根据 verifier 反馈）：删除 `current` 符号链接，把 `jdk-21/*` 全部 `mv` 到 `jdk/` 根目录，删除空 `jdk-21/` 子目录。最终 `/workspace/agy/jdk/bin/java` 是真实文件路径。
- **验证输出**（contract 路径）：
  ```
  $ /workspace/agy/jdk/bin/java -version
  openjdk version "21.0.12.1" 2026-08-18 LTS
  OpenJDK Runtime Environment Temurin-21.0.12.1+1 (build 21.0.12.1+1-LTS)
  OpenJDK 64-Bit Server VM Temurin-21.0.12.1+1 (build 21.0.12.1+1-LTS, mixed mode, sharing)

  $ /workspace/agy/jdk/bin/javac -version
  javac 21.0.12.1
  ```

### 2.2 Go 1.22.10

- **Tuna 不通**：`https://mirrors.tuna.tsinghua.edu.cn/golang/` 根 404；具体文件 `go1.22.0.linux-amd64.tar.gz` 也 404
- **Huawei 不通**：`https://mirrors.huaweicloud.com/golang/` 返回 401 Unauthorized（华为 API 网关需要鉴权）
- **最终源（Aliyun）**：`https://mirrors.aliyun.com/golang/go1.22.10.linux-amd64.tar.gz`
  - HTTP 200, content-type `application/octet-stream`, content-length 68,991,036
- **下载实测**：单连接 5 秒内下完
- **解压**（attempt 1）：`tar -xzf go1.22.10.tar.gz -C go_extract` → **被 30s bash timeout 截断，只解了 ~7/72 个 src 包**
- **补救**（attempt 4）：重新下到 `/tmp/go_check/go1.22.10.tar.gz`，完整解压到 `/tmp/go_full_extract/go/`（72 个 src 包全在），然后 `cp -a /tmp/go_full_extract/go/src /workspace/agy/go/src` 覆盖原破损的 src/，再 `chmod -R a+rX` 修 700→755 权限
- **布局**（v1 → v2）：扁平化到 `go/` 根目录（v2），删 `current` 符号链接（v2）
- **GOPROXY 配置**（`/workspace/agy/go/go.env`，已根据扁平布局更新 GOROOT）：
  ```sh
  export GOROOT=/workspace/agy/go
  export GOPATH=/workspace/.home/go
  export GOPROXY=https://goproxy.cn,direct
  export GOSUMDB=off
  export PATH=$GOROOT/bin:$GOPATH/bin:$PATH
  ```
- **验证输出**（contract 路径 + 关键 stdlib 测试）：
  ```
  $ /workspace/agy/go/bin/go version
  go version go1.22.10 linux/amd64

  $ /workspace/agy/go/bin/go test fmt
  ok      fmt    0.068s

  $ source /workspace/agy/go/go.env && go env GOPROXY GOSUMDB GOROOT
  https://goproxy.cn,direct
  off
  /workspace/agy/go

  $ cat > /tmp/hello.go <<'EOF'
  package main; import "fmt"
  func main() { fmt.Println("hello") }
  EOF
  $ /workspace/agy/go/bin/go run /tmp/hello.go
  hello
  ```

### 2.3 rea-agents 6.4.0

- **npm registry 切换**：`npm config set registry https://registry.npmmirror.com`
- **包信息核验**（直接从 npmmirror 拉 JSON，不走 SEO）：
  ```
  GET https://registry.npmmirror.com/rea-agents/6.4.0 → 200
    name        : rea-agents
    version     : 6.4.0
    description : Reverse engineer anything from your terminal or agent with one CLI and MCP server.
    bin         : { rea: 'scripts/rea.mjs', 'rea-agents': 'scripts/rea.mjs' }
    dist.tarball: https://registry.npmmirror.com/rea-agents/-/rea-agents-6.4.0.tgz
  ```
- **安装**：`npm install -g rea-agents@6.4.0`（在后台跑，避开 30s bash 超时；实际 17s 完成 `added 144 packages`）
- **安装位置**：`/usr/local/lib/node_modules/rea-agents/`
- **CLI 注册**：`/usr/local/bin/rea` 和 `/usr/local/bin/rea-agents` 都是指向 `scripts/rea.mjs` 的 npm wrapper 软链
- **验证输出**：
  ```
  $ rea --version
  6.4.0
  $ rea-agents --version
  6.4.0
  $ readlink -f /usr/local/bin/rea
  /usr/local/lib/node_modules/rea-agents/scripts/rea.mjs
  ```
- **CLI 表面**（`rea --help | head -60`）：60+ 个子命令。

## 3. 镜像源 / 兜底决策表

| 工具 | 首选 | 备选 | 兜底 | 结果 |
|---|---|---|---|---|
| JDK 21 | Tuna `Adoptium/21/jdk/x64/linux/` | Huawei `openjdk/21/` | — | Tuna 一次成功（207MB） |
| Go 1.22+ | Tuna `/golang/`（404）| Huawei `/golang/`（401）| Aliyun `/golang/` | Aliyun 兜底成功 |
| rea-agents | `registry.npmmirror.com` | — | — | 一次成功 |
| antigravity | codeload.github.com (前置) | — | — | 已就位 |

## 4. 失败 / 兜底详细记录

### 4.1 Tuna 的 `/golang/` 路径不存在
- `curl -I https://mirrors.tuna.tsinghua.edu.cn/golang/` → HTTP 404
- 结论：Tuna 没同步 Go 发行版 tarball。**直接判定不可用，切换 Aliyun。**

### 4.2 Huawei 的 `/golang/` 鉴权拦截
- `curl -I https://mirrors.huaweicloud.com/golang/` → HTTP 401
- 响应体：`{"errors":[{"status":401,"message":"Unauthorized or Bad credentials"}]}`
- 结论：Huawei 把 `/golang/` 当成 OBS API 网关，需要 AK/SK 鉴权签名。**直接判定不可用，切换 Aliyun。**

### 4.3 Aliyun 的 `/Adoptium/` 路径不存在
- `curl -I https://mirrors.aliyun.com/Adoptium/21/jdk/x64/linux/` → HTTP 404
- 结论：Aliyun 没同步 Adoptium。Tuna 一次成功，未触发兜底。

### 4.4 npm install 卡在 30s bash 超时（attempt 1）
- `npm install -g rea-agents@6.4.0` 在 30s bash timeout 下被打断
- 处置：清半成品 + 后台重跑（17s 完成 144 包）

### 4.5 verifier 第 1 轮反馈：contract 路径不直接
- 我用了 `<tool>/current/bin/...`，但 contract 是 `<tool>/bin/...`
- 处置（v2）：删除 `current` 符号链接，把 `<tool>/<tool>-<ver>/*` 全部 `mv` 到 `<tool>/` 根目录

### 4.6 Go tar 解压被 30s bash timeout 截断（attempt 1，attempt 4 修复）
- **症状**：`tar -xzf go1.22.10.tar.gz -C go_extract` 与 JDK 提取共用同一个 bash 调用，被 30s 硬超时打断。Go 解压慢（JDK 已经先占了时间），所以只解了 ~7/72 个 stdlib 包。
- **影响**：`/workspace/agy/go/src/` 缺 `fmt`, `runtime`, `errors`, `sync` 等关键包。任何 `go run` / `go test` 都会 fail："package fmt is not in std"。
- **发现**：verifier 在 attempt 3 拒绝（"Go stdlib src 缺失, restore-symbols 要 go run 必须补"）。
- **修复**（attempt 4）：
  1. 重新下载 tarball 到 `/tmp/go_check/go1.22.10.tar.gz`（5 秒）
  2. 在 `/tmp` 本地完整解压到 `/tmp/go_full_extract/go/`（src/ 72 包齐全）
  3. 后台 `cp -a /tmp/go_full_extract/go/src /workspace/agy/go/src`（NAS 写小文件慢，~2 分钟）
  4. 后台 `chmod -R a+rX /workspace/agy/go/src`（把 700 改回 755，避免后续 agent 用非 root 跑 go 时读不到）
  5. 验证：`go run hello.go` 输出 "hello" + `go test fmt` 输出 "ok"

### 4.7 JDK 提取未受影响
- 虽然 attempt 1 的 `tar -xzf` 命令也跑到 JDK，但 JDK 提取比 Go 快（更少的小文件），30s 内完成。后续 javac 编译测试 + 69 个 jmods 都齐全。

### 4.8 go_extract 残留目录
- NAS 挂载上 `rmdir` 返回 `errno 39 Directory not empty`
- 处置：留着无害（外层空、内层 NAS 不可删），不影响任何 contract 路径

## 5. 环境变量设置（复用命令）

```bash
# JDK
export JAVA_HOME=/workspace/agy/jdk
export PATH=$JAVA_HOME/bin:$PATH
java -version
# openjdk version "21.0.12.1" 2026-08-18 LTS

# Go (source go.env 即可)
source /workspace/agy/go/go.env
# 等价于：
export GOROOT=/workspace/agy/go
export GOPATH=/workspace/.home/go
export GOPROXY=https://goproxy.cn,direct
export GOSUMDB=off
export PATH=$GOROOT/bin:$GOPATH/bin:$PATH
go version
# go version go1.22.10 linux/amd64

# rea-agents (已经全局安装)
rea --version
# 6.4.0
```

## 6. 最终可用工具清单

| 工具 | Contract 路径（真实文件） | 验证命令 | 状态 |
|---|---|---|---|
| java | `/workspace/agy/jdk/bin/java` | `java -version` → 21.0.12.1 LTS | ✅ |
| javac | `/workspace/agy/jdk/bin/javac` | `javac -version` → 21.0.12.1 | ✅ |
| go | `/workspace/agy/go/bin/go` | `go version` → go1.22.10 linux/amd64 | ✅ |
| go test | `/workspace/agy/go/bin/go test fmt` | `ok fmt 0.068s` | ✅ |
| go run | `/workspace/agy/go/bin/go run <file>.go` | 任意 hello world 可跑 | ✅ |
| rea | `/usr/local/bin/rea` → `/usr/local/lib/node_modules/rea-agents/scripts/rea.mjs` | `rea --version` → 6.4.0 | ✅ |
| rea-agents | `/usr/local/bin/rea-agents` → `/usr/local/lib/node_modules/rea-agents/scripts/rea.mjs` | `rea-agents --version` → 6.4.0 | ✅ |
| antigravity | `/workspace/agy/install/agy` → `/workspace/agy/install/antigravity` | 214 MB ELF64 | ✅ |

`readlink -f` 解析到 NAS 实际挂载点（正常 sandbox 行为，路径合法）。
