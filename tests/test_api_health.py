import io

import numpy as np
from fastapi.testclient import TestClient
from PIL import Image

from tests.conftest import checkerboard
from wheat_api.main import MAX_IMAGE_BYTES


def _png(image: np.ndarray) -> bytes:
    buffer = io.BytesIO()
    Image.fromarray(image, mode="RGB").save(buffer, format="PNG")
    return buffer.getvalue()


def test_health(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["service"] == "wheat-api"
    assert body["version"]


def test_capabilities_do_not_claim_measurements(client: TestClient) -> None:
    response = client.get("/api/v1/capabilities")
    assert response.status_code == 200
    body = response.json()
    assert body["phase"] == "0"
    assert body["image_quality"]["status"] == "experimental"
    for name in (
        "vegetation_coverage",
        "rows",
        "gaps",
        "plant_count",
        "greenness",
        "calibration",
    ):
        assert body[name]["status"] == "unavailable"


def test_quality_endpoint_returns_flags_only(client: TestClient) -> None:
    response = client.post(
        "/api/v1/images/quality",
        files={"file": ("frame.png", _png(checkerboard()), "image/png")},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["flags"] == []
    assert body["width_px"] == 64
    assert "vegetation_coverage" not in body
    assert "provisional" in body["notes"]


def test_quality_endpoint_rejects_garbage(client: TestClient) -> None:
    response = client.post(
        "/api/v1/images/quality",
        files={"file": ("notes.txt", b"not-an-image", "text/plain")},
    )
    assert response.status_code == 422
    assert "decode" in response.json()["detail"].lower()


def test_quality_endpoint_rejects_oversized_uploads(client: TestClient) -> None:
    payload = b"\x00" * (MAX_IMAGE_BYTES + 1)
    response = client.post(
        "/api/v1/images/quality",
        files={"file": ("big.bin", payload, "application/octet-stream")},
    )
    assert response.status_code == 413
