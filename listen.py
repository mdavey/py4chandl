#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import urlparse

import dl


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
        url_components = urlparse.urlparse(self.path)
        url_query = urlparse.parse_qs(url_components.query)
        print(repr(url_query))
        if 'u' in url_query and 'p' in url_query:
            try:
                image_count = dl.main(url_query['u'][0], 'c:/images/test/' + url_query['p'][0], 4, False)
                self.done('Done.  Downloaded ' + str(image_count) + ' images')
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
    server = ThreadedHTTPServer(('127.0.0.1', 8080), CustomHandler)
    print 'Listening on 127.0.0.1:8080'

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print 'Server stopping'
        server.socket.close()