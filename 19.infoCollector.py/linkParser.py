#!/usr/bin/env python
# -*- coding: utf-8 -*-
#此脚本为链接解析器（Praser）使用时采取BS方法
from anonBrowser import *
from bs4 import BeautifulSoup
import os
import re
import optparse

def printLinks(url):
    ab = anonBrowser()
    ab.anonymize()#sleep = True
    page = ab.open(url)
    html = page.read()
    try:
        print '[+] Printing Links From Regex.'
        link_finder = re.compile('href="(.*?)"')
        links = link_finder.findall(html)
        for link in links:
            print link
    except Exception,e:
        print e
        pass
    try:
        print '\n[+] Printing Links From BeautifulSoup.'
        soup = BeautifulSoup(html, "html.parser")
        links = soup.findAll(name='a')
        for link in links:
            if link in links:
                if link.has_key('href'):
                    print link['href']
    except:
        pass

def main():
    usage = "%prog -u <target url>"
    parser = optparse.OptionParser(usage, version="%prog 1.0")
    parser.add_option('-u', dest='tgtURL', type='string',\
                    help='specify target url')
    (options, args) = parser.parse_args()
    url = options.tgtURL
    if url is None:
        print parser.print_help()
        exit(0)
    else:
        printLinks(url)

if __name__ == '__main__':
    main()
