from importlib.machinery import SourceFileLoader

class BaseService:
    def baz(self):
        print("gs")

def find_file(name):
    return name + '.py'

def service(name, *args, **kwargs):
    service_module = SourceFileLoader(name, find_file(name)).load_module(name)
    return service_module.Service(*args, **kwargs)
