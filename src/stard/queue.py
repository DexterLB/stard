
class Queue:
    def __init__(self, services=set()):
        self.update(services)

    def update(self, services)
        self.running = set()
        self.stopped = set()

        self.starting = set()
        self.stopping = set()

        for service in services:
            if service.is_running():
                self.running.add(service)
            else:
                self.stopped.add(service)

    def mark_starting(self, service):
        self.stopping.remove(service)
        self.starting.add(service)

    def get_startable(self):
        for service in self.stopped:
            if service.parents < self.running:
                self.mark_starting(service)
                return service
