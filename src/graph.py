from src.hub import Hub
from src.connection import Connection
from typing import Optional


class Graph:
    def __init__(self, nb_drones: int, start: Hub, end: Hub,
                 hubs: list[Hub], connection: list[Connection]):
        self.nb_drones = nb_drones
        self.hubs = hubs
        self.connect = connection
        self.start = start
        self.end = end

    def get_infos(self) -> str:
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
        for connect in self.connect:
            if ((connect.start == hub1 and connect.end == hub2) or
               (connect.start == hub2 and connect.end == hub1)):
                return connect
        return None
