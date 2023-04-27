from scapy.all import sr, TCP, IP, IPv6
import argparse
import concurrent.futures
import multiprocessing
import signal
import sys
from modules.probe_subnet import *
from modules.read_targets import *
from modules.scan_ports import *





# 捕捉Ctrl+C信号
def signal_handler(signal, frame):
    print('Stopping...')
    for process in multiprocessing.active_children():
        process.terminate()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)

    parser = argparse.ArgumentParser(description="TCP Port Scanner")
    parser.add_argument("-p", "--ports", help="Port(s) to scan e.g., 80,443,1000-2000 (default: 1-1024)")
    parser.add_argument("-iL", "--inputfilename", help="Target(s) in the file to scan ")
    parser.add_argument("-iR", "--randomtargets", action='store_true', help="Random targets to scan ")
    parser.add_argument("-sS", "--sS", action='store_true', help="Scan ports with TCP SYN packets")
    parser.add_argument("-sL", "--sL", action='store_true', help="List targets you will scan")
    parser.add_argument("-PP", "--PP", action='store_true', help="ICMP ping with type 13")
    parser.add_argument("-PM", "--PM", action='store_true', help="ICMP ping with type 17")
    parser.add_argument("--max_threads", type=int, default=50, help="Maximum number of threads (default: 10)")
    parser.add_argument("--exclude",  help="Exclude hosts/networks")
    parser.add_argument("--excludefile",  help="Exclude list from file")
    parser.add_argument("-F", "--fast", action="store_true",  help="fast scan with few port")
    parser.add_argument('others', nargs=argparse.REMAINDER)
    args = parser.parse_args()

    # READ IP
    if args.inputfilename:
        ips = read_ips_file(sys.argv[-1])
    else:
        ips = read_ips(sys.argv[-1])

    # READ PORTS
    if args.ports:
        ports = read_ports(args.ports)
    elif args.fast:
        ports = read_ports_file_fast("resources/ports_fast.txt")
    else:
        ports = read_ports_file_normal("resources/ports_normal.txt")

    # PORTS --exclude & --ecludefile
    if args.exclude:
        ports.remove(args.exclude)
    elif args.excludefile:
        exclude_ports = read_ports_file_fast(args.excludefile)
        for port in exclude_ports:
            if port in ports:
                ports.remove(port)

    # PROBE SUBNET & SCAN PORTS
    scanner = Scanner(ips, ports)
    prober = Prober(ips, ports)
    if args.sS:
        pass
    elif args.sL:
        scanner.sL()
    elif args.PP:
        prober.PP()
    elif args.PM:
        prober.PM()

