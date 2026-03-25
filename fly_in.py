from src.graph import Graph
from src.parser import Parser
from src.dijkstra import dijkstra_graph
from src.drone import Drone
from src.hub import Hub
from src.connection import Connection
from src.visualisation import Visualizer
import sys
from typing import Optional


class ControlCenter:
    """Orchestrate drone routing and turn-by-turn movement simulation.

    The ControlCenter builds the initial drone fleet, assigns each drone
    a load-balanced path via Dijkstra, then simulates movement turn by turn
    while respecting hub capacity, connection throughput, and restricted
    zone transit rules.
    """

    def __init__(self, graph: Graph):
        """Initialize the ControlCenter with a parsed graph.

        Assigns paths to all drones using load-aware Dijkstra, distributing
        traffic to avoid congestion.

        Args:
            graph: The Graph object representing the full routing network.
        """
        self.graph = graph
        self.turn = 1
        self.drones: list[Drone] = []
        self.load: dict[Hub, int] = {}
        self.load_drones()

    def load_drones(self) -> None:
        """Instantiate all drones and assign each a load-balanced path.

        Iterates over the required number of drones. For each drone, runs
        Dijkstra with the current load state to find the least-congested path,
        then updates the load map before computing the next drone's path.
        """
        i = 1
        load: dict[Hub, int] = {}
        for _ in range(self.graph.nb_drones):
            _, path = dijkstra_graph(self.graph, load)
            drone = Drone(f"D{i}", self.graph.start, path)
            self.drones.append(drone)

            for hub in path:
                load[hub] = load.get(hub, 0) + 1
            i += 1

    def get_drones(self) -> None:
        """Print the current state of all drones to stdout."""
        for drone in self.drones:
            print(drone.get_info())
            print()

    def run(self) -> None:
        """Run the full simulation until all drones have reached the
        destination.

        On each turn, calls step() to advance all drones by one move and
        prints the result. Stops when no drones remain in the fleet.
        """
        while self.drones:
            moves = self.step()
            if moves:
                print(f"Turn {self.turn}: {moves}")
                self.turn += 1
        self.turn -= 1

    def step(self) -> Optional[str]:
        """Advance all drones by one simulation step.

        Processes each drone in order of descending path progress (drones
        closest to the destination move first) to avoid blocking. Respects:
        - Hub capacity (max_drones per hub)
        - Connection throughput (max_link_capacity per connection per turn)
        - Restricted zone transit: drones entering a restricted hub do so
          over two turns — first reserving the slot, then completing the move.

        Returns:
            A string summarising all drone movements this turn, or None
            if a fatal routing error was encountered.
        """
        try:
            position: dict[Hub, int] = {}
            link_us: dict[Connection, int] = {}

            for drone in self.drones:
                position[drone.position] = position.get(drone.position, 0) + 1

            sort_drone = sorted(self.drones, key=lambda d: d.path_index,
                                reverse=True)
            res_str: str = ""
            for d in sort_drone:
                if d.transit:
                    nh = d.dest_res
                    if nh is None:
                        raise ValueError(f"Error at turn {self.turn}")
                    in_next = position.get(nh, 0)
                    if in_next < nh.max_drones:
                        cn_to_next = self.graph.get_connection(
                            d.position, nh)
                        if cn_to_next is None:
                            raise ValueError(f"Error at turn {self.turn}")
                        position[d.position] = (
                            position.get(d.position, 0) - 1)
                        position[nh] = (position.get(nh, 0) + 1)
                        d.transit = False
                        d.dest_res = None
                        link_us[cn_to_next] = link_us.get(cn_to_next, 0) + 1
                        d.to_next_hub(nh)
                        res_str += f"{d.id}-{nh.get_name()}"
                    else:
                        raise ValueError("Errorr")

                else:
                    nh = d.get_next_hub()
                    next_hub = nh

                    if next_hub is None:
                        d.is_arrived = True
                    else:
                        cn_to_next = self.graph.get_connection(
                            d.position, next_hub)
                        in_next = position.get(next_hub, 0)
                        if cn_to_next is None:
                            raise ValueError(f"Error at turn {self.turn}: "
                                             f"{d.id} has an invalid "
                                             "connection")

                        if (next_hub.zone == "restricted" and not d.transit
                            and in_next < next_hub.max_drones and
                           link_us.get(cn_to_next, 0) < cn_to_next.max):
                            d.transit = True
                            d.dest_res = next_hub
                            cn_to_next = self.graph.get_connection(
                                d.position, next_hub)
                            in_next = position.get(next_hub, 0)
                            position[d.position] = (
                                position.get(d.position, 0) - 1)
                            position[next_hub] = (position.get(
                                next_hub, 0) + 1)
                            link_us[cn_to_next] = link_us.get(
                                cn_to_next, 0) + 1
                            if cn_to_next is None:
                                raise ValueError(f"Error at turn {self.turn}:"
                                                 f" {d.id} has an invalid "
                                                 "connection")
                            res_str += f"{d.id}-{cn_to_next.get_str()} "
                        else:
                            d.transit = False
                            if cn_to_next is None:
                                raise ValueError(f"Error at turn {self.turn}: "
                                                 f"{d.id} has an invalid "
                                                 "connection")

                            if (in_next < next_hub.max_drones and
                               link_us.get(cn_to_next, 0) < cn_to_next.max):

                                position[d.position] = (
                                    position.get(d.position, 0) - 1)
                                position[next_hub] = (
                                    position.get(next_hub, 0) + 1)
                                link_us[cn_to_next] = link_us.get(
                                    cn_to_next, 0) + 1
                                d.to_next_hub(next_hub)

                                res_str += f"{d.id}-{next_hub.get_name()} "

            self.drones = [d for d in self.drones if not d.is_arrived]
            return res_str
        except ValueError as e:
            print(e)
            return None


def main() -> None:
    """Advance all drones by one simulation step.

    Processes each drone in order of descending path progress (drones
    closest to the destination move first) to avoid blocking. Respects:
    - Hub capacity (max_drones per hub)
    - Connection throughput (max_link_capacity per connection per turn)
    - Restricted zone transit: drones entering a restricted hub do so
      over two turns — first reserving the slot, then completing the move.

    Returns:
        A string summarising all drone movements this turn, or None
        if a fatal routing error was encountered.
    """
    try:
        if len(sys.argv) == 2:
            path = sys.argv[1]
            graph = Parser.load(path)
            cc = ControlCenter(graph)
            cc.run()
            Visualizer.load_visu(graph, sys.argv[1], cc.turn)
        else:
            print("No arguments")
            sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(1)


if __name__ == "__main__":
    main()
