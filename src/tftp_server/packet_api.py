import struct

OP_RRQ = 1
OP_WRQ = 2
OP_DATA = 3
OP_ACK = 4
OP_ERROR = 5


def parse_datagram(data: bytes) -> dict:
    opcode = struct.unpack("!H", data[:2])[0]

    if opcode == OP_RRQ or opcode == OP_WRQ:
        parts = data[2:].split(b"\x00")
        filename = parts[0].decode()
        mode = parts[1].decode()
        return {
            "opcode": opcode,
            "filename": filename,
            "mode": mode,
        }

    elif opcode == OP_DATA:
        block = struct.unpack("!H", data[2:4])[0]
        payload = data[4:]
        return {
            "opcode": opcode,
            "block": block,
            "data": payload,
        }

    elif opcode == OP_ACK:
        block = struct.unpack("!H", data[2:4])[0]
        return {
            "opcode": opcode,
            "block": block,
        }

    elif opcode == OP_ERROR:
        code = struct.unpack("!H", data[2:4])[0]
        message = data[4:-1].decode()
        return {
            "opcode": opcode,
            "code": code,
            "message": message,
        }

    else:
        raise ValueError("Invalid opcode")


def build_data(block: int, payload: bytes) -> bytes:
    return struct.pack("!HH", OP_DATA, block) + payload


def build_ack(block: int) -> bytes:
    return struct.pack("!HH", OP_ACK, block)


def build_error(code: int, message: str) -> bytes:
    return struct.pack("!HH", OP_ERROR, code) + message.encode() + b"\x00"