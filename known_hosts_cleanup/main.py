#!/usr/bin/env python

import os
import random
import socket
from subprocess import run

timeout = 3
known_hosts_file = os.path.join(
        os.environ.get('HOME'), '.ssh', 'known_hosts')


def is_open(connection):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect(connection)
        s.shutdown(socket.SHUT_RDWR)
        return True
    except (socket.timeout, socket.gaierror, OSError) as e:
        print(f"{connection}: {e}")
        return False
    finally:
        s.close()


class Host(object):
    def __init__(self, host_string: str):
        object.__init__(self)
        self.addresses = []
        for h in host_string.split(','):
            if ':' in h:
                host_part, port = h.split(':')
                self.add_host_info(host_part[1:-1], int(port))
            else:
                self.add_host_info(h)
        self.is_dead = not is_open(self.addresses[0])

    def add_host_info(self, addr: str, port: int = 22):
        self.addresses.append((addr, port))

    def verify(self):
        result = True
        for host in self.addresses:
            if is_open(host):
                continue
            else:
                return False
        return result

    def __repr__(self):
        return f"{self.addresses} is {'Down' if self.is_dead else 'Up'}"


def main():
    with open(known_hosts_file, 'r') as f:
        lines = f.readlines()
        random.shuffle(lines)
        for line in iter(lines):
            host = Host(line.split(' ')[0])
            if host.is_dead:
                cmd = ['ssh-keygen', '-R', f"{line.split(' ')[0].split(',')[0]}"]
                run(cmd, capture_output=True, encoding='utf-8')
                # print(f"{results.stdout}")


if __name__ == '__main__':
    main()
