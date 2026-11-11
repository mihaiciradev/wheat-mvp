# Roadmap

Phases are an order of work, not a schedule. Finish the current phase before opening the next feature set.

## Phase 0 — Foundation

Status: implemented in this repository, pending the owner's review.

- Monorepo, Boss instructions, three subagents, docs, smoke tests.
- Vision package loads images and abstains from agronomic measurements.
- API health, capability list, and experimental quality endpoint.
- Placeholder web page. No analysis UI.

## Phase 1 — Image feasibility

Status: blocked on real photographs.

Deliverable: `docs/experiments/phase1-feasibility.md` using the protocol in `docs/CV_STRATEGY.md`.

Decide, from evidence:

- Can a person, and can an algorithm, locate plot corners?
- Do known side lengths produce a usable homography?
- Which of ExG, HSV, and adaptive thresholding is worth keeping for a first mask?
- Which frames should be rejected for blur, exposure, or geometry?

No gap lengths and no plant counts in this phase.

## Phase 2 — Core measurements

Vegetation cover on the rectified plot, row lines with manual edit, candidate gaps, overlays, and a benchmark against the small reviewed set. Report errors with the method from `docs/DATA_STRATEGY.md`.

## Phase 3 — Application MVP

Microplot records, image upload into `LocalImageStore`, analysis API, overlay view, corrections stored separately from predictions, and a basic per-plot report. SQLite starts here.

## Phase 4 — Validation

Independent reference measurements, error analysis, and a decision on whether counting is worth building. Counting stays experimental until that comparison exists.

## Phase 5 — Pilot

AWS plan reviewed against actual credits, then a small deployment only with approval. Field usability and cost notes.

## Phase 6 — Later research

Drone stills or orthomosaics as additional RGB inputs, larger maps, and a compact learned model only where Phase 4 showed a classical method failing.

## Priority reminder

Priority 1 is boundaries, vegetation cover, rows, and gaps. Priority 2 is counting, density, greenness, and comparison across plots. Priority 3 is monitoring over time and aerial mapping.
