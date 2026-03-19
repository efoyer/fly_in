import matplotlib.pyplot as plt
# import numpy as np
from src.graph import Graph


class Visualizer:
    @staticmethod
    def load_visu(graph: Graph, map: str):

        for h in graph.hubs:
            plt.scatter(h.x, h.y, h.color, 200)
            plt.text(h.x + 0.02, h.y + 0.002, h.name, 0)

        for c in graph.connect:
            plt.plot(c.start.x, c.end.y, 'black')
        plt.gcf().canvas.manager.set_window_title(map)
        plt.show()
