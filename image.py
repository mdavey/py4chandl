import httplib
import os
import time


class Image:
    def __init__(self, host, page):
        self.host = host
        self.page = page
        self.download_time = None
        self.download_size = None

    def __str__(self):
        return 'host: %s, page:%s' % (self.host, self.page)

    def get_filename(self):
        return self.page[self.page.rfind('/')+1:]

    def download(self, dest):
        if os.path.exists(dest):
            return False

        start_time = time.time()

        conn = httplib.HTTPSConnection(self.host)
        conn.putrequest('GET', self.page)
        conn.endheaders()
        response = conn.getresponse()
        data = response.read()

        f = open(dest, 'wb+')
        f.write(data)
        f.close()

        self.download_time = time.time() - start_time
        self.download_size = len(data)

        return True

    def download_to(self, directory):
        return self.download(directory + '/' + self.get_filename())