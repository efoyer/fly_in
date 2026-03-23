from typing import Optional
from typing import TypedDict


class MetaDict(TypedDict):
    color: str | None
    zone: str
    max_drones: int


class Hub:
    def __init__(self, name: str, x: int, y: int,
                 meta: MetaDict | None = None):
        self.name = name
        self.x = x
        self.y = y
        if meta is None:
            self.color = None
            self.zone = "normal"
            self.max_drones = 1
        else:
            self.color = meta["color"]
            self.zone = meta["zone"]
            self.max_drones = meta["max_drones"]
        self.cost: Optional[int] = None
        if self.zone == "normal" or self.zone == "priority":
            self.cost = 1
        elif self.zone == "blocked":
            self.cost = None
        elif self.zone == "restricted":
            self.cost = 2
        else:
            self.cost = 1

    def get_name(self) -> str:
        return self.name

    def get_name_meta(self) -> str:
        return f"{self.name} [{self.color} {self.zone} {self.max_drones}]"

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name
