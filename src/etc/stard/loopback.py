from stard.services import Executable

class Service(Executable):
    start_command = tuple('ip link set up dev lo'.split())
    oneshot = True

    def init_service(self):
        self.add_parent('system_mountpoints')
