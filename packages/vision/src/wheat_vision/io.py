"""Load photographs as upright RGB arrays. Original files are never modified."""

from io import BytesIO
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps, UnidentifiedImageError


class ImageReadError(ValueError):
    """The bytes or path could not be decoded as an image."""


def load_rgb(path: Path) -> np.ndarray:
    try:
        data = path.read_bytes()
    except OSError as exc:
        raise ImageReadError(f"Could not read {path}.") from exc
    return load_rgb_bytes(data)


def load_rgb_bytes(data: bytes) -> np.ndarray:
    """Decode image bytes to uint8 RGB with EXIF orientation applied.

    Returns an array of shape (height, width, 3).
    """
    if not data:
        raise ImageReadError("Image is empty.")
    try:
        with Image.open(BytesIO(data)) as image:
            upright = ImageOps.exif_transpose(image)
            rgb = upright.convert("RGB")
            array = np.asarray(rgb)
    except (UnidentifiedImageError, OSError) as exc:
        raise ImageReadError("Could not decode the image.") from exc
    if array.ndim != 3 or array.shape[2] != 3 or array.dtype != np.uint8:
        raise ImageReadError("Decoded image is not uint8 RGB.")
    return array
