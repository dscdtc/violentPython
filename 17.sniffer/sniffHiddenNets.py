import optparse
from scapy.all import *

hiddenNets = []
unhiddenNets = []

def sniffDot11(pkt):
    '''Detect hidden 802.11 Beacon and net name'''
    if pkt.haslayer(Dot11ProbeResp):
        addr2 = pkt.getlayer(Dot11).addr2
        if (addr2 in hiddenNets) & (addr2 not in unhiddenNets):
            netName = pkt.getlayer(Dot11ProbeResp).info
            print '[+] Decloaked Hidden SSID: %s for MAC: %s'%\
                (netName, addr2)
            unhiddenNets.append(addr2)
    if pkt.haslayer(Dot11Beacon):
        if pkt.getlayer(Dot11Beacon).info is None:
            addr2 = pkt.getlayer(Dot11).addr2
        if addr2 not in hiddenNets:
            probeReqs.append(netName)
            print '[-] Detected Hidden SSID with MAC: ' + addr2

if __name__ == '__main__':
    interface = 'Microsoft Hosted Network Virtual Adapter'
    sniff(iface=interface, prn=sniffDot11)
