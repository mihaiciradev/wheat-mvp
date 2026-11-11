import pytest

from wheat_api.storage import LocalImageStore


def test_local_store_round_trip(tmp_path) -> None:
    store = LocalImageStore(tmp_path)
    store.put("plots/a/frame.jpg", b"jpeg-bytes")
    assert store.exists("plots/a/frame.jpg")
    assert store.get("plots/a/frame.jpg") == b"jpeg-bytes"


def test_local_store_rejects_path_escape(tmp_path) -> None:
    store = LocalImageStore(tmp_path)
    for key in ("../secret", "/etc/passwd", "", "..", "a/../../b"):
        with pytest.raises(ValueError):
            store.put(key, b"nope")


def test_missing_object_raises(tmp_path) -> None:
    store = LocalImageStore(tmp_path)
    with pytest.raises(FileNotFoundError):
        store.get("missing.jpg")
