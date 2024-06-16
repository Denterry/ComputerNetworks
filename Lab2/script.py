import click
import socket
from enum import Enum
import subprocess
import platform

MAXSIZE = 1024
MINSIZE = 1
HEADERSIZE = 28
SYSTEM = platform.system().lower()

def reacheable_host(host) -> bool:
        ping = subprocess.Popen(
            f"ping {host} -c 1", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True
        )
        ping.communicate()
        return ping.returncode == 0

def enabled_icmp() -> bool:
    global SYSTEM

    if SYSTEM == "linux":
        try:
            file = open("/proc/sys/net/ipv4/icmp_echo_ignore_all", "r")
            return file.readline()[0] == "0"
        except Exception:
            print("Couldn't open ICMP data.")
            return False
    return True

def ping(host, size) -> bool:
        global SYSTEM

        command = ""
        if SYSTEM == "linux":
            command = f"ping {host} -c 1 -M do -s {size}"
        elif SYSTEM == "darwin":
            command = f"ping {host} -D -s {size} -c 1"
        elif SYSTEM == "windows":
            command = f"ping {host} -n 1 -M do -s {size}"
        else:
            raise Exception(f"Unknown system: {SYSTEM}")

        ping = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True
        )
        print(ping.communicate()[0].decode("utf-8"))
        return ping.returncode == 0

def find_optimal_mtu(host) -> int:
        global MAXSIZE
        global MINSIZE
        global HEADERSIZE

        if not reacheable_host(host):
            print(f"Unreacheable host: {host}!")
            exit(1)
        if not enabled_icmp():
            print(f"Unsupprted ICMP!")
            exit(1)

        mtu = MAXSIZE
        while mtu == MAXSIZE:
            MAXSIZE *= 2
            max_size = MAXSIZE
            min_size = MINSIZE
            while min_size < max_size:
                pkg_size = (min_size + max_size + 1)//2
                if not ping(host=host, size=pkg_size):
                    max_size = pkg_size - 1
                else:
                    min_size = pkg_size
            mtu = min_size

        mtu += HEADERSIZE
        return mtu

@click.command()
@click.option("--host", required=True, help="Host address.")
def main(host):
    try:
        socket.gethostbyname(host)
    except:
        print(f"Invalid host argument {host}")
        exit(1)

    mtu = find_optimal_mtu(host)
    if mtu > 0:
        print(f"MTU: {mtu} bytes", flush=True)


if __name__ == '__main__':
    main()