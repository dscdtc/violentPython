##!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import optparse
from anonBrowser import *
from bs4 import BeautifulSoup

def mirrorImages(url, dir):
    ab = anonBrowser()
    ab.anonymize()
    html = ab.open(url)
    soup = BeautifulSoup(html, "html.parser")
    image_tags = soup.findAll('img')
    for image in image_tags:
        filename = image['src'].lstrip('http://')
        filename = os.path.join(dir, \
            filename.split('%2F')[-1].replace('/','_').split('?')[0])
        print '[+] Saving ' + str(filename)
        data = ab.open(image['src']).read()
        ab.back()
        save = open(filename, 'wb')
        save.write(data)
        save.close()

def main():
    usage = "%prog -u <target url> -d <destination directory>"
    parser = optparse.OptionParser(usage, version="%prog 1.0")
    parser.add_option('-u', dest='tgtURL', type='string',\
                    help='specify target url')
    parser.add_option('-d', dest='dir', type='string',\
                    help='specify destina directory')
    (options, args) = parser.parse_args()
    url = options.tgtURL
    dir = options.dir
    if (url and dir) is None:
        print parser.print_help()
        exit(0)
    else:
        try:
            mirrorImages(url, dir)
        except Exception, e:
            print '[-] Error Mirroring Images.'
            print '[-] ' + str(e)

if __name__ == '__main__':
    main()
