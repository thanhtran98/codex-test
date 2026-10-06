#!/usr/bin/env bash
# Bọc mediakit shot: trỏ Playwright vào Chromium đã tải trong .venv (tránh ghi ~/Library/Caches).
set -euo pipefail
cd "$(dirname "$0")/.."
export PLAYWRIGHT_BROWSERS_PATH="$PWD/.venv/ms-playwright"
exec .venv/bin/python tools/mediakit.py shot "$@"
