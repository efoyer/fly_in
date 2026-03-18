from src.hub import Hub


class Drone:
    def __init__(self, id: str, pos: Hub, path: tuple[Hub]):
        self.id = id
        self.position = pos
        self.path = path
        self.path_index = 0
        self.is_arrived = False
        self.waiting = 0

    def get_next_hub(self):
        if not self.is_arrived and self.path_index + 1 < len(self.path):
            return self.path[self.path_index + 1]
        return None

    def to_next_hub(self, next_hub: Hub):
        self.position = next_hub
        self.path_index += 1

    def get_info(self) -> str:
        return (f"{self.id}:\n"
                f"  - position: {self.position}\n"
                f"  - path: {self.path}\n"
                f"  - is_arrived: {self.is_arrived}")

    def __str__(self):
        return self.id
