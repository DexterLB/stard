from stard.services import Executable

class Service(Executable):
    start_command = ('mount', '-a')
    post_start_commands = (
        ('mount', '-o', 'remount,rw', '/'),
    )
    oneshot = True

    def init_service(self):
        self.add_parent('system_mountpoints')
        self.add_parent('udev')
