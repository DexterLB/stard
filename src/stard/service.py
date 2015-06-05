from importlib.machinery import SourceFileLoader
import xdg.BaseDirectory
import os

class BaseService:
    def baz(self):
        print("gs")

CONFIG_BASE_DIRS = xdg.BaseDirectory.xdg_config_dirs + ['/etc']
CONFIG_DIRS = map(lambda directory: os.path.join(directory, 'stard'),
                  CONFIG_BASE_DIRS)

def find_file(name):
    for directory in CONFIG_DIRS:
        filename = os.path.join(directory, name + '.py')
        if os.path.isfile(filename):
            return filename

    raise RuntimeError('cannot locate service ' + name)

def service(name, *args, **kwargs):
    service_module = SourceFileLoader(name, find_file(name)).load_module(name)
    return service_module.Service(*args, **kwargs)
