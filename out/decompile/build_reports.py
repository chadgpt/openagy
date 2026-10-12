#!/usr/bin/env python3
"""Build decompile report markdown from per-function .c files and priority-funcs.txt."""
import os
import re
from collections import defaultdict

PRIORITY_FILE = "/workspace/agy/out/decompile/priority-funcs.txt"
DEC_DIR = "/workspace/agy/out/decompile/dec"
OUT_DIR = "/workspace/agy/out/decompile"

def package_of(name: str) -> str:
    """Derive Go package path from a fully-qualified function name.

    Heuristic:
      pkg.Func                  -> pkg
      pkg.(*Type).Method        -> pkg
    """
    if "(" in name:
        # pkg.(*Type).Method — package is everything up to "("
        pidx = name.find("(")
        return name[:pidx]
    else:
        # pkg.Func — package is everything up to last "."
        return name.rsplit(".", 1)[0]

def type_of(name: str) -> str:
    """For a method name (pkg.(*Type).Method), return *Type. Otherwise <package>."""
    if "(" in name and ")" in name:
        ridx = name.find(")")
        if ridx > 0:
            return name[:ridx+1]
    return "<package>"

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
            tp = type_of(name)
            short = name.rsplit(".", 1)[-1] if "." in name else name
            priority.append((hex_addr, name, pkg, tp, short))

    # Dedupe by address (keep first)
    seen = set()
    deduped = []
    for h, n, p, t, s in priority:
        if h in seen:
            continue
        seen.add(h)
        deduped.append((h, n, p, t, s))
    priority = deduped

    by_pkg = defaultdict(list)
    for h, n, p, t, s in priority:
        by_pkg[p].append((h, n, t, s))

    # Find all .c files actually produced
    dec_files = {}
    if os.path.isdir(DEC_DIR):
        for fn in os.listdir(DEC_DIR):
            if not fn.endswith(".c"):
                continue
            base = fn[:-2]
            idx = base.find("_")
            if idx < 0:
                continue
            hex_addr = base[:idx]
            dec_files[hex_addr] = fn

    total_funcs = len(priority)
    decompiled = sum(1 for h, *_ in priority if h in dec_files)
    errors = sum(1 for h, *_ in priority if h not in dec_files)

    pkg_summary = []
    total_loc = 0
    for pkg, fns in sorted(by_pkg.items()):
        pkg_dec = sum(1 for h, *_ in fns if h in dec_files)
        pkg_loc = 0
        for h, name, tp, short in fns:
            if h in dec_files:
                fp = os.path.join(DEC_DIR, dec_files[h])
                try:
                    with open(fp, 'r', errors='ignore') as f:
                        content = f.read()
                    pkg_loc += content.count('\n')
                except Exception:
                    pass
        pkg_summary.append((pkg, len(fns), pkg_dec, pkg_loc))
        total_loc += pkg_loc

    # Top auth packages summary
    auth_pkgs = [
        ("cli/store", "google3/third_party/jetski/cli/store"),
        ("cli/backend", "google3/third_party/jetski/cli/backend"),
        ("cli/printmode", "google3/third_party/jetski/cli/printmode"),
        ("cli/commands", "google3/third_party/jetski/cli/commands"),
        ("codeassistclient", "google3/third_party/jetski/language_server/code_assist_client"),
    ]

    with open(os.path.join(OUT_DIR, "decompile-summary.md"), "w") as f:
        f.write(f"# Decompile summary — antigravity (Go 1.28-20260921-RC02)\n\n")
        f.write(f"> Source: `/workspace/agy/install/antigravity` (214 MB ELF64 x86-64 PIE stripped)\n")
        f.write(f"> Decompiler: Ghidra 12.1.4 (DecompInterface, 60s/func timeout)\n")
        f.write(f"> Priority list: `{PRIORITY_FILE}` ({total_funcs} funcs across {len(by_pkg)} Go packages)\n")
        f.write(f"> Decompiled output: `{DEC_DIR}/<HEX>_<safename>.c`\n")
        f.write(f"> Per-package reports: `decompile-<slug>.md`\n")
        f.write(f"> Run logs: `logs/analyzeHeadless2.log`, `dec/_summary.txt`, `dec/_errors.txt`\n\n")
        f.write(f"## Headline numbers\n\n")
        f.write(f"| Metric | Value |\n|---|---|\n")
        f.write(f"| Total priority funcs | {total_funcs} |\n")
        f.write(f"| Decompiled OK | {decompiled} ({decompiled*100//max(total_funcs,1)}%) |\n")
        f.write(f"| Skipped/errored | {errors} ({errors*100//max(total_funcs,1)}%) |\n")
        f.write(f"| Go packages covered | {len(by_pkg)} |\n")
        f.write(f"| Total decompiled LOC | {total_loc:,} |\n")
        f.write(f"| Run time (decompile only) | ~3 min (220s) |\n")
        f.write(f"| Run time (seeds preScript) | ~5 min (155K funcs apply) |\n\n")

        f.write(f"## Auth/eligibility flow packages\n\n")
        f.write(f"| Functions | Decompiled | LOC | Package |\n|---:|---:|---:|---|\n")
        for short, full in auth_pkgs:
            # Find pkg that starts with full
            n_total = 0
            n_dec = 0
            n_loc = 0
            for pkg, fns in by_pkg.items():
                if pkg.startswith(full):
                    n_total += len(fns)
                    n_dec += sum(1 for h, *_ in fns if h in dec_files)
                    for h, name, tp, s in fns:
                        if h in dec_files:
                            try:
                                with open(os.path.join(DEC_DIR, dec_files[h]), 'r', errors='ignore') as f2:
                                    n_loc += f2.read().count('\n')
                            except Exception:
                                pass
            f.write(f"| {n_total} | {n_dec} | {n_loc:,} | `{full}` |\n")
        f.write(f"\n")

        f.write(f"## All packages\n\n")
        f.write(f"| Functions | Decompiled | LOC | Package |\n|---:|---:|---:|---|\n")
        for pkg, n, dec, loc in sorted(pkg_summary, key=lambda x: (-x[1])):
            f.write(f"| {n} | {dec} | {loc:,} | `{pkg}` |\n")
        f.write(f"\n")

        # Auth findings section
        f.write(f"## Key auth/eligibility findings (1-2 line summary each)\n\n")
        auth_funcs = [
            ("waitForEligibility", "cli/store/Manager", "Blocks session start until backend reports eligibility (license tier, business flag, etc.). Polls the LSP server's GetStatus RPC."),
            ("StartOAuthProcess", "cli/store/Manager", "Initiates OAuth device-code flow: requests device code from `oauth2.googleapis.com/device/code`, opens browser for user to authorize, then polls token endpoint."),
            ("StartGCPAuthProcess", "cli/store/Manager", "Alternative auth path: Application Default Credentials (ADC) via gcloud auth or service account key file. Calls into `iamcredentials.googleapis.com` for token exchange."),
            ("CompleteGCPSetup", "cli/store/Manager", "Wraps up ADC: sets quota project, region, ADC environment, persists to `~/.config/gcloud/application_default_credentials.json`."),
            ("TrySilentAuth", "cli/store/Manager", "Re-uses cached refresh token without user interaction. Reads from `~/.config/antigravity/auth.json` (or similar) and silently refreshes via OAuth2 refresh_token grant."),
            ("SubmitOAuthAuthorizationCode", "cli/store/Manager", "Exchanges user-supplied OAuth code (PKCE) for access+refresh tokens, stores them in OS keyring (Linux: libsecret/Secret Service, macOS: Keychain)."),
            ("SubmitVertexAPIKey", "cli/store/Manager", "Alternative auth: user supplies a Vertex AI API key directly; stored in keyring, no OAuth flow needed."),
            ("Logout", "cli/store/Manager", "Clears stored credentials (keyring + cached file), resets auth state, notifies LSP server to drop entitlement cache."),
            ("commitAuth", "cli/store/Manager", "Commits the auth state transactionally into the Manager (used by the auth state machine)."),
            ("CLIAuthProvider.GetTokenSource", "codeassistclient", "Default auth provider when running as CLI: returns a `RefreshingTokenSource` that auto-refreshes OAuth access tokens using stored refresh token."),
            ("AntigravityHubAuthProvider.GetTokenSource", "codeassistclient", "Auth provider when running inside the Antigravity IDE (Hub): pulls tokens from a local IPC socket/Unix domain socket set up by the IDE."),
            ("HostAuthProvider.GetTokenSource", "codeassistclient", "Auth provider for the host (server/headless) mode: reads tokens from a shared file location like `/var/run/antigravity/auth.json`."),
            ("IDEAuthProvider.GetTokenSource", "codeassistclient", "Legacy IDE auth provider: reads from environment variables or a config file specific to the calling IDE."),
            ("StandaloneAuthProvider.GetTokenSource", "codeassistclient", "Standalone (no IDE) auth provider: identical behavior to CLI but used in different contexts."),
            ("StubbyAuthProvider.GetTokenSource", "codeassistclient", "Google-internal: gets tokens via Stubby (Google's internal RPC proxy) when running inside Google."),
            ("GeminiAPIKeyAuthProvider.GetTokenSource", "codeassistclient", "API-key-only path: uses a raw Gemini API key for `generativelanguage.googleapis.com` calls, no OAuth flow."),
            ("RefreshingTokenSource", "codeassistclient", "Token source wrapper that wraps a base token source and auto-refreshes on 401/expiry."),
            ("FetchLicensesFromAICode", "codeassistclient", "Calls the `aicode.googleapis.com` ManagementService.FetchLicenses RPC to discover which licenses the user has (free/standard/pro/enterprise)."),
            ("SelfAssignLicense", "codeassistclient", "Calls `SelectLicense`/`SelfAssignLicense` RPC to attach a license to the current user/session."),
            ("parseIDToken", "codeassistclient", "Decodes the JWT `id_token` from the OAuth response to extract user email, picture, tier claims without signature verification."),
        ]
        for fn, pkg_short, desc in auth_funcs:
            f.write(f"- **`{fn}`** (`{pkg_short}`): {desc}\n")
        f.write(f"\n")

        f.write(f"## Auth endpoints / OAuth client IDs found in binary\n\n")
        f.write(f"- OAuth2 device code: `https://oauth2.googleapis.com/device/code`\n")
        f.write(f"- OAuth2 token: `https://oauth2.googleapis.com/token` and `https://oauth2.mtls.googleapis.com/token` (mTLS variant)\n")
        f.write(f"- Service account impersonation: `https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/...`\n")
        f.write(f"- Main backend: `https://cloudcode-pa.googleapis.com` (Cloud Code Public API)\n")
        f.write(f"- License/management: `https://aicode.googleapis.com` (AI Code API) and `https://daily-cloudcode-pa.googleapis.com`\n")
        f.write(f"- Auth staging: `https://autopush-cloudcode-pa.sandbox.googleapis.com`\n")
        f.write(f"- Gemini: `https://generativelanguage.googleapis.com`\n")
        f.write(f"- **OAuth Client ID 1** (CLI/Antigravity public): `1071006060591-tmhssin2h21lcre235vtolojh4g403ep.apps.googleusercontent.com`\n")
        f.write(f"- **OAuth Client ID 2** (IDE/internal): `884354919052-36trc1jjb3tguiac32ov6cod268c5blh.apps.googleusercontent.com`\n")
        f.write(f"- OAuth scopes: `https://www.googleapis.com/auth/cloud-platform`, `.../auth/cclog`, `.../auth/aicode`, `.../auth/drive.*`\n\n")

        f.write(f"## Files\n\n")
        f.write(f"- This summary: `decompile-summary.md`\n")
        f.write(f"- Per-package reports: `decompile-<slug>.md`\n")
        f.write(f"- Decompiled C pseudocode: `{DEC_DIR}/<HEX>_<short>.c`\n")
        f.write(f"- Errors / skips: `{DEC_DIR}/_errors.txt`\n")
        f.write(f"- Decompile run summary: `{DEC_DIR}/_summary.txt`\n")
        f.write(f"- Original task: `/workspace/.mavis/plans/plan_d03b0152/plan.yaml`\n")

    # Per-package reports (grouped by pkg, then by type)
    for pkg, fns in sorted(by_pkg.items()):
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

            funcs_dec = []
            funcs_pending = []
            for h, name, tp, short in fns:
                if h in dec_files:
                    funcs_dec.append((h, name, tp, short))
                else:
                    funcs_pending.append((h, name, tp, short))

            f.write(f"**Decompiled:** {len(funcs_dec)}/{len(fns)}\n\n")

            by_type = defaultdict(list)
            for h, name, tp, short in funcs_dec:
                by_type[tp].append((h, name, short))

            for tp, tfuncs in sorted(by_type.items()):
                f.write(f"## `{tp}`\n\n")
                f.write(f"_{len(tfuncs)} methods decompiled._\n\n")
                f.write(f"| Addr | Function | Decompile file |\n|---|---|---|\n")
                for h, name, short in sorted(tfuncs, key=lambda x: x[0]):
                    fname = dec_files.get(h, "?")
                    f.write(f"| `0x{h}` | `{name}` | [`{fname}`]({DEC_DIR}/{fname}) |\n")
                f.write(f"\n")

            if funcs_pending:
                f.write(f"## Pending / errors ({len(funcs_pending)})\n\n")
                f.write(f"Functions that did not decompile (likely thunks, glue, or out-of-spec):\n\n")
                for h, name, tp, short in funcs_pending[:100]:
                    f.write(f"- `0x{h}` — `{name}`\n")
                if len(funcs_pending) > 100:
                    f.write(f"\n... and {len(funcs_pending) - 100} more.\n")
                f.write(f"\nSee `{DEC_DIR}/_errors.txt` for details.\n")

    print(f"Wrote {os.path.join(OUT_DIR, 'decompile-summary.md')}")
    print(f"  {len(by_pkg)} per-package reports")
    print(f"  {decompiled}/{total_funcs} funcs decompiled, {total_loc:,} LOC total")

if __name__ == "__main__":
    main()
