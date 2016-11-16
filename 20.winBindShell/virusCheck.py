##!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os
import time
import httplib
import optparse
from urlparse import urlparse

def uploadFile(fileName):
    print '[*] Uploading file to VirSCAN...' + fileName.split('\\')[-1]
    fileContents = open(fileName, 'rb').read()
    header = {'Content-Type':'multipart/form-data; \
              boundary=---------------------------286132535624094'}
    params ='''
        Content-Length: 3993824

        -----------------------------286132535624094
        Content-Disposition: form-data; name="UPLOAD_IDENTIFIER"

        KEY73e741b97af5edf155f4e89c2eef2821
        -----------------------------286132535624094
        Content-Disposition: form-data; name="langkey"

        1
        -----------------------------286132535624094
        Content-Disposition: form-data; name="setcookie"

        0
        -----------------------------286132535624094
        Content-Disposition: form-data; name="tempvar"


        -----------------------------286132535624094
        Content-Disposition: form-data; name="upfile"; filename='''
    params += fileName.split('\\')[-1] + \
            '\r\n Content-Type: application/octet-stream'
    params += fileContents
    params +='''
        -----------------------------286132535624094
        Content-Disposition: form-data; name="fpath"

        bindshell.exe
        -----------------------------286132535624094--
        '''
    conn = httplib.HTTPConnection('www.virscan.org')
    conn.request('GET', '/',params, header)
    response = conn.getresponse()
    #location = response.getheader('location')
    location = re.findall(r"href=\'http://www.virscan.org/scan/.*\'",\
                          response.read())
    print location
    conn.close()
    return location

def printResults(url):
    status = 200
    host = urlparse(url)[1]
    path = urlparse(url)[2]
    if 'report' not in path:
        while status is not 302:
            conn = httplib.HTTPConnection(host)
            conn.request('GET', path)
            resp = conn.getresponse()
            status = resp.status
            print '[+] Scanning file...'
            conn.close()
            time.sleep(15)
    print '[+] Scan Complete.'
    path = path.replace('scan', 'report')
    conn = httplib.HTTPConnection(host)
    conn.request('GET', path)
    resp = conn.getresponse()
    data = resp.read()
    conn.close()
    reResults = re.findall(u'扫描结果:.*</font>', data)
    print reResults
    htmlSripRes = reResults[1].\
                replace('<font color="#666666">', '').\
                replace('</font>', '')
    print '[+] ' + str(htmlSripRes)

def main():
    usage = "%prog -f <filename>"
    parser = optparse.OptionParser(usage, version="%prog 1.0")
    parser.add_option('-f', dest='fileName', type='string',\
                    help='specify filename to check')
    (options, args) = parser.parse_args()
    fileName = options.fileName

    if fileName is None:
        print parser.print_help()
        exit(0)
    elif os.path.isfile(fileName) is False:
        print '[-] %s does not exist.'
        exit(0)
    else:
        loc = uploadFile(fileName)
        printResults(loc)

if __name__ == '__main__':
    main()
