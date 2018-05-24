# -*- coding: utf-8 -*-

import urllib2


def do_crawler(url, header=None, param=None):
    if header is None:
        header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        }
    request = urllib2.Request(url, param, header)
    return urllib2.urlopen(request, timeout=10).read()
