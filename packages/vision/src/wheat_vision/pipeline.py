"""Analysis entry point.

Unavailable measurements stay unavailable. Do not substitute zeros or estimates.
"""

from dataclasses import dataclass
from enum import StrEnum

import numpy as np

from wheat_vision.quality import QualityReport, assess_quality


class MeasurementStatus(StrEnum):
    UNAVAILABLE = "unavailable"


@dataclass(frozen=True)
class UnavailableMeasurement:
    status: MeasurementStatus
    reason: str


@dataclass(frozen=True)
class AnalysisResult:
    quality: QualityReport
    vegetation_coverage: UnavailableMeasurement
    rows: UnavailableMeasurement
    gaps: UnavailableMeasurement
    plant_count: UnavailableMeasurement
    greenness: UnavailableMeasurement
    calibration: UnavailableMeasurement


def analyze_image(image_rgb: np.ndarray) -> AnalysisResult:
    """Run the implemented checks and mark every agronomic output unavailable."""
    return AnalysisResult(
        quality=assess_quality(image_rgb),
        vegetation_coverage=UnavailableMeasurement(
            status=MeasurementStatus.UNAVAILABLE,
            reason="Vegetation segmentation is not implemented.",
        ),
        rows=UnavailableMeasurement(
            status=MeasurementStatus.UNAVAILABLE,
            reason="Row detection is not implemented.",
        ),
        gaps=UnavailableMeasurement(
            status=MeasurementStatus.UNAVAILABLE,
            reason=(
                "Gap detection is not implemented. Physical lengths require a valid calibration."
            ),
        ),
        plant_count=UnavailableMeasurement(
            status=MeasurementStatus.UNAVAILABLE,
            reason="Plant counting is experimental and is not implemented.",
        ),
        greenness=UnavailableMeasurement(
            status=MeasurementStatus.UNAVAILABLE,
            reason="Relative greenness is not implemented and would not be a nitrogen measurement.",
        ),
        calibration=UnavailableMeasurement(
            status=MeasurementStatus.UNAVAILABLE,
            reason=(
                "Scale is unavailable until corners and known microplot dimensions are supplied."
            ),
        ),
    )
