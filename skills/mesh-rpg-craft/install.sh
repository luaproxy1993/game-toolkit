#!/usr/bin/env bash
# Usage: ./install.sh [--dir TARGET] [--force]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DEFAULT_DEST="${HOME}/.grok/skills/mesh-rpg-craft"
DEST="$DEFAULT_DEST"
FORCE=0

usage() {
  cat <<'EOF'
Usage: install.sh [OPTIONS]
  --dir PATH    Install destination (default: ~/.grok/skills/mesh-rpg-craft)
  --force       Overwrite existing installation
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dir) DEST="${2:?}"; shift 2 ;;
    --force) FORCE=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage; exit 1 ;;
  esac
done

DEST="${DEST/#\~/$HOME}"
mkdir -p "$(dirname "$DEST")"

if [[ -e "$DEST" ]]; then
  if [[ "$FORCE" -ne 1 ]]; then
    echo "Already exists: $DEST (use --force)" >&2
    exit 1
  fi
  rm -rf "$DEST"
fi

mkdir -p "$DEST"
rsync -a --exclude dist --exclude '.staging-*' --exclude .DS_Store "$SCRIPT_DIR/" "$DEST/"
chmod +x "$DEST/install.sh" "$DEST/scripts/"*.sh 2>/dev/null || true
echo "Installed: $DEST"
echo "Slash: /mesh-rpg-craft"
