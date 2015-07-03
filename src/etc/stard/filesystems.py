from stard.services import Executable

class Service(Executable):
    start_command = ('mount', '-a')
    post_start_commands = (
        ('mount', '-o', 'remount,rw', '/'),
    )

    stop_command = ('sh', '-c', 'umount -af; true')
    post_stop_commands = (
        ('mount', '-o', 'remount,ro', '/'),
    )

    oneshot = True

    def init_service(self):
        self.add_parent('system_mountpoints')
        self.add_parent('udev')
