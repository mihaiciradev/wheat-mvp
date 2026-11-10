.PHONY: install test lint format smoke api web

install:
	bash scripts/cloud-agent-install.sh

test:
	.venv/bin/pytest

lint:
	.venv/bin/ruff check .
	.venv/bin/ruff format --check .
	npm --prefix apps/web run lint
	npm --prefix apps/web run typecheck

format:
	.venv/bin/ruff format .
	.venv/bin/ruff check --fix .

smoke:
	bash scripts/smoke.sh

api:
	.venv/bin/uvicorn wheat_api.main:app --host 127.0.0.1 --port 8000 --reload

web:
	npm --prefix apps/web run dev
