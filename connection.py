from .hub import Zone


class Connection:
    def __init__(self,  start: Zone, end: Zone):
        self.start = start
        self.end = end