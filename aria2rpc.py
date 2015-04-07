#!/usr/bin/env python

import urllib2
import json


class Aria2Rpc(object):
    def __init__(self, host):
        self.host = host

    def request(self, method, params):
        req = json.dumps({'jsonrpc': '2.0',
                          'id': 'chan',
                          'method': method,
                          'params': params})
        conn = urllib2.urlopen(self.host, req)

        return json.loads(conn.read())
