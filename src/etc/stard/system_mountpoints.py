from stard.services import BaseService

class Service(BaseService):
    def init_service(self):
        self.add_parent(
            'mount', 'proc', '/proc', 
            fstype='proc', options='nosuid,noexec,nodev'
        )
        self.add_parent(
            'mount', 'sys', '/sys', 
            fstype='sysfs', options='nosuid,noexec,nodev'
        )
        self.add_parent(
            'mount', 'run', '/run', 
            fstype='tmpfs', options='mode=0755,nosuid,nodev'
        )
        self.add_parent(
            'mount', 'dev', '/dev', 
            fstype='devtmpfs', options='mode=0755,nosuid'
        )
        self.add_parent(
            'mount', 'devpts', '/dev/pts', 
            fstype='devpts', options='mode=0620,gid=5,nosuid,noexec',
            mkdir=True
        )
        self.add_parent(
            'mount', 'shm', '/dev/shm', 
            fstype='tmpfs', options='mode=1777,nosuid,noexec',
            mkdir=True
        )
