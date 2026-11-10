"""Local image storage. S3 can implement the same methods later; it is not wired up."""

from pathlib import Path
from typing import Protocol


class ImageStore(Protocol):
    def put(self, key: str, data: bytes) -> str: ...

    def get(self, key: str) -> bytes: ...

    def exists(self, key: str) -> bool: ...


class LocalImageStore:
    """Stores bytes on the local filesystem under a root directory.

    Keys are relative paths. The store refuses absolute paths and `..` so a
    caller cannot escape the root.
    """

    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def put(self, key: str, data: bytes) -> str:
        path = self._path(key)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return key

    def get(self, key: str) -> bytes:
        path = self._path(key)
        if not path.is_file():
            raise FileNotFoundError(key)
        return path.read_bytes()

    def exists(self, key: str) -> bool:
        return self._path(key).is_file()

    def _path(self, key: str) -> Path:
        if not key or "\\" in key:
            raise ValueError("Invalid storage key.")
        parts = Path(key).parts
        if key.startswith("/") or ".." in parts or not parts:
            raise ValueError("Invalid storage key.")
        path = (self.root / key).resolve()
        if not path.is_relative_to(self.root):
            raise ValueError("Invalid storage key.")
        return path
