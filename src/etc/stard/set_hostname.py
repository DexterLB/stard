from stard.services import Copy

class Service(Copy):
    source = '/etc/hostname'
    # destination = '/proc/sys/kernel/hostname'
    destination = '/tmp/foo_hostname'
