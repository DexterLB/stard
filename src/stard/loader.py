from importlib.machinery import SourceFileLoader
import xdg.BaseDirectory
import os

from stard import services

class Loader:
    builtin_services = {
        'executable': services.Executable,
        'mount': services.Mount,
        'copy': services.Copy
    }

    def __init__(self, config_dirs=[]):
        config_base_dirs = xdg.BaseDirectory.xdg_config_dirs + ['/etc']
        self.config_dirs = config_dirs + list(map(
            lambda directory: os.path.join(directory, 'stard'),
            config_base_dirs
        ))

        self.services = {}

    def find_file(self, name):
        for directory in self.config_dirs:
            filename = os.path.join(directory, name + '.py')
            if os.path.isfile(filename):
                return filename

        raise RuntimeError('cannot locate service ' + name +
                           ' in ' + ' '.join(self.config_dirs))

    def service(self, name, *args, **kwargs):
        id = services.BaseService.service_id(name, *args, **kwargs)
        if id not in self.services:
            if name in self.builtin_services:
                service_class = self.builtin_services[name]
            else:
                service_module = SourceFileLoader(
                    name, self.find_file(name)
                ).load_module(name)
                service_class = service_module.Service

            service = service_class(self, name, args, kwargs)
            self.services[id] = service

        return self.services[id]

    def populate_relatives(self):
        for _, service in self.services.items():
            for child in service.children:
                child.parents.add(service)
            for parent in service.parents:
                parent.children.add(service)


