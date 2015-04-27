import re

from bs4 import BeautifulSoup


def get_name():
    return '4chan.net-0.2'


def can_handle(url):
    return 'https://boards.4chan.org/' in url


def get_links(html):
    urls = []
    links = []

    soup = BeautifulSoup(html)

    for link in soup.find_all('a'):
        href = link.get('href')

        if href is None:
            continue

        # <a href="//i.4cdn.org/g/1430100220828.jpg" target="_blank">cof_orange_hex_400x400.jpg</a>
        match = re.search('//(i.4cdn.org/[a-z0-9]+/)(\d+)(\.[a-zA-Z]{3,4})', href, re.DOTALL)

        if match is not None:
            url = 'https://' + match.group(1) + match.group(2) + match.group(3)
            if url not in urls:
                urls.append(url)
                original_filename = link.string
                links.append({'url': url, 'name': original_filename})

                # if original_filename == match.group(2) + match.group(3):
                #     links.append({'url': url, 'name': original_filename})
                # else:
                #     links.append({'url': url, 'name': match.group(2) + '_' + original_filename})

    return links