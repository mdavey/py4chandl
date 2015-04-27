#!/usr/bin/python

import os

from flask import Flask
from flask import render_template
from flask import request

from siteplugins import get_plugin_for_url
from downloadpool import DownloadPool
from downloadhttps import download_url


app = Flask('py4chandl')
app.debug = True


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/list/<path:url>')
def list_links(url):
    plugin = get_plugin_for_url(url)
    if plugin is None:
        return render_template('noplugin.html', url=url)

    links = plugin.get_links(download_url(url))
    return render_template('list.html', url=url, links=links)


@app.route('/download', methods=['POST'])
def download():
    count = 0
    path = request.form['path']

    if not os.path.exists(path):
        os.makedirs(path)

    for (name, value) in request.form.iteritems():
        if value == 'on':
            url = request.form['url_' + name]
            filename = request.form['filename_' + name]
            download_pool.add_file(url, path, filename)
            count += 1

    return 'Images added: ' + str(count)


if __name__ == "__main__":
    download_pool = DownloadPool(4)
    download_pool.start()

    try:
        app.run()
    except KeyboardInterrupt:
        print 'Waiting for download pool to finish'
        download_pool.join()
        print 'Done'
