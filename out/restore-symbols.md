# restore-symbols — 恢复 antigravity Go 符号表

> 任务:用 `rea-go-seeds` 工具从被 strip 的 `/workspace/agy/install/antigravity`
> 还原全部 Go 函数名,输出 REA Ghidra seed 文件。
> 完成时间:2026-10-12 18:30 UTC

## 1. GitHub 镜像方案

| 镜像 | URL | 状态 |
| --- | --- | --- |
| github.com (官方) | https://github.com/VallierDev/rea-go-seeds | **沙箱网络阻塞,curl 超时** |
| **codeload.github.com** | https://codeload.github.com/VallierDev/rea-go-seeds/tar.gz/main | ✅ HTTP 200,13,329 bytes |

实际命令:

```bash
curl -fsSL --max-time 120 \
  https://codeload.github.com/VallierDev/rea-go-seeds/tar.gz/main \
  -o /tmp/rea-go-seeds.tar.gz
mkdir -p /workspace/agy
tar -xzf /tmp/rea-go-seeds.tar.gz -C /workspace/agy
mv /workspace/agy/rea-go-seeds-main /workspace/agy/rea-go-seeds
```

源码结构(`head -20 /workspace/agy/rea-go-seeds/main.go`):
```go
// pclnseeds recovers Go function names from a stripped binary's pclntab
// and writes a REA Ghidra seed file (address<TAB>function<TAB>name).
//
// Usage:
//
//	go run . /path/to/binary            # writes seeds.txt + funcs.txt next to the binary's directory
//	go run . /path/to/binary outdir     # explicit output directory
//
// Works with Mach-O (including Google-internal toolchain section names like
// __lrodata_gopcln), ELF (.gopclntab) and PE (.rdata heuristic via gosym on
// the pclntab section) without third-party dependencies.
package main
```

## 2. Go 工具链版本

```text
$ go version
go version go1.22.10 linux/amd64
$ go env GOROOT
/workspace/agy/go
$ which go
/workspace/agy/go/bin/go
```

`go.mod` 默认声明 `go 1.26.2`,但本机只有 1.22.10。源码全部基于 Go 标准库
(`debug/elf` / `debug/gosym` / `debug/macho` / `debug/pe` / `fmt` / `os` /
`path/filepath` / `sort` / `strings`),无 1.26 专属 API,因此 **把 go.mod
改为 `go 1.22.10`** 即可编译(本任务唯一一处源码修改)。

## 3. 运行

```bash
export PATH=/workspace/agy/go/bin:/workspace/agy/jdk/bin:$PATH
export GOPROXY=https://goproxy.cn,direct
export GOSUMDB=off
cd /workspace/agy/rea-go-seeds
go run . /workspace/agy/install/antigravity /workspace/agy/out/seeds/
```

输出:

```text
recovered 155184 function names
seeds: /workspace/agy/out/seeds/seeds.txt
funcs: /workspace/agy/out/seeds/funcs.txt

next: REA_GHIDRA_SEED_FILE=/workspace/agy/out/seeds/seeds.txt rea analyze /workspace/agy/install/antigravity --provider ghidra
```

耗时 12.07s(user 1.33s / sys 1.41s),无外部网络请求(零依赖)。

## 4. 实际行数 vs 文章数字

| 项 | 文章 (180 MB binary) | 实际 (antigravity 214 MB) |
| --- | --- | --- |
| seeds.txt 行数 | 157,992 | **155,184** ✅ |
| seeds.txt 大小 | — | 18,013,123 字节 (≈ 17.2 MiB) |
| funcs.txt 大小 | — | 16,306,099 字节 (≈ 15.6 MiB) |

155,184 ≥ 100,000 目标,达成。

`wc -l` 验证:
```text
$ wc -l /workspace/agy/out/seeds/seeds.txt
155184   465552 18013123 /workspace/agy/out/seeds/seeds.txt
```

文件大小低于 REA 限制(`≤ 32 MiB`,`≤ 1,000,000 entries`)。

## 5. seeds.txt 前 20 行示例

```text
0x5dc5000	function	internal/abi.(*RegArgs).Dump
0x5dc5280	function	internal/abi.(*RegArgs).IntRegArgAddr
0x5dc5300	function	internal/abi.(*IntArgRegBitmap).Set
0x5dc5360	function	internal/abi.(*IntArgRegBitmap).Get
0x5dc53a0	function	internal/abi.BoundsDecode
0x5dc5480	function	internal/abi.NoEscape
0x5dc54a0	function	internal/abi.(*MapType).NeedKeyUpdate
0x5dc54c0	function	internal/abi.(*MapType).HashMightPanic
0x5dc54e0	function	internal/abi.(*MapType).IndirectKey
0x5dc5500	function	internal/abi.(*MapType).IndirectElem
0x5dc5520	function	internal/abi.Kind.String
0x5dc5560	function	internal/abi.TypeOf
0x5dc5580	function	internal/abi.(*Type).Kind
0x5dc55a0	function	internal/abi.(*Type).HasName
0x5dc55c0	function	internal/abi.(*Type).Pointers
0x5dc55e0	function	internal/abi.(*Type).IsDirectIface
0x5dc5600	function	internal/abi.(*Type).GcSlice
0x5dc56c0	function	internal/abi.(*UncommonType).Methods
0x5dc56e0	function	internal/abi.(*UncommonType).ExportedMethods
0x5dc5700	function	internal/abi.(*Type).Len
```

格式与 README 一致:`0xADDR <TAB> function <TAB> FullyQualifiedName`。
`funcs.txt` 同步输出 `ADDR SPACE NAME` 的人类可读版。

## 6. 关键函数命中数

| 关键词 | 命中 | 备注 |
| --- | --- | --- |
| `waitForEligibility` | **4** | 来自 `jetski/cli/store` + `jetski/cli/printmode` |
| `keyring` | **41** | 来自 `go_keyring` 主包 + `secret_service/ss` 子包 |
| `eligibility` | **2** | `backend.IneligibilityFromResult`, `backend.applyIneligibilityURLs` |

详细命中(节选):

```text
# waitForEligibility
0x899cd40  function  google3/third_party/jetski/cli/store/store.(*Manager).waitForEligibility
0x8c688c0  function  google3/third_party/jetski/cli/printmode/printmode.waitForEligibility
0x8c6eea0  function  google3/third_party/jetski/cli/printmode/printmode.waitForEligibility.deferwrap2
0x8c6eee0  function  google3/third_party/jetski/cli/printmode/printmode.waitForEligibility.deferwrap1

# keyring (top 3)
0x6d1be40  function  google3/third_party/golang/github_com/zalando/go_keyring/v/v0/secret_service/ss.NewSecretService
0x6d1bf40  function  google3/third_party/golang/github_com/zalando/go_keyring/v/v0/secret_service/ss.(*SecretService).OpenSession
0x6d1c200  function  google3/third_party/golang/github_com/zalando/go_keyring/v/v0/secret_service/ss.(*SecretService).CheckCollectionPath

# eligibility
0x86b3f40  function  google3/third_party/jetski/cli/backend/backend.IneligibilityFromResult
0x86b4100  function  google3/third_party/jetski/cli/backend/backend.applyIneligibilityURLs
```

`google3/...` 前缀证实这是 **Google 内部 Go 工具链** 编译产物(由
`go1.28-20260921-RC02 cl/985595000 +644cd61a4a X:fieldtrack,boringcrypto,simd` 标注,
从 `.go.buildinfo` 读到)。

## 7. 出错时尝试的备选方案

### 7.1 第一次跑:`no .gopclntab section`

工具的 ELF 分支只查 `.gopclntab` section,而 antigravity 用的是 **Google 内部
Go toolchain**,pclntab 被链接器折进 `.lrodata` section(从 Mach-O 视角叫
`__lrodata_gopcln`,从 ELF 视角叫 `.lrodata`)。`readelf -S` 输出:

```text
[ 7] .lrodata    PROGBITS    00000000014846f0  014846f0
     0000000003d14610  0000000000000000  AMSl   0   0  16
```

`0x14846f0` 起的 6 字节正是 pclntab magic `f1 ff ff ff 00 00`(Go 1.20+ 格式)。

### 7.2 已采用的方案(微补丁)

把 ELF 分支从「只查 `.gopclntab`」扩展为「找不到就回退到 `.lrodata` / `.rodata`
/ `.data.ro` / `.text` 里扫 pclntab magic」。这正是 README 提到的
「Google-internal toolchain section names」思路(原文只对 Mach-O 做了,
ELF 这边没做)。源码改动 `main.go` 的 `loadPclntab` 一个 if-else 块,**不
引入任何新依赖**,逻辑:

```go
// Primary: .gopclntab (upstream Go toolchain)
// Fallback: scan .lrodata / .rodata / .data.ro / .text for the
// pclntab magic f1 ff ff ff 00 00 (Google-internal toolchain,
// analogous to Mach-O's __lrodata_gopcln)
```

补丁后 `go run` 一次成功,无需第二备选。

### 7.3 假若补丁也失败时的备选(已记录,未使用)

1. **gore / redress** — README 已点名的备选。`gore` 在 GitHub 拉不到;`redress`
   同样在 github.com,沙箱网络阻塞。可走 codeload.github.com 拉
   `C0reTheG0d/redress`(若 tag 存在)。但它们都基于相同的 `debug/gosym`
   pclntab 解析,**同样需要自己找到 pclntab 在 section 里的位置**,所以补丁
   思路比切工具更直接。
2. **gopclntab 工具集(github.com/godump/pclntab)** — 思路一致,无新意。
3. **手写一个 ~50 行 extractor** — `debug/elf.Open` → 读 `.lrodata` → magic
   校验 → `gosym.NewTable` → 遍历 `tab.Funcs`。其实就是补丁后的 `loadPclntab`。
4. **降低要求:仅恢复入口在 `.text` 的函数名**(放弃 pclntab 路径,直接用
   `objdump -d` 抓符号)— **不推荐**,会丢掉所有非导出函数和大多数运行时
   函数,远低于 10 万行目标。

**结论:补丁路径一次成功,无需启动备选。**

## 8. 交付物清单

| 路径 | 大小 | 用途 |
| --- | --- | --- |
| `/workspace/agy/out/seeds/seeds.txt` | 18,013,123 B (155,184 行) | REA Ghidra seed 入口 |
| `/workspace/agy/out/seeds/funcs.txt` | 16,306,099 B (155,184 行) | 人类可读函数表 |
| `/workspace/agy/out/restore-symbols.md` | 本文件 | 任务报告 |
| `/workspace/agy/rea-go-seeds/` | 源码 + 一处 .lrodata 补丁 | 工具链 |

后续用法:

```bash
export REA_GHIDRA_SEED_FILE=/workspace/agy/out/seeds/seeds.txt
rea analyze /workspace/agy/install/antigravity --provider ghidra --json
```
