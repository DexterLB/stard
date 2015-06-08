from service import BaseService

class Service(BaseService):
    def init_service(self):
        self.children = {self.service('child')}
