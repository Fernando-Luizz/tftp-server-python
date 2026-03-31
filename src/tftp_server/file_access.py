from pathlib import Path


class FileAccess:
    def __init__(self, root: Path) -> None:
        self._root = root.resolve()

    def _safe_path(self, relative_path: str) -> Path:
        target = (self._root / relative_path).resolve()
        if not target.is_relative_to(self._root):
            raise PermissionError(f"Access denied: {relative_path}")
        return target

    def read_chunk(self, relative_path: str, offset: int, length: int) -> bytes:
        path = self._safe_path(relative_path)
        with open(path, "rb") as f:
            f.seek(offset)
            return f.read(length)

    def write_chunk(self, relative_path: str, data: bytes, append: bool) -> None:
        path = self._safe_path(relative_path)
        mode = "ab" if append else "wb"
        with open(path, mode) as f:
            f.write(data)
