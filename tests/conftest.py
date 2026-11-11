import numpy as np
import pytest
from fastapi.testclient import TestClient

from wheat_api.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def checkerboard(size: int = 64, block: int = 4) -> np.ndarray:
    yy, xx = np.indices((size, size))
    mask = ((xx // block) + (yy // block)) % 2 == 0
    image = np.empty((size, size, 3), dtype=np.uint8)
    image[mask] = (40, 140, 50)
    image[~mask] = (190, 180, 150)
    return image
