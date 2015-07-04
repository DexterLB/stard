# stard
A service daemon

# installation

    * install an init process other than systemd (like busybox or sinit)
    * make it run /usr/bin/rc.init on startup and /usr/bin/rc.shutdown
      on shutdown
    * use setup.py install or the PKGBUILD to install stard
    * read the services in /etc/stard and modify them according to your system

# service files
Each service has a service file. The filename matches the service name.
Service files are python classes.

Sample service:
```python
# /etc/stard/ftpd.py

from stard.service import BaseService

class Service(Executable):
    command = 'ftpd'

    def init_service(self):
        self.add_parent('network')
        self.add_parent('filesystems')
```

A not so traditional service:
```python
# /etc/stard/brightness.py

from stard.service import BaseService
from shutil import copyfile

class Service(BaseService):
    _brightness_file = '/sys/class/backlight/intel_backlight/brightness'

    def init_service(self):
        self.add_parent('intel')

    def start(self):
        copyfile('/run/brightness', self._brightness_file)

    def stop(self):
        copyfile(self._brightness_file, '/run/brightness')
```

A service with arguments:
```python
# /etc/stard/dhcpcd.py

from stard.service import Executable

class Service(Executable):
    def init_service(self, interface):
        self.start_command = ('dhcpcd', '-q', '-w', interface)
        self.stop_command = ('dhcpcd', '-x', interface)

# /etc/stard/network.py

from stard.service import BaseService

class Service(BaseService):
    self.add_parent('dhcpcd', interface='eth0')
```
