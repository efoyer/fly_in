class Hub:
    def __init__(self, name: str, x: int, y: int,
                 meta: dict = None):
        self.name = name
        self.x = x
        self.y = y

    def get_name(self) -> str:
        return self.name
