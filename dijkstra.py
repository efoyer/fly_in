from graph import Graph
from parser import Parser


def dijkstra_graph(g: Graph, load: dict):
    import heapq
    adjaency = {}
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

    queue = [(0, bonus, i, g.start, ())]
    visited, dist = set(), {g.start: 0.0}
    while queue:
        cost, bonus, _, node, path = heapq.heappop(queue)
        if node not in visited:
            visited.add(node)
            path += (node,)
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


if __name__ == '__main__':
    graph = Parser.load("maps/hard/01_maze_nightmare.txt")
    cost, path = dijkstra_graph(graph)
    print(f"Coût total: {cost}")
    print(f"Chemin: {' -> '.join(str(hub) for hub in path)}")
