class Manager:
    def __init__(self, queue):
        self.queue = queue

    def process_service(self):
        service = self.queue.pop()
        if not service:
            return False

        if self.queue.mode == 'start':
            service.start()
            print('started ' + service.service_name)
        elif self.queue.mode == 'stop':
            service.stop()
            print('stopped ' + service.service_name)
        else:
            raise RuntimeError('service mode must be "start" or "stop"')

        self.queue.finalize(service)
        return True

    def __call__(self):
        while self.process_service():
            pass
