from graph import Graph
from parser import Parser
from dijkstra import dijkstra_graph
from drone import Drone


class ControlCenter:
    def __init__(self, graph: Graph):
        self.graph = graph
        _, self.path = dijkstra_graph(graph)
        self.turn = 0
        self.drones: list[Drone] = []
        self.load_drones()

    def load_drones(self) -> None:
        i = 1
        for drone in range(self.graph.nb_drones):
            drone = Drone(f"D{i}", self.graph.start, self.path)
            self.drones.append(drone)
            i += 1

    def get_drones(self):
        for drone in self.drones:
            print(drone.get_info())
            print()


if __name__ == "__main__":
    graph = Parser.load("test.txt")
    cc = ControlCenter(graph)
    print(cc.get_drones())
