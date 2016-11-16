from bluetooth import *
def rfcommCon(addr, port):
    sock = BluetoothSocket(RFCOMM)
    try:
        sock.connect((addr, port))
        print '[+] RFCOMM Port ' + str(port) + ' open'
        sock.close()
    except Exception, e:
        print '[-] RFCOMM Port ' + str(port) + ' closed'
for port in range(1, 30):
    rfcommCon('68:76:4F:50:CB:3C', port)
    #'A4:5E:60:F2:91:A4';'4F:A7:EE:EF:1D:CB';'41:9A:C8:D4:EA:0C'
    '''
[*] Found Bluetooth Device: QiKU~gaozhibin
[+] MAC address: 74:AC:5F:33:25:A5
    [+] RFCOMM Port 21 open
    [+] RFCOMM Port 22 open
    [+] RFCOMM Port 23 open
[*] Found Bluetooth Device: Xperia Z1
[+] MAC address: 68:76:4F:50:CB:3C

[*] Found Bluetooth Device:
[+] MAC address: EC:5A:86:41:5B:AF
    '''
