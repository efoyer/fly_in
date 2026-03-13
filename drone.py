from hub import Hub


class Drone:
    def __init__(self, id: str, pos: Hub, path: tuple[Hub]):
        self.id = id
        self.position = pos
        self.path = path
        self.path_index = 0
        self.is_arrived = False

    def next_hub(self):
        if not self.is_arrived and self.path_index + 1 < len(self.path):
            return self.path[self.path_index + 1]
        return None

    def get_info(self) -> str:
        return (f"{self.id}:\n"
                f"  - position: {self.position}\n"
                f"  - path: {self.path}\n"
                f"  - is_arrived: {self.is_arrived}")

    def __str__(self):
        return self.id
