__author__ = 'dscdtc'
import os

try:
    import pygeoip
except:
    os.system("pip install -U pygeoip")
    import pygeoip

datPath = os.path.split(os.path.realpath(__file__))[0] \
        +'\GeoLiteCity.dat'
gi = pygeoip.GeoIP(datPath)

def printRecord(tgt):
    rec = gi.record_by_name(tgt)
    city = rec['city']
    region = rec['region_code']
    country = rec['country_code']
    long = rec['longitude']
    lat = rec['latitude']
    print '\n[*] Target: %s Geo-located.' % tgt
    print '[+] %s, %s, %s' % \
            (str(city), str(region), str(country))
    print '[+] Latitude: %s, Longitude: %s' % \
            (str(lat), str(long))

def main():
    tgt = '27.221.104.74'
    printRecord(tgt)

if __name__ == '__main__':
    main()
