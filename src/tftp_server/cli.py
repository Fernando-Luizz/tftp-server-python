import argparse
import sys
from pathlib import Path

from tftp_server.transfer_manager import serve


def main() -> None:
    parser = argparse.ArgumentParser(prog="tftp-server")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=69)
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        sys.exit("root must be an existing directory")
    serve(bind_host=args.host, port=args.port, root_dir=root)


if __name__ == "__main__":
    main()
