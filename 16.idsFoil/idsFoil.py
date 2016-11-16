import optparse
from scapy.all import *
from random import randint

def ddosTest(src, dst, iface, count):
    '''
    ddos.rules: alert icmp -> Port:any
        <DDoS TFN Probe> ICMP ID = 678; ICMPE TYPE = 8; Data = 1234
    ......
    '''
    #icmp any <DDoS TFN Probe>
    pkt = IP(src=src, dst=dst)/ICMP(type=8, id=678)/Raw(load='1234')
    send(pkt, iface=iface, count=count)
    #icmp any <DDoS tfn2k icmp possible communication>
    pkt = IP(src=src, dst=dst)/ICMP(type=0)/Raw(load='AAAAAAAAAA')
    send(pkt, iface=iface, count=count)
    #udp 31335 <DDoS Trin00 Daemon to Master PONG message detected>
    pkt = IP(src=src, dst=dst)/UDP(dport=31335)/Raw(load='PONG')
    send(pkt, iface=iface, count=count)
    #icmp any <DDoS TFN client command BE>
    pkt = IP(src=src, dst=dst)/ICMP(type=0, id=456)
    send(pkt, iface=iface, count=count)

def exploitTest(src, dst, iface, count):
    '''
    exploit.tules: alert udp ->
        <EXPLOIT ntalkd x86 Linux overflow>
            content:"|01 03 00 00 00 00 00 01 00 02 02 E8|"
        <EXPLOIT x86 Linux mountd overflow>
            content:"^|B0 02 89 06 FE C8 89|F|04 B0 06 89|F"
    '''
    #udp 518 <EXPLOIT ntalkd x86 Linux overflow>
    pkt = IP(src=src, dst=dst)/UDP(dport=518) \
        /Raw(load='^\x01\x03\x00\x00\x00\x00\x00\x01\x00\x02\x02\xE8')
    send(pkt, iface=iface, count=count)
    #udp 635 <EXPLOIT x86 Linux mountd overflow>
    pkt = IP(src=src, dst=dst)/UDP(dport=635) \
        /Raw(load='^\xB0\x02\x89\x06\xFE\xC8\x89F\x04\xB0\x06\x89F')
    send(pkt, iface=iface, count=count)

def scanTest(src, dst, iface, count):
    #udp 7 <SCAN cybercop udp bomb>
    pkt = IP(src=src, dst=dst)/UDP(dport=7)/Raw(load='cybercop')
    send(pkt, iface=iface, count=count)
    #udp 10080 <SCAN Amanda client version request>
    pkt = IP(src=src, dst=dst)/UDP(dport=10080)/Raw(load='Amanda')
    send(pkt, iface=iface, count=count)

def main():
    usage = "%prog -i<iface> -s <src> -t <target> -c <count>"
    parser = optparse.OptionParser(usage, version="%prog 1.0")
    parser.add_option('-i', dest='iface', type='string',\
                    help='specify network interface')
    parser.add_option('-s', dest='src', type='string',\
                    help='specify source address')
    parser.add_option('-t', dest='tgt', type='string',\
                    help='specify target address')
    parser.add_option('-c', dest='count', type='int',\
                    help='specify packet count')
    (options, args) = parser.parse_args()

    iface = options.iface
    src = options.src
    dst = options.tgt
    count = options.count
    if not iface:
        iface = 'eth0'
    if not src:
        src = '.'.join([str(randint(1,254)) for x in range(4)])
        print 'Creat random src:' + src
    if not dst:
        print parser.print_help()
        exit(0)
    if not count:
        count = 1

    print 'Running ddos test...'
    ddosTest(src, dst, iface, count)
    print 'Running exploit test...'
    exploitTest(src, dst, iface, count)
    print 'Running scan test...'
    scanTest(src, dst, iface, count)

if __name__ == '__main__':
    main()
