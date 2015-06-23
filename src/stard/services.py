class BaseService:
    children = set()
    parents = set()

    @staticmethod
    def service_id(name, *args, **kwargs):
        return (name, tuple(args), frozenset(kwargs.items()))

    def __init__(self, loader, service_name, service_args, service_kwargs):
        self.loader = loader
        self.service_name = service_name
        self.service_args = service_args
        self.service_kwargs = service_kwargs
        self._hash = hash(BaseService.service_id(
            service_name, *service_args, **service_kwargs
        ))
        self.init_service(*service_args, **service_kwargs)

    def __hash__(self):
        return self._hash

    def __eq__(self, other):
        return (
            (self.service_name, self.service_args, self.service_kwargs) ==
            (other.service_name, other.service_args, other.service_kwargs)
        )

    def service(self, name, *args, **kwargs):
        return self.loader.service(name, *args, **kwargs)

    def init_service(self, *args, **kwargs):
        pass

    @property
    def is_running(self):
        return False

class Executable(BaseService):
    pass
