"""Module defining the Drone class used during simulation."""

from src.hub import Hub
from typing import Optional


class Drone:
    """Represent a drone navigating through the hub network.

    Each drone holds its current position, its pre-computed path,
    and state flags for tracking movement and restricted zone transit.
    """

    def __init__(self, id: str, pos: Hub, path: tuple[Hub, ...]):
        """Initialize a Drone with an identity, starting position, and path.

        Args:
            id: Unique identifier for the drone (e.g. 'D1').
            pos: The hub where the drone starts (typically the graph's start).
            path: Ordered tuple of hubs the drone will follow, from start
                to destination.
        """

        self.id = id
        self.position = pos
        self.path = path
        self.path_index: int = 0
        self.is_arrived = False
        self.dest_res: Optional[Hub] = None
        self.transit: bool = False

    def get_next_hub(self) -> Optional[Hub]:
        """Return the next hub in the drone's path, if one exists.

        Returns:
            The next Hub object in the path, or None if the drone has
            reached or passed the last hub.
        """

        if not self.is_arrived and self.path_index + 1 < len(self.path):
            return self.path[self.path_index + 1]
        return None

    def to_next_hub(self, next_hub: Hub) -> None:
        """Advance the drone to the given hub and update its path index.

        Args:
            next_hub: The hub the drone is moving to. Must be the next
                hub in the drone's planned path.
        """

        self.position = next_hub
        self.path_index += 1

    def get_info(self) -> str:
        """Return a human-readable summary of the drone's current state.

        Returns:
            A formatted string showing the drone's id, current position,
            full path, and arrival status.
        """
        return (f"{self.id}:\n"
                f"  - position: {self.position}\n"
                f"  - path: {self.path}\n"
                f"  - is_arrived: {self.is_arrived}")

    def __str__(self) -> str:
        return self.id
