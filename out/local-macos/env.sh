# RE + Ghidra reverse-engineering environment for the local agy binary (macOS/arm64).
#   source ~/.config/agy-re/env.sh
export JAVA_HOME=/opt/homebrew/opt/openjdk@21
export GHIDRA_INSTALL_DIR="$HOME/tools/ghidra_12.1.4_PUBLIC"
export REA_GHIDRA_SEED_FILE="$(pwd)/out/local-macos/seeds/seeds.txt"
export PATH="$JAVA_HOME/bin:$PATH"
