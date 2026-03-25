"""Module defining the Hub class and its associated types."""

from typing import Optional
from typing import TypedDict


class MetaDict(TypedDict):
    color: str | None
    zone: str
    max_drones: int


class Hub:
    """Represent a node in the drone routing network.

    A hub is a waypoint that drones can occupy. It has a position,
    a zone type that affects traversal cost and rules, and a maximum
    drone capacity.
    """
    def __init__(self, name: str, x: int, y: int,
                 meta: MetaDict | None = None):
        """Initialize a Hub with position and optional metadata.

        Args:
            name: Unique identifier for the hub.
            x: Horizontal coordinate on the map.
            y: Vertical coordinate on the map.
            meta: Optional metadata dict containing color, zone, and
                max_drones. Defaults to gray, normal zone, capacity 1.
        """
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
        """Return the hub's name.

        Returns:
            The name string of this hub.
        """
        return self.name

    def get_name_meta(self) -> str:
        """Return a formatted string with the hub's name and metadata.

        Returns:
            A string in the format 'name [color zone max_drones]'.
        """
        return f"{self.name} [{self.color} {self.zone} {self.max_drones}]"

    def __str__(self) -> str:
        """Return the hub's name as its string representation.

        Returns:
            The name of the hub.
        """
        return self.name

    def __repr__(self) -> str:
        """Return the hub's name as its repr string.

        Returns:
            The name of the hub.
        """
        return self.name
