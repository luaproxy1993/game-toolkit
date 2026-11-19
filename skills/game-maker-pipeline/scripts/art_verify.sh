#!/usr/bin/env bash
# Verify art registry ↔ disk coverage (RE-19, RE-26).
# Usage: art_verify.sh [project_root]
#   project_root — grokmaker/{slug} directory (default: parent of scripts/)
set -euo pipefail

if [[ $# -ge 1 ]]; then
  ROOT="$(cd "$1" && pwd)"
else
  ROOT="$(cd "$(dirname "$0")/.." && pwd)"
fi

REG="$ROOT/art/art-prompt-registry.json"
AUDIT="$ROOT/art/prompt-audit.json"

if [[ ! -f "$REG" ]]; then
  echo "FAIL: missing $REG"
  exit 1
fi

python3 - <<'PY' "$ROOT" "$REG" "$AUDIT"
import json, pathlib, sys
root, reg_path, audit_path = map(pathlib.Path, sys.argv[1:4])
reg = json.loads(reg_path.read_text())
registered = {a["output_path"] for a in reg.get("assets", [])}
on_disk = set()
for base in ("assets/v01/scenes", "assets/v01/characters", "assets/v01/ui", "art/staging", "screenshots/silhouette", "screenshots/diegetic", "screenshots/scenes"):
    d = root / base
    if d.is_dir():
        for f in d.iterdir():
            if f.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
                on_disk.add(str(pathlib.Path(base) / f.name))
if (root / "cover.png").exists():
    on_disk.add("cover.png")

missing_reg = sorted(on_disk - registered)
missing_disk = sorted(registered - on_disk)
forbidden = set(reg.get("forbidden_assets", []))

errors = []
if missing_reg:
    errors.append(f"RE-19: on disk but NOT in registry: {missing_reg}")
if missing_disk:
    errors.append(f"RE-19: in registry but NOT on disk: {missing_disk}")

for a in reg.get("assets", []):
    p = a.get("prompt") or a.get("prompt_delta") or ""
    if len(p) < 80 and "prompt_block" not in p:
        errors.append(f"RE-20: {a['asset_id']} prompt too short / missing prompt_block ref")
    if not a.get("references"):
        errors.append(f"RE-22: {a['asset_id']} missing references[]")

if errors:
    print("ART VERIFY FAIL:")
    for e in errors:
        print(" -", e)
    raise SystemExit(1)

print("ART VERIFY OK")
print(f"  project: {root}")
print(f"  registered: {len(registered)}  on_disk: {len(on_disk)}")
if not audit_path.exists():
    print("WARN: art/prompt-audit.json missing (RE-26)")
PY