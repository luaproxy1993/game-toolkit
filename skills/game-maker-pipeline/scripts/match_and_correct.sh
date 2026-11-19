#!/usr/bin/env bash
# RE-27: Art asset matcher — compare batch assets against master style anchor.
# Usage: match_and_correct.sh [project_root]
# Writes:
#   art/art-match-audit.json
#   scripts/batch_fix_commands.sh
# Updates registry entries flagged with new_registry_entry_required.
set -euo pipefail

if [[ $# -ge 1 ]]; then
  ROOT="$(cd "$1" && pwd)"
else
  ROOT="$(cd "$(dirname "$0")/.." && pwd)"
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
python3 "$SCRIPT_DIR/art_asset_matcher.py" "$ROOT"