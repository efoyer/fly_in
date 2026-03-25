"""Module defining the Connection class representing edges in the graph."""

from src.hub import Hub


class Connection:
    """Represent a bidirectional link between two hubs.

    A connection defines a traversable edge in the drone routing network,
    with an optional maximum number of drones that can use it per turn.
    """

    def __init__(self,  start: Hub, end: Hub, max: int):
        """Initialize a Connection between two hubs.

        Args:
            start: The hub at one end of the connection.
            end: The hub at the other end of the connection.
            max: Maximum number of drones allowed on this link per turn.
        """
        self.start = start
        self.end = end
        self.max = max

    def get_str(self) -> str:
        """Return a string representation of this connection.

        Returns:
            A string in the format 'start_name-end_name'.
        """
        return f"{self.start.get_name()}-{self.end.get_name()}"
