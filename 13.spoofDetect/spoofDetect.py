import os
import optparse
from scapy.all import *
try:
    from IPy import IP as IPTEST
except:
    os.system('pip -U install IPy')
    from IPy import IP as IPTEST #avoid conflict with Scapy.IP

ttlValues = {}
THRESH = 5
def checkTTL(ipsrc, ttl):
    #remove private IP such as: 10.*.*.*\192.168.*.*\172.16.0.0~172.31.255.255
    if IPTEST(ipsrc).iptype() == 'PRIVATE':
        return
    if not ttlValues.has_key(ipsrc):
        pkt = srl(IP(dst=ipsrc) / ICMP(), \
                retry=0, timeout=1, verbose=0)
        ttlValues[ipsrc] = pkt.ttl
    if abs(int(ttl) - int(ttlValues[ipsrc])) > THRESH:
        print ('\n[!] Detected Possible Spoofed Packet From: '\
                + ipsrc)
        print ('[!] TTL: %s, Actual TTL: ' + str(ttlValues[ipsrc]))

def testTTL(pkt):
    try:
        if pkt.haslayer(IP):
            ipsrc = pkt.getlayer(IP).src
            ttl = str(pkt.ttl)
            #print '[+] Pkt Received From: %s with TTL:' % ipsrc + ttl
            checkTTL()
    except:
        pass

def main():
    usage = "%prog -i <interface> -t <thresh>"
    parser = optparse.OptionParser(usage, version="%prog 1.0")
    parser.add_option('-i', dest='iface', type='string',\
                        help='specify network interface')
    parser.add_option('-t', dest='thresh', type='string',\
                        help='specify threshold count')
    (options, args) = parser.parse_args()
    conf.iface = options.iface
    THRESH = options.thresh
    if not conf.iface:
        conf.iface = 'eth0'
    if not THRESH:
        THRESH = 5

    sniff(prn=testTTL, store=0)

if __name__ == '__main__':
    main()
