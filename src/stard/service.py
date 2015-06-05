from importlib.machinery import SourceFileLoader
import xdg.BaseDirectory
import os

class Manager:
    def __init__(self, config_dirs=[]):
        config_base_dirs = xdg.BaseDirectory.xdg_config_dirs + ['/etc']
        self.config_dirs = config_dirs + list(map(
            lambda directory: os.path.join(directory, 'stard'),
            config_base_dirs
        ))

    def find_file(self, name):
        for directory in self.config_dirs:
            filename = os.path.join(directory, name + '.py')
            if os.path.isfile(filename):
                return filename

        raise RuntimeError('cannot locate service ' + name +
                           ' in ' + ' '.join(self.config_dirs))

    def service(self, name, *args, **kwargs):
        service_module = SourceFileLoader(name, self.find_file(name)).load_module(name)
        service = service_module.Service(self)
        service.init_service(*args, **kwargs)
        return service

class BaseService:
    def __init__(self, manager):
        self.manager = manager

    def service(self, name, *args, **kwargs):
        self.manager.service(name, *args, **kwargs)

    def init_service(self, *args, **kwargs):
        self.arguments = args
        for name, value in kwargs.items():
            self.__dict__[name] = value
