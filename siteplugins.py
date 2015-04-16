import os
import imp
from glob import glob


def load_plugins(directory):
    plugins = []
    for filename in glob(os.path.join(directory, '*.py')):
        if filename == os.path.join(directory, '__init__.py'):
            continue
        plugin_name = os.path.basename(filename).split('.')[0]
        plugin_details = imp.find_module(plugin_name, [directory])
        plugins.append(imp.load_module(plugin_name, *plugin_details))
    return plugins


def get_plugin_for_url(url):
    for plugin in load_plugins('sites'):
        if plugin.can_handle(url):
            return plugin
    return None
