from pathlib import Path


class FileAccess:
    def __init__(self, root: Path) -> None:
        self._root = root

    def read_chunk(self, relative_path: str, offset: int, length: int) -> bytes:
        raise NotImplementedError

    def write_chunk(self, relative_path: str, data: bytes, append: bool) -> None:
        raise NotImplementedError
