from graph import Graph


def dijkstra(g, src, target):
    import heapq
    queue = [(0, src, ())]
    visited, dist = set(), {src: 0.0}
    while queue:
        cost, node, path = heapq.heappop(queue)
        if node not in visited:
            visited.add(node)
            path += (node,)
            if node == target:
                return (cost, path)

            for cost2, node2 in g.get(node, ()):
                if node2 in visited:
                    continue
                if cost + cost2 < dist.get(node2, float('inf')):
                    dist[node2] = cost + cost2
                    heapq.heappush(queue, (cost + cost2, node2, path))
    return (float('inf'), ())


def dijkstra_graph(g: Graph):
    import heapq
    adjaency = {}
    for c in g.connect:
        if c.end.cost is None:
            continue
        if c.start not in adjaency:
            adjaency[c.start] = []
        adjaency[c.start].append((c.end.cost, c.end))
        if c.end not in adjaency:
            adjaency[c.end] = []
        adjaency[c.end].append((c.start.cost, c.start))



if __name__ == '__main__':
    edges = [
        ('A', 'B', 7),
        ('A', 'D', 5),
        ('B', 'C', 8),
        ('B', 'D', 9),
        ('B', 'E', 7),
        ('C', 'E', 5),
        ('D', 'E', 15),
        ('D', 'F', 6),
        ('E', 'F', 8),
        ('E', 'G', 9),
        ('F', 'G', 11)
    ]
    g = {}
    for src, target, cost in edges:
        if src not in g:
            g[src] = []
        g[src].append((cost, target))
    src, target = 'A', 'G'
    print(f"{src} -> {target}:")
    print(dijkstra(g, src, target))
