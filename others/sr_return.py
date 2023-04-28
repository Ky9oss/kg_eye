from scapy.all import * 

packet = IP(src='127.0.0.1', dst='127.0.0.1')/TCP(dport=[21,22,23], flags='S')
ans, unans = sr(packet, timeout=2)
print('---------------------------------------')
print(ans)
print(type(ans))
print(ans.stats)
print(ans.res)
print('---------------------------------------')
print(unans)
print(type(unans))
print(unans.stats)
print(unans.res)
for r in unans.res:
    print(r)
