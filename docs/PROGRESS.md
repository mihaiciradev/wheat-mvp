# Progress

## Done

Phase 0 foundation is in the working tree:

- Monorepo layout, `AGENTS.md`, `.cursor/agents/{cv,fullstack,qa}.md`, `.cursor/rules/project.mdc`.
- Docs listed in the project brief.
- `wheat_vision` image loading, EXIF orientation, provisional quality flags, and an analysis result that abstains.
- FastAPI `/health`, `/api/v1/capabilities`, and `POST /api/v1/images/quality`.
- Local image-store implementation, not yet used by a route.
- Next.js placeholder page at `apps/web`.
- Pytest, Ruff, ESLint, TypeScript, and `scripts/smoke.sh`.
- GitHub Actions workflow at `.github/workflows/ci.yml`.

No field images have been analyzed. No accuracy number exists. No AWS resource has been created. No model has been trained.

## Test status

Checked on 10 November 2026 (Europe/Bucharest) with `bash scripts/smoke.sh`, then a second `bash scripts/cloud-agent-install.sh`.

- Pytest: 17 passed.
- Ruff check and format: passed.
- Web ESLint, `tsc --noEmit`, and `next build`: passed.
- These tests use synthetic images. They do not validate field measurements.

`npm audit` in `apps/web` reports 8 moderate issues, all from `minimatch` through the TypeScript ESLint tooling that Next.js pins. They are not in the production page runtime. They were left in place rather than forcing a breaking lint upgrade.

## Next

Phase 1 image feasibility, after real photographs and the four answers in `docs/OPEN_QUESTIONS.md` are available. The CV work is specified in `docs/CV_STRATEGY.md`.

## Blockers

- No representative microplot photographs.
- Plot dimensions, border appearance, and growth stage are unknown.
- Project subagents are files on disk. This Cloud Agent's built-in task list does not expose `cv`, `fullstack`, or `qa` as invocable types; Cursor project sessions load `.cursor/agents/`.

## Environment

The linked Cloud Agent environment is personal and dashboard-managed. It has no finished build, so this session started from the default image and installed dependencies with `scripts/cloud-agent-install.sh`. A saved install script for later agents is proposed separately and does not apply until that proposal is saved.
