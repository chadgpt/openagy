#!/bin/bash
# Regenerate the reconstructed Go module from seeds.txt and verify it compiles.
#
#   ./rebuild-gosrc.sh [outdir]     (default: ./gosrc)
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT="${1:-$HERE/gosrc}"
SEEDS="$HERE/seeds/seeds.txt"

echo "==> generating into $OUT"
rm -rf "$OUT"
mkdir -p "$OUT"
python3 "$HERE/gen_gosrc.py" "$SEEDS" "$OUT"
python3 "$HERE/write_symsearch.py" "$OUT"
cp "$HERE/README.go.md" "$OUT/README.md"

cat > "$OUT/go.mod" <<'EOF'
module google3/third_party/jetski

go 1.26.2
EOF

echo "==> gofmt -w"
# Let gofmt own the layout rather than trying to predict its line-breaking rules in
# the generator; this also guarantees the output is canonical Go, not just valid.
(cd "$OUT" && gofmt -w .)

if [ -n "$(cd "$OUT" && gofmt -l .)" ]; then
  echo "ERROR: gofmt still reports unformatted files"; exit 1
fi

echo "==> go build ./..."
(cd "$OUT" && go build ./...)

echo "==> go vet ./..."
(cd "$OUT" && go vet ./...)

PKGS=$(cd "$OUT" && go list ./... | wc -l | tr -d ' ')
DECLS=$(grep -rh '^func ' "$OUT" --include='*.go' | wc -l | tr -d ' ')
echo "OK: $PKGS packages, $DECLS declarations, builds and vets clean"