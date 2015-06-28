from argparse import ArgumentParser
from stard.loader import Loader
from stard.service_queue import ServiceQueue
from stard.manager import Manager

class Stard:
    def __init__(self):
        self.parser = ArgumentParser(description='start or stop services')
        self.parser.add_argument(
            '-d', '--dir', type=str, dest='service_dir',
            default='/etc/stard',
            help='directory in which to look for service files'
        )
        self.parser.add_argument(
            'mode', choices=['start', 'stop'],
            help='choose whether to start or stop a service'
        )
        self.parser.add_argument(
            'service', type=str,
            help='name of a service'
        )

    def run(self):
        args = self.parser.parse_args()

        loader = Loader([args.service_dir])
        queue = ServiceQueue(loader.service(args.service), mode=args.mode)
        manager = Manager(queue)
        manager()

def main():
    Stard().run()

if __name__ == '__main__':
    main()
