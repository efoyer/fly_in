"""Module implementing a load-aware Dijkstra's algorithm for drone routing."""

from src.graph import Graph
from src.hub import Hub
import heapq


def dijkstra_graph(g: Graph,
                   load: dict[Hub, int]) -> tuple[float, tuple[Hub, ...]]:
    """Find the least-cost path from start to end hub using Dijkstra's algo.

    This is a load-aware variant: the cost to visit a hub is increased by
    the number of drones already assigned to pass through it. This naturally
    distributes drones across alternative routes and prevents congestion.

    Hubs with zone type 'blocked' (cost=None) are excluded from the search.
    Hubs with zone type 'priority' receive a tie-breaking bonus to be
    preferred over normal hubs when costs are equal.

    Args:
        g: The graph containing all hubs, connections, and start/end nodes.
        load: A dictionary mapping each hub to the number of drones already
            routed through it. Used to increase traversal cost for busy hubs.

    Returns:
        A tuple of (total_cost, path) where total_cost is the accumulated
        weighted cost of the path, and path is an ordered tuple of Hub
        objects from start to end (inclusive). Returns (inf, ()) if no
        path exists.
    """

    adjaency: dict[Hub, list[tuple[int, Hub]]] = {}
    for c in g.connect:
        if c.end.cost is None or c.start.cost is None:
            continue
        if c.start not in adjaency:
            adjaency[c.start] = []
        adjaency[c.start].append((c.end.cost, c.end))
        if c.end not in adjaency:
            adjaency[c.end] = []
        adjaency[c.end].append((c.start.cost, c.start))
    i = 0
    if g.start.zone == "priority":
        bonus = 0
    else:
        bonus = 1

    queue: list[tuple[int, int, int, Hub, tuple[Hub, ...]]] = [
        (0, bonus, i, g.start, ())]
    visited, dist = set(), {g.start: 0.0}

    while queue:
        cost, bonus, _, node, path = heapq.heappop(queue)
        if node not in visited:
            visited.add(node)
            path = path + (node,)
            if node == g.end:
                return (cost, path)

            for cost2, node2 in adjaency.get(node, ()):
                if node2 in visited:
                    continue
                if node2.zone == "priority":
                    bonus_priority = 0
                else:
                    bonus_priority = 1
                load_cost = cost2 + load.get(node2, 0)
                if cost + load_cost < dist.get(node2, float('inf')):
                    dist[node2] = cost + load_cost
                    i += 1
                    heapq.heappush(queue, (cost + load_cost, bonus_priority,
                                           i, node2, path))
    return (float('inf'), ())
