class Hub:
    def __init__(self, name: str, x: int, y: int,
                 meta: dict = None):
        self.name = name
        self.x = x
        self.y = y
        self.color = (meta or {}).get("color", None)
        self.zone = (meta or {}).get("zone", "normal")
        self.max_drones = (meta or {}).get("max_drones", 1)

    def get_name(self) -> str:
        return self.name
    
    def get_name_meta(self) -> str:
        return f"{self.name} [{self.color} {self.zone} {self.max_drones}]"
