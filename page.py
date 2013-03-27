__author__ = 'Matthew'

import httplib

from bs4 import BeautifulSoup

from image import Image


class Page:
    def __init__(self, host, page):
        self.host = host
        self.page = page
        self.contents = False

    def download(self):
        print "Downloading page %s%s" % (self.host, self.page)
        conn = httplib.HTTPSConnection(self.host)
        conn.putrequest('GET', self.page)
        conn.endheaders()
        response = conn.getresponse()
        self.contents = response.read()

    def get_images(self):
        page_seen = []

        soup = BeautifulSoup(self.contents)

        for link in soup.find_all('a'):
            href = link.get('href')
            if href is not None and href[:18] == '//images.4chan.org':
                host = 'images.4chan.org'
                page = href[18:]

                if page not in page_seen:
                    yield Image(host, page)
                    page_seen.append(page)