import re
import optparse
from scapy.all import *
cookieTable = {}

def fireCatcher(pkt):
    raw = pkt.sprintf('%Raw.load%')
    r = re.findall('wordpress_[0-9a-fA-F]{32}', raw)
    if r and 'Set' not in raw:
        if r[0] not in cookieTable.keys():
            cookieTable[r[0]] = pkt.getlayer(IP).src
            print '[+] Detected and indexed cookie.'
        elif cookieTable[r[0]] != pkt.getlayer(IP).src

def main():
    usage = "%prog -i <interface>"
    parser = optparse.OptionParser(usage, version="%prog 1.0")
    parser.add_option('-i', dest='interface', type='string',\
                    help='specify interface to listen on')
    (options, args) = parser.parse_args()

    if options.interface is None:
        print parser.print_help()
        exit(0)
    else:
        conf.iface = options.interface
    try:
        print '[*] Starting Hotel Guest Sniffer...'
        sniff(filter='tcp port 80', prn=fireCatcher)
    except KeyboardInterrupt:
        exit(0)

if __name__ == '__main__':
    main()
