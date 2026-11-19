#!/usr/bin/env bash
# Ingest SuperGrok Imagine drops from art/incoming/
# Usage: ingest_imagine_assets.sh <project_root> [--promote] [--asset ID ...]
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
if [[ $# -lt 1 ]]; then
  echo "Usage: ingest_imagine_assets.sh <project_root> [--promote] [--asset ID ...]"
  exit 1
fi
ROOT="$(cd "$1" && pwd)"
shift
python3 "$SCRIPT_DIR/ingest_imagine_assets.py" "$ROOT" "$@"