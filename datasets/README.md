# Datasets

Raw field photographs are not stored in Git.

Place a local feasibility set in `datasets/incoming/` (gitignored). Describe it with a copy of `manifest.example.json` named `manifest.json` (also keep that copy out of Git if it contains local paths you do not want published).

`datasets/raw/` and `datasets/derived/` are reserved for originals and generated masks or overlays. Both are gitignored.

Twenty to thirty photographs are a technical feasibility set, not a production training set. See `docs/DATA_STRATEGY.md` for the manifest fields and the separation between predictions, corrections, and ground truth.
