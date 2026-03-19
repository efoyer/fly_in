from src.hub import Hub
from typing import Optional


class Drone:
    def __init__(self, id: str, pos: Hub, path: tuple[Hub, ...]):
        self.id = id
        self.position = pos
        self.path = path
        self.path_index: int = 0
        self.is_arrived = False
        self.dest_res: Optional[Hub] = None
        self.transit: bool = False

    def get_next_hub(self) -> Optional[Hub]:
        if not self.is_arrived and self.path_index + 1 < len(self.path):
            return self.path[self.path_index + 1]
        return None

    def to_next_hub(self, next_hub: Hub) -> None:
        self.position = next_hub
        self.path_index += 1

    def get_info(self) -> str:
        return (f"{self.id}:\n"
                f"  - position: {self.position}\n"
                f"  - path: {self.path}\n"
                f"  - is_arrived: {self.is_arrived}")

    def __str__(self) -> str:
        return self.id
