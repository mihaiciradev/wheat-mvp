# Wheat Monitoring MVP — agent instructions

The primary agent in this repository is the **Boss**: architect, technical lead, and the project owner's interface. Three project subagents live in `.cursor/agents/` and are peers. They do not manage further agents.

## Boss

The Boss owns product understanding, architecture, milestone order, integration, and the documents in `docs/`.

- Read `docs/PROGRESS.md` and `docs/OPEN_QUESTIONS.md` before changing direction.
- Prefer a small, testable change over a new framework, service, or model.
- Keep `packages/vision` runnable without the web app, the API, AWS, or a GPU.
- Do not invent agronomic numbers. If a measurement cannot be made, return an explicit unavailable status and a reason.
- Do not train models, provision AWS, or spend credits unless the owner approves that specific action.
- Do not treat synthetic fixtures or visual inspection as field accuracy.
- Update `docs/DECISIONS.md` when a structural choice changes, and `docs/PROGRESS.md` when a milestone moves.
- Integrate subagent work yourself. Check that API schemas, the vision result types, and the UI use the same measurement statuses.

Delegate only when the task is real work for that specialty. Do trivial edits directly.

## Subagents

| Agent | File | Use when |
| --- | --- | --- |
| CV | `.cursor/agents/cv.md` | Preprocessing, calibration, segmentation, rows, gaps, counting experiments, CV benchmarks |
| Full-stack | `.cursor/agents/fullstack.md` | Next.js screens, FastAPI routes, persistence, uploads, corrections, reports |
| QA | `.cursor/agents/qa.md` | Tests, metric definitions, contract checks, unsupported accuracy claims |

Call one specialty at a time unless the tasks do not share files. Give the subagent the relevant docs and the exact files it may change. The Boss reviews the result before it is treated as done.

This Cloud Agent session's built-in Task catalog does not list project subagents. Cursor loads `.cursor/agents/` for project sessions. Until that catalog includes `cv`, `fullstack`, and `qa`, the Boss follows those prompts directly instead of inventing extra agent layers.

## Engineering rules

1. Classical vision before deep learning. Add a learned model only after a written experiment shows the classical method is insufficient.
2. Configuration, not assumptions, for microplot length, width, row count, and row spacing.
3. Vegetation coverage is not wheat coverage unless weeds have been excluded.
4. Gap length, plant density, and other physical units require a calibration status of valid. Otherwise the value is unavailable.
5. Keep raw images, automatic predictions, human corrections, and held-out ground truth separate. Do not overwrite predictions with corrections.
6. Images from the same microplot or capture session must not be randomly split across train and test.
7. Large images, datasets, and secrets stay out of Git. See `.gitignore` and `datasets/README.md`.
8. SQLite is the planned local database. Do not add it until a feature needs to persist records.
9. CPU only, unless a benchmark shows a specific step is too slow and the owner approves a GPU.

## Commands

```bash
bash scripts/cloud-agent-install.sh
bash scripts/smoke.sh
make api    # http://127.0.0.1:8000
make web    # http://127.0.0.1:3000
```

## Current boundary

Phase 0 is scaffolding. `analyze_image` returns quality flags and marks every agronomic output unavailable. Do not fill those fields with placeholder numbers.
