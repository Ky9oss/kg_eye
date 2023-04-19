from re import T
from scapy.all import sr, TCP, IP, ICMP
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

class Prober():
    def __init__(self, target_ips, target_ports) -> None:
        self.host_ip = get_host_ip()
        self.target_ips = target_ips
        self.target_ports = target_ports

    # ICMP ping: 时间戳请求--code13
    def PP(self):
        icmp = ICMP(type=13, code=0)
        ip = IP(src=self.host_ip, dst=self.target_ips)
        packet = ip / icmp
        ans, unans = sr(packet, timeout=3, threaded=True, retry=2)
        ans.summary()

    # ICMP ping: 地址掩码请求--code17
    def PM(self):
        icmp = ICMP(type=17, code=0)
        ip = IP(src=self.host_ip, dst=self.target_ips)
        packet = ip / icmp
        ans, unans = sr(packet, timeout=3, threaded=True, retry=2)
        ans.summary()
