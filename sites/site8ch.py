from bs4 import BeautifulSoup
import re


def get_name():
    return '8ch.net-0.1'


def can_handle(url):
    return 'https://8ch.net/' in url


def get_images(html):
    urls = []

    soup = BeautifulSoup(html)

    for link in soup.find_all('a'):
        href = link.get('href')

        if href is None:
            continue

        match = re.search('(https://media\.8ch\.net/.*?/src/.*?\.[a-zA-Z]{3,4})', href, re.DOTALL)

        if match is not None:
            url = match.group(1)
            if url not in urls:
                urls.append(url)
                
    return urls
