from src.hub import Hub


class Connection:
    def __init__(self,  start: Hub, end: Hub, max: int):
        self.start = start
        self.end = end
        self.max = max

    def get_str(self) -> str:
        return f"{self.start.get_name()}-{self.end.get_name()}"
