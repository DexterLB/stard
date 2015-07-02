import subprocess
import os
import sys
import traceback
import pickle

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
        self._hash = hash(self.id)
        self.init_service(*service_args, **service_kwargs)

    @property
    def id(self):
        return BaseService.service_id(
            self.service_name, *self.service_args, **self.service_kwargs
        )

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
    executable = None
    start_executable = None
    stop_executable = None
    pidfile = None

    def init_service(self, executable=None,
                     start_executable=None, stop_executable=None,
                     pidfile=None):
        self.executable = executable or self.executable
        self.start_executable = start_executable or self.start_executable
        self.stop_executable = stop_executable or self.stop_executable
        self.pidfile = pidfile or self.pidfile

    def execute(self, argv):
        subprocess.check_call(argv)

    def fork(self, argv, pidfile):
        child_pid = os.fork()
        if child_pid == 0:
            try:
                service_pid = subprocess.Popen(argv).pid
                if pidfile:
                    with open(pidfile, 'w') as f:
                        f.write(str(service_pid) + "\n")
            except Exception as exception:
                traceback.print_exc()
                sys.exit(1)
            else:
                sys.exit(0)
        else:
            status = os.waitpid(child_pid, 0)[1]
            if status != 0:
                raise RuntimeError('forking failed')


    def start(self):
        if self.start_executable:
            self.execute(self.start_executable)
        else:
            self.fork(self.executable, self.pidfile)
   
    def process_name(self):
        if self.executable:
            return self.executable[0]
        else:
            return self.start_executable[0]

    def pid(self):
        if self.pidfile:
            try:
                with open(self.pidfile, 'r') as f:
                    pid = int(f.read())
                try:
                    os.kill(pid, 0)
                except ProcessLookupError:
                    return None
                else:
                    return pid

            except IOError:
                return None
        else:
            try:
                with open('/dev/null', 'w') as devnull:
                    return int(subprocess.check_output(
                        ['pidof', str(self.process_name())],
                        stderr=devnull
                    ).split()[0])
            except subprocess.CalledProcessError:
                return None
        
    def is_running(self):
        return bool(self.pid())

    def stop(self):
        if self.stop_executable:
            self.execute(self.stop_executable)
        else:
            pid = self.pid()
            if not pid:
                return

            os.kill(pid, 15)    # 15 = TERM

class Mount(Executable):
    def init_service(self, source=None, mountpoint=None,
                     options=None, fstype=None, mkdir=False):
        self.source = source
        self.mountpoint = mountpoint
        self.mkdir = mkdir

        self.start_executable = ['mount']
        self.stop_executable = ['umount']

        if fstype:
            self.start_executable += ['-t', fstype]
        if options:
            self.start_executable += ['-o', options]

        if source:
            self.start_executable += [source]
        if mountpoint:
            self.start_executable += [mountpoint]
            self.stop_executable += [mountpoint]
        else:
            raise RuntimeError("can't mount without mountpoint")

    def start(self):
        if self.mkdir:
            os.makedirs(self.mountpoint, exist_ok=True)
        Executable.start(self)

    def is_running(self):
        return (subprocess.call(['mountpoint', '-q', self.mountpoint]) == 0)

class Oneshot:
    service_file = '/var/run/stard/running.services'

    @classmethod
    def mark_running_services(cls, services, trunc=False):
        os.makedirs(os.path.dirname(cls.service_file), exist_ok=True)

        with open(cls.service_file, 'wb' if trunc else 'ab') as f:
            for service in services:
                pickle.dump(service, f)

    @classmethod
    def mark_running(cls, service):
        cls.mark_running_services({service})

    @classmethod
    def unmark_running_services(cls, services):
        running_services = set()
        with open(cls.service_file, 'rb') as f:
            while True:
                try:
                    running_services.add(pickle.load(f))
                except (EOFError, pickle.UnpicklingError):
                    break
        cls.mark_running_services(running_services - services, trunc=True)

    @classmethod
    def unmark_running(cls, service):
        cls.unmark_running_services({service})


    @classmethod
    def is_running(cls, service):
        try:
            with open(cls.service_file, 'rb') as f:
                while True:
                    if service == pickle.load(f):
                        return True
        except (FileNotFoundError, EOFError, pickle.UnpicklingError):
            return False    
