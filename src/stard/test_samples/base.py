from stard.services import BaseService

class Service(BaseService):
    def is_running(self):
        return True

    def stop(self):
        pass
