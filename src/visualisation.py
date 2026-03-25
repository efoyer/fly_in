"""Module providing a matplotlib-based visual representation of the network."""

import matplotlib.pyplot as plt
from src.graph import Graph
import matplotlib.colors as mcolors
from typing import Any
import mplcursors as mpc


class Visualizer:
    """Provide static methods to render the drone network as an
    interactive map."""
    @staticmethod
    def load_visu(graph: Graph, map: str, turn: int) -> None:
        """Render the hub network as an interactive matplotlib scatter plot.

        Each hub is drawn as a colored dot at its (x, y) coordinates.
        Connections
        are drawn as black lines between hubs. Hovering over a hub displays a
        tooltip with its name, zone type, and maximum drone capacity.

        The window title is set to the map filename, and the x-axis label
        shows the total number of simulation turns.

        Args:
            graph: The Graph object containing all hubs and connections
            to render.
            map: The map filename, used as the window title.
            turn: Total number of turns the simulation ran, displayed on
            the axis.
        """

        scatters = []
        for h in graph.hubs:
            color = h.color if h.color is not None else "gray"
            if not mcolors.is_color_like(color):
                color = 'gray'
            hub = plt.scatter(h.x, h.y, c=color, s=200, zorder=2)
            plt.text(h.x + 0.08, h.y + 0.08, h.name, rotation=20, zorder=3)
            scatters.append((hub, h))

        cursor = mpc.cursor([s[0] for s in scatters],
                            hover=mpc.HoverMode.Transient)

        @cursor.connect("add")
        def on_add(sel: Any) -> None:
            """Handle hover events by displaying hub metadata in a tooltip.

            Args:
                sel: The mplcursors selection object containing the artist
                    and annotation to update.
            """

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
        manager = plt.gcf().canvas.manager
        if manager is not None:
            manager.set_window_title(map)
        plt.xlabel(f"Total turn: {turn}")
        plt.show()
