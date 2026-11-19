#!/usr/bin/env bash
# Package {slug}.rpc for Remnant Pocket offline bundle.
# Usage: ship.sh [project_root]
# Preflight: art_verify.sh PASS + art: accept recorded in pipeline_state.json
set -euo pipefail

if [[ $# -ge 1 ]]; then
  ROOT="$(cd "$1" && pwd)"
else
  ROOT="$(cd "$(dirname "$0")/.." && pwd)"
fi

SLUG="$(basename "$ROOT")"
STAGE="$(mktemp -d)"
OUT="$ROOT/${SLUG}.rpc"
SKILL_ART_VERIFY="$(cd "$(dirname "$0")" && pwd)/art_verify.sh"

for req in manifest.json cover.png game/index.html; do
  if [[ ! -f "$ROOT/$req" ]]; then
    echo "FAIL: missing $ROOT/$req"
    exit 1
  fi
done

if [[ -x "$SKILL_ART_VERIFY" ]]; then
  "$SKILL_ART_VERIFY" "$ROOT" || {
    echo "FAIL: art_verify.sh — fix registry before ship (RE-26)"
    exit 1
  }
fi

rm -f "$OUT"
mkdir -p "$STAGE/game" "$STAGE/screenshots"

cp "$ROOT/manifest.json" "$ROOT/cover.png" "$STAGE/"
cp "$ROOT/game/index.html" "$ROOT/game/styles.css" "$ROOT/game/game.js" "$STAGE/game/" 2>/dev/null || \
  cp "$ROOT/game/index.html" "$STAGE/game/"

for sub in silhouette diegetic scenes; do
  if [[ -d "$ROOT/screenshots/$sub" ]]; then
    mkdir -p "$STAGE/screenshots/$sub"
    shopt -s nullglob
    for f in "$ROOT/screenshots/$sub"/*.{png,jpg,jpeg,webp}; do
      [[ -f "$f" ]] && cp "$f" "$STAGE/screenshots/$sub/"
    done
    shopt -u nullglob
  fi
done

cd "$STAGE"
zip -rq "$OUT" manifest.json cover.png game screenshots
cd - >/dev/null
rm -rf "$STAGE"

SIZE=$(du -h "$OUT" | cut -f1)
echo "Shipped: $OUT ($SIZE)"
echo "Contents: manifest.json, cover.png, game/, screenshots/"