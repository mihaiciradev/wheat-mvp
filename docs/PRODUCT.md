# Product

## Goal

Help an agricultural researcher judge how wheat has established inside one small, delimited microplot: how uniform the vegetation is, and where the visible gaps are.

The product reports measurements that can be checked. It does not score "crop health" from a photograph.

## Users

- Researchers and agronomists reviewing microplots.
- Field operators who capture smartphone photos and correct boundaries or rows.

The interface is a work tool, not a consumer app.

## First product

**Wheat Microplot Establishment Analysis.** Each microplot has an identifier, physical dimensions, optional planting metadata, one or more still photographs, analysis results, human corrections, and later a history of revisits.

The answer the software should eventually give:

> How well has wheat established in this microplot, how uniformly is it growing, and where are the visible gaps?

## In scope for the MVP

1. Microplot boundary, automatic only if it holds up, with manual corners as the supported fallback.
2. Vegetation segmentation and percent cover inside the plot.
3. Row detection and human-editable row lines.
4. Visible low-occupancy intervals along rows, with lengths in metres only when scale is valid.
5. Image-quality flags for blur, exposure, and unusable geometry.
6. Upload of one or more RGB stills per microplot.

## Explicitly later

Individual plant counting, density, and relative greenness are priority 2 and stay experimental until they are compared with manual references. Repeated growth monitoring, drones, orthomosaics, field-wide maps, weeds, stress, lodging, and disease are out of the first MVP.

## Non-goals

- Video.
- Dependence on DJI Pilot, Terra, or FlightHub. Later inputs must be ordinary RGB images, orthomosaics, or tiles.
- Claiming wheat cover when weeds are not separated.
- Reporting nitrogen, chlorophyll, or physiological health from uncontrolled RGB.
- Treating a gap in vegetation as proof of a missing seed.
- A production plant count before manual-count comparison.
- GPU services, distributed workers, or always-on cloud infrastructure.

## Provisional success targets

These are engineering targets to review with the agronomic expert. They are not current results.

| Target | Bar | Requires |
| --- | --- | --- |
| Vegetation coverage | Mean absolute error ≤ 5 percentage points | Reviewed masks |
| Expected rows | ≥ 95% of rows on eligible images | An agreed row definition |
| Gaps | Precision and recall ≥ 80% each | An agreed gap definition |
| Quality flags | ≥ 90% agreement with accepted captures | Supported capture conditions |
| Plant counting | No production bar yet | Manual counts |

Also track manual-correction rate, review time per plot, calibration failure rate, and images rejected as unmeasurable. Every reported percentage needs a written evaluation method in `docs/experiments/` or `docs/DATA_STRATEGY.md`.
