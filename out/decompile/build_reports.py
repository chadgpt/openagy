#!/usr/bin/env python3
"""Build decompile report markdown from per-function .c files and priority-funcs.txt.

Output:
  - decompile-summary.md  (top-level)
  - decompile-<pkg>.md    (one per Go package)
"""
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

PRIORITY_FILE = "/workspace/agy/out/decompile/priority-funcs.txt"
DEC_DIR = "/workspace/agy/out/decompile/dec"
OUT_DIR = "/workspace/agy/out/decompile"

def package_of(name: str) -> str:
    """Derive Go package path from a fully-qualified function name.

    e.g. "google3/third_party/jetski/cli/store.(*Manager).Start" -> "google3/third_party/jetski/cli/store"
         "google3/third_party/jetski/cli/store.Start" -> "google3/third_party/jetski/cli/store"
         "internal/abi.BoundsDecode" -> "internal/abi"
    """
    # Remove the function name (last segment after final dot)
    # but preserve the receiver (*Manager), so the package is everything
    # up to the last "." where what follows is a method (uppercase) or
    # everything up to the first "(" for types.
    # Heuristic: take everything up to the last "." for a func name, or
    # everything up to "." after the last "/" segment for a method.
    if "(" in name:
        # type.Method style: e.g. pkg/path.(*Type).Method
        # Find the last ")" to locate the method name
        ridx = name.rfind(")")
        if ridx > 0 and ridx < len(name) - 1 and name[ridx+1] == ".":
            # type.Method - method is after the ")"
            method = name[ridx+2:]
            # package is everything up to the first "("
            pidx = name.find("(")
            return name[:pidx]
        # else fallback: take everything up to "."
        return name.rsplit(".", 1)[0]
    else:
        # package.Func style
        return name.rsplit(".", 1)[0]

def main():
    priority = []
    with open(PRIORITY_FILE) as f:
        for ln in f:
            ln = ln.strip()
            if not ln or ln.startswith("#"):
                continue
            parts = ln.split("\t")
            if len(parts) < 3:
                continue
            addr, kind, name = parts[0], parts[1], parts[2]
            if kind != "function":
                continue
            hex_addr = addr[2:] if addr.startswith("0x") else addr
            pkg = package_of(name)
            short = name.rsplit(".", 1)[-1] if "." in name else name
            priority.append((hex_addr, name, pkg, short))

    by_pkg = defaultdict(list)
    for hex_addr, name, pkg, short in priority:
        by_pkg[pkg].append((hex_addr, name, short))

    # Find all .c files actually produced
    dec_files = {}
    if os.path.isdir(DEC_DIR):
        for fn in os.listdir(DEC_DIR):
            if not fn.endswith(".c"):
                continue
            # format: HEX_SHORT.c
            base = fn[:-2]  # remove .c
            # HEX may have _ in it (just hex chars actually)
            # find first _ separating hex from short
            idx = base.find("_")
            if idx < 0:
                continue
            hex_addr = base[:idx]
            dec_files[hex_addr] = fn

    # Build summary
    total_funcs = len(priority)
    decompiled = sum(1 for h, *_ in priority if h in dec_files)
    errors = sum(1 for h, *_ in priority if h not in dec_files)
    
    pkg_summary = []
    total_loc = 0
    for pkg, fns in sorted(by_pkg.items()):
        pkg_dec = sum(1 for h, *_ in fns if h in dec_files)
        pkg_loc = 0
        for h, name, short in fns:
            if h in dec_files:
                fp = os.path.join(DEC_DIR, dec_files[h])
                with open(fp, 'r', errors='ignore') as f:
                    content = f.read()
                pkg_loc += content.count('\n')
                total_loc += content.count('\n')
        pkg_summary.append((pkg, len(fns), pkg_dec, pkg_loc))

    # Build top-level summary
    with open(os.path.join(OUT_DIR, "decompile-summary.md"), "w") as f:
        f.write(f"# Decompile summary — antigravity (Go 1.28-20260921-RC02)\n\n")
        f.write(f"> Source: `/workspace/agy/install/antigravity` (214 MB ELF64 x86-64 PIE stripped)\n")
        f.write(f"> Decompiler: Ghidra 12.1.4 (DecompInterface, 60s/func timeout)\n")
        f.write(f"> Priority list: `{PRIORITY_FILE}` ({total_funcs} funcs across {len(by_pkg)} Go packages)\n")
        f.write(f"> Decompiled output: `{DEC_DIR}/<HEX>_<safename>.c`\n\n")
        f.write(f"## Headline numbers\n\n")
        f.write(f"| Metric | Value |\n|---|---|\n")
        f.write(f"| Total priority funcs | {total_funcs} |\n")
        f.write(f"| Decompiled OK | {decompiled} ({decompiled*100//max(total_funcs,1)}%) |\n")
        f.write(f"| Skipped/errored | {errors} ({errors*100//max(total_funcs,1)}%) |\n")
        f.write(f"| Go packages covered | {len(by_pkg)} |\n")
        f.write(f"| Total decompiled LOC | {total_loc:,} |\n\n")
        f.write(f"## Per-package breakdown\n\n")
        f.write(f"| Functions | Decompiled | LOC | Package |\n|---:|---:|---:|---|\n")
        for pkg, n, dec, loc in sorted(pkg_summary, key=lambda x: (-x[1])):
            short = pkg.split("/")[-1] if "/" in pkg else pkg
            f.write(f"| {n} | {dec} | {loc:,} | `{pkg}` |\n")
        f.write(f"\n## Top auth-flow packages\n\n")
        # Highlight auth-relevant packages
        auth_pkgs = [
            "google3/third_party/jetski/cli/store",
            "google3/third_party/jetski/cli/backend",
            "google3/third_party/jetski/cli/printmode",
            "google3/third_party/jetski/cli/commands",
            "google3/third_party/jetski/language_server/code_assist_client",
            "google3/third_party/jetski/language_server_pb",
        ]
        for ap in auth_pkgs:
            if ap in by_pkg:
                n = len(by_pkg[ap])
                dec = sum(1 for h, *_ in by_pkg[ap] if h in dec_files)
                f.write(f"- **{ap}**: {n} funcs, {dec} decompiled\n")
        f.write(f"\n## Files\n\n")
        f.write(f"- This summary: `decompile-summary.md`\n")
        f.write(f"- Per-package reports: `decompile-<package-slug>.md`\n")
        f.write(f"- Decompiled C pseudocode: `{DEC_DIR}/<HEX>_<short>.c`\n")
        f.write(f"- Errors / skips: `{DEC_DIR}/_errors.txt`\n")
        f.write(f"- Decompile run summary: `{DEC_DIR}/_summary.txt`\n")

    # Build per-package reports
    for pkg, fns in sorted(by_pkg.items()):
        # Make a safe filename
        slug = re.sub(r'[^A-Za-z0-9._-]+', '_', pkg)
        slug = slug.strip('_')
        if not slug:
            slug = "root"
        if len(slug) > 80:
            slug = slug[:80]
        out_path = os.path.join(OUT_DIR, f"decompile-{slug}.md")
        with open(out_path, "w") as f:
            f.write(f"# Decompile report — `{pkg}`\n\n")
            f.write(f"> {len(fns)} priority functions in this Go package\n\n")
            
            # Identify auth-relevant functions in this package
            auth_hints = re.compile(
                r"(auth|Auth|login|Login|onboard|Onboard|eligibility|Elig|license|License|"
                r"credential|Credential|token|Token|GCP|gcp|account|Account|user|User|"
                r"validate|Validate|fetch|Fetch|select|Select|selfassign|SelfAssign|"
                r"startauth|StartAuth|getauthstate|GetAuthState|storecred|StoreCred|"
                r"keyring|Keyring|refresh|Refresh|exchange|Exchange)",
                re.IGNORECASE,
            )
            
            funcs_dec = []
            funcs_pending = []
            for hex_addr, name, short in fns:
                if hex_addr in dec_files:
                    funcs_dec.append((hex_addr, name, short))
                else:
                    funcs_pending.append((hex_addr, name, short))
            
            f.write(f"**Decompiled:** {len(funcs_dec)}/{len(fns)}\n\n")
            
            # Group by receiver (type)
            by_type = defaultdict(list)
            for hex_addr, name, short in funcs_dec:
                m = re.match(r"^(.+)\.([^.]+)$", name)
                if m and "(" in name:
                    # type.Method
                    t = m.group(1)
                else:
                    t = "<package>"
                by_type[t].append((hex_addr, name, short))
            
            for t, tfuncs in sorted(by_type.items()):
                f.write(f"## `{t}`\n\n")
                f.write(f"_{len(tfuncs)} methods decompiled._\n\n")
                f.write(f"| Addr | Function | Auth-relevant | Notes |\n|---|---|---|---|\n")
                for hex_addr, name, short in sorted(tfuncs, key=lambda x: x[0]):
                    auth_flag = "**yes**" if auth_hints.search(name) else ""
                    f.write(f"| `0x{hex_addr}` | `{name}` | {auth_flag} | |\n")
                f.write(f"\n")
                
            if funcs_pending:
                f.write(f"## Pending / errors ({len(funcs_pending)})\n\n")
                f.write(f"Functions that did not decompile (likely thunks, glue, or out-of-spec):\n\n")
                for hex_addr, name, short in funcs_pending[:50]:
                    f.write(f"- `0x{hex_addr}` — `{name}`\n")
                if len(funcs_pending) > 50:
                    f.write(f"\n... and {len(funcs_pending) - 50} more.\n")
                f.write(f"\nSee `{DEC_DIR}/_errors.txt` for details.\n")

    print(f"Wrote {os.path.join(OUT_DIR, 'decompile-summary.md')}")
    print(f"  {len(by_pkg)} per-package reports")
    print(f"  {decompiled}/{total_funcs} funcs decompiled, {total_loc:,} LOC total")

if __name__ == "__main__":
    main()
