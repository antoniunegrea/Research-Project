from similarity import calculate_final_similarity
from static_matching import calculate_group_cost
import random

def _calculate_delta_cost(group, new_route, graph, alpha, beta):
    """
    Calculates the *change* in cost by adding new_route to group.
    Delta_cost = cost(G + Uk) - cost(G)
    """
    cost_before = calculate_group_cost(group, graph, alpha, beta)

    cost_increase = 0
    for existing_route in group:
        similarity = calculate_final_similarity(existing_route, new_route, graph, alpha, beta)
        cost_increase += (1.0 - similarity)

    return cost_increase

def run_greedy_matching(routes, graph, alpha, beta):
    """
    Implements the greedy matching algorithm.
    Each incoming route (request) is assigned to the group
    with the minimum Delta_cost.
    """
    groups = []

    requests = list(routes)
    random.shuffle(requests)

    for new_route in requests:
        min_delta_cost = float('inf')
        best_group_index = -1

        for i, group in enumerate(groups):
            delta_cost = _calculate_delta_cost(group, new_route, graph, alpha, beta)

            if delta_cost < min_delta_cost:
                min_delta_cost = delta_cost
                best_group_index = i

        JOIN_COST_THRESHOLD = 0.5

        if best_group_index != -1 and min_delta_cost < JOIN_COST_THRESHOLD:
            groups[best_group_index].append(new_route)
        else:
            groups.append([new_route])

    return groups