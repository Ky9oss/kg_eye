from scapy.all import sr, TCP, IP, IPv6
import socket
import sys
import threading 


# 获取自己的IP
def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
    except Exception as e:
        #print(f'{e}')
        sys.exit()
    return ip

class Scanner():
    def __init__(self, target_ips, target_ports) -> None:
        self.host_ip = get_host_ip()
        self.target_ips = target_ips
        self.target_ports = target_ports

    def sS(self):
        try:
            pass
        finally:
            print("Done")

    def sL(self):
        print(">>>将要扫描的ip:")
        for ip in self.target_ips:
            print(f"Target: {ip}")
        print(">>>将要扫描的port:")
        for port in self.target_ports:
            print(f"Port: {port}")

