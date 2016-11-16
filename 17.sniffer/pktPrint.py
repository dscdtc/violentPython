from scapy.all import *
def pktPrint(pkt):
    '''In order to test detected 802.11 beacon'''
    if pkt.haslayer(Dot11Beacon):
        print '[+] Detected 802.11 Beacon Frame'
    elif pkt.haslayer(Dot11Beacon):
        print '[+] Detected 802.11 Probe Request Frame'
    elif pkt.haslayer(TCP):
        print '[+] Detected a TCP Packet'
    elif pkt.haslayer(DNS):
        print '[+] Detected a DNS Packet'
conf.iface = 'Realtek RTL8723BE Wireless LAN 802.11n PCI-E NIC'
sniff(prn=pktPrint)
