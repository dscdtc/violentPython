# -*- coding:utf-8 -*-
__author__ = 'dscdtc'

import urllib2
import optparse
from urlparse import urlsplit
from os import system
from os.path import basename

try:
    from bs4 import BeautifulSoup
except ImportError:
    system("pip install -U beautifulsoup4")
    from bs4 import BeautifulSoup
try:
    from PIL import Image
    from PIL.ExifTags import TAGS
except ImportError:
    system("pip install -U pillow")
    from PIL import Image
    from PIL.ExifTags import TAGS


def findImages(url):
    '''Find all image tags in HTML.'''
    print '[+] Finding images on ' + url
    urlContent = urllib2.urlopen(url).read()
    soup = BeautifulSoup(urlContent, "html.parser")
    imgTags = soup.findAll('img')
    return imgTags

def downloadImage(imgTag):
    try:
        print '[+] Fownloading image...'
        imgSrc = imgTag['src']
        print imgSrc
        imgContent = urllib2.urlopen(imgSrc).read()
        imgFileName = basename(urlsplit(imgSrc)[2])
        imgFile = open(imgFileName, 'wb')
        imgFile.write(imgContent)
        imgFile.close()
        return imgFileName
    except Exception, e:
        print e
        return ''

def testForExif(imgFileName):
    print ("Reading MetaData...")
    try:
        exifData = {}
        imgFile = Image.open(imgFileName)
        info = imgFile._getexif()
        if info:
            print info
            for (tag, value) in info.items():
                decoded = TAGS.get(tag, tag)
                exifData[decoded] = value
            exifGPS = exifData['GPSInfo']
            if exifGPS:
                print '[*] ' + imgFileName + \
                ' contains GPS MetaData'
        else:
            print ("This pic have no MetaData.")
    except:
        print '[-] Get MetaData Failed...'
        return

def main():
    usage = "usage: %prog -u <target url>"
    parser = optparse.OptionParser(usage, version="%prog 1.0")
    parser.add_option('-u', dest='url', type='string',\
                    help='specify target url address')
    (options, args) = parser.parse_args()
    url = options.url
    if url == None:
        print '[-] You must specify a target url.'
        print parser.print_help()
        exit(0)
    imgTags = findImages(url)
    if imgTags:
        print '[+] Fownloading image...\n'
        for imgTag in imgTags:
            imgFileName = downloadImage(imgTag)
            testForExif(imgFileName)
    else:
        print '[-] Get image failed...'

if __name__ == '__main__':
    main()
