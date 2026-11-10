from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


class MeasurementCapability(BaseModel):
    status: str
    detail: str


class CapabilitiesResponse(BaseModel):
    phase: str
    image_quality: MeasurementCapability
    vegetation_coverage: MeasurementCapability
    rows: MeasurementCapability
    gaps: MeasurementCapability
    plant_count: MeasurementCapability
    greenness: MeasurementCapability
    calibration: MeasurementCapability


class QualityResponse(BaseModel):
    blur_variance: float
    mean_luminance: float
    clipped_low_fraction: float
    clipped_high_fraction: float
    flags: list[str]
    notes: str
    width_px: int = Field(ge=1)
    height_px: int = Field(ge=1)


class ErrorResponse(BaseModel):
    error: str
    detail: str
