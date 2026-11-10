#!/usr/bin/env bash
set -euo pipefail

export NEXT_TELEMETRY_DISABLED=1

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

.venv/bin/ruff check .
.venv/bin/ruff format --check .
.venv/bin/pytest
npm --prefix apps/web run lint
npm --prefix apps/web run typecheck
npm --prefix apps/web run build
