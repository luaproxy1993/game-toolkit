#!/usr/bin/env bash
# One-time link: grokmaker/game-maker-pipeline → ~/.grok/skills/game-maker-pipeline
# Idempotent. Does NOT copy/rsync — skill always reads from grokmaker workspace.
set -euo pipefail

SRC="$(cd "$(dirname "$0")/.." && pwd)"
DEST="${HOME}/.grok/skills/game-maker-pipeline"

mkdir -p "${HOME}/.grok/skills"

if [[ -L "$DEST" ]]; then
  current="$(readlink "$DEST")"
  if [[ "$current" == "$SRC" ]]; then
    echo "Already linked: $DEST → $SRC"
    exit 0
  fi
  rm "$DEST"
elif [[ -e "$DEST" ]]; then
  echo "Removing stale copy at $DEST (use workspace source only)"
  rm -rf "$DEST"
fi

ln -s "$SRC" "$DEST"
chmod +x "$SRC/scripts/"*.sh 2>/dev/null || true

echo "Linked: $DEST → $SRC"
echo "GROKMAKER_ROOT: $(dirname "$SRC")"
echo "Invoke: /game-maker-pipeline"