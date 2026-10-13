#!/usr/bin/env python3
"""Reconstruct a compilable Go module skeleton from a pclntab symbol list.

What survives in a stripped Go binary and is therefore recovered here:
  - the import path of every function
  - the package it belongs to
  - for methods, the receiver type and whether the receiver is a pointer
  - the function name, and whether it is exported

What does NOT survive, and is therefore stubbed:
  - parameter types, parameter names, return types
  - all function bodies
  - struct fields, interface method sets on non-receiver types, constants, variables

The output is a real `go build`-clean module: it mirrors the internal repository
layout, declares every recovered symbol with a correct receiver, and carries the
original address in a doc comment so any declaration can be traced back to the
binary (and to its decompiled pseudocode in ../../dec/).

Usage:
    gen_gosrc.py <seeds.txt> <outdir> [--prefix google3/third_party/jetski]
"""
import os
import re
import sys
from collections import defaultdict

SEEDS, OUT = sys.argv[1], sys.argv[2]
PREFIX = sys.argv[sys.argv.index("--prefix") + 1] if "--prefix" in sys.argv \
    else "google3/third_party/jetski"

# Synthetic symbols the compiler emits, which are not declarations:
#   init.N        one synthetic initialiser per package-level variable
#   .funcN/.gowrapN/.deferwrapN   closures and wrapper thunks
#   -fm           method value
#   -rangeN       the range-over-func wrapper Go 1.23+ emits for `range` over an iterator
DROP_RE = re.compile(
    r"(init\.\d+|\.func\d+|\.gowrap\d+|\.deferwrap\d+|-fm|-range\d+)$"
)
# Generic instantiations: keep the bare declaration, drop the type argument.
GENERIC = re.compile(r"\[go\.shape[^\]]*\]$")
# Method values and some wrappers carry an argument-word suffix after a dash.
DASH_TAIL = re.compile(r"-fm$")
# The linker embeds a second copy of the symbol table for reflection/plugin use,
# under names like `internal/abi..embed.1.0.internal/abi.(*Type).Align`. Those are
# mirrors of symbols that already exist, not distinct declarations.
EMBED = re.compile(r"\.\.embed\.\d+\.\d+\.")
RECEIVER = re.compile(r"\((?P<star>\*?)(?P<type>[A-Za-z_][A-Za-z0-9_]*)\)\.(?P<name>[^.()\[\]]+)$")
IDENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
KEYWORDS = {
    "break", "case", "chan", "const", "continue", "default", "defer", "else",
    "fallthrough", "for", "func", "go", "goto", "if", "import", "interface",
    "map", "package", "range", "return", "select", "struct", "switch", "type",
    "var",
}


def parse_explicit(symbol: str):
    """Parse only the `pkg.(*T).M` / `pkg.(T).M` shape.

    Returns (pkg, "method", T, is_ptr, M) or None. This is the only shape that
    gives positive evidence that T is a type.
    """
    name = GENERIC.sub("", symbol)
    m = RECEIVER.search(name)
    if not m:
        return None
    pkg = name[: m.start()].rstrip(".")
    if not re.fullmatch(r"[A-Za-z0-9_/\-]+", pkg):
        return None
    return pkg, "method", m["type"], bool(m["star"]), m["name"]


def parse_implicit(symbol: str, known_types):
    """Parse `pkg.Func` and `pkg.Type.M`.

    `pkg.Type.M` is ambiguous — the same text can be a function literally named
    `Type.M`, or a method on `Type`. It is only accepted when `Type` was already
    confirmed as a receiver by parse_explicit; otherwise declaring it would
    invent a type that collides with real declarations.
    """
    name = GENERIC.sub("", symbol)

    slash = name.rfind("/")
    dot = name.find(".", slash + 1)
    if dot <= slash + 1:
        return None
    pkg = name[:dot].rstrip(".")
    if not re.fullmatch(r"[A-Za-z0-9_/\-]+", pkg):
        return None
    base = name[dot + 1 :]

    if "." in base:
        rtype, _, mname = base.rpartition(".")
        if rtype in known_types and accept(mname):
            return pkg, "method", rtype, False, mname
        return None
    return pkg, "func", None, False, base


def synthetic(symbol: str) -> bool:
    """True when the whole symbol is compiler-generated.

    This must be matched against the FULL symbol, not the trailing identifier:
    `profiling.Record.deferwrap1` is a defer wrapper, but its bare name
    `deferwrap1` does not match a `.`-anchored pattern.
    """
    return bool(DROP_RE.search(GENERIC.sub("", symbol)))


def accept(name: str) -> bool:
    """True when `name` is usable as a Go identifier."""
    if not name or not IDENT.match(name):
        return False
    if name in KEYWORDS:
        return False
    if DROP_RE.search(name) or DASH_TAIL.search(name):
        return False
    return True


# A handful of method signatures are fixed by standard-library interfaces, so they
# are known even though parameter types generally are not. Supplying them keeps
# `go vet`'s stdmethods check clean and makes the stubs actually satisfy the
# interface they claim to implement.
STANDARD_SIGNATURES = {
    "MarshalJSON":   "() ([]byte, error)",
    "UnmarshalJSON": "([]byte) error",
}


def signature_for(mname: str) -> str:
    return STANDARD_SIGNATURES.get(mname, "()")


def main():
    os.makedirs(OUT, exist_ok=True)
    total_in_scope = skipped = 0

    # Pass 1 — every symbol in scope, with explicit receivers resolved.
    records = []
    for line in open(SEEDS):
        parts = line.rstrip("\n").split("\t")
        if len(parts) != 3 or parts[1] != "function":
            continue
        addr, symbol = parts[0], parts[2]
        if EMBED.search(symbol) or synthetic(symbol):
            continue
        if not symbol.startswith(PREFIX + "/"):
            continue
        total_in_scope += 1
        records.append((addr, symbol))

    # Pass 2 — the set of names we have positive evidence are types.
    known_types = set()
    for _, symbol in records:
        e = parse_explicit(symbol)
        if e and accept(e[4]):
            known_types.add(e[2])

    # Pass 3 — classify and collect.
    pkgs = defaultdict(lambda: {"funcs": set(), "methods": {}})
    addresses = {}
    for addr, symbol in records:
        parsed = parse_explicit(symbol) or parse_implicit(symbol, known_types)
        if not parsed:
            skipped += 1
            continue
        pkg, kind, rtype, rptr, base = parsed
        if not accept(base) or (kind == "method" and not accept(rtype)):
            skipped += 1
            continue

        slot = pkgs[pkg]
        if kind == "method":
            # Go forbids declaring both `func (t T) M()` and `func (t *T) M()`.
            # Pointer form wins: a `*T` receiver covers calls through `*T` and the
            # method set of `T`, so it is the superset.
            prev = slot["methods"].get((rtype, base))
            if prev is None or (prev is False and rptr):
                slot["methods"][(rtype, base)] = rptr
        else:
            slot["funcs"].add(base)

        key = (pkg, kind, rtype, base)
        if key not in addresses or addr < addresses[key]:
            addresses[key] = addr

    written = 0
    for pkg, slot in sorted(pkgs.items()):
        rel = pkg[len(PREFIX) + 1 :] or "root"
        d = os.path.join(OUT, rel)
        os.makedirs(d, exist_ok=True)
        pname = os.path.basename(rel).split(".")[-1] or "pkg"
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", pname):
            pname = "pkg"

        lines = [
            "// Code generated by gen_gosrc.py. DO NOT EDIT.",
            "//",
            f"// Reconstructed from the pclntab of the agy binary: {len(slot['funcs'])} functions",
            f"// and {len(slot['methods'])} methods were recovered for this package.",
            "//",
            "// Every declaration below is a STUB. Signatures beyond the receiver type and",
            "// the name are not recoverable from a stripped Go binary, and no body is.",
            "// Each stub's doc comment carries the original virtual address so the real",
            "// implementation can be looked up in Ghidra (or in ../../../dec/*.c when the",
            "// function was decompiled).",
            "",
            f"package {pname}",
            "",
        ]

        def addr_of(kind, rtype, base):
            return addresses.get((pkg, kind, rtype, base), "?")

        # Every receiver type referenced by this package must be declared, or the
        # methods on it will not compile. Fields are not recoverable; these exist
        # only to carry the method set.
        recvs = sorted({rtype for rtype, _ in slot["methods"]})
        if recvs:
            lines.append("// Receiver types referenced by this package. Struct fields are not")
            lines.append("// recoverable from a stripped binary, so these are empty.")
            lines.append("")
            for rtype in recvs:
                lines.append(f"type {rtype} struct{{}}")
                lines.append("")

        if slot["funcs"]:
            lines.append("// Package-level functions.")
            lines.append("")
            for fn in sorted(slot["funcs"]):
                lines.append(f"// {fn} was at {addr_of('func', None, fn)} in the original binary.")
                lines.append(f"func {fn}() {{ panic(\"agentrecon: not reconstructed\") }}")
                lines.append("")

        for (rtype, mname), rptr in sorted(slot["methods"].items()):
            recv = f"(m *{rtype})" if rptr else f"(m {rtype})"
            lines.append(
                f"// {rtype}.{mname} was at {addr_of('method', rtype, mname)} "
                "in the original binary."
            )
            body = 'panic("agentrecon: not reconstructed")'
            sig = signature_for(mname)
            lines.append(f"func {recv} {mname}{sig} {{ {body} }}")
            lines.append("")

        with open(os.path.join(d, "api_generated.go"), "w") as f:
            f.write("\n".join(lines))
        written += 1

    # A flat, greppable index: address, import path, kind, receiver, name.
    # This is the artefact to use when you want to go from a string you found in the
    # binary back to the code that references it.
    index = os.path.join(OUT, "symbols.tsv")
    with open(index, "w") as f:
        f.write("# addr\timport_path\tkind\treceiver\tname\n")
        rows = []
        for (pkg, kind, rtype, base), addr in addresses.items():
            recv = ("*" if rtype and kind == "method" else "") or ""
            rows.append((addr, pkg, kind, f"{recv}{rtype or ''}", base))
        for addr, pkg, kind, recv, base in sorted(rows):
            f.write(f"{addr}\t{pkg}\t{kind}\t{recv}\t{base}\n")

    print(f"packages: {written}")
    print(f"declarations: {len(addresses)}")
    print(f"symbols in scope: {total_in_scope}")
    print(f"dropped (compiler-generated/keywords): {skipped}")
    print(f"outdir: {OUT}")


if __name__ == "__main__":
    main()