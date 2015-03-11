#!/usr/bin/env python

import imp
import os
from glob import glob
import argparse

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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download all images from a page to a directory')
    parser.add_argument('url', help='Source url')
    parser.add_argument('dest', help='Destination directory')
    parser.add_argument('--pool', type=int, help='Number of concurrent downloads (default: 4)', default=4)
    args = parser.parse_args()

    images = None

    for plugin in load_plugins('sites'):
        if plugin.can_handle(args.url):
            print 'Using plugin', plugin.get_name()
            page_html = download_url(args.url)
            images = plugin.get_images(page_html)
            break

    if images is None:
        print 'No plugin was found to handle url'
    elif len(images) == 0:
        print 'No images found to download'
    else:
        if not os.path.exists(args.dest):
            os.makedirs(args.dest)

        thread_pool = DownloadPool(args.pool)

        for image in images:
            thread_pool.add_file(image)

        print "Found {count} images".format(count=len(images))
        thread_pool.download(args.dest)
        print "Done"
