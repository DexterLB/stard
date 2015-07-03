from stard.services import Executable

class Service(Executable):
    def init_service(self, interface=None):
        self.add_parent('multiuser')

        if interface:
            self.pidfile = '/run/dhcpcd-' + interface + '.pid'
            self.start_command = ('dhcpcd', '-q', '-w', interface)
            self.stop_command = ('dhcpcd', '-x', interface)
        else:
            self.pidfile = '/run/dhcpcd.pid'
            self.start_command = ('dhcpcd', '-q')
            self.stop_command = ('dhcpcd', '-x')
