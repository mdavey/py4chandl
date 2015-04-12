#!/usr/bin/env python

import imp
import os
from glob import glob
import argparse

from aria2rpc import Aria2Rpc
from downloadpool import DownloadPool
from downloadhttps import download_url


def load_plugins(directory):
    plugins = []
    for filename in glob(os.path.join(directory, '*.py')):
        if filename == os.path.join(directory, '__init__.py'):
            continue
        plugin_name = os.path.basename(filename).split('.')[0]
        plugin_details = imp.find_module(plugin_name, [directory])
        plugins.append(imp.load_module(plugin_name, *plugin_details))
    return plugins


def get_images_for_url(url):
    for plugin in load_plugins('sites'):
        if plugin.can_handle(url):
            print 'Using plugin', plugin.get_name()
            page_html = download_url(url)
            return plugin.get_images(page_html)

    return None


def download_images_internally(dest, images, pool):
    if not os.path.exists(dest):
        os.makedirs(dest)

    thread_pool = DownloadPool(pool)

    for image in images:
        thread_pool.add_file(image)

    print "Found {count} images".format(count=len(images))
    thread_pool.download(dest)
    print "Done"


def download_images_aria2(dest, images):
    # http://ziahamza.github.io/webui-aria2/
    aria2rpc = Aria2Rpc('http://localhost:6800/jsonrpc')
    print aria2rpc.request('aria2.getGlobalStat', [[]])

    for image in images:
        print aria2rpc.request('aria2.addUri', [[image], {'dir': dest}])

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