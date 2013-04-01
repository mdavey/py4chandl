__author__ = 'Matthew'

import os
import argparse

from page import Page
from threadpool import ThreadPool


def download(host, page, directory, pool_size):
    if not os.path.exists(directory):
        os.makedirs(directory)

    page = Page(host, page)
    page.download()

    thread_pool = ThreadPool(pool_size)

    all_images = list(page.get_images())
    for image in all_images:
        thread_pool.add_image(image)

    print "Found {count} images".format(count=len(all_images))
    thread_pool.download(directory)
    print "Done"


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download all images from a 4chan thread to a specific directory')
    parser.add_argument('thread', help='Source thread.  e.g. /a/res/82138812')
    parser.add_argument('dest', help='Destination directory.  e.g. c:/images')
    parser.add_argument('--pool', type=int, help='Number of concurrent downloads (default: 4)', default=4)
    args = parser.parse_args()

    download('boards.4chan.org', args.thread, args.dest, args.pool)

