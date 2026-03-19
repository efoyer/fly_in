import matplotlib.pyplot as plt
import mplcursors
# import numpy as np
from src.graph import Graph
import matplotlib.colors as mcolors


class Visualizer:
    @staticmethod
    def load_visu(graph: Graph, map: str, turn: int):
        scatters = []
        for h in graph.hubs:
            color = h.color
            if not mcolors.is_color_like(color):
                color = 'gray'
            hub = plt.scatter(h.x, h.y, c=color, s=200, zorder=2)
            plt.text(h.x + 0.08, h.y + 0.08, h.name, rotation=20, zorder=3)
            scatters.append((hub, h))

        cursor = mplcursors.cursor([s[0] for s in scatters],
                                   hover=mplcursors.HoverMode.Transient)

        @cursor.connect("add")
        def on_add(sel):
            hub = next(h for sc, h in scatters if sc == sel.artist)
            sel.annotation.set_text(
                f"Name: {hub.name}\n"
                f"Type: {hub.zone}\n"
                f"Max drones: {hub.max_drones}"
            )
            sel.annotation.get_bbox_patch().set(fc="white", alpha=0.9)

        for c in graph.connect:
            x = [c.start.x, c.end.x]
            y = [c.start.y, c.end.y]
            plt.plot(x, y, color='black', zorder=1)
        plt.gcf().canvas.manager.set_window_title(map)
        plt.xlabel(f"Total turn: {turn}")
        plt.show()
