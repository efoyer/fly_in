from .hub import Zone
from .connection import Connection


class Graph:
    def __init__(self, nb_drones: int, start: Zone, end: Zone,
                 hubs: list[Zone], connection: list[Connection]):
        self.nb_drones = nb_drones
        self.hubs = hubs
        self.connect = connection
        self.start = start
        self.end = end