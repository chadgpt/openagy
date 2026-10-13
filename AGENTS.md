# AGENTS.md

## What this repository is

This is **not an application**. It is a reverse-engineering research workspace with two
things in it:

| Path | What it is |
|---|---|
| `rea-go-seeds/` | A vendored copy of the upstream OSS project [`VallierDev/rea-go-seeds`](https://github.com/VallierDev/rea-go-seeds). One Go file (`main.go`, ~175 lines) that recovers Go function names from a stripped binary's `pclntab` and writes a REA/Ghidra seed file. Module name is `pclnseeds`, **stdlib-only, zero third-party dependencies** (a hard project constraint — see `out/two-prong-attack.md` §9). |
| `out/` | The committed evidence directory: reports, seed files, call graph, Ghidra postScripts, raw `readelf`/`strings` dumps. Everything here is a *result*, not a program. |

Three subtrees live under `out/`, and they are **not interchangeable**:

| Subtree | Target | Built on |
|---|---|---|
| `out/` top level + `out/decompile/` | Linux/ELF sandbox | Debian 12 at `/workspace/agy/`, agy ~1.0 |
| `out/local-macos/` | **this machine**, macOS/arm64 | agy **1.3.4** — the working pipeline |
| `rea-go-seeds/README.md`, `docs/TUTORIAL.md` | macOS/Mach-O walkthrough | the tutorial case |

`out/local-macos/` is the live one. Start there; `out/local-macos/FINDINGS.md` records
what the current agy build actually contains.

The target binary under study is **Antigravity CLI** (`agy`) — a closed-source Google
internal monorepo agent CLI (`google3/third_party/jetski/...`), built with Google’s
internal Go toolchain (`go1.28-20260921-RC02`, tags `fieldtrack,boringcrypto,simd`).

---

## Two different environments — the single biggest source of confusion

The committed artifacts were produced in a **Debian 12 x86-64 sandbox rooted at
`/workspace/agy/`**. This checkout lives on macOS/arm64. Two distinct targets exist:

| | macOS/arm64 case | Linux sandbox case |
|---|---|---|
| Target | `~/.local/bin/agy` | `/workspace/agy/install/antigravity` |
| Format | Mach-O arm64, 180 MB | ELF64 x86-64 PIE, 214 MB |
| pclntab section | `__lrodata_gopcln` (62.5 MB) | folded into `.lrodata` |
| `.text` start address | `0x1000011c0` (loaded at `0x100000000`) | `0x5dc5000` (PIE, no fixed base) |
| Write-ups | `rea-go-seeds/README.md`, `rea-go-seeds/docs/TUTORIAL.md` | everything in `out/` |

**Never mix addresses between the two.** A function named
`.../store.store.(*Manager).waitForEligibility` exists at `0x899cd40` in the ELF build
and at `0x10262f660` in the Mach-O build. The `.text` start address is what gets
handed to `gosym.NewLineTable`, and getting it wrong silently shifts every PC.

Everything under `out/` — except `out/local-macos/` — is hardcoded to `/workspace/agy/`.
`out/decompile/DecompilePriority.java` has 6 such references and
`out/decompile/build_reports.py` has 4. **Rewrite these constants if you run them
elsewhere**, or they will silently write to a nonexistent tree.

### Toolchain — installed and working on this machine

The macOS/arm64 pipeline has been configured and run end-to-end here; see
**`out/local-macos/FINDINGS.md`** for results and `out/local-macos/env.sh` for the
environment.

| Tool | Version | Path |
|---|---|---|
| Go | 1.27.0 | `/Users/gear/go/bin/go` |
| JDK | 21.0.12.1 (Homebrew `openjdk@21`) | `/opt/homebrew/opt/openjdk@21` |
| Ghidra | 12.1.4 | `~/tools/ghidra_12.1.4_PUBLIC` |
| rea-agents | 6.4.0 | `/opt/homebrew/bin/rea` |

`rea doctor --provider ghidra` is all-green. Node is v26.11.1 (REA needs 22/24/26+).

Four things this machine gotcha-checks, each of which cost real time:

1. **The official Ghidra zip ships no macOS decompiler.** You must build it:
   `cd ~/tools/ghidra_12.1.4_PUBLIC/support/gradle && JAVA_HOME=<jdk21> ./gradlew buildNatives`
   (~3 min) → `Ghidra/Features/Decompiler/build/os/mac_arm_64/decompile`. Without it
   `rea doctor` fails `ghidra-native_decompiler`.
2. **REA defaults Ghidra's heap to `-Xmx2G`** (`dist/ghidra/GhidraJavaLaunch.js:53`);
   override with `GHIDRA_HEADLESS_MAXMEM`. Raising it is worth doing but is **not** the
   cause of the wrapper failures — see the next section.
3. **Ghidra searches the current working directory for scripts before `-scriptPath`.** A
   stray `DecompilePriority.java` in the CWD is picked up and fails with *"Failed to find
   source bundle containing script"*. Run `analyzeHeadless` from a neutral CWD (e.g.
   `/tmp`) and keep the script in its own directory.
4. **`~/GitHub` is a symlink to `~/Documents/GitHub`.** Ghidra canonicalises paths, which
   shows up in error messages; harmless once you know.

`.crush/` is Crush runtime state (sqlite db + logs), not project content. `.crush/init` is
empty.

---

## Commands

### Go tool (`rea-go-seeds/`)

```bash
cd rea-go-seeds

# Build (verified working: exit 0, ~3 MB binary)
go build -o /tmp/pclnseeds .

# Generate seeds — writes <outdir>/seeds.txt and <outdir>/funcs.txt
go run . /path/to/stripped-binary /path/to/outdir
#   ~12 s for a 214 MB binary, no network, no dependencies

# Checks — there are NO tests and no CI in this repo
go vet ./...      # clean
gofmt -l .        # clean
```

- `go.mod` declares `go 1.26.2`, but the source is pure stdlib and **compiles fine on
  1.22.10** (proven in `out/restore-symbols.md` §2, and again with a from-source Go 1.27.2
  in `out/go-build-evidence/`). Do not “fix” the go directive — output is byte-identical
  (SHA-256 `e1504128…`) across 1.22.10 / 1.26.2 / 1.27.2-from-source. That
  reproducibility is a deliberate verified claim in this repo.
- With only one argument, output goes to the *current* directory, not next to the binary
  (the doc comment in `main.go` says otherwise — the comment is wrong, the code defaults
  `outdir = "."`).

### REA + Ghidra (historical; requires the gitignored toolchains)

```bash
npm install -g rea-agents@6.4.0        # bare install gets stale 4.0.1
export JAVA_HOME=<jdk21>
export GHIDRA_INSTALL_DIR=<ghidra_12.1.4_PUBLIC>
export REA_GHIDRA_SEED_FILE=$PWD/out/seeds.txt
rea doctor --provider ghidra --json     # must be all-green
rea analyze <binary> --provider ghidra --json
```

**`rea analyze` has a hard ~5.5-minute internal timeout** (`provider_timeout`,
`timeout_ms: 330000`) with no `--timeout` / `--max-wait` flag and no documented env var to
raise it (`out/ghidra-analyze.md` §8). On a 155K-function Go binary Ghidra needs
20–40 min, so **the REA wrapper cannot be used for full analysis**.

**Do not assume a bigger heap fixes the wrapper.** Three attempts were measured on this
machine, and none of them produced an answer:

| `GHIDRA_HEADLESS_MAXMEM` | Outcome |
|---|---|
| default `2G` | `binary_overview` failed after ~60 s with `Ghidra headless launch failed`; the bridge died and the run's **orphaned Ghidra JVM kept running for ~25 min** |
| `8G` (`rea analyze`) | ran until externally cancelled — never returned a result |
| `10G` (`rea --mcp`) | survived **621 s** (the seeds alone need ~10 min) then the MCP server exited `rc=0` without answering |

The real constraint is the wrapper's time budget versus the ~10 min that 154,525 seeds
take to apply, at any heap size. The orphan is the nastiest part: after the wrapper gives
up it leaves a JVM burning CPU and ~1.3 GB in
`/var/folders/*/T/rea-ghidra-*`. Check `pgrep -f AnalyzeHeadless` and clear it with
`/bin/kill -9 <pid>` (the shell's `kill` builtin is not available here) plus `rm -rf` on
the orphaned temp dir.

Bypass the wrapper entirely — this is the verified-working recipe:

```bash
cd /tmp                                  # neutral CWD, see gotcha 3 above
export JAVA_HOME=/opt/homebrew/opt/openjdk@21
export GHIDRA_INSTALL_DIR=~/tools/ghidra_12.1.4_PUBLIC
SEEDS=/Users/gear/GitHub/openagy/out/local-macos/seeds/seeds.txt
SCRIPTS=/Users/gear/GitHub/openagy/out/local-macos/ghidra-scripts
PROJ=/Users/gear/GitHub/openagy/out/local-macos/proj
mkdir -p "$PROJ"

# ① import + seed  (~11 min, measured)
MAXMEM=8G VMARGS="-XX:ParallelGCThreads=4 -XX:CICompilerCount=4" \
  "$GHIDRA_INSTALL_DIR/support/analyzeHeadless" "$PROJ" agy \
  -import ~/.local/bin/agy -noanalysis -max-cpu 4 \
  -scriptPath /opt/homebrew/lib/node_modules/rea-agents/bridge/ghidra \
  -preScript  ReaGhidraApplySeeds.java  "$SEEDS" \
  -postScript ReaGhidraNoReturnFix.java
# no -deleteProject: you want the project to persist for step ②

# ② decompile a hand-picked list  (56 s for 1,959 functions)
MAXMEM=8G VMARGS="-XX:ParallelGCThreads=4 -XX:CICompilerCount=4" \
  "$GHIDRA_INSTALL_DIR/support/analyzeHeadless" "$PROJ" agy \
  -process -noanalysis -max-cpu 4 \
  -scriptPath "$SCRIPTS" -postScript DecompilePriority.java
```

- **`-noanalysis` is the single most important flag.** Two separate reasons:
  1. Ghidra’s *Decompiler Switch Analyzer* decompiles every function to recover switch
     tables; on 155K Go functions that takes days.
  2. Importing with `-noanalysis` means **no disassembly pass has run when the seeds are
     applied**, so Go thunks cannot collide with instruction boundaries. The Linux/ELF
     pass in `out/` imported *with* analyzers and got **860/1498 = 57 %**, skipping 637
     functions as *"function X inside instruction at Y"*. The macOS pass got
     **2101/2101 = 100 %, 0 failures**. This is why the failure rate in `out/` is not a
     property of the binary.
- Omit `-deleteProject` on the import so step ② can `-process` the same project.
- `DecompilePriority.java` is **resume-safe**: it skips any function whose output file
  already exists and is >100 bytes, so re-running only decompiles what is new (the
  second run above took 13 s to add 142 functions).
- Heap for this machine (16 GB): `MAXMEM=8G`. The sandbox used `MAXMEM=2G` on 3 GB.

### MCP plan format

`rea-go-seeds/examples/plan-agy.jsonl` — one JSON object per line:

```json
{"label": "open", "tool": "open_binary", "args": {"path": "/abs/path", "provider_id": "ghidra"}}
{"label": "x", "tool": "procedure_pseudo_code", "args": {"procedure": "0x1028b6010"}}
```

`reamcp.py` writes each response to `./mcp/<NN>-<label>.json`, dumps the tool catalog to
`./mcp/tools.json`, and server stderr to `./mcp/server.err`.

**The addresses in the shipped `plan-agy.jsonl` are stale.** They belong to the build the
tutorial was written against; `agy` 1.3.4 shifts all of them (e.g. `waitForEligibility`
moved `0x10260fc60` → `0x10262f660`). Use `out/local-macos/build_plan.py`, which resolves
names → addresses from a fresh `seeds.txt` instead of hardcoding them:

```bash
python3 out/local-macos/build_plan.py out/local-macos/seeds/seeds.txt ~/.local/bin/agy \
  > out/local-macos/plan-local.jsonl
```

It prints any unresolved targets to stderr — that list must be empty.

---

## Architecture / data flow

```
stripped Go binary
      │
      ▼  ①  rea-go-seeds/main.go  loadPclntab()
   pclntab bytes + .text start vaddr
      │
      ▼  gosym.NewLineTable → gosym.NewTable → tab.Funcs
   155,184 {entry, name} pairs, deduped by entry, sorted by address
      │
      ├──────────────► seeds.txt   (0xADDR \t function \t NAME)   ← the commit-checked artifact
      │                funcs.txt   (ADDR SPACE NAME)
      │
      ▼  ②  REA_GhidraApplySeeds.java preScript (REA_GHIDRA_SEED_FILE)
   Ghidra program DB with ~155K named functions
      │
      ▼  ③  DecompilePriority.java postScript
   dec/<HEX>_<shortname>.c
      │
      ▼  ④  build_reports.py
   decompile-summary.md + 26 × decompile-<pkg>.md
```

A **second, independent path** produces the call graph (Subagent B in
`out/two-prong-attack.md` §4): `objdump -d` the `.text` → stream-parse `call <addr>`
instructions → bisect against `seeds.txt` addresses for function boundaries →
`call-graph.json` / `call-graph.dot` / `xrefs.txt`. This bypasses Ghidra entirely.

### Stage ① — `loadPclntab` (the only non-obvious code in the repo)

Tries container formats in order: Mach-O → ELF → PE.

- **Mach-O**: `__gopclntab`, then `__lrodata_gopcln` (Google-internal toolchain rename).
- **ELF**: `.gopclntab` first; if absent, scan `.lrodata` / `.rodata` / `.data.ro` /
  `.text` for the Go 1.20+ pclntab magic `f1 ff ff ff 00 00`. **The ELF fallback is a
  local patch**, not upstream — upstream only handled the Mach-O rename, which is why
  `gore` and `redress` find nothing here. Preserve it.
- **PE**: scan `.rdata` / `.text` for the same magic.

**The second argument to `gosym.NewLineTable` must be the `.text` start address, not the
pclntab address.** The ELF branch computes `pclnVaddr`, uses it to locate the section, then
explicitly discards it (`_ = pclnVaddr`) and passes `.text.Addr`. Passing the pclntab base
yields silently wrong PCs.

Filters applied to `tab.Funcs`: skip empty names, names containing space/tab/NUL, names
longer than 2000 chars, and duplicate entry addresses (Go emits `.deferwrap1/2`,
`func1`, thunk aliases at shared addresses).

### Stage ③ — `DecompilePriority.java`

Ghidra `GhidraScript`; **class name must match the filename**. Reads `priority-funcs.txt`
(same TSV as seeds.txt), 60 s per-function timeout, writes `dec/<HEX>_<stem>.c` where
`stem` = everything after the last `.` in the Go name, non-alphanumerics → `_`,
truncated to 80 chars.

Resume-safe: a function whose output file already exists and is `> 100` bytes is skipped,
and every line is processed independently, so a crash keeps partial progress.
`_progress.txt`, `_errors.txt`, `_summary.txt` are written alongside.

### Stage ④ — `build_reports.py`

Package split heuristic: if the name contains `(`, the package is everything **before the
first `(`** (covers `pkg.(*Type).Method`); otherwise everything before the **last `.`**
(covers `pkg.Func`). Recounts by scanning `dec/` for `.c` files and matching the hex
prefix — it does not trust `_summary.txt`.

---

## Data formats

| File | Format |
|---|---|
| `out/seeds/seeds.txt`, `out/decompile/priority-funcs.txt` | `0xADDR<TAB>function<TAB>NAME`. REA seed format: ≤ 1,000,000 entries, ≤ 32 MiB, names must contain no whitespace. Also accepts `label` / `code` kinds; this project only emits `function`. |
| `out/seeds/funcs.txt` | `ADDR NAME` — no `0x` prefix, single space. |
| `out/decompile/xrefs.txt` | `from_addr<TAB>from_name<TAB>to_addr<TAB>to_name<TAB>count`, `#` comment lines allowed. |
| `out/decompile/call-graph.json` | `{metadata{...}, nodes[{addr,name,package,in_priority}], edges[]}`. Renderable with Graphviz via `call-graph.dot`. |
| Decompiled `.c` header | `// Source: 0x<hex>  <name>` / `// Decompiled at: <date>` / `// Signature: <sig>` |
| `out/*.json` (e.g. `ghidra-analysis.json`) | Raw REA `--json` error envelopes — `{"error","code","category","retryable","remediation","details"}`. These are **failure logs**, not results. |

**Sanity check on any seed work:** the canonical output is 155,184 lines / 18,013,123 B
with SHA-256 `e1504128b7661974855e2f4009a4c6c26ee53e2f64ba587bb7b8cf7b8ba8aa3a`, recorded in
`out/seeds/SHA256`. If your run differs, something about the pclntab location changed.

---

## Gotchas

**Analysis fidelity (Go-specific, all recorded in `out/deep-analysis-v3.md`)**

- **A static call graph sees ~3 % of the real control flow.** Goroutines, channels and
  interface dispatch mean *0 static callers ≠ dead code* — usually it means
  `runtime.newproc` or a func-pointer call. `out/decompile/auth-flow.md` states this
  explicitly and reports both what disassembly shows and what the name implies.
- `out/deep-analysis-v3.md` contains a **v2→v3 correction section** that retracts earlier
  claims in `out/qa-report.md` (notably the 30 s/60 s timeout attribution and the
  usefulness of the call graph). When the two disagree, **v3 is authoritative**.
- ~1.5 % of seeds fail in Ghidra with `function X inside instruction at Y` — Go thunks
  share an address with their target and Ghidra cannot disambiguate. Those functions never
  exist in the DB, so `DecompilePriority` reports them as `SKIP no function at`. 637 of
  1,498 priority funcs skipped for this reason. **This is expected, not a script bug.**
- Timeout constants are format-string parameterized (`…did not settle within %s`), so
  `strings` will never show “30” or “60”. You have to find the immediate in the
  disassembly (`0x2faf080` = 50 ms) or read the decompiled control flow.
- Binary strings are frequently truncated mid-token (`AGY_CLI_DISABLE_AUTO_UPDATEF`, flags
  like `--approv`). Flag and env-var names recovered this way are inferred, not exact.

**Tooling**

- Ghidra’s `search_strings` only indexes NUL-terminated `Data`; most Go strings are
  absent. Use `strings(1)` on the binary for anything string-shaped and cross-reference.
  This is why `out/urls-google.txt`, `out/models-gemini.txt`, `out/grpc-paths.txt`,
  `out/gopclntab-strings.txt` exist alongside the REA JSON.
- Ghidra sometimes resolves rodata string addresses to a blob of neighbouring data in the
  decompiler window. Read the file manually at that offset. For the Mach-O target
  `addr − 0x100000000` = file offset holds exactly.
  **Slice by the emitted length, not to the next NUL.** Ghidra writes `&UNK_<vaddr>,<len>`
  and Go's linker concatenates every short string into one blob, so reading to a NUL
  returns the neighbouring strings as garbage — see `out/local-macos/resolve_strings.py`.
- Only *short* literals reach the decompiler this way. Long user-facing strings reach the
  code through Go's `concatstring` call path and never appear as `UNK_` refs; `strings(1)`
  is the tool for those. **Cross-check both** — a finding from one that the other does not
  confirm is weak.
- REA’s own `search_strings` missing a string does not mean the string is absent.
- `inspect-go-binary` is documented upstream but **not shipped in npm 6.4.0** (main-branch
  only). Read docs against the installed version, not the website.
- Ghidra official zips ship **no macOS native decompiler**. You must build it:
  `cd $GHIDRA/support/gradle && JAVA_HOME=<jdk21> ./gradlew buildNatives` (~100 s) →
  `Ghidra/Features/Decompiler/build/os/mac_arm_64/decompile`.
- REA supports only Node 22.x (≥22.19) / 24.x (≥24.11) / 26+. Node 25.x makes
  `rea doctor` report `missing_dependency` even though the CLI runs.
- `observe-native-calls` sets breakpoints **by symbol name**, so it is useless on a
  stripped Go binary unless you re-symbolize first.

**Environment (sandbox-specific, from `out/prep-env.md`)**

- `github.com` is network-blocked there; `codeload.github.com/<owner>/<repo>/tar.gz/main`
  works. Mirrors that did work: `mirrors.aliyun.com/golang`, `mirrors.tuna…/Adoptium`,
  `registry.npmmirror.com`. Tuna has no `/golang/`; Huawei's `/golang/` returns 401;
  Aliyun has no `/Adoptium/`.
- A 30 s bash timeout truncated both `npm install -g` and the Go tarball extraction on
  first attempt (Go lost 65 of 72 stdlib packages, breaking every later `go run`).
  Extract to `/tmp` (tmpfs) first, then `cp -a` to the NAS mount, and
  `chmod -R a+rX` afterwards.
- Keep `<tool>/<tool>-<version>/*` flattened into `<tool>/` root. A `current` symlink
  breaks the expected contract paths.

---

## Conventions

- **Zero third-party dependencies** is a stated constraint (`out/two-prong-attack.md` §9).
  Go: stdlib only. `build_reports.py`: stdlib only. Java: Ghidra API only.
- **Evidence grading** used throughout the reports — keep it when adding findings:
  【一手】first-hand verified against the binary · 【反编译】from decompiled output at a
  confirmed address · 【strings】string-table hit only · 【推测】hypothesis.
- **Report language follows the file being edited**: `out/*.md` is zh-CN;
  `out/decompile/*.md`, `out/go-build-evidence/*` and `rea-go-seeds/README.md` are English.
  Mixed-language commits are normal here.
- `out/` reports end with a 硬约束 / 存疑 / limitations section enumerating what was
  *not* verified. New reports follow that structure — do not omit it.
- Go style: tabs, standard library naming, `error` strings lowercase. Single-file
  `main` package, no internal packages.

---

## Where to start

**On this machine, start here** — the macOS pipeline is already configured and has been
run end to end:

| If you want to… | Read / run |
|---|---|
| See what was found in *your* agy build | `out/local-macos/FINDINGS.md` |
| Set the environment | `source out/local-macos/env.sh` |
| Re-derive the 154,525 names | `cd rea-go-seeds && go run . ~/.local/bin/agy ../out/local-macos/seeds` |
| Change which functions get decompiled | edit `PACKAGES` in `out/local-macos/build_priority.py`, re-run it, then re-run `analyzeHeadless -process` (incremental, ~13 s) |
| Rebuild the MCP query plan for a new agy | `out/local-macos/build_plan.py` (addresses shift on every release) |
| Watch a run | `tmux new-session -d -s reagy -c /tmp` then paste the ①/② `analyzeHeadless` block from **Commands** above. Do **not** use `run-re.sh` — it drives the REA MCP path, which does not complete on this binary (see the wrapper table). |

**Historical / reference material:**

| If you want to… | Read |
|---|---|
| Understand the tool | `rea-go-seeds/README.md`, then `main.go` (175 lines, the whole thing) |
| Understand the full RE story | `rea-go-seeds/docs/TUTORIAL.md` (zh-CN, macOS/Mach-O case) |
| Understand the Linux/ELF pipeline | `out/restore-symbols.md` → `out/ghidra-analyze.md` → `out/decompile/deliverable.md` |
| Understand the analysis methods and their limits | `out/deep-analysis-v3.md` (read the corrections section), `out/decompile/auth-flow.md` |
| See what was concluded on the ELF build | `out/qa-report.md` (zh-CN, superseded on some points), `out/decompile/decompile-summary.md` |
| Write a new Ghidra script | `out/local-macos/ghidra-scripts/DecompilePriority.java` |
| Drive REA programmatically | `rea-go-seeds/examples/reamcp.py` + a plan from `build_plan.py` |
