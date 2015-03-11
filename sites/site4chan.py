from bs4 import BeautifulSoup
import re


def get_name():
    return '4chan.net-0.1'


def can_handle(url):
    return 'https://boards.4chan.org/' in url


def get_images(html):
    urls = []

    soup = BeautifulSoup(html)

    for link in soup.find_all('a'):
        href = link.get('href')

        if href is None:
            continue

        match = re.search('//(i.4cdn.org/v/\d+\.[a-zA-Z]{3,4})', href, re.DOTALL)

        if match is not None:
            url = 'https://' + match.group(1)
            if url not in urls:
                urls.append(url)

    return urls