__author__ = 'Matthew'

import os
import argparse

from page import Page


def download(host, page, directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

    page = Page(host, page)
    page.download()

    for image in page.get_images():
        image.download_to(directory)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download all images from a 4chan thread to a specific directory')
    parser.add_argument('thread', help='Source thread.  e.g. /a/res/82138812')
    parser.add_argument('dest', help='Destination directory.  e.g. c:/images')
    # parser.add_argument('--board', default='boards.4chan.org')
    args = parser.parse_args()

    # download('boards.4chan.org', '/a/res/82138812', 'z:\\foo')
    download('boards.4chan.org', args.thread, args.dest)

