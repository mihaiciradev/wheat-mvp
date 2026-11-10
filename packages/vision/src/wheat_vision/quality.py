"""Technical quality checks. Thresholds are provisional and not field-validated."""

from dataclasses import dataclass

import cv2
import numpy as np

# These cutoffs are engineering defaults for flagging obviously poor frames.
# They must be retuned on real microplot photographs before any acceptance rate
# is reported. A missing flag is not evidence that a photograph is usable.
BLUR_VARIANCE_MIN = 80.0
UNDEREXPOSED_MEAN = 40.0
OVEREXPOSED_MEAN = 220.0
CLIP_FRACTION = 0.02
SHADOW_LEVEL = 5
HIGHLIGHT_LEVEL = 250

NOTES = (
    "Blur and exposure flags use provisional thresholds. "
    "They are not a validated acceptance test and they do not measure the crop."
)


@dataclass(frozen=True)
class QualityReport:
    blur_variance: float
    mean_luminance: float
    clipped_low_fraction: float
    clipped_high_fraction: float
    flags: tuple[str, ...]
    width_px: int
    height_px: int
    notes: str = NOTES


def assess_quality(image_rgb: np.ndarray) -> QualityReport:
    """Score blur and exposure on an upright uint8 RGB image."""
    _require_rgb(image_rgb)
    gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
    blur_variance = float(cv2.Laplacian(gray, cv2.CV_64F).var())
    mean_luminance = float(gray.mean())
    clipped_low = float(np.mean(gray <= SHADOW_LEVEL))
    clipped_high = float(np.mean(gray >= HIGHLIGHT_LEVEL))

    flags: list[str] = []
    if blur_variance < BLUR_VARIANCE_MIN:
        flags.append("blur_suspected")
    if mean_luminance < UNDEREXPOSED_MEAN:
        flags.append("underexposed")
    if mean_luminance > OVEREXPOSED_MEAN:
        flags.append("overexposed")
    if clipped_low > CLIP_FRACTION:
        flags.append("shadow_clipping")
    if clipped_high > CLIP_FRACTION:
        flags.append("highlight_clipping")

    height, width = gray.shape
    return QualityReport(
        blur_variance=blur_variance,
        mean_luminance=mean_luminance,
        clipped_low_fraction=clipped_low,
        clipped_high_fraction=clipped_high,
        flags=tuple(flags),
        width_px=int(width),
        height_px=int(height),
    )


def _require_rgb(image_rgb: np.ndarray) -> None:
    if image_rgb.ndim != 3 or image_rgb.shape[2] != 3:
        raise ValueError("Expected an RGB image with shape (height, width, 3).")
    if image_rgb.dtype != np.uint8:
        raise ValueError("Expected a uint8 RGB image.")
    if image_rgb.shape[0] < 2 or image_rgb.shape[1] < 2:
        raise ValueError("Image is too small to assess.")
