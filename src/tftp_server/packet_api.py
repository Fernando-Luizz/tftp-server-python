def parse_datagram(data: bytes) -> object:
    raise NotImplementedError


def build_data(block: int, payload: bytes) -> bytes:
    raise NotImplementedError


def build_ack(block: int) -> bytes:
    raise NotImplementedError


def build_error(code: int, message: str) -> bytes:
    raise NotImplementedError
