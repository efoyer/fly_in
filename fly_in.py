from src.graph import Graph
from src.parser import Parser
from src.dijkstra import dijkstra_graph
from src.drone import Drone
from src.hub import Hub
from src.visualisation import Visualizer
import sys


class ControlCenter:
    def __init__(self, graph: Graph):
        self.graph = graph
        self.turn = 1
        self.drones: list[Drone] = []
        self.load = {}
        self.load_drones()

    def load_drones(self) -> None:
        i = 1
        load: dict = {}
        for drone in range(self.graph.nb_drones):
            _, path = dijkstra_graph(self.graph, load)
            drone = Drone(f"D{i}", self.graph.start, path)
            self.drones.append(drone)

            for hub in path:
                load[hub] = load.get(hub, 0) + 1
            i += 1

    def get_drones(self):
        for drone in self.drones:
            print(drone.get_info())
            print()

    def run(self):
        while self.drones:
            moves = self.step()
            if moves:
                print(f"Turn {self.turn}: {moves}")
                self.turn += 1

    def step(self):
        try:
            position: dict = {}
            link_us: dict = {}
            for drone in self.drones:
                position[drone.position] = position.get(drone.position, 0) + 1

            sort_drone = sorted(self.drones, key=lambda d: d.path_index,
                                reverse=True)
            res_str: str = ""
            for d in sort_drone:
                if d.waiting > 0:
                    d.waiting -= 1
                    continue

                next: Hub = d.get_next_hub()
                if next is None:
                    d.is_arrived = True
                else:
                    cn_to_next = self.graph.get_connection(d.position, next)
                    if cn_to_next is None:
                        raise ValueError(f"Error at turn {self.turn}: "
                                         f"{d.id} has an invalid connection")
                    in_next = position.get(next, 0)
                    if (in_next < next.max_drones and
                       link_us.get(cn_to_next, 0) < cn_to_next.max):
                        position[d.position] = (
                            position.get(d.position, 0) - 1)
                        position[next] = (position.get(next, 0) + 1)
                        link_us[cn_to_next] = link_us.get(cn_to_next, 0) + 1
                        d.to_next_hub(next)
                        if next.zone == "restricted":
                            d.waiting = 1
                        res_str += f"{d.id}-{next.get_name()} "

            self.drones = [d for d in self.drones if not d.is_arrived]
            return res_str
        except ValueError as e:
            print(e)


def main():
    if len(sys.argv) == 2:
        path = sys.argv[1]
        graph = Parser.load(path)
        cc = ControlCenter(graph)
        cc.run()
        Visualizer.load_visu(graph)
    else:
        print("No arguments")
        sys.exit(1)


if __name__ == "__main__":
    main()
