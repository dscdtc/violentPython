# -*- coding:utf-8 -*-
__author__ = 'dscdtc'

import nmap
import optparse
import threading

def nmapScan(tgtHost, tgtPort):
    nmScan = nmap.PortScanner()
    nmScan.scan(tgtHost, tgtPort)
    state = nmScan[tgtHost]['tcp'][int(tgtPort)]['state']
    print (" [*] %s tcp/%s %s") % (tgtHost, tgtPort, state)
        
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

    for tgtPort in tgtPorts:
        nmapScan(tgtHost, tgtPort)

if __name__ == '__main__':
    main()