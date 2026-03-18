import matplotlib.pyplot as plt
import numpy as np
from src.graph import Graph
from src.hub import Hub


class Visualizer:
    @staticmethod
    def load_visu(graph: Graph):
        x_pos = [hub.x for hub in graph.hubs]
        y_pos = [hub.y for hub in graph.hubs]
        xpoints = np.array(x_pos)
        ypoints = np.array(y_pos)
        plt.plot(xpoints, ypoints, 'o')
        plt.show()