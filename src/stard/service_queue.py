from algorithms import walk_parents, walk_children

class ServiceQueue:
    def __init__(self, service, mode):
        self.mode = mode

        self.to_do = set()
        self.current = set()
        self.done = set()

        if self.mode == 'start':
            for service in walk_parents(service):
                if service.is_running:
                    self.done.add(service)
                else:
                    self.to_do.add(service)
        elif self.mode == 'stop':
            for service in walk_children(service):
                if service.is_running:
                    self.to_do.add(service)
                else:
                    self.done.add(service)

    def top(self):
        if self.mode == 'start':
            for service in self.to_do:
                if service.parents <= self.done:
                    return service
        elif self.mode == 'stop':
            for service in self.to_do:
                if service.children <= self.done:
                    return service

    def pop(self):
        top = self.top()
        self.to_do.remove(top)
        self.current.add(top)
        return top

    def finalize(self, service):
        self.current.remove(service)
        self.done.add(service)
