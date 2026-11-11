# Decisions

## D1. Repository root is the monorepo

Date: 2026-11-10

The GitHub repository is already `wheat-mvp`. Nesting another `wheat-mvp/` directory would add a path prefix with no boundary benefit. Apps, packages, docs, and tests live at the root.

## D2. One Python project, two import packages

Date: 2026-11-10

`wheat_vision` and `wheat_api` are installed from one `pyproject.toml`. A workspace tool such as uv is not required for two packages. The vision package does not import FastAPI.

## D3. No database until records exist

Date: 2026-11-10

SQLite is the intended local store, and the URL is reserved in `.env.example`. Creating tables, an ORM, or a migration tool before the microplot entity exists adds a schema to keep in sync with nothing. Phase 3 introduces persistence. PostgreSQL remains a connection-string change if concurrent users show up.

## D4. Quality checks are flags, not acceptance

Date: 2026-11-10

Blur and exposure use named provisional thresholds. The API calls that output experimental. Retune them on real photos before comparing them with the 90% acceptance target.

## D5. Uploads are not stored in Phase 0

Date: 2026-11-10

`LocalImageStore` is implemented and tested so the S3-shaped interface exists. The quality route is stateless. Saving files starts when a microplot id owns them.

## D6. Manual corners are the calibration path

Date: 2026-11-10

Known plot dimensions plus located corners can estimate scale. Automatic boundary detection is allowed to fail. Uncalibrated images do not receive gap lengths or densities.

## D7. Next.js without a component library

Date: 2026-11-10

The UI is a small set of researcher screens. Plain CSS is enough. Tailwind or a design system can be reconsidered if screen count makes it cheaper, not before.

## D8. No cloud resources in Phase 0

Date: 2026-11-10

AWS stays in `docs/AWS_PLAN.md`. The owner must approve any account change after credits and eligible services are known.

## D9. Next.js 16 and Python 3.12

Date: 2026-11-10

The Cloud Agent image has Node 22 and Python 3.12. The web app uses Next.js 16.4.6 with the App Router. The API uses FastAPI and the vision stack named in the project brief: OpenCV, NumPy, scikit-image, Pillow.

## D10. First public site is the explanation, not the analysis API

Date: 2026-11-11

The Next.js pages can be hosted on Vercel by themselves. The FastAPI and OpenCV service stays local until a measurement is ready to run for a user. Putting the computer-vision process on a host now would add cost and a deployment without a result to serve. The Vercel project root is `apps/web`, set in the dashboard. `vercel.json` cannot contain `rootDirectory`.

## D11. The public site is Fenia, not a wheat-only page

Date: 2026-11-11

`fenia.ro` is the company site. The landing page describes field measurements from photographs and does not name a crop. Sunflower and wheat are named only on Technical approach. The wheat microplot work remains the first measurement product, and later crops reuse that approach.
