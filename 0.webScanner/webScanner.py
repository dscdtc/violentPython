__author__ = 'dscdtc'

import os
import sys
import socket

def retBanner(ip, port):
    '''Connect to Web server and return banner.'''
    try:
        socket.setdefaulttimeout(1)
        s = socket.socket()
        s.connect((ip, port))
        s.send('ViolentPython\r\n')
        banner = s.recv(1024)
        return banner
    except:
        return

def checkVulns(banner, filename):
    '''Check Vulnerablity on this server.'''
    f = open(filename, 'r')
    for line in f.readlines():
        if line.strip('\n') in banner:
            print '[+] Server is vulnerable: '+\
                banner.strip('\n')
            return

def main():
    if len(sys.argv) == 2:
        #filename = sys.argv[1]
        filename = 'vuln_banners.txt'
        if not os.path.isfile(filename):
            print '[-] '+filename+' does not exist.'
            exit(0)
        if not os.access(filename, os.R_OK):
            print '[-] '+filename +\
                'access denied.'
            exit(0)
    else:
        print '[-] Usage: '+str(sys.argv[0]) +\
            ' <vuln filename>'
        exit(0)
    portList = [21,22,23,25,80,110,135,137,\
                138,139,443,445,593,1025,2475,\
                3127,3389,6129,8080,8086]
    portList = [445]#
    for x in range (1, 255):
        ip = '121.42.157.'+str(x)
        for port in portList:
            banner = retBanner(ip, port)
            if banner:
                print '[+] %s:%s is open' % (ip, port)
                checkVulns(banner, filename)
            else:
                print '[-] %s:%s is unvulnerable' % (ip, port)
                pass

if __name__ == '__main__':
    __author__ = 'dscdtc'
    main()
