# stard
Each service will have a service file. The filename matches the service name.
Service files are python classes.

Sample service:
```python
# /etc/stard/ftpd.py

from stard.service import BaseService

class Service(BaseService):
    description = 'FTP daemon'
    executable = 'ftpd'

    def init_service(self):
        self.parents = {
            self.service('network'),
            self.service('fstab')
        }
```

A not so traditional service:
```python
# /etc/stard/brightness.py

from stard.service import BaseService
from shutil import copyfile

class Service(BaseService):
    description = 'Save brightness'

    _brightness_file = '/sys/class/backlight/intel_backlight/brightness'

    def init_service(self):
        self.parents = {
            self.service('intel'),
        }

    def start(self):
        copyfile('/run/brightness', self._brightness_file)

    def stop(self):
        copyfile(self._brightness_file, '/run/brightness')
```

A service with arguments:
```python
# /etc/stard/dhcpcd.py

from stard.service import BaseService

class Service(BaseService):
    description = 'DHCP daemon'

    def init_service(self, interface):
        self.exec_start = ('dhcpcd', '-q', '-w', interface)
        self.exec_stop = ('dhcpcd', '-x', interface)

# /etc/stard/network.py

from stard.service import BaseService

class Service(BaseService):
    description = 'network node'
    
    parents = {
        self.service('dhcpcd', interface='eth0')
    }
```

services will have:

- is_running()
- start()
- stop()
- executable - used by default start() and stop() (like systemd's Simple type)
- parents, children - sets of services that define the order of execution
- user, group
