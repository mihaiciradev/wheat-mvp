"""Read one DJI Mavic 3M shutter group and say what this system can do with it.

A group is the color JPEG plus four single-band TIFFs that share one capture id.
Spectral values stay 16-bit. No index is computed, and nothing here is a plot measurement.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image

from wheat_vision.io import ImageReadError, load_rgb
from wheat_vision.quality import QualityReport, assess_quality

# A reflectance panel is photographed from well under this height. A survey,
# even a low one, is above it. This only sorts files. It does not detect a panel.
GROUND_LEVEL_M = 3.0
# DJI writes saturated spectral pixels at the top of the 16-bit range.
SPECTRAL_CLIP_LEVEL = 65000
SPECTRAL_KEYS = ("G", "R", "RE", "NIR")

_CAPTURE_RGB = re.compile(r"^(?P<capture_id>.+)_D\.(?:jpg|jpeg)$", re.IGNORECASE)
_ATTR = re.compile(rb'(?:drone-dji:|tiff:)([A-Za-z0-9]+)="([^"]*)"')


class CaptureReadError(ValueError):
    """A shutter group is missing a file or a file could not be read."""


@dataclass(frozen=True)
class BandSummary:
    key: str
    name: str | None
    frequency: str | None
    width_px: int
    height_px: int
    black_level: int | None
    irradiance: float | None
    clipped_fraction: float


@dataclass(frozen=True)
class CaptureSummary:
    """What one shutter group contains, and why it is not a microplot result."""

    capture_id: str
    model: str | None
    role: str
    relative_altitude_m: float | None
    nominal_metres_per_pixel: float | None
    rgb_width_px: int
    rgb_height_px: int
    bands: tuple[BandSummary, ...]
    quality: QualityReport
    usable_for_microplot: bool
    reasons: tuple[str, ...]


def list_capture_ids(directory: Path) -> tuple[str, ...]:
    """Return capture ids that have a color JPEG, in filename order."""
    found: list[str] = []
    for path in sorted(Path(directory).iterdir()):
        match = _CAPTURE_RGB.match(path.name)
        if match:
            found.append(match.group("capture_id"))
    return tuple(found)


def summarize_capture(directory: Path, capture_id: str) -> CaptureSummary:
    """Load one group, score the color photo, and refuse a microplot measurement."""
    directory = Path(directory)
    rgb_path = _rgb_path(directory, capture_id)
    try:
        rgb = load_rgb(rgb_path)
    except ImageReadError as exc:
        raise CaptureReadError(str(exc)) from exc
    rgb_meta = _attributes(rgb_path.read_bytes())
    quality = assess_quality(rgb)

    bands: list[BandSummary] = []
    for key in SPECTRAL_KEYS:
        path = _band_path(directory, capture_id, key)
        bands.append(_read_band(path, key))

    altitude = _float_attr(rgb_meta, "RelativeAltitude")
    focal_px = _float_attr(rgb_meta, "CalibratedFocalLength")
    nominal = None
    if altitude is not None and focal_px is not None and focal_px > 0:
        nominal = altitude / focal_px
    role = _role(altitude)
    return CaptureSummary(
        capture_id=capture_id,
        model=rgb_meta.get("Model"),
        role=role,
        relative_altitude_m=altitude,
        nominal_metres_per_pixel=nominal,
        rgb_width_px=int(rgb.shape[1]),
        rgb_height_px=int(rgb.shape[0]),
        bands=tuple(bands),
        quality=quality,
        usable_for_microplot=False,
        reasons=_reasons(role, altitude, nominal, tuple(bands)),
    )


def summarize_directory(directory: Path) -> tuple[CaptureSummary, ...]:
    ids = list_capture_ids(directory)
    if not ids:
        raise CaptureReadError(f"No Mavic 3M color photos were found in {directory}.")
    return tuple(summarize_capture(directory, capture_id) for capture_id in ids)


def _reasons(
    role: str,
    altitude: float | None,
    nominal_metres_per_pixel: float | None,
    bands: tuple[BandSummary, ...],
) -> tuple[str, ...]:
    reasons = [
        "Microplot cover, rows, gaps, and counts need one plot photograph "
        "with marked corners and known side lengths. This capture does not supply them."
    ]
    if role == "ground_level" and altitude is not None:
        reasons.append(
            f"Relative altitude is {altitude:.2f} m, a ground-level shot such as a "
            "reflectance panel rather than a view of a plot."
        )
    elif role == "aerial" and altitude is not None and nominal_metres_per_pixel is not None:
        reasons.append(
            f"Relative altitude is {altitude:.1f} m. Nominal RGB spacing is "
            f"{nominal_metres_per_pixel * 100:.1f} cm per pixel, from that height and the "
            "focal length stored in the file. That spacing is not a plot calibration."
        )
    elif role == "unknown":
        reasons.append("Relative altitude is missing, so the frame cannot be placed.")

    reasons.append(
        "The four spectral bands were kept as separate 16-bit images. "
        "They were not aligned and no index was computed."
    )
    if any(band.clipped_fraction > 0.02 for band in bands):
        reasons.append(
            "At least one spectral band is clipped at the top of the 16-bit range, "
            "so this group cannot set a reflectance scale."
        )
    return tuple(reasons)


def _role(altitude: float | None) -> str:
    if altitude is None:
        return "unknown"
    if altitude < GROUND_LEVEL_M:
        return "ground_level"
    return "aerial"


def _rgb_path(directory: Path, capture_id: str) -> Path:
    for suffix in (".JPG", ".jpg", ".JPEG", ".jpeg"):
        path = directory / f"{capture_id}_D{suffix}"
        if path.is_file():
            return path
    raise CaptureReadError(f"Color photo {capture_id}_D.JPG is missing.")


def _band_path(directory: Path, capture_id: str, key: str) -> Path:
    for suffix in (".TIF", ".tif", ".TIFF", ".tiff"):
        path = directory / f"{capture_id}_MS_{key}{suffix}"
        if path.is_file():
            return path
    raise CaptureReadError(f"Spectral band {capture_id}_MS_{key}.TIF is missing.")


def _read_band(path: Path, key: str) -> BandSummary:
    try:
        with Image.open(path) as image:
            array = np.asarray(image)
    except OSError as exc:
        raise CaptureReadError(f"Could not read {path.name}.") from exc
    if array.ndim != 2 or array.dtype != np.uint16:
        raise CaptureReadError(f"{path.name} is not a single 16-bit band.")
    meta = _attributes(path.read_bytes())
    clipped = float(np.mean(array >= SPECTRAL_CLIP_LEVEL))
    return BandSummary(
        key=key,
        name=meta.get("BandName"),
        frequency=meta.get("BandFreq"),
        width_px=int(array.shape[1]),
        height_px=int(array.shape[0]),
        black_level=_int_attr(meta, "BlackLevel"),
        irradiance=_float_attr(meta, "Irradiance"),
        clipped_fraction=clipped,
    )


def _attributes(data: bytes) -> dict[str, str]:
    found: dict[str, str] = {}
    for match in _ATTR.finditer(data):
        key = match.group(1).decode("ascii")
        found.setdefault(key, match.group(2).decode("utf-8", "replace"))
    return found


def _float_attr(attributes: dict[str, str], name: str) -> float | None:
    raw = attributes.get(name)
    if raw is None:
        return None
    try:
        return float(raw)
    except ValueError:
        return None


def _int_attr(attributes: dict[str, str], name: str) -> int | None:
    raw = attributes.get(name)
    if raw is None:
        return None
    try:
        return int(raw)
    except ValueError:
        return None
