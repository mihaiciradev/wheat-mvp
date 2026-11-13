"""Build the figures for the /research page from a local Mavic 3M sample folder.

The sample photos are not in Git. Pass the folder that contains one shutter group
per five files. Outputs are web-sized JPEGs and a JSON record of the numbers.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

from wheat_vision.capture import summarize_directory

PREVIEW_WIDTH = 1400
# Hand-checked rectangles in each spectral frame, x0, y0, x1, y1.
# They are not detected plots. Frame two has moved, so its soil box is different.
REGIONS = {
    "DJI_20240405154706_0001": {
        "green cover": (180, 180, 780, 620),
        "bare soil": (200, 1250, 900, 1750),
    },
    "DJI_20240405154711_0002": {
        "green cover": (180, 180, 780, 620),
        "bare soil": (820, 1620, 1180, 1920),
    },
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sample", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    captures = []
    for summary in summarize_directory(args.sample):
        captures.append(_one(args.sample, args.out, summary))
    payload = {
        "source": (
            "Pix4D DJI Mavic 3 Multispectral example, winter barley, 5 April 2024. "
            "These are not Fenia plots."
        ),
        "captures": captures,
    }
    (args.out / "results.json").write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


def _one(sample: Path, out: Path, summary) -> dict:
    capture_id = summary.capture_id
    rgb = np.asarray(Image.open(sample / f"{capture_id}_D.JPG").convert("RGB"))
    share, overlay = _excess_green(rgb)
    _save(out / f"{capture_id}-rgb.jpg", rgb)
    _save(out / f"{capture_id}-exg.jpg", overlay)

    record = {
        "id": capture_id,
        "role": summary.role,
        "altitude_m": summary.relative_altitude_m,
        "rgb": f"{capture_id}-rgb.jpg",
        "exg": f"{capture_id}-exg.jpg",
        "vegetation_share": round(share, 4),
        "bands": [
            {"key": band.key, "name": band.name, "clipped": round(band.clipped_fraction, 4)}
            for band in summary.bands
        ],
    }
    if summary.nominal_metres_per_pixel is not None:
        record["nominal_cm_per_px"] = round(summary.nominal_metres_per_pixel * 100, 2)
        record["two_metre_px"] = int(round(2.0 / summary.nominal_metres_per_pixel))

    if capture_id in REGIONS:
        false_color, regions = _spectral(sample, capture_id)
        _save(out / f"{capture_id}-false.jpg", false_color)
        record["false_color"] = f"{capture_id}-false.jpg"
        record["regions"] = regions
        if capture_id == "DJI_20240405154706_0001":
            record["scale"] = f"{capture_id}-scale.jpg"
            _save(out / record["scale"], _scale_crop(rgb, record["two_metre_px"]))
    return record


def _excess_green(rgb: np.ndarray) -> tuple[float, np.ndarray]:
    image = rgb.astype(np.float32)
    exg = 2 * image[:, :, 1] - image[:, :, 0] - image[:, :, 2]
    exg_u8 = cv2.normalize(exg, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    _threshold, mask = cv2.threshold(exg_u8, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    share = float(np.mean(mask > 0))
    overlay = rgb.copy()
    tint = np.array([90, 210, 130], dtype=np.float32)
    selected = mask > 0
    overlay[selected] = (0.55 * overlay[selected] + 0.45 * tint).astype(np.uint8)
    return share, overlay


def _spectral(sample: Path, capture_id: str) -> tuple[np.ndarray, list[dict]]:
    bands = {}
    for key in ("G", "R", "NIR"):
        path = sample / f"{capture_id}_MS_{key}.TIF"
        raw = np.asarray(Image.open(path)).astype(np.float32)
        meta = _attributes(path.read_bytes())
        leveled = np.clip(raw - float(meta["BlackLevel"]), 0, None)
        matrix = np.array(
            [float(value) for value in meta["CalibratedHMatrix"].split(",")],
            dtype=np.float64,
        ).reshape(3, 3)
        bands[key] = cv2.warpPerspective(leveled, matrix, (leveled.shape[1], leveled.shape[0]))

    nir = bands["NIR"]
    red = bands["R"]
    denominator = nir + red
    index = np.full(nir.shape, np.nan, dtype=np.float32)
    valid = denominator > 50
    index[valid] = (nir[valid] - red[valid]) / denominator[valid]

    false_color = np.dstack([_stretch(nir), _stretch(red), _stretch(bands["G"])])
    regions = []
    for name, (x0, y0, x1, y1) in REGIONS[capture_id].items():
        cv2.rectangle(
            false_color,
            (x0, y0),
            (x1, y1),
            (255, 214, 80) if name == "green cover" else (110, 190, 255),
            6,
        )
        window = index[y0:y1, x0:x1]
        regions.append({"name": name, "index_mean": round(float(np.nanmean(window)), 3)})
    return false_color, regions


def _scale_crop(rgb: np.ndarray, box_px: int) -> np.ndarray:
    crop = rgb[400:1000, 500:1300].copy()
    cv2.rectangle(crop, (36, 36), (36 + box_px, 36 + box_px), (255, 214, 80), 4)
    return crop


def _stretch(values: np.ndarray) -> np.ndarray:
    low, high = np.percentile(values, (2, 98))
    scaled = np.clip((values - low) / (high - low + 1e-6), 0, 1)
    return (scaled * 255).astype(np.uint8)


def _save(path: Path, rgb: np.ndarray) -> None:
    height, width = rgb.shape[:2]
    if width > PREVIEW_WIDTH:
        scale = PREVIEW_WIDTH / width
        rgb = cv2.resize(
            rgb,
            (PREVIEW_WIDTH, int(round(height * scale))),
            interpolation=cv2.INTER_AREA,
        )
    Image.fromarray(rgb).save(path, quality=80, optimize=True)


def _attributes(data: bytes) -> dict[str, str]:
    found: dict[str, str] = {}
    for match in re.finditer(rb'(?:drone-dji:|tiff:)([A-Za-z0-9]+)="([^"]*)"', data):
        found.setdefault(match.group(1).decode("ascii"), match.group(2).decode())
    return found


if __name__ == "__main__":
    main()
