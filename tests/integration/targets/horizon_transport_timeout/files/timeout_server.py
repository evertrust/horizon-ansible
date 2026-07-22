# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

import argparse
import os
import socket
import time


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("connect", "read"))
    parser.add_argument("port_file")
    parser.add_argument("completion_file")
    return parser.parse_args()


def main():
    args = parse_args()
    blockers = []
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(("127.0.0.1", 0))
    listener.listen(1)
    listener.settimeout(0.1)

    if args.mode == "connect":
        # Fill the loopback accept queue without accepting connections so the
        # SDK's subsequent TCP connection attempt reaches its connect timeout.
        for _unused in range(32):
            blocker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            blocker.setblocking(False)
            blocker.connect_ex(listener.getsockname())
            blockers.append(blocker)

    with open(args.port_file, "w", encoding="utf-8") as port_file:
        port_file.write(str(listener.getsockname()[1]))

    try:
        if args.mode == "read":
            while not os.path.exists(args.completion_file):
                try:
                    connection, _address = listener.accept()
                except socket.timeout:
                    continue

                with connection:
                    connection.settimeout(1)
                    connection.recv(65536)
                    time.sleep(1)
                break
        else:
            while not os.path.exists(args.completion_file):
                time.sleep(0.1)
    finally:
        for blocker in blockers:
            blocker.close()
        listener.close()


if __name__ == "__main__":
    main()
