from stard.services import BaseService

class Service(BaseService):
    def init_service(self):
        self.add_parent('sys_mountpoints')
        self.add_parent('filesystems')
        self.add_parent('set_hostname')
        self.add_parent('udev')
        self.add_parent('loopback')
