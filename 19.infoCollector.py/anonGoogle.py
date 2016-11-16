##!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import urllib
import optparse
from anonBrowser import *

class Google_Result:
    def __init__(self, title, text, url):
        self.title = title
        self.text = text
        self.url = url
    def __repr__(self):
        return self.title

def google(search_term):
    ab = anonBrowser()
    ab.anonymize()
    search_term = urllib.quote_plus(search_term)
    response = ab.open('https://cse.google.com'+\
            '/cse/publicurl?cx=001525899533114698157:dddpeaabyrc'+\
            '&num=15&alt=json&q=' + search_term)
    print response.read()
    objects = json.load(response)
    #print objects
    results = []
    for result in objects['responseData']['results']:
        url = result['url']
        title = result['titleNoFormatting']
        text = result['content']
        new_gr = Google_Result(title, text, url)
        results.append(new_gr)
    return results

def main():
    usage = "%prog -k <keywords>"
    parser = optparse.OptionParser(usage, version="%prog 1.0")
    parser.add_option('-k', dest='keyword', type='string',\
                    help='specify target url')
    (options, args) = parser.parse_args()
    keyword = options.keyword
    if keyword is None:
        print parser.print_help()
        exit(0)
    else:
        results = google(keyword)
        print results

if __name__ == '__main__':
    main()
