# Hosting the website on Vercel

The first Vercel project is `apps/web` only: the overview and the technical notes. The FastAPI analysis service is not part of this deploy. No environment variables are required for these two pages.

`vercel.json` at the repository root sets `rootDirectory` to `apps/web`. Confirm that value in the Vercel import screen before the first deploy.

## Connect the GitHub repository

1. Open [vercel.com/new](https://vercel.com/new) and sign in with the GitHub account that owns `mihaiciradev/wheat-mvp`.
2. Import that repository. Approve Vercel’s GitHub access if GitHub asks.
3. Set the project name if you want one other than the repository name.
4. Confirm **Root Directory** is `apps/web`. If the importer shows the repository root, choose Edit and select `apps/web`.
5. Framework preset: **Next.js**. Build command: `npm run build`. Install command: `npm install`. Leave the output directory empty so Next.js uses its default.
6. Do not add env vars for this site.
7. Deploy. A preview URL is enough. Production can follow `main` after the pull request is merged. Until then, deploy the branch `cursor/phase-0-foundation-ef2d` or use the preview built from the pull request.

Open `/` and `/tech` on the resulting URL. Both pages should describe the product and should not show a coverage number.

## Later, from the command line

Do this on your own machine after the dashboard project exists. Do not commit `.vercel/`.

```bash
npm i -g vercel
cd apps/web
vercel login
vercel link
vercel project inspect --non-interactive
```

`vercel link` from `apps/web` should match the project whose root directory is that folder. Stop if the inspect output names a different project.

## Out of this step

- The Python API, image storage, and any paid Vercel add-on.
- A custom domain, until you want one.
- Deploying from this repository’s automation. Connecting the Git account in the dashboard is the link.
