#OUI search at http://regauth.standards.ieee.org/standards-ra-web/pub/view.html#registries
from scapy.all import *
from bluetooth import *

def retBtAddr(addr):
    btAddr = str(hex(int(addr.replace(':', ''), 16) + 1))[2:]
    btAddr = btAddr[:2]+':'+btAddr[2:4]+':'+btAddr[4:6]+':'+\
            btAddr[6:8]+':'+btAddr[8:10]+':'+btAddr[10:12]
    return btAddr

def checkBluetooth(btAddr):
    btName = lookup_name(btAddr)
    if btName:
        print '[+] Dectected Bluetooth Device: ' + btName
    else:
        print '[-] Fail to Detect Bluetooth Device.'

def wifiPrint(pkt):
    iPhone4S_OUI = 'd0:23:db'
    if pkt.haslayer(Dot11):
        wifiMAC = pkt.getlayer(Dot11).addr2
        if iPhone4S_OUI == wifiMAC[:8]:
            print '[*] Detected iPhone4S MAC: ' + wifiMAC
            btAddr = retBtAddr(wifiMAC)
            print '[+] Testing Bluetooth MAC: ' + btAddr
            checkBluetooth(btAddr)

if __name__ == '__main__':
    conf.iface = 'Realtek RTL8723BE Wireless LAN 802.11n PCI-E NIC'
    sniff(prn=wifiPrint)
