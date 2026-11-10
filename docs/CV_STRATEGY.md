# Computer-vision strategy

Use classical methods until a documented experiment on real photographs shows they are not good enough. Do not label a large training set in advance.

## Assumptions that are not accepted

- A visible microplot border does not by itself give metres per pixel. Scale requires known side lengths and located corners, then a homography into a top-down plane. If the corners or the dimensions are missing, physical measurements are unavailable.
- Plot edges may be boards, strings, bare soil, or paint, and they may not be perfectly rectangular. Automatic detection is an experiment. Manual corners are the supported path.
- Green pixels are vegetation. They are wheat only after weeds are excluded, which the MVP does not do.
- One overview photo may be enough for cover and coarse gaps. It is not assumed to be enough to count plants.
- Low occupancy along a row is a candidate gap, not proof of a missing plant.
- Relative greenness, if added later, is a comparative RGB index, not nitrogen or chlorophyll.

## Pipeline order

Each stage must be callable and testable on its own.

1. **Load.** RGB, EXIF orientation applied, original file untouched. Implemented.
2. **Quality.** Laplacian variance and luminance clipping. Implemented with provisional thresholds in `wheat_vision.quality`. Not a field-acceptance test.
3. **Corners and scale.** Manual corners plus `width_m` and `length_m`. Rectify when the correspondence is consistent. Automatic boundary finding is optional and may fail.
4. **Vegetation mask inside the plot.** Compare Excess Green, HSV, and adaptive thresholding on a few reviewed masks. Morphology and connected components as cleanup. Report cover as a percent of the plot area, with the method name.
5. **Rows.** Estimate direction, then expected lines from a projection profile or robust line fit, using row spacing only as a prior when it was provided. Partial rows must not force a full set of false lines. Coverage does not wait on rows.
6. **Gaps.** Along each expected row, low-occupancy intervals above a configurable threshold. Positions always. Lengths in metres only if calibration is valid.
7. **Counting, later and experimental.** Connected components, opening, watershed, or local maxima. Abstain when leaves or tillers merge. Do not train a detector until those fail on real images.

## First experiment

Name: `phase1-image-feasibility`. Do not start it without real photographs.

For each manifest entry:

- Record blur, exposure, resolution, and whether the whole plot is in frame.
- Say whether a person can place four corners unambiguously. Note the border material.
- If `width_m` and `length_m` are present and corners are marked, fit a homography and record whether the rectified plot looks rectangular and whether the scale is stable. If not, calibration stays unavailable.
- Inside the plot, write masks for ExG, HSV, and adaptive thresholding and save overlays under `datasets/derived/` (not Git).
- Do not estimate gaps, density, or plant counts in this experiment.
- Write the note at `docs/experiments/phase1-feasibility.md` as observations. No accuracy percentage until reviewed masks exist.

## Libraries

OpenCV, NumPy, Pillow, and scikit-image. scikit-image is a dependency for the morphology and watershed work in later phases. Phase 0 does not call it, so no unused import is kept around to "prove" the dependency.
