class UdpSocketAdapter:
    def __init__(self, bind_host: str, port: int) -> None:
        self._bind_host = bind_host
        self._port = port

    def bind(self) -> None:
        raise NotImplementedError

    def recvfrom(self, bufsize: int) -> tuple[bytes, tuple[str, int]]:
        raise NotImplementedError

    def sendto(self, data: bytes, addr: tuple[str, int]) -> None:
        raise NotImplementedError

    def close(self) -> None:
        raise NotImplementedError
