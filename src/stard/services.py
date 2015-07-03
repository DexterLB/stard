import subprocess
import os
import sys
import traceback

from stard.util import Oneshot

class BaseService:
    @staticmethod
    def service_id(name, *args, **kwargs):
        return (name, tuple(args), frozenset(kwargs.items()))

    def __init__(self, loader, service_name, service_args, service_kwargs):
        self.loader = loader
        self.service_name = service_name
        self.service_args = service_args
        self.service_kwargs = service_kwargs
        self._hash = hash(self.id)

        self.children = set()
        self.parents = set()

        if service_name != 'base':
            self.add_parent('base')

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

    def start(self):
        pass

    def stop(self):
        pass

    def add_child(self, name, *args, **kwargs):
        self.children.add(self.service(name, *args, **kwargs))

    def add_parent(self, name, *args, **kwargs):
        self.parents.add(self.service(name, *args, **kwargs))

    @property
    def is_running(self):
        for parent in self.parents:
            if not parent.is_running:
                return False
        return True

class Executable(BaseService):
    command = None
    start_command = None
    pre_start_commands = None
    post_start_commands = None
    pre_stop_commands = None
    post_stop_commands = None
    stop_command = None
    pidfile = None
    oneshot = False

    def init_service(self, command=None,
                     start_command=None, stop_command=None,
                     pre_start_commands=None, post_start_commands=None,
                     pre_stop_commands=None, post_stop_commands=None,
                     pidfile=None, oneshot=False):
        self.command = command or self.command
        self.start_command = start_command or self.start_command
        self.pre_start_commands = pre_start_commands or self.pre_start_commands
        self.post_start_commands = post_start_commands or self.post_start_commands
        self.pre_stop_commands = pre_stop_commands or self.pre_stop_commands
        self.post_stop_commands = post_stop_commands or self.post_stop_commands
        self.stop_command = stop_command or self.stop_command
        self.pidfile = pidfile or self.pidfile
        self.oneshot = oneshot or self.oneshot

    def execute(self, argv):
        subprocess.check_output(list(argv), stderr=subprocess.STDOUT)

    def execute_commands(self, commands):
        if commands:
            for command in commands:
                self.execute(command)

    def fork(self, argv, pidfile):
        child_pid = os.fork()
        if child_pid == 0:
            try:
                service_pid = subprocess.Popen(list(argv)).pid
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
                raise RuntimeError('forking failed for ' + str(argv))


    def start(self):
        self.execute_commands(self.pre_start_commands)

        if self.start_command:
            self.execute(self.start_command)
        else:
            self.fork(self.command, self.pidfile)
        if self.oneshot:
            Oneshot.mark_running(self.id)
   
        self.execute_commands(self.post_start_commands)

    def process_name(self):
        if self.command:
            return self.command[0]
        else:
            return self.start_command[0]

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
       
    @property
    def is_running(self):
        if self.oneshot:
            return Oneshot.is_running(self.id)
        return bool(self.pid())

    def stop(self):
        self.execute_commands(self.pre_stop_commands)

        if self.stop_command:
            self.execute(self.stop_command)
        else:
            if not self.oneshot:
                pid = self.pid()
                if pid:
                    os.kill(pid, 15)    # 15 = TERM
        if self.oneshot:
            Oneshot.unmark_running(self.id)

        self.execute_commands(self.pre_start_commands)

class Mount(Executable):
    def init_service(self, source=None, mountpoint=None,
                     options=None, fstype=None, mkdir=False):
        self.source = source
        self.mountpoint = mountpoint
        self.mkdir = mkdir

        self.start_command = ['mount']
        self.stop_command = ['umount']

        if fstype:
            self.start_command += ['-t', fstype]
        if options:
            self.start_command += ['-o', options]

        if source:
            self.start_command += [source]
        if mountpoint:
            self.start_command += [mountpoint]
            self.stop_command += [mountpoint]
        else:
            raise RuntimeError("can't mount without mountpoint")

    def start(self):
        if self.mkdir:
            os.makedirs(self.mountpoint, exist_ok=True)
        Executable.start(self)

    @property
    def is_running(self):
        return (subprocess.call(['mountpoint', '-q', self.mountpoint]) == 0)

class Copy(BaseService):
    append = False

    def init_service(self, source=None, destination=None, append=False):
        self.source = source = source or self.source
        self.destination = destination or self.destination
        self.append = append or self.append

    def start(self):
        with open(self.source, 'rb') as input:
            write_mode = 'ab' if self.append else 'wb'
            with open(self.destination, write_mode) as output:
                output.write(input.read())
        Oneshot.mark_running(self.id)

    def stop(self):
        Oneshot.unmark_running(self.id)

    @property
    def is_running(self):
        return Oneshot.is_running(self.id)

class Module(Executable):
    module_name = None

    def init_service(self, module_name=None):
        self.module_name = module_name or self.module_name

    def start(self):
        subprocess.check_output(
            ['modprobe', self.module_name],
            stderr=subprocess.STDOUT
        )

    @property
    def is_running(self):
        mod_list = subprocess.check_output(
            ['lsmod'], stderr=subprocess.STDOUT
        ).decode().split("\n")
        modules = [line.split()[0] for line in mod_list if line]
        return (self.module_name in modules)

    def stop(self):
        subprocess.check_output(
            ['modprobe', '--remove-dependencies', self.module_name],
            stderr=subprocess.STDOUT
        )
