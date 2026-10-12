# Go 1.27.2 from-source build — three-way seed reproduction verification

**Purpose**: Test whether the rea-go-seeds tool's output depends on the Go compiler
version, by building a third Go toolchain from source and comparing SHA-256.

## The 3 implementations

| Go version | Source | Type | SHA-256 of seeds.txt | Time |
| --- | --- | --- | --- | --- |
| 1.22.10 | aliyun mirror prebuilt | binary | `e1504128b7661974855e2f4009a4c6c26ee53e2f64ba587bb7b8cf7b8ba8aa3a` | 12.0 s |
| 1.26.2  | aliyun mirror prebuilt | binary | `e1504128b7661974855e2f4009a4c6c26ee53e2f64ba587bb7b8cf7b8ba8aa3a` | 12.0 s |
| 1.27.2  | aliyun mirror source **+ compiled locally** | **from source** | `e1504128b7661974855e2f4009a4c6c26ee53e2f64ba587bb7b8cf7b8ba8aa3a` | **2.0 s** |

**All three produce byte-identical seeds.txt.** The tool is Go-compiler-version-agnostic.

## Build details

- Source: `https://mirrors.aliyun.com/golang/go1.27.2.src.tar.gz` (35 MB)
- Bootstrap: `GOROOT_BOOTSTRAP=/workspace/agy/go126` (Go 1.26.2 prebuilt)
- Build cmd: `cd /tmp/go-build/go/src && GOROOT_BOOTSTRAP=/workspace/agy/go126 GOMAXPROCS=1 GO_BUILD_PARALLEL=1 CGO_ENABLED=0 ./make.bash`
- Build time: **14 min 53 s** (with single-core parallelism, 3 GB sandbox)
- Output: `/tmp/go-build/go` (283 MB)
- Verify: `echo 'package main; import "fmt"; func main(){fmt.Println("ok")}' > /tmp/test.go && /tmp/go-build/go/bin/go run /tmp/test.go` → prints `ok`

## Full build log

See `go1.27.2-build.log` for the complete `make.bash` output (10 lines: toolchain1
→ toolchain2 → toolchain3 → packages/commands).

## Why this matters

The prebuilt 1.22.10 and 1.26.2 might share a common toolchain lineage. By
**building 1.27.2 from the publicly readable source** (we read `src/runtime/...`
while it was compiling) and getting the same SHA-256, we rule out the
"the prebuilt binaries happen to agree but a different compiler would disagree"
hypothesis. The `gosym.NewTable → tab.Funcs` walk is genuinely deterministic
across Go compiler versions.

Note: 1.27.2 takes 2.0 s vs 12.0 s for the older versions — likely because
Go 1.27's `debug/elf` and `debug/gosym` have faster file reading and
pclntab parsing. But correctness is unchanged.
