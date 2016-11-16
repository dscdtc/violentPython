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
    import dpkt #operating with *.pcap
except:
    os.system("pip install -U dpkt")
    import dpkt

currentPath = os.path.split(os.path.realpath(__file__))[0]
gi = pygeoip.GeoIP(currentPath+'\GeoLiteCity.dat')

def retKML(ip):
    rec = gi.record_by_name(ip)
    try:
        longitude = rec['longitude']
        latitude = rec['latitude']
        kml = (
            '<Placemark>\n'
            '<name>%s</name>\n'
            '<Point>\n'
            '<coordinates>%6f,%6f</coordinates>\n'
            '</Point>\n'
            '</Placemark>\n'
        ) % (ip, longitude, latitude)
        return kml
    except:
        return ''

def retGeoStr(ip):
#    try:
        rec = gi.record_by_name(ip)
        city = rec['city']
        country = rec['country_code3']
        if city:
            geoLoc = city + ', ' + country
        else:
            geoLoc = country
        return geoLoc
#    except:
#        return 'Unregistered!!'

def plotIPs(pcap):
    kmlPts = ''
    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            srcKML = retKML(src)
            dst = socket.inet_ntoa(ip.dst)
            dstKML = retKML(dst)
            kmlPts = kmlPts + srcKML + dstKML
        except:
            pass
    return kmlPts

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

    kmlHeader = '<?xml version="1.0" encoding="UTF-8"?>\
        \n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n'
    kmlFooter = '</Document>\n</kml>\n'
    f = open(pcapFile)
    pcap = dpkt.pcap.Reader(f)
    kmlDoc = kmlHeader + plotIPs(pcap) + kmlFooter
    f.close()
    f = open('.\GeoIP.kml','w')
    f.write(kmlDoc)
    f.close()
    print kmlDoc


if __name__ == '__main__':
	main()
