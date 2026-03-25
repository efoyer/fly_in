*This project has been created as part of the 42 curriculum by efoyer.*

# fly_in

## Description

**fly_in** is a drone traffic simulation system designed to route a fleet of drones from a start hub to an end hub through a network of interconnected nodes. Each hub in the network has properties such as a zone type, a maximum drone capacity, and positional coordinates. Connections between hubs may also have limited capacity.

The goal is to route all drones as efficiently as possible — minimizing the total number of turns — while respecting all constraints: hub capacity, connection throughput, and zone-specific rules (blocked, restricted, priority, or normal).

### Key Features

- **Graph-based routing**: The network is modeled as a weighted, undirected graph parsed from a custom file format.
- **Multi-drone pathfinding**: Each drone is assigned an optimal path using a load-aware variant of Dijkstra's algorithm, preventing congestion by distributing traffic across alternative routes.
- **Zone system**: Hubs can belong to four zone types — `normal`, `priority`, `restricted`, and `blocked` — each affecting traversal cost and behavior.
- **Turn-by-turn simulation**: The control center simulates drone movement step by step, handling capacity constraints, restricted zone transit logic, and connection throughput limits.
- **Interactive visualization**: A matplotlib-based map renders the network graphically, with hover tooltips displaying hub metadata.

---

## Algorithm Choices and Implementation Strategy

### Dijkstra with Load Balancing

The core routing algorithm is a modified Dijkstra's shortest path algorithm (`src/dijkstra.py`). Standard Dijkstra finds the single shortest path — but with multiple drones, routing all of them along the same path would create congestion. The solution is a **load-aware cost function**:

- Each time a drone is assigned a path, the nodes it passes through are recorded in a `load` dictionary.
- When computing the next drone's path, the cost to visit a node is increased by its current load: `cost = base_cost + load[node]`.
- This naturally spreads drones across alternative routes, reducing bottlenecks.

Zone types influence traversal cost:
- `priority`: cost bonus of 0 (preferred)
- `normal`: cost of 1
- `restricted`: cost of 2 (penalized, and requires transit logic)
- `blocked`: excluded from pathfinding (`cost = None`)

### Turn Simulation and Transit Logic

The control center (`fly_in.py`) simulates movement turn by turn. On each step:

1. Drones are sorted by their current `path_index` in descending order — drones closest to the destination move first, preventing blocking.
2. For each drone, the system checks whether the next hub has capacity and whether the connection allows additional traffic.
3. **Restricted zones** use a two-phase transit mechanism: a drone first "enters transit" toward a restricted hub (occupying it virtually), then resolves its move on the next step. This prevents race conditions where two drones both think a restricted hub is available.

### Parser

The parser (`src/parser.py`) reads a custom key-value configuration file defining the graph. It validates hub names, zone types, colors, connection capacity, and enforces structural rules such as no duplicate hubs, no self-connections, and the presence of a path to the end hub.

---

## Visual Representation

The visualization (`src/visualisation.py`) uses **matplotlib** and **mplcursors** to render the drone network as an interactive 2D map:

- **Nodes** (hubs) are displayed as colored scatter points. Colors are defined per hub in the input file (e.g., red, blue, green, gray).
- **Edges** (connections) are drawn as black lines between hubs.
- **Hub labels** are shown next to each node with a slight offset and rotation for readability.
- **Hover tooltips**: Using `mplcursors`, hovering over any hub displays a popup with its name, zone type, and maximum drone capacity. This allows quick inspection of the network without reading the source file.
- The window title shows the map filename, and the x-axis label displays the total number of turns the simulation took.

This visual layer makes it easy to reason about network topology, identify bottlenecks, and verify routing decisions at a glance.

---

## Instructions

### Requirements

- Python 3.10+
- pip packages: `matplotlib`, `mplcursors`, `flake8`, `mypy`

### Installation

```bash
make install
```

Or using a virtual environment:

```bash
make venv
source venv/bin/activate
```

### Running

```bash
make run ARG=maps/your_map_file.txt
```

Or directly:

```bash
python3 fly_in.py maps/your_map_file.txt
```

### Linting

```bash
make lint
```

### Input File Format

The input file uses a simple key-value format:

```
nb_drones: 3
start_hub: A 0 0
end_hub: Z 10 10
hub: B 5 5 [color=blue zone=restricted max_drones=2]
connection: A-B
connection: B-Z [max_link_capacity=2]
```

**Keys:**
| Key | Description |
|---|---|
| `nb_drones` | Number of drones to route |
| `start_hub` | Starting hub (name x y [meta]) |
| `end_hub` | Destination hub (name x y [meta]) |
| `hub` | Intermediate hub (name x y [meta]) |
| `connection` | Edge between two hubs, with optional `[max_link_capacity=N]` |

**Zone types:** `normal`, `priority`, `restricted`, `blocked`

**Colors:** `red`, `blue`, `green`, `gray`, `white`, `black`, `pink`

---

## Resources

### Dijkstra's Algorithm

- [Dijkstra's algorithm — Wikipedia](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- [Python `heapq` documentation](https://docs.python.org/3/library/heapq.html)

### Python Type Checking

- [mypy documentation](https://mypy.readthedocs.io/en/stable/)
- [PEP 484 — Type Hints](https://peps.python.org/pep-0484/)

### Visualization

- [matplotlib documentation](https://matplotlib.org/stable/index.html)
- [mplcursors documentation](https://mplcursors.readthedocs.io/en/stable/)

### AI Usage

AI was used **exclusively for educational purposes** throughout this project — it provided no direct code. Specifically:

- **Dijkstra's algorithm**: AI helped clarify concepts (priority queues, relaxation, load-aware cost functions) by asking guiding questions that helped develop and validate my own understanding and implementation ideas.
- **Visualization**: AI explained matplotlib and mplcursors concepts and helped me think through how to structure interactive hover behavior, without writing any code.
- **Type checking (mypy / flake8)**: AI helped me understand type annotation errors and linting rules by discussing them conceptually, leaving me to apply fixes independently.

In all cases, the approach was Socratic: AI asked questions to help me develop my own ideas rather than providing solutions.