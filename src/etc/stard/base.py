from stard.services import BaseService

class Service(BaseService):
    @property
    def is_running(self):
        return True

    def stop(self):
        print('Dead.')
