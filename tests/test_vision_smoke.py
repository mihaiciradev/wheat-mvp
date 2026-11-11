import io

import numpy as np
import pytest
from PIL import Image

from tests.conftest import checkerboard
from wheat_vision.io import ImageReadError, load_rgb_bytes
from wheat_vision.pipeline import MeasurementStatus, analyze_image
from wheat_vision.quality import assess_quality


def test_checkerboard_has_no_quality_flags() -> None:
    report = assess_quality(checkerboard())
    assert report.flags == ()
    assert report.width_px == 64
    assert report.height_px == 64
    assert report.blur_variance > 80


def test_dark_frame_is_flagged_without_inventing_a_crop_measurement() -> None:
    dark = np.zeros((32, 32, 3), dtype=np.uint8)
    report = assess_quality(dark)
    assert "underexposed" in report.flags
    assert "blur_suspected" in report.flags
    assert "shadow_clipping" in report.flags


def test_blown_highlights_are_flagged() -> None:
    bright = np.full((32, 32, 3), 255, dtype=np.uint8)
    report = assess_quality(bright)
    assert "overexposed" in report.flags
    assert "highlight_clipping" in report.flags


def test_analysis_abstains_from_agronomic_values() -> None:
    result = analyze_image(checkerboard())
    for measurement in (
        result.vegetation_coverage,
        result.rows,
        result.gaps,
        result.plant_count,
        result.greenness,
        result.calibration,
    ):
        assert measurement.status is MeasurementStatus.UNAVAILABLE
        assert measurement.reason
        assert not hasattr(measurement, "value")


def test_rejects_empty_and_non_image_bytes() -> None:
    with pytest.raises(ImageReadError):
        load_rgb_bytes(b"")
    with pytest.raises(ImageReadError):
        load_rgb_bytes(b"this is not an image")


def test_exif_orientation_swaps_stored_dimensions() -> None:
    image = Image.new("RGB", (8, 2), (20, 120, 20))
    exif = Image.Exif()
    exif[274] = 6
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", exif=exif.tobytes())
    loaded = load_rgb_bytes(buffer.getvalue())
    assert loaded.shape == (8, 2, 3)


def test_quality_rejects_a_single_pixel() -> None:
    with pytest.raises(ValueError, match="too small"):
        assess_quality(np.zeros((1, 1, 3), dtype=np.uint8))
