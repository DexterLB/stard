from stard.services import Executable

class Service(Executable):
    def init_service(self, terminal):
        self.command = (
            'sh', '-c', "agetty -8 -s 38400 tty%d linux" % terminal
        )
        self.add_parent('multiuser')
