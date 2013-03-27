__author__ = 'Matthew'

import httplib
import os


class Image:
    def __init__(self, host, page):
        self.host = host
        self.page = page

    def __str__(self):
        return 'host: %s, page:%s' % (self.host, self.page)

    def get_filename(self):
        return self.page[self.page.rfind('/')+1:]

    def download(self, dest):
        if os.path.exists(dest):
            print 'Skipping image %s%s to %s' % (self.host, self.page, dest)
            return

        print 'Downloading image %s%s to %s' % (self.host, self.page, dest)

        conn = httplib.HTTPSConnection(self.host)
        conn.putrequest('GET', self.page)
        conn.endheaders()
        response = conn.getresponse()
        data = response.read()

        file = open(dest, 'wb+')
        file.write(data)

    def download_to(self, directory):
        self.download(directory + '/' + self.get_filename())