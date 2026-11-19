#!/usr/bin/env bash
# Scaffold RE pipeline project + empty design-bible skeleton.
# Usage: scaffold_project.sh <project_slug> [grokmaker_root]
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: scaffold_project.sh <project_slug> [grokmaker_root]"
  exit 1
fi

SLUG="$1"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Resolve grokmaker root: skill co-located in grokmaker/ or explicit arg / env
if [[ $# -ge 2 ]]; then
  GROK="$(cd "$2" && pwd)"
elif [[ -d "$SKILL_ROOT/../reverse-game-template" ]]; then
  GROK="$(cd "$SKILL_ROOT/.." && pwd)"
elif [[ -n "${GROKMAKER_ROOT:-}" ]]; then
  GROK="$(cd "$GROKMAKER_ROOT" && pwd)"
elif [[ -f "$SKILL_ROOT/../.grokmaker-root" ]]; then
  GROK="$(cd "$(cat "$SKILL_ROOT/../.grokmaker-root")" && pwd)"
else
  GROK="${HOME}/grokmaker"
fi

TEMPLATE="$GROK/reverse-game-template"
DEST="$GROK/$SLUG"

if [[ ! -d "$TEMPLATE" ]]; then
  echo "Missing template: $TEMPLATE"
  exit 1
fi

if [[ -e "$DEST" ]]; then
  echo "Already exists: $DEST"
  exit 1
fi

"$TEMPLATE/scripts/init_project.sh" "$SLUG"
mkdir -p "$DEST/production/design-bible"/{volumes,constraints,appendices}
mkdir -p "$DEST/art" "$DEST/screenshots/author-ref"

python3 "$SCRIPT_DIR/generate_design_bible.py" "$DEST" --slug "$SLUG"

# Copy pipeline scripts into project
cp "$SCRIPT_DIR/art_verify.sh" "$SCRIPT_DIR/ship.sh" "$SCRIPT_DIR/match_and_correct.sh" "$SCRIPT_DIR/art_asset_matcher.py" \
  "$SCRIPT_DIR/supergrok_batch_prompts.py" "$SCRIPT_DIR/ingest_imagine_assets.py" \
  "$SCRIPT_DIR/ingest_imagine_assets.sh" "$SCRIPT_DIR/supergrok_imagine.sh" "$DEST/scripts/"
chmod +x "$DEST/scripts/"*.sh "$DEST/scripts/"*.py 2>/dev/null || true
mkdir -p "$DEST/art"/{incoming,staging,master,supergrok}

# Seed art contract templates
cp "$SKILL_ROOT/references/art-prompt-registry.TEMPLATE.json" "$DEST/art/art-prompt-registry.json"
cp "$SKILL_ROOT/references/wireframe-to-pixel-contract.TEMPLATE.json" "$DEST/art/wireframe-to-pixel-contract.json"
python3 - <<PY
import json, pathlib
slug = "$SLUG"
for name in ("art-prompt-registry.json", "wireframe-to-pixel-contract.json"):
    p = pathlib.Path("$DEST/art") / name
    text = p.read_text().replace("{slug}", slug).replace("{SLUG}", slug.upper().replace("-", "_"))
    p.write_text(text)
PY

echo "Created: $DEST"
echo "Next: fill idea-brief author_raw_input → /game-maker-pipeline grokmaker/$SLUG"