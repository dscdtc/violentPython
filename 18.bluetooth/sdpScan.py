#SDP is Bluetooth Service Discovery Protocol
from bluetooth import *
def sdpBrowse(addr):
    services = find_service(address=addr)
    for service in services:
        name = str(service['name'])
        proto = str(service['protocol'])
        port = str(service['port'])
        print '[+] Found %s on %s:%s' % (name, proto, port)

sdpBrowse('74:AC:5F:33:25:A5')
