#!/usr/bin/env python3
"""Create minimal reverse-game-template skeleton."""
from __future__ import annotations
import json
from pathlib import Path

GROK = Path("/Users/a123/grokmaker")
TEMPLATE = GROK / "reverse-game-template"

if TEMPLATE.exists():
    import shutil
    shutil.rmtree(TEMPLATE)

dirs = [
    "scripts", "screenshots/variants", "screenshots/scenes", "screenshots/author-ref",
    "screenshots/structure-ref", "visual-scan", "game", "production/session-state",
    "production/design-bible/volumes", "production/design-bible/constraints",
    "production/design-bible/appendices", "gdd", "art/incoming", "art/staging",
    "examples",
]
for d in dirs:
    (TEMPLATE / d).mkdir(parents=True, exist_ok=True)

pipeline_state = {
    "pipeline_id": "reverse-engineering-game-pipeline",
    "pipeline_version": "1.8.1",
    "project_slug": "CHANGE_ME",
    "status": "active",
    "current_layer": "re_layer_00_intent",
    "next_layer": "re_layer_00b_gdd_art",
    "awaiting_author_gate": "re_layer_00_intent",
    "decisions": {
        "constitution_status": None,
        "intent_status": None,
        "gdd_status": None,
        "screenshot_pick": None,
        "scope_status": None,
        "art_status": None,
        "whitebox_status": None,
        "playtest_status": None,
    },
    "revision_log": [],
    "blocked_note": None,
    "prior_project_excluded": [],
}

idea_brief_shell = {
    "pipeline_id": "reverse-engineering-game-pipeline",
    "project_slug": "CHANGE_ME",
    "author_raw_input": "(待作者填写)",
    "hook": "",
    "genre_tags": [],
    "viewport": {"width": 640, "height": 480, "aspect": "4:3"},
    "input_profile": "rp_gamepad_v1",
    "策划案": {},
}

files = {
    "pipeline_state.json": pipeline_state,
    "idea-brief.json": idea_brief_shell,
    "gamer-brief.json": {"pipeline_id": "reverse-engineering-game-pipeline", "author_raw_input": "(待作者填写)"},
    "mockup-briefs.json": {"layer": "re_layer_01_screenshot_gen", "variants": []},
    "screenshot-spec.json": {},
    "screenshot-structure-spec.json": {},
    "interaction-spec.json": {},
    "content-slots.json": {},
    "state-machine.json": {},
    "gameplay-spec.json": {},
    "author-selection.json": {},
    "delivery-contract.json": {"target": "rp-web", "format": "rpc"},
    "content-units-tracker.json": {"units": []},
    "asset-decomposition.json": {},
    "screenshot-gen-manifest.json": {},
}

for name, data in files.items():
    (TEMPLATE / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

(TEMPLATE / "scripts" / "init_project.sh").write_text(
    """#!/usr/bin/env bash
set -euo pipefail
if [[ $# -lt 1 ]]; then echo "Usage: init_project.sh <slug>"; exit 1; fi
SLUG="$1"
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
TEMPLATE="$ROOT/reverse-game-template"
DEST="$ROOT/$SLUG"
if [[ -e "$DEST" ]]; then echo "Already exists: $DEST"; exit 1; fi
cp -R "$TEMPLATE" "$DEST"
find "$DEST" -name '.DS_Store' -delete 2>/dev/null || true
python3 - <<PY
import json, pathlib
dest = pathlib.Path("$DEST")
slug = "$SLUG"
for name in ("pipeline_state.json", "idea-brief.json"):
    p = dest / name
    data = json.loads(p.read_text())
    data["project_slug"] = slug
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\\n")
PY
chmod +x "$DEST/scripts/serve.sh" 2>/dev/null || true
echo "Created: $DEST"
""",
    encoding="utf-8",
)

(TEMPLATE / "scripts" / "serve.sh").write_text(
    """#!/usr/bin/env bash
set -euo pipefail
PORT="${1:-8765}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
echo "Serving $ROOT at http://127.0.0.1:$PORT"
python3 -m http.server "$PORT"
""",
    encoding="utf-8",
)

(TEMPLATE / "scripts" / "init_project.sh").chmod(0o755)
(TEMPLATE / "scripts" / "serve.sh").chmod(0o755)

(TEMPLATE / "screenshots" / "gallery.html").write_text(
    """<!DOCTYPE html>
<html lang="zh"><head><meta charset="UTF-8"><title>Mockup Gallery</title>
<style>body{font-family:system-ui;background:#111;color:#eee;padding:24px} a{color:#6cf}</style></head>
<body><h1>Mockup Gallery</h1><p>Variants will appear here after re_01.</p></body></html>""",
    encoding="utf-8",
)

print(f"Created: {TEMPLATE}")