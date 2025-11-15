import random

BASE_LAT = 40.7000
BASE_LON = -74.0000
STEP_LAT = 0.0005
STEP_LON = 0.0005
GRID_SIZE = 5

def generate_graph():
    """
    Generates a graph where each node (i, j) has (lat, lon) coordinates.
    Returns a dictionary: {(i, j): (lat, lon)}
    """
    graph = {}
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            lat = BASE_LAT + i * STEP_LAT
            lon = BASE_LON + j * STEP_LON
            graph[(i, j)] = (lat, lon)
    return graph

def generate_random_route(graph, min_len=3, max_len=5):
    """Helper to create a single random route on the graph."""

    start_node = random.choice(list(graph.keys()))
    route = [start_node]

    current_node = start_node
    route_len = random.randint(min_len, max_len)

    for _ in range(route_len - 1):
        possible_moves = []
        i, j = current_node

        if (i + 1, j) in graph: possible_moves.append((i + 1, j))
        if (i - 1, j) in graph: possible_moves.append((i - 1, j))
        if (i, j + 1) in graph: possible_moves.append((i, j + 1))
        if (i, j - 1) in graph: possible_moves.append((i, j - 1))

        if len(route) > 1 and len(possible_moves) > 1:
            last_node = route[-2]
            if last_node in possible_moves:
                possible_moves.remove(last_node)

        if not possible_moves:
            break

        next_node = random.choice(possible_moves)
        route.append(next_node)
        current_node = next_node

    return route

def generate_routes(graph, scenario, num_routes=10):
    """
    Generates a list of routes based on the specified scenario.
    A route is a list of nodes, e.g., [(0,0), (0,1), (1,1)]
    """
    routes = []
    if scenario == 'identical':
        route = generate_random_route(graph)
        for _ in range(num_routes):
            routes.append(list(route))
    elif scenario == 'partial':
        main_route = generate_random_route(graph, min_len=5, max_len=5)
        routes.append(main_route)

        mid_point_idx = len(main_route) // 2
        shared_segment = main_route[mid_point_idx - 1: mid_point_idx + 2]

        for _ in range(num_routes - 1):
            prefix = generate_random_route(graph, min_len=2, max_len=2)

            suffix = generate_random_route(graph, min_len=2, max_len=2)

            new_route = prefix + shared_segment + suffix
            routes.append(new_route)
    elif scenario == 'different':
        for _ in range(num_routes):
            routes.append(generate_random_route(graph))

    print(f"  Generator: Created {len(routes)} routes for '{scenario}' scenario.")
    return routes
