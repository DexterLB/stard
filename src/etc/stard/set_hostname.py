from stard.services import Copy

class Service(Copy):
    def init_service(self):
        self.add_parent('system_mountpoints')
        Copy.init_service(self)
    source = '/etc/hostname'
    destination = '/proc/sys/kernel/hostname'
