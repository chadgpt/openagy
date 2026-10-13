#!/usr/bin/env python3
"""Resolve Ghidra UNK_ rodata references in decompiled .c files back to strings.

For this Mach-O target the mapping is exact: file_offset = vaddr - 0x100000000.
Ghidra emits unresolved string references as `&UNK_<hex>,<length>`.

Usage:
    resolve_strings.py <agy-binary> <dec-dir> [--max N]
"""
import os
import re
import sys

BIN, DEC = sys.argv[1], sys.argv[2]
LIMIT = int(sys.argv[sys.argv.index("--max") + 1]) if "--max" in sys.argv else 40
IMAGE_BASE = 0x100000000
# Ghidra emits `&UNK_<vaddr>,<byte-length>` — the length is authoritative. Go's linker
# concatenates every short string into one blob, so reading to the next NUL over-reads
# into neighbouring strings and returns garbage.
REF = re.compile(r"&UNK_([0-9a-fA-F]{6,})\s*,\s*(0x[0-9a-fA-F]+|\d+)")

blob = open(BIN, "rb").read()

seen, rows = set(), []
for fn in sorted(os.listdir(DEC)):
    if not fn.endswith(".c"):
        continue
    text = open(os.path.join(DEC, fn), errors="ignore").read()
    src = next((l[11:].strip() for l in text.splitlines()
                if l.startswith("// Source: ")), fn)
    for m in REF.finditer(text):
        addr, length = int(m.group(1), 16), int(m.group(2), 0)
        off = addr - IMAGE_BASE
        if off < 0 or off + length > len(blob) or length == 0 or length > 300:
            continue
        try:
            s = blob[off:off + length].decode("utf-8")
        except UnicodeDecodeError:
            continue
        if not s.strip():
            continue
        key = (s, src.split()[0] if src else fn)
        if key in seen:
            continue
        seen.add(key)
        rows.append((addr, length, src, s))

rows.sort()
for addr, n, src, s in rows[:LIMIT]:
    print(f"0x{addr:x} [{n}] {src}\n    {s!r}")

print(f"\n# {len(rows)} unique string references resolved from "
      f"{len([f for f in os.listdir(DEC) if f.endswith('.c')])} decompiled files",
      file=sys.stderr)
