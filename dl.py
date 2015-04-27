#!/usr/bin/env python

import os
import argparse

from aria2rpc import Aria2Rpc
from downloadpool import DownloadPool
from downloadhttps import download_url
from siteplugins import get_plugin_for_url


def get_images_for_url(url):
    plugin = get_plugin_for_url(url)

    if plugin is None:
        return None

    print 'Using plugin', plugin.get_name()
    page_html = download_url(url)
    return plugin.get_links(page_html)


def download_images_internally(dest, links, pool):
    if not os.path.exists(dest):
        os.makedirs(dest)

    thread_pool = DownloadPool(pool)

    for link in links:
        thread_pool.add_file(link.url, dest, link.name)

    print "Found {count} images".format(count=len(links))
    thread_pool.start()
    thread_pool.join()
    print "Done"


def download_images_aria2(dest, links):
    # http://ziahamza.github.io/webui-aria2/
    aria2rpc = Aria2Rpc('http://localhost:6800/jsonrpc')
    print aria2rpc.request('aria2.getGlobalStat', [[]])

    for link in links:
        print aria2rpc.request('aria2.addUri', [[link.url], {'dir': dest}])

    print aria2rpc.request('aria2.getGlobalStat', [[]])
    print 'Images sent'


def main(url, destination, pool_size=4, with_aria2=False):
    images = get_images_for_url(url)

    if images is None:
        raise(Exception('No plugin was found to handle url'))
    elif len(images) == 0:
        raise(Exception('No images found'))
    elif with_aria2:
        download_images_aria2(destination, images)
    else:
        download_images_internally(destination, images, pool_size)

    return len(images)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download all images from a page to a directory')
    parser.add_argument('url', help='Source url')
    parser.add_argument('dest', help='Destination directory')
    parser.add_argument('--pool', type=int, help='Number of concurrent downloads (default: 4)', default=4)
    parser.add_argument('--aria2', action='store_true', help='Send downloads to local aria2 daemon')
    args = parser.parse_args()

    main(args.url, args.dest, args.pool, args.aria2)