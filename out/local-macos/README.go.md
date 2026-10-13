# Reconstructed Go module — `google3/third_party/jetski`

This module was **generated**, not recovered. It is a structural reconstruction of the
Go package tree that ships inside the stripped `agy` binary, built from the function names
recovered out of the binary's `pclntab`.

```
361 packages · 37,832 declarations · go build ./... clean · go vet ./... clean
```

## What is real and what is not

Read this before trusting anything in here.

| Recovered faithfully | Not recoverable |
|---|---|
| Import path of every function | Parameter types and parameter names |
| Package membership | Return types |
| Method receiver type | Function bodies |
| Pointer vs value receiver | Struct fields |
| Declared name | Interface satisfaction (except two, see below) |
| Exported vs unexported | Constants, variables, types with no methods |
| Virtual address of each symbol | The original source layout, comments, build tags |

A stripped Go binary keeps `pclntab` — the panic/stack-unwind table — and that table
holds exactly one thing per function: an entry address and a name. Everything else that
would make this a real build is gone. This module is therefore an accurate **map of the
API surface**, not an implementation.

Every declaration carries the virtual address it occupied in the original binary:

```go
// waitForEligibility was at 0x10262f660 in the original binary.
func (m *Manager) waitForEligibility() {
	panic("agentrecon: not reconstructed")
}
```

That address is the useful part: it points at the real code in `~/.local/bin/agy`, and for
2,101 of these functions it also names a decompiled pseudocode file in `../dec/`.

## Two exceptions to "not recoverable"

`MarshalJSON` and `UnmarshalJSON` are declared with their real signatures
(`() ([]byte, error)` and `([]byte) error`), because those signatures are fixed by
`encoding/json` rather than by the author. This is also what keeps `go vet`'s
`stdmethods` check clean.

## Layout

The directory tree mirrors the import paths recovered from the binary, so
`google3/third_party/jetski/cli/store/store` became `cli/store/store/`, and so on. That is
the internal Google monorepo layout, which is not something you will find on any public
go.dev.

```
cli/store/store/api_generated.go     package store — recovered functions and methods
cli/backend/backend/api_generated.go package backend
...
symbols.tsv                         flat index: addr, import path, kind, receiver, name
cmd/symsearch/                      search CLI over symbols.tsv
```

## Searching

```bash
# by name, across every field
go run ./cmd/symsearch waitForEligibility

# reverse lookup: address -> package and function
go run ./cmd/symsearch -addr 0x10262f660

# narrow by import path
go run ./cmd/symsearch -pkg cli/backend/auth

# only exported declarations
go run ./cmd/symsearch -pkg cli/store -exported OAuth
```

`symbols.tsv` is plain TSV, so `grep`/`awk` work on it too:

```bash
grep -i eligibility symbols.tsv
awk -F'\t' '$2 ~ /cli\/store/ && $4 != ""' symbols.tsv | head
```

## Regenerating

This directory is disposable. Everything in it comes from one command:

```bash
../rebuild-gosrc.sh
```

That regenerates from `../seeds/seeds.txt`, runs `gofmt -w`, and fails the run unless both
`go build ./...` and `go vet ./...` pass. The output is byte-for-byte reproducible.

## How the names were parsed

`../gen_gosrc.py` handles the shapes Go's linker emits. The parts that took real work:

- **`pkg.(*T).M` and `pkg.(T).M`** — explicit receivers. This is the only shape that gives
  positive evidence that `T` is a type.
- **`pkg.T.M`** — the same information without the receiver, used for methods on generic
  types and protobuf's `T.Descriptor` helpers. Ambiguous: `pkg.T.M` could equally be a
  function literally named `T.M`. It is only accepted when `T` was already confirmed as a
  receiver, because otherwise the generator invents types that collide with real
  declarations (`profiling.Record` is a function, not a type).
- **`pkg.T.M` vs `func (m T) M`** — Go forbids declaring both on one type, so a pointer
  receiver always wins; it covers both call sites.
- **Compiler-generated symbols, dropped:** `-fm` (method value), `-rangeN` (the
  range-over-func wrapper Go 1.23+ emits), `.funcN` / `.gowrapN` / `.deferwrapN` (closures
  and thunks), `init.N` (one synthetic initialiser per package-level variable),
  `[go.shape.…]` generic instantiations (folded to the bare declaration), and
  `…..embed.1.0.…` — a second copy of the symbol table the linker embeds for reflection.

## Provenance

- Binary: `~/.local/bin/agy`, agy 1.3.4, Mach-O arm64, SHA-256
  `9da414c0624c27aa2969a86030a070b5341c0657700512eba70b21725ce253f5`
- Toolchain: `go1.28-20260921-RC02` (Google internal, tags `fieldtrack,boringcrypto,simd`)
- Symbol source: 154,525 entries in `../seeds/seeds.txt`; 41,739 in this module's scope
- Findings and their evidence grading: `../FINDINGS.md`