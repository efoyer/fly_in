from src.hub import Hub
from src.connection import Connection
from typing import Optional


class Graph:
    """Represent the full drone routing network as a graph.

    Holds all hubs and connections, along with the start/end hubs
    and the number of drones to route.
    """

    def __init__(self, nb_drones: int, start: Hub, end: Hub,
                 hubs: list[Hub], connection: list[Connection]):
        """Initialize the Graph with all network components.

        Args:
            nb_drones: Total number of drones to route through the network.
            start: The starting hub where all drones begin.
            end: The destination hub where all drones must arrive.
            hubs: Complete list of all hubs in the network.
            connection: Complete list of all connections between hubs.
        """

        self.nb_drones = nb_drones
        self.hubs = hubs
        self.connect = connection
        self.start = start
        self.end = end

    def get_infos(self) -> str:
        """Return a formatted summary of the graph's contents.

        Returns:
            A multi-line string listing drone count, start/end hubs,
            all hubs with metadata, and all connections.
        """
        hubs_list = "\n".join(f"  - {hub.get_name_meta()}"
                              for hub in self.hubs)
        conn_list = "\n".join(f"  - {con.get_str()}" for con in self.connect)
        return (f"nb_drones: {self.nb_drones}\n"
                f"start_hub: {self.start.get_name_meta()}\n"
                f"end_hub: {self.end.get_name_meta()}\n"
                "List hubs:\n"
                f"{hubs_list}\n"
                "List connection:\n"
                f"{conn_list}"
                )

    def get_connection(self, hub1: Hub, hub2: Hub) -> Optional[Connection]:
        """Find and return the connection between two hubs, if it exists.

        Connections are bidirectional, so the order of hub1 and hub2
        does not matter.

        Args:
            hub1: One endpoint of the desired connection.
            hub2: The other endpoint of the desired connection.

        Returns:
            The matching Connection object, or None if no connection exists
            between the two hubs.
        """
        for connect in self.connect:
            if ((connect.start == hub1 and connect.end == hub2) or
               (connect.start == hub2 and connect.end == hub1)):
                return connect
        return None
