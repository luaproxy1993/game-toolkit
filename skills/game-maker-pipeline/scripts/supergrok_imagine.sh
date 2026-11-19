#!/usr/bin/env bash
# SuperGrok Imagine Pipeline orchestrator
# Usage: supergrok_imagine.sh <project_root> [prompts|ingest|verify|all]
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "${1:?project_root}" && pwd)"
CMD="${2:-all}"

run_prompts() {
  python3 "$SCRIPT_DIR/supergrok_batch_prompts.py" "$ROOT"
  echo ""
  echo "→ Open: $ROOT/art/supergrok/batch-prompts.md"
  echo "→ Generate in SuperGrok Imagine, save to: $ROOT/art/incoming/{ASSET_ID}.png"
}

run_ingest() {
  "$SCRIPT_DIR/ingest_imagine_assets.sh" "$ROOT" --promote "$@"
}

run_verify() {
  if [[ -x "$ROOT/scripts/art_verify.sh" ]]; then
    "$ROOT/scripts/art_verify.sh" "$ROOT"
  else
    "$SCRIPT_DIR/art_verify.sh" "$ROOT"
  fi
  if [[ -x "$ROOT/scripts/match_and_correct.sh" ]]; then
    "$ROOT/scripts/match_and_correct.sh" "$ROOT" || true
  else
    "$SCRIPT_DIR/match_and_correct.sh" "$ROOT" || true
  fi
}

case "$CMD" in
  prompts) run_prompts ;;
  ingest) shift 2; run_ingest "$@" ;;
  verify) run_verify ;;
  all)
    run_prompts
    echo ""
    echo "After SuperGrok generation + art/incoming/ drops:"
    echo "  $SCRIPT_DIR/supergrok_imagine.sh $ROOT ingest"
    echo "  $SCRIPT_DIR/supergrok_imagine.sh $ROOT verify"
    ;;
  *) echo "Usage: supergrok_imagine.sh <project> [prompts|ingest|verify|all]"; exit 1 ;;
esac