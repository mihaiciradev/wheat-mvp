#!/usr/bin/env bash
# Idempotent dependency install for local development and Cloud Agent builds.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if ! python3 -c "import ensurepip" >/dev/null 2>&1; then
  sudo apt-get update
  sudo apt-get install -y python3.12-venv
fi

python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -e ".[dev]"

if [[ -f apps/web/package-lock.json ]]; then
  npm --prefix apps/web ci
else
  npm --prefix apps/web install
fi
