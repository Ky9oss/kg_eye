import sys
import re

#从命令行参数中读取IP地址列表
def read_ips(ip_arg):
    return [ip.strip() for ip in ip_arg.split(',')]

#从用户的txt文件中读取IP地址列表
def read_ips_file(filename):
    if filename.endswith('.txt'):
        with open(filename, 'r') as f:
            return [line.strip() for line in f.readlines()]
    else:
        print("Please use txt file!")
        sys.exit()

#-F 从ports_fast文件中读取port
def read_ports_file_fast(filename):
    if filename.endswith('.txt'):
        with open(filename, 'r') as f:
            return [line.strip() for line in f.readlines()]
    else:
        print("Please use txt file!")
        sys.exit()


#不加-p或-F时，从ports_normal文件中读取端口
def read_ports_file_normal(filename):
    if filename.endswith('.txt'):
        with open(filename, 'r') as f:
            ports=[]
            for line in f.readlines():
                port = re.search(r"(\d+)/(?:tcp|udp)", line)
                if port:
                    ports.append(port.group(1))
            return ports
    else:
        print("Please use txt file!")
        sys.exit()


#从命令行参数或txt文件中读取端口号列表
def read_ports(port_arg):
    ports = []
    for port_range in port_arg.split(','):
        if '-' in port_range:
            start_port, end_port = port_range.split('-')
            ports += list(range(int(start_port), int(end_port)+1))
        else:
            ports.append(int(port_range))
    return ports

