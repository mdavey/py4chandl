import httplib
import urlparse


def download_resource(host, resource):
    conn = httplib.HTTPSConnection(host)
    conn.putrequest('GET', resource)
    conn.endheaders()
    response = conn.getresponse()
    contents = response.read()
    response.close()
    conn.close()
    return contents


def download_url(url, filename=None):
    url_details = urlparse.urlparse(url)
    data = download_resource(url_details.netloc, url_details.path)
    if filename is None:
        return data
    else:
        f = open(filename, 'wb+')
        f.write(data)
        f.close()
        return data