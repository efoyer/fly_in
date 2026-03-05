from .zone import Zone


class Graph:
    def __init__(self, nb_drones: int, zones: dict,
                 connect: dict, start: Zone, end: Zone):
        self.nb_drones = nb_drones
        self.zones = zones
        self.connect = connect
        self.start = start
        self.end = end