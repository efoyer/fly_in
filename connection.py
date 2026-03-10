from .hub import Hub


class Connection:
    def __init__(self,  start: Hub, end: Hub):
        self.start = start
        self.end = end

    def get_str(self) -> str:
        return f"{self.start.get_name()}-{self.end.get_name()}"
