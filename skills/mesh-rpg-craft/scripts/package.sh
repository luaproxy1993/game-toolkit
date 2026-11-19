#!/usr/bin/env bash
set -euo pipefail

SKILL_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VERSION="$(tr -d '[:space:]' < "$SKILL_ROOT/VERSION")"
NAME="mesh-rpg-craft-v${VERSION}"
OUT_DIR="${1:-$SKILL_ROOT/dist}"
STAGING="$OUT_DIR/.staging-$NAME"
ARCHIVE="$OUT_DIR/${NAME}.tar.gz"

rm -rf "$STAGING"
mkdir -p "$OUT_DIR" "$STAGING/$NAME"
rsync -a --exclude dist --exclude '.staging-*' --exclude .DS_Store "$SKILL_ROOT/" "$STAGING/$NAME/"
chmod +x "$STAGING/$NAME/install.sh" "$STAGING/$NAME/scripts/"*.sh 2>/dev/null || true
tar -czf "$ARCHIVE" -C "$STAGING" "$NAME"
rm -rf "$STAGING"
if command -v shasum >/dev/null 2>&1; then
  shasum -a 256 "$ARCHIVE" > "${ARCHIVE}.sha256"
fi
echo "Package: $ARCHIVE"
[[ -f "${ARCHIVE}.sha256" ]] && cat "${ARCHIVE}.sha256"
