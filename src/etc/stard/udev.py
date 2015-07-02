from stard.services import Executable

class Service(Executable):
    udev_binary = '/usr/lib/systemd/systemd-udevd'
    # udev-binary = 'udevd'

    start_command = (udev_binary, '--daemon')
    post_start_commands = (
        ('udevadm', 'trigger', '--action=add', '--type=subsystems'),
        ('udevadm', 'trigger', '--action=add', '--type=devices')
    )

    def init_service(self):
        self.add_parent('system_mountpoints')
