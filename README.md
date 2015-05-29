# stard
config file for each service (python file?)

services have:

- is_running()
- start()
- stop()
- executable - used by default start() and stop() (like systemd's Simple type)
- before, after: arrays of other services
