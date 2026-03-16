from graph import Graph
from parser import Parser
from dijkstra import dijkstra_graph
from drone import Drone
from hub import Hub


class ControlCenter:
    def __init__(self, graph: Graph):
        self.graph = graph
        self.turn = 0
        self.drones: list[Drone] = []
        self.load = {}
        self.load_drones()

    def load_drones(self) -> None:
        i = 1
        load: dict = {}
        for drone in range(self.graph.nb_drones):
            _, path = dijkstra_graph(graph, load)
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
        position: dict = {}
        for drone in self.drones:
            position[drone.position] = position.get(drone.position, 0) + 1
        sort_drone = sorted(self.drones, key=lambda d: d.path_index,
                            reverse=True)
        res_str: str = ""
        for drone in sort_drone:
            if drone.waiting > 0:
                drone.waiting -= 1
                continue

            next: Hub = drone.get_next_hub()
            if next is None:
                drone.is_arrived = True
            else:
                in_next = position.get(next, 0)
                if in_next < next.max_drones:
                    position[drone.position] = (
                        position.get(drone.position, 0) - 1)
                    position[next] = (position.get(next, 0) + 1)
                    drone.to_next_hub(next)
                    if next.zone == "restricted":
                        drone.waiting = 1
                    res_str += f"{drone.id}-{next.get_name()} "

        self.drones = [drone for drone in self.drones if not drone.is_arrived]
        return res_str


if __name__ == "__main__":
    graph = Parser.load("maps/hard/03_ultimate_challenge.txt")
    # graph = Parser.load("test.txt")
    cc = ControlCenter(graph)
    cc.run()
