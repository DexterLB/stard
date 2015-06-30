import subprocess

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
    pidfile = None
    forking = False
    arguments = []

    def execute(self, argv):
        subprocess.check_call(argv)

    def fork(self, argv):
        return subprocess.Popen(argv)

    def start(self):
        if self.forking:
            self.fork([self.executable] + self.arguments)
        else:
            self.execute([self.executable] + self.arguments)
    
    def pid(self):
        with open('/dev/null', 'w') as devnull:
            if self.pidfile:
                try:
                    with open(self.pidfile, 'r') as f:
                        pid = int(f.read())
                    if subprocess.call(
                        ['kill', '-0', str(pid)],
                        stdout=devnull,
                        stderr=devnull
                    ) == 0:
                        return pid
                    else:
                        return None

                except IOError:
                    return None
            else:
                try:
                    return int(subprocess.check_output(
                        ['pidof', str(self.executable)],
                        stderr=devnull
                    ).split()[0])
                except subprocess.CalledProcessError:
                    return None
        
    def is_running(self):
        return bool(self.pid())
