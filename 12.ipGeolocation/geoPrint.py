__author__ = 'dscdtc'

import os
import socket
import optparse

try:
    import pygeoip
except:
    os.system("pip install -U pygeoip")
    import pygeoip
try:
    import dpkt
except:
    os.system("pip install -U dpkt")
    import dpkt

datPath = os.path.split(os.path.realpath(__file__))[0] \
        +'\GeoLiteCity.dat'
gi = pygeoip.GeoIP(datPath)

def retGeoStr(ip):
    try:
        rec = gi.record_by_name(ip)
        city = rec['city']
        country = rec['country_code3']
        if city:
            geoLoc = city + ', ' + country
        else:
            geoLoc = country
        return geoLoc
    except:
        return 'Unregistered!!'

def printPcap(pcap):
    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)
            print '[+] Src: %s --> Dst: %s' %\
                (src, dst)
            print '[+] Src: %s --> Dst: %s' %\
                (retGeoStr(src), retGeoStr(dst))
        except:
            pass

def main():
    usage = "%prog -p <pcap file>"
    parser = optparse.OptionParser(usage, version="%prog 1.0")
    parser.add_option('-p', dest='pcapFile', type='string',\
                    help='specify pcap filename')
    (options, args) = parser.parse_args()
    pcapFile = options.pcapFile
    if pcapFile == None:
        print parser.print_help()
        exit(0)

    f = open(pcapFile)
    pcap = dpkt.pcap.Reader(f)
    printPcap(pcap)

if __name__ == '__main__':
    main()
