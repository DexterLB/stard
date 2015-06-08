# stard
Each service will have a service file. The filename matches the service name.
Service files are python classes.

Sample service:
```python
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
from stard.service import BaseService
from shutil import copyfile

class Service(BaseService):
    description = 'Save brightness'
    user = 'human'

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

services will have:

- is_running()
- start()
- stop()
- executable - used by default start() and stop() (like systemd's Simple type)
- before, after: arrays of other services
