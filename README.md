# Wheat Monitoring MVP

Software for measuring how wheat has established in small, delimited microplots. The aim is a checkable agronomic measurement, not a model demo.

**Phase 0 is a foundation.** The API can flag blur and exposure with provisional thresholds. Vegetation cover, rows, gaps, plant counts, greenness, and physical scale are unavailable on purpose. No field result is claimed.

## Layout

| Path | Role |
| --- | --- |
| `apps/web` | Next.js overview and technical notes |
| `apps/api` | FastAPI |
| `packages/vision` | Image pipeline, usable without the API |
| `docs` | Product, architecture, and decisions |
| `datasets` | Manifest example only; photographs stay local |
| `.cursor/agents` | CV, full-stack, and QA subagents |

The primary agent instructions are in `AGENTS.md`.

## Local setup

Requires Python 3.12, Node.js 22, and `python3.12-venv`.

```bash
bash scripts/cloud-agent-install.sh
bash scripts/smoke.sh
```

API:

```bash
make api
```

`GET http://127.0.0.1:8000/health`

Web placeholder:

```bash
make web
```

`http://127.0.0.1:3000`

Copy `.env.example` to `.env` only if you need to override paths. Do not commit `.env`.

## Data

Put photographs in `datasets/incoming/` and describe them with a local manifest. See `datasets/README.md`. Those files are gitignored.

## Status

Next milestone: image feasibility on real microplot photos (`docs/ROADMAP.md`, `docs/CV_STRATEGY.md`). Open blockers: `docs/OPEN_QUESTIONS.md`.
