import io
from pathlib import Path

import numpy as np
import pytest
from PIL import Image

from wheat_vision.capture import CaptureReadError, summarize_capture, summarize_directory


def _xmp(**fields: str) -> bytes:
    attrs = " ".join(f'drone-dji:{key}="{value}"' for key, value in fields.items())
    return (
        f'<x:xmpmeta xmlns:drone-dji="http://www.dji.com/drone-dji/1.0/" '
        f'xmlns:tiff="http://ns.adobe.com/tiff/1.0/">'
        f"<rdf:Description {attrs}/></x:xmpmeta>"
    ).encode()


def _write_color(path: Path, altitude: str, focal: str = "1000") -> None:
    image = Image.new("RGB", (32, 24), (30, 140, 40))
    packet = _xmp(RelativeAltitude=altitude, CalibratedFocalLength=focal)
    packet = packet.replace(b"<rdf:Description ", b'<rdf:Description tiff:Model="M3M" ', 1)
    image.save(path, format="JPEG", xmp=packet)


def _write_band(path: Path, key: str, hot: bool) -> None:
    values = np.full((8, 6), 4000, dtype=np.uint16)
    if hot:
        values[:2, :] = 65520
    image = Image.fromarray(values)
    packet = _xmp(
        BandName={"G": "Green", "R": "Red", "RE": "RedEdge", "NIR": "NIR"}[key],
        BandFreq="560(+/-16)nm",
        BlackLevel="3200",
        Irradiance="1000.5",
    )
    image.save(path, format="TIFF", tiffinfo={700: packet})


def _write_group(directory: Path, capture_id: str, altitude: str, hot: bool) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    _write_color(directory / f"{capture_id}_D.JPG", altitude)
    for key in ("G", "R", "RE", "NIR"):
        _write_band(directory / f"{capture_id}_MS_{key}.TIF", key, hot)


def test_ground_level_group_is_not_a_microplot(tmp_path: Path) -> None:
    _write_group(tmp_path, "DJI_1", "0.80", hot=True)
    summary = summarize_capture(tmp_path, "DJI_1")
    assert summary.role == "ground_level"
    assert summary.model == "M3M"
    assert summary.usable_for_microplot is False
    assert summary.relative_altitude_m == pytest.approx(0.8)
    assert summary.nominal_metres_per_pixel == pytest.approx(0.0008)
    assert summary.bands[0].name == "Green"
    assert summary.bands[0].black_level == 3200
    assert summary.bands[0].clipped_fraction == pytest.approx(2 / 8)
    assert any("reflectance panel" in reason for reason in summary.reasons)
    assert any("cannot set a reflectance scale" in reason for reason in summary.reasons)
    assert any("no index" in reason for reason in summary.reasons)


def test_aerial_group_reports_nominal_spacing_without_a_plot_scale(tmp_path: Path) -> None:
    _write_group(tmp_path, "DJI_2", "30", hot=False)
    summary = summarize_capture(tmp_path, "DJI_2")
    assert summary.role == "aerial"
    assert summary.usable_for_microplot is False
    assert summary.nominal_metres_per_pixel == pytest.approx(0.03)
    assert summary.bands[0].clipped_fraction == 0
    assert any("not a plot calibration" in reason for reason in summary.reasons)
    assert not any("reflectance scale" in reason for reason in summary.reasons)


def test_missing_band_is_an_error(tmp_path: Path) -> None:
    _write_group(tmp_path, "DJI_3", "90", hot=False)
    (tmp_path / "DJI_3_MS_NIR.TIF").unlink()
    with pytest.raises(CaptureReadError, match="MS_NIR"):
        summarize_capture(tmp_path, "DJI_3")


def test_directory_summary_keeps_filename_order(tmp_path: Path) -> None:
    _write_group(tmp_path, "DJI_b", "10", hot=False)
    _write_group(tmp_path, "DJI_a", "1", hot=False)
    summaries = summarize_directory(tmp_path)
    assert [item.capture_id for item in summaries] == ["DJI_a", "DJI_b"]


def test_eight_bit_tiff_is_rejected(tmp_path: Path) -> None:
    _write_group(tmp_path, "DJI_4", "10", hot=False)
    gray = Image.fromarray(np.zeros((8, 6), dtype=np.uint8))
    buffer = io.BytesIO()
    gray.save(buffer, format="TIFF")
    (tmp_path / "DJI_4_MS_G.TIF").write_bytes(buffer.getvalue())
    with pytest.raises(CaptureReadError, match="16-bit"):
        summarize_capture(tmp_path, "DJI_4")
