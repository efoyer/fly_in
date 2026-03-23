from typing import Optional


class Hub:
    def __init__(self, name: str, x: int, y: int,
                 meta: Optional[dict[str, object]] = None):
        self.name = name
        self.x = x
        self.y = y
        self.color: Optional[str | object] = (meta or {}).get("color", None)
        self.zone: Optional[str | object] = (meta or {}).get("zone", "normal")
        self.max_drones: Optional[str | object] = (meta or {}).get(
            "max_drones", 1)
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
