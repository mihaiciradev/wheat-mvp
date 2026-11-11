# Data strategy

There is no wheat dataset in this repository. A first technical set of about 20–30 photographs should cover different plots, densities, light, soil, growth stages, weeds, and camera angles. That set cannot support a claim of general field accuracy.

## What is stored where

| Kind | Location | In Git |
| --- | --- | --- |
| Raw photographs | `datasets/incoming/` or `datasets/raw/` | No |
| Manifest | Local `datasets/manifest.json`, copied from `datasets/manifest.example.json` | Example only |
| Automatic predictions | Written by the pipeline, never replaced in place | No |
| Human corrections | Separate records referencing the prediction | No, until a small approved fixture is needed |
| Ground truth | Held out from development images | No |
| Synthetic unit-test images | Created in memory by tests | Not as files |

## Manifest fields

`version`, and `images[]` with:

- `id`, `microplot_id`, `path`
- `width_m`, `length_m`, `row_count`, `row_spacing_m` — null when unknown
- `growth_stage`, `border_marking`, `captured_at`, `camera_notes`

Do not guess a null field in code.

## Label only what a metric needs

Corners or plot boundary, row centerlines, vegetation masks on a small benchmark subset, confirmed gaps, manual plant counts, and optional plant-base points.

Do not label every leaf, weed species, or disease for this MVP.

## Leakage

Photographs of the same microplot, the same field visit, or a repeated capture of the same plants stay in one split. Do not shuffle them independently into train and test.

## Evaluation method, required before a percentage

State the image list, who labeled the reference, the exact definition (for example the minimum gap length), and the statistic (mean absolute error, precision, recall). Images used to tune a threshold are not the images used to report it.

Quality flags, coverage error, row detection, and gap scores are separate. A sharp photo can still have an unusable plot boundary.
