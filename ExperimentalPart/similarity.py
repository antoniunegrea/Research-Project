import math

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance in kilometers between two points
    on the earth (specified in decimal degrees).
    """
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371
    return c * r * 1000

def _get_route_points_coords(route, graph):
    """Helper to get a list of (lat, lon) tuples for a route."""
    return [graph[node] for node in route if node in graph]

def _get_route_segments(route):
    """
    Helper to convert a list of nodes into a set of segments (edges).
    e.g., [A, B, C] -> {(A, B), (B, C)}
    """
    segments = set()
    for i in range(len(route) - 1):
        # Use a consistent order (e.g., sorted tuple) to handle A-B vs B-A
        segment = tuple(sorted((route[i], route[i + 1])))
        segments.add(segment)
    return segments

def calculate_geometric_similarity(route1, route2, graph):
    """
    Implements S_geo from the document.
    S_geo = 1 - (1/|R1|) * sum(min_dist(p_in_R1, q_in_R2))

    Note: We interpret p and q as the *nodes* (GPS points) on the routes.
    """
    route1_coords = _get_route_points_coords(route1, graph)
    route2_coords = _get_route_points_coords(route2, graph)

    if not route1_coords or not route2_coords:
        return 0.0

    total_min_dist = 0
    for p_lat, p_lon in route1_coords:
        min_dist = float('inf')
        for q_lat, q_lon in route2_coords:
            dist = haversine(p_lat, p_lon, q_lat, q_lon)
            if dist < min_dist:
                min_dist = dist
        total_min_dist += min_dist

    avg_min_dist = total_min_dist / len(route1_coords)

    TOLERANCE_METERS = 100

    similarity = 1.0 - (avg_min_dist / TOLERANCE_METERS)

    return max(0.0, min(1.0, similarity))


def calculate_segment_overlap(route1, route2):
    """
    Implements S_overlap from the document.
    S_overlap = |R1 intersect R2| / max(|R1|, |R2|)

    Note: We interpret R1 and R2 as the set of *segments* in the routes.
    """
    segments1 = _get_route_segments(route1)
    segments2 = _get_route_segments(route2)

    if not segments1 or not segments2:
        return 0.0

    intersection_count = len(segments1.intersection(segments2))
    max_count = max(len(segments1), len(segments2))

    if max_count == 0:
        return 0.0

    return intersection_count / max_count


def calculate_final_similarity(route1, route2, graph, alpha, beta):
    """
    Implements S_final from the document.
    S_final = alpha * S_geo + beta * S_overlap
    """
    s_geo = calculate_geometric_similarity(route1, route2, graph)
    s_overlap = calculate_segment_overlap(route1, route2)

    return (alpha * s_geo) + (beta * s_overlap)