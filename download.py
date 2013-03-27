__author__ = 'Matthew'

import os

from page import Page


def download(host, page, directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

    page = Page(host, page)
    page.download()

    for image in page.get_images():
        image.download_to(directory)

# download('boards.4chan.org', '/a/res/82138812', 'z:\\foo')

