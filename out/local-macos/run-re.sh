#!/bin/bash
# RE session against the locally installed agy, inside tmux.
#   tmux new-session -d -s reagy -c "$PWD/out/local-macos" './out/local-macos/run-re.sh'
#   tmux attach -t reagy        # observe
#   tmux capture-pane -pt reagy  # non-interactive check
cd /Users/gear/GitHub/openagy/out/local-macos || exit 1
source ./env.sh
export REA_GHIDRA_SEED_FILE="/Users/gear/GitHub/openagy/out/local-macos/seeds/seeds.txt"
export REA_GHIDRA_STARTUP_TIMEOUT_MS=21600000
# rea-agents defaults the Ghidra JVM to -Xmx2G (dist/ghidra/GhidraJavaLaunch.js:53).
# Measured 2026-10-14, three attempts — none produced a result on agy 1.3.4:
#   2G  -> binary_overview fails after ~60s, "Ghidra headless launch failed", bridge dies,
#          orphaned Ghidra JVM keeps running for ~25 min (kill it: /bin/kill -9 <pid>)
#   8G  -> rea analyze runs until externally cancelled, never answers
#   10G -> MCP server survives 621s, then exits rc=0 with no result
# 154,525 seeds take ~10 min to apply; the wrapper's budget does not cover that at any
# heap size.
#
# For real work prefer the direct analyzeHeadless path in AGENTS.md: 11 min import +
# 56 s decompile, no re-analysis per query, 100% decompile success rate.
export GHIDRA_HEADLESS_MAXMEM=10G
export PATH="$JAVA_HOME/bin:$PATH"

echo "=== RE session $(date) ==="
echo "target : $HOME/.local/bin/agy ($(du -h $HOME/.local/bin/agy | cut -f1), Mach-O arm64)"
echo "seeds  : $REA_GHIDRA_SEED_FILE ($(wc -l < "$REA_GHIDRA_SEED_FILE") entries)"
echo "ghidra : $GHIDRA_INSTALL_DIR  heap=$GHIDRA_HEADLESS_MAXMEM"
echo "java   : $($JAVA_HOME/bin/java -version 2>&1 | head -1)"
echo "plan   : plan-local.jsonl ($(grep -c . plan-local.jsonl) steps)"
echo "==========================================="

python3 ../../rea-go-seeds/examples/reamcp.py plan-local.jsonl 2>&1 | tee reamcp.log
echo "=== RE session finished $(date) — artifacts in ./mcp/ ==="
exec zsh