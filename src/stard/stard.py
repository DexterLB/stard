from argparse import ArgumentParser
from stard.loader import Loader
from stard.service_queue import ServiceQueue
from stard.manager import Manager

class Stard:
    def __init__(self):
        self.parser = ArgumentParser(description='start or stop services')
        self.parser.add_argument(
            '-d', '--dir', type=str, dest='service_dir',
            default=None,
            help='directory in which to look for service files'
        )
        self.parser.add_argument(
            'mode', choices=['start', 'stop', 'status'],
            help='choose what to do with a service'
        )
        self.parser.add_argument(
            'service', type=str,
            help='name of a service'
        )

    def run(self, service_name, service_mode, service_dir=None):
        if service_dir:
            loader = Loader([service_dir])
        else:
            loader = Loader()

        loader.load_services()
        loader.populate_relatives()

        if service_mode == 'status':
            print('running: ' + str(loader.service(service_name).is_running))
        else:
            queue = ServiceQueue(loader.service(service_name), mode=service_mode)
            manager = Manager(queue)
            manager()

    def run_from_args(self):
        args = self.parser.parse_args()
        self.run(args.service, args.mode, args.service_dir)


    def run_from_init(self):
        self.run('init', 'start')

    def run_from_shutdown(self):
        self.run('base', 'stop')


def main():
    Stard().run_from_args()

def init():
    Stard().run_from_init()

def shutdown():
    Stard().run_from_shutdown()

if __name__ == '__main__':
    main()
