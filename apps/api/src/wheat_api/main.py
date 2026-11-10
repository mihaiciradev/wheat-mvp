from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from wheat_api import __version__
from wheat_api.schemas import (
    CapabilitiesResponse,
    ErrorResponse,
    HealthResponse,
    MeasurementCapability,
    QualityResponse,
)
from wheat_vision.io import ImageReadError, load_rgb_bytes
from wheat_vision.quality import assess_quality

MAX_IMAGE_BYTES = 30 * 1024 * 1024

app = FastAPI(
    title="Wheat microplot API",
    version=__version__,
    summary="Foundation API. Agronomic measurements are not implemented.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


def _unavailable(detail: str) -> MeasurementCapability:
    return MeasurementCapability(status="unavailable", detail=detail)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="wheat-api", version=__version__)


@app.get("/api/v1/capabilities", response_model=CapabilitiesResponse)
def capabilities() -> CapabilitiesResponse:
    return CapabilitiesResponse(
        phase="0",
        image_quality=MeasurementCapability(
            status="experimental",
            detail=(
                "Blur and exposure flags use provisional thresholds. "
                "They are not a validated field-acceptance test."
            ),
        ),
        vegetation_coverage=_unavailable("Vegetation segmentation is not implemented."),
        rows=_unavailable("Row detection is not implemented."),
        gaps=_unavailable("Gap detection is not implemented."),
        plant_count=_unavailable("Plant counting is not implemented."),
        greenness=_unavailable("Relative greenness is not implemented."),
        calibration=_unavailable(
            "Scale is unavailable until microplot corners and physical dimensions are supplied."
        ),
    )


@app.post(
    "/api/v1/images/quality",
    response_model=QualityResponse,
    responses={413: {"model": ErrorResponse}, 422: {"model": ErrorResponse}},
)
async def image_quality(
    file: UploadFile = File(...),  # noqa: B008
) -> QualityResponse:
    """Assess technical image quality. This does not measure the crop."""
    data = await file.read(MAX_IMAGE_BYTES + 1)
    if len(data) > MAX_IMAGE_BYTES:
        raise HTTPException(
            status_code=413,
            detail="Image exceeds the 30 MB upload limit.",
        )
    try:
        image = load_rgb_bytes(data)
        report = assess_quality(image)
    except (ImageReadError, ValueError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return QualityResponse(
        blur_variance=report.blur_variance,
        mean_luminance=report.mean_luminance,
        clipped_low_fraction=report.clipped_low_fraction,
        clipped_high_fraction=report.clipped_high_fraction,
        flags=list(report.flags),
        notes=report.notes,
        width_px=report.width_px,
        height_px=report.height_px,
    )
