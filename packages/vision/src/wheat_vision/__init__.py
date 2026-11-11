"""Classical computer-vision pipeline for wheat microplot photographs.

The package must stay runnable without the web API, a database, or cloud storage.
Phase 0 exposes image loading and experimental quality checks only.
"""

from wheat_vision.io import ImageReadError, load_rgb, load_rgb_bytes
from wheat_vision.pipeline import AnalysisResult, analyze_image
from wheat_vision.quality import QualityReport, assess_quality

__all__ = [
    "AnalysisResult",
    "ImageReadError",
    "QualityReport",
    "analyze_image",
    "assess_quality",
    "load_rgb",
    "load_rgb_bytes",
]
