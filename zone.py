class Zone:
    def __init__(self, name: str, x: int, y: int,
                 meta: dict):
        self.name = name
        self.x = x
        self.y = y

    def get_name(self) -> str:
        return self.name
