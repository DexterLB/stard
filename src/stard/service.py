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

        self.services = {}

    def find_file(self, name):
        for directory in self.config_dirs:
            filename = os.path.join(directory, name + '.py')
            if os.path.isfile(filename):
                return filename

        raise RuntimeError('cannot locate service ' + name +
                           ' in ' + ' '.join(self.config_dirs))

    @staticmethod
    def service_hash(name, *args, **kwargs):
        return (name, tuple(args), frozenset(kwargs.items()))

    def service(self, name, *args, **kwargs):
        hash = Manager.service_hash(name, *args, **kwargs)
        if hash not in self.services:
            service_module = SourceFileLoader(
                name, self.find_file(name)
            ).load_module(name)

            service = service_module.Service(self, name, args, kwargs)
            self.services[hash] = service

        return self.services[hash]

    def populate_relatives(self):
        for _, service in self.services.items():
            for child in service.children:
                child.parents.add(service)
            for parent in service.parents:
                parent.children.add(service)


class BaseService:
    children = set()
    parents = set()

    def __init__(self, manager, service_name, service_args, service_kwargs):
        self.manager = manager
        self.service_name = service_name
        self.service_args = service_args
        self.service_kwargs = service_kwargs
        self._hash = hash(Manager.service_hash(
            service_name, *service_args, **service_kwargs
        ))
        self.init_service(*service_args, **service_kwargs)

    def __hash__(self):
        return self._hash

    def __eq__(self, other):
        return (
            (self.service_name, self.service_args, self.service_kwargs)
            == (other.service_name, other.service_args, other.service_kwargs)
        )

    def service(self, name, *args, **kwargs):
        return self.manager.service(name, *args, **kwargs)

    def init_service(self, *args, **kwargs):
        pass
