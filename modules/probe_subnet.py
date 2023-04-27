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

    #在IPv4中，私有IP地址范围是：
        #10.0.0.0 到 10.255.255.255
        #172.16.0.0 到 172.31.255.255
        #192.168.0.0 到 192.168.255.255
    #这些IP地址不会被路由器转发到Internet上，并且只在局域网或组织内部使用。
    #所以，当你试图探测内网中的其他IP地址时，因为不知道对方的MAC地址，所以不得不广播ARP查询来查找对方的地址

    # ICMP ping: 时间戳请求--code13
    def PP(self):
        icmp = ICMP(type=13, code=0)
        ip = IP(src=self.host_ip, dst=self.target_ips)
        packet = ip / icmp
        ans, unans = sr(packet, timeout=3, threaded=True, retry=1) #verbose参数调整输出的详细程度

    # ICMP ping: 地址掩码请求--code17
    def PM(self):
        icmp = ICMP(type=17, code=0)
        ip = IP(src=self.host_ip, dst=self.target_ips)
        packet = ip / icmp
        ans, unans = sr(packet, timeout=3, threaded=True, retry=1)
        ans.summary()
