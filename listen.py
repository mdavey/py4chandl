#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import urlparse
import os

from siteplugins import get_plugin_for_url
from downloadpool import DownloadPool
from downloadhttps import download_url

# This is a really horrible thing
# Don't use it
# We've a threaded server, running a method that starts more threads without proper communication between the layers
# I'm not sure why it even works the way it does
# ... Turns out it doesn't work the way I thought it did.  Weird.  But expected.
#
# Reason for this abomination  (it's a bookmarklet)
# javascript:
# var new_url = 'http://127.0.0.1:8080/?u=' + window.location.href + '&p=' + prompt('Download directory', 'test');
# window.open(new_url);


class CustomHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global download_pool

        url_components = urlparse.urlparse(self.path)
        url_query = urlparse.parse_qs(url_components.query)

        if 'u' in url_query and 'p' in url_query:
            try:

                url = url_query['u'][0]
                plugin = get_plugin_for_url(url)

                if plugin is None:
                    self.done('No plugin found for: ' + url)
                    return

                images = plugin.get_images(download_url(url))

                if len(images) == 0:
                    self.done('No images found')
                    return

                path = 'c:/images/test/' + url_query['p'][0]
                if not os.path.exists(path):
                    os.makedirs(path)

                for image in images:
                    download_pool.add_file(image, path)

                self.done(str(len(images)) + ' queued for download')

            except Exception, e:
                self.done('Error: ' + e.message)
        else:
            self.done('Missing params: ' + repr(url_query))

    def done(self, text):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(text)
        return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


if __name__ == '__main__':

    download_pool = DownloadPool(4)
    download_pool.start()
    server = ThreadedHTTPServer(('127.0.0.1', 8088), CustomHandler)
    print 'Listening on 127.0.0.1:8088'

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print 'Server stopping'
        server.socket.close()
        print 'Waiting for download pool to finish'
        download_pool.join()
        print 'Done'
