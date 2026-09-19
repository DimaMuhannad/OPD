#!/usr/bin/env bash
# Сборка одной Marp-колоды: .md -> .pptx (для показа) + .png по слайдам (для визуальной проверки).
# Использование: tools/marp/build.sh zanyatiya/marp-src/имя.md
set -euo pipefail
SRC="$1"
BASE="$(basename "$SRC" .md)"
OUTDIR="$(dirname "$SRC")/../$(basename "$(dirname "$SRC")" | sed 's/marp-src//')"
OUTDIR="zanyatiya"
QADIR="/tmp/claude-marp-qa/$BASE"
mkdir -p "$QADIR"
export CHROME_PATH=/opt/pw-browsers/chromium-1194/chrome-linux/chrome

npx --yes @marp-team/marp-cli@4.5.1 "$SRC" \
  --theme tools/marp/theme.css \
  --pptx --allow-local-files \
  -o "$OUTDIR/$BASE.pptx"

npx --yes @marp-team/marp-cli@4.5.1 "$SRC" \
  --theme tools/marp/theme.css \
  --images png --allow-local-files \
  -o "$QADIR/slide.png"

echo "PPTX: $OUTDIR/$BASE.pptx"
echo "PNG:  $QADIR/"
