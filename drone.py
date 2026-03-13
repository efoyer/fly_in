from hub import Hub


class Drone:
    def __init__(self, id: str, pos: Hub, path: tuple[Hub]):
        self.id = id
        self.position = pos
        self.path = path
        self.path_index = 0
        self.is_arrived = False

    def next_hub(self):
        if not self.is_arrived:
            return self.path[self.path_index + 1]
        return None

