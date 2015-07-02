from stard.services import Executable

class Service(Executable):
    start_executable = tuple('ip link set up dev lo'.split())
    oneshot = True
