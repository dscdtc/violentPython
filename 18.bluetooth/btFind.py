from time import sleep
from bluetooth import *
from datetime import datetime
tgtName = 'Xperia Z1'


print '[*] Scanning for Bluetooth Device: ' + tgtName,
def findTgt(tgtName):
    foundDevs = discover_devices(lookup_names=True)
    for (addr, name) in foundDevs:
        if tgtName == name:
        #is compare with id ;== compare with value
            print '\n[+] Found Target Device ' + tgtName
            print '[+] With MAC Address: ' + addr
            print '[+] Time is: '+str(datetime.now())

while True:
    print '.',
    try:
        findTgt(tgtName)
    except IOError:
        pass
    sleep(5)
