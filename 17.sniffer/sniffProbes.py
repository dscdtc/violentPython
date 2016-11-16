import optparse
from scapy.all import *

probeReqs = []

def sniffProbe(pkt):
    '''Detect 802.11 Probe Requests'''
    if pkt.haslayer(Dot11ProbeReq):
        netName = pkt.getlayer(Dot11ProbeReq).info
        if netName not in probeReqs:
            probeReqs.append(netName)
            print '[+] Detected Source IP: ' + pkt.getlayer(IP).src
            print '[+] Detected New Probe Request: ' + netName

if __name__ == '__main__':
    interface = 'Microsoft Hosted Network Virtual Adapter'
    sniff(iface=interface, prn=sniffProbe)
