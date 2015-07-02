import pickle
import os

class Oneshot:
    service_file = '/var/run/stard/running.services'

    @classmethod
    def mark_running_services(cls, services, trunc=False):
        os.makedirs(os.path.dirname(cls.service_file), exist_ok=True)

        with open(cls.service_file, 'wb' if trunc else 'ab') as f:
            for service in services:
                pickle.dump(service, f)

    @classmethod
    def mark_running(cls, service):
        cls.mark_running_services({service})

    @classmethod
    def unmark_running_services(cls, services):
        running_services = set()
        with open(cls.service_file, 'rb') as f:
            while True:
                try:
                    running_services.add(pickle.load(f))
                except (EOFError, pickle.UnpicklingError):
                    break
        cls.mark_running_services(running_services - services, trunc=True)

    @classmethod
    def unmark_running(cls, service):
        cls.unmark_running_services({service})


    @classmethod
    def is_running(cls, service):
        try:
            with open(cls.service_file, 'rb') as f:
                while True:
                    if service == pickle.load(f):
                        return True
        except (FileNotFoundError, EOFError, pickle.UnpicklingError):
            return False    
