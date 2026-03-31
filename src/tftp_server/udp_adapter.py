import socket


class UdpSocketAdapter:
    def __init__(self, bind_host: str, port: int, timeout: float = 5.0) -> None:
        self._bind_host = bind_host
        self._port = port
        self._timeout = timeout
        self._sock: socket.socket | None = None

    def bind(self) -> None:
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.settimeout(self._timeout)
        self._sock.bind((self._bind_host, self._port))

    def recvfrom(self, bufsize: int) -> tuple[bytes, tuple[str, int]]:
        return self._sock.recvfrom(bufsize)

    def sendto(self, data: bytes, addr: tuple[str, int]) -> None:
        self._sock.sendto(data, addr)

    def close(self) -> None:
        if self._sock:
            self._sock.close()
            self._sock = None
