from similarity import _get_route_segments

def _get_route_length(route):
    """Returns the length of a route in number of segments."""
    return len(_get_route_segments(route))

def calculate_travel_gain(groups, all_routes):
    """
    Implements TravelGain = (D_solo - D_shared) / D_solo

    D_solo = Total segments of all routes driven individually.
    D_shared = Total unique segments driven by all groups.
    """

    d_solo = 0
    for route in all_routes:
        d_solo += _get_route_length(route)

    if d_solo == 0:
        return 0.0

    d_shared = 0
    for group in groups:
        if not group:
            continue

        group_segments = set()
        for route in group:
            group_segments.update(_get_route_segments(route))

        d_shared += len(group_segments)

    if d_solo == 0:
        return 0.0

    travel_gain = (d_solo - d_shared) / d_solo
    return travel_gain

def calculate_fairness(groups):
    """
    Implements the Fairness metric: Maximum Relative Detour (MRD).

    MRD = max( (T_shared,i - T_solo,i) / T_solo,i ) for all travelers i.

    In this abstract model, T is represented by the number of segments (length).
    T_shared is approximated by the length of the longest route in the group.
    """
    max_relative_detour = 0.0

    for group in groups:
        if len(group) < 2:
            continue

        # 1. Find the length of the Shared Route (T_shared) for the group.
        shared_route_length = max(_get_route_length(route) for route in group)

        # 2. Iterate over each traveler (route) in the group
        for route_i in group:
            t_solo_i = _get_route_length(route_i)
            t_shared_i = shared_route_length

            if t_solo_i <= 0:
                continue

            # Relative Detour (D_i)
            relative_detour = (t_shared_i - t_solo_i) / t_solo_i

            if relative_detour > max_relative_detour:
                max_relative_detour = relative_detour

    return max_relative_detour

def calculate_avg_group_size(groups):
    """Calculates the average number of routes per group."""
    if not groups:
        return 0.0
    total_routes = sum(len(group) for group in groups)
    return total_routes / len(groups)
