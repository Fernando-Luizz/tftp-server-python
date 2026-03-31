from pathlib import Path

from tftp_server.packet_api import (
    parse_datagram,
    build_data,
    build_ack,
    build_error,
    OP_RRQ,
    OP_WRQ,
)

from tftp_server.udp_adapter import UdpSocketAdapter
from tftp_server.file_access import FileAccess


def serve(bind_host: str, port: int, root_dir: Path) -> None:
    udp = UdpSocketAdapter(bind_host, port)
    udp.bind()

    fs = FileAccess(root_dir)

    print(f"TFTP server running on {bind_host}:{port}")

    while True:
        try:
            data, addr = udp.recvfrom(1024)
        except TimeoutError:
            continue

        try:
            packet = parse_datagram(data)

            if packet["opcode"] == OP_RRQ:
                handle_rrq(udp, fs, packet, addr)

            elif packet["opcode"] == OP_WRQ:
                handle_wrq(udp, fs, packet, addr)

        except Exception as e:
            err = build_error(0, str(e))
            udp.sendto(err, addr)


def handle_rrq(udp, fs, packet, addr):
    filename = packet["filename"]

    block = 1
    offset = 0

    while True:
        chunk = fs.read_chunk(filename, offset, 512)

        udp.sendto(build_data(block, chunk), addr)

        resp, _ = udp.recvfrom(1024)
        ack = parse_datagram(resp)

        if ack["opcode"] != 4 or ack["block"] != block:
            continue

        if len(chunk) < 512:
            break

        offset += 512
        block += 1


def handle_wrq(udp, fs, packet, addr):
    filename = packet["filename"]

    udp.sendto(build_ack(0), addr)

    expected_block = 1

    while True:
        data, _ = udp.recvfrom(1024)
        pkt = parse_datagram(data)

        if pkt["opcode"] != 3:
            continue

        if pkt["block"] == expected_block:
            fs.write_chunk(filename, pkt["data"], append=True)

            udp.sendto(build_ack(expected_block), addr)

            if len(pkt["data"]) < 512:
                break

            expected_block += 1