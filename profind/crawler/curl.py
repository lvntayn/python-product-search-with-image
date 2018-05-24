#!/usr/bin/python
# -*- coding: utf-8 -*-

import pycurl
import certifi
from io import BytesIO
import urllib.request


class Curl(object):
    def fetch(self, url):
        """ Fetches html codes from given url """
        c = pycurl.Curl()
        b = BytesIO()
        c.setopt(c.URL, url)
        # disabled debugging
        c.setopt(c.VERBOSE, 0)
        # path to Certificate Authority (CA) bundle
        c.setopt(pycurl.CAINFO, certifi.where())
        # user agent
        c.setopt(c.HTTPHEADER, ["User-Agent: Mozilla/5.001 (windows; U; NT4.0; en - us) Gecko / 25250101", "Agent: "])
        # output of fetched url
        c.setopt(c.WRITEDATA, b)
        # follow HTTP 3xx redirects. 1 is to enable
        c.setopt(c.FOLLOWLOCATION, 1)
        # timeout for the connect phase
        c.setopt(c.CONNECTTIMEOUT, 30)
        # maximum time an operation is allowed to tak
        c.setopt(c.TIMEOUT, 300)
        #  skip all signal handling
        c.setopt(c.NOSIGNAL, 1)
        # maximum number of redirects allowed
        c.setopt(c.MAXREDIRS, 5)
        # verify the peer's SSL certificate
        c.setopt(c.SSL_VERIFYPEER, False)
        c.perform()
        c.close()
        return b.getvalue()

    def download(self, url, path):
        """ Download file to path from given url """
        urllib.request.urlretrieve(url, path)
