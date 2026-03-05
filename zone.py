class Zone:
    def __init__(self, name: str, x: int, y: int,
                 type: str = None, color: str = None):
        self.name = name
        self.x = x
        self.y = y
        self.type = type
        self.color = color
