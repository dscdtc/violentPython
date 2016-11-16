# -*- coding:utf-8 -*-
__author__ = 'dscdtc'

import socket
import optparse
import threading

def connScan(tgtHost, tgtPort):
    screenLock = threading.Semaphore(value=1)
    try:
        connSkt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connSkt.connect((tgtHost, tgtPort))
        connSkt.send('ViolentPython\r\n')
        results = connSkt.recv(100)
        screenLock.acquire()
        print '[+] %d/tcp open' % tgtPort
        print '[+] ' + str(results)
    except:
        screenLock.acquire()
        print '\n[-] %d/tcp closed' % tgtPort
    finally:
        screenLock.release()
        connSkt.close()
        
        
def portScan(tgtHost, tgtPorts):
    try:
        tgtIP = socket.gethostbyname(tgtHost)
    except:
        print "[-] Cannot resolve '%s': Unknown host" % tgtHost
        return
    try:
        tgtName = socket.gethostbyaddr(tgtIP)
        print '\n[+] Scan Results for: ' + tgtName[0]
    except:
        print '\n[+] Scan Results for: ' + tgtIP
    socket.setdefaulttimeout(1)
    for tgtPort in tgtPorts:
        print 'Scanning port %s...' % tgtPort
        t = threading.Thread(target=connScan,\
                            args=(tgtHost, int(tgtPort)))
        t.start()
        
def main():

    #解析命令行参数
    #创建OptionParser对象；定义命令行参数;调用parse_args()解析命令行
    usage = "usage: %prog -H <target host> -p <target port>"
    parser = optparse.OptionParser(usage, version="%prog 1.0")
    parser.add_option('-H', dest='tgtHost', type='string',\
                    help='specify target host')
    parser.add_option('-p', dest='tgtPort', type='string',\
                    help='specify target port[s] separated by comma')
    (options, args) = parser.parse_args()

    #按位或运算判断flags是否为空
    tgtHost = options.tgtHost
    tgtPorts = str(options.tgtPort).split(',')
    if (tgtHost == None) | (tgtPorts[0] == None):
        print '[-] You must specify a target host and port[s].'
        print parser.print_help()
        exit(0)

    portScan(tgtHost, tgtPorts)

if __name__ == '__main__':
    main()