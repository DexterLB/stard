from stard.services import BaseService

class Service(BaseService):
    def init_service(self):
        self.add_parent('multiuser')
        self.add_parent('dhcpcd')
        self.add_parent('getty', terminal=1)
