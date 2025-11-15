from similarity import calculate_final_similarity


def calculate_group_cost(group, graph, alpha, beta):
    """
    Calculates the cost of a single group.
    cost(G) = sum(1 - S_final(Ri, Rj)) for all pairs (i, j) in G.
    """
    cost = 0
    if len(group) < 2:
        return 0.0

    for i in range(len(group)):
        for j in range(i + 1, len(group)):
            route_i = group[i]
            route_j = group[j]
            similarity = calculate_final_similarity(route_i, route_j, graph, alpha, beta)
            cost += (1.0 - similarity)

    return cost


def run_static_matching(routes, graph, alpha, beta):
    """
    Implements a simple agglomerative clustering based on the
    "Partition Merging" description.

    It iteratively merges the two "closest" groups (the merge
    that results in the lowest cost increase) until no
    more "good" merges can be made.
    """
    # 1. Start with each route in its own group
    groups = [[route] for route in routes]

    while len(groups) > 1:
        best_merge = None
        min_cost_increase = float('inf')

        # 2. Find the best pair of groups to merge
        for i in range(len(groups)):
            for j in range(i + 1, len(groups)):
                group_i = groups[i]
                group_j = groups[j]

                cost_before = calculate_group_cost(group_i, graph, alpha, beta) + \
                              calculate_group_cost(group_j, graph, alpha, beta)

                merged_group = group_i + group_j
                cost_after = calculate_group_cost(merged_group, graph, alpha, beta)

                cost_increase = cost_after - cost_before

                if cost_increase < min_cost_increase:
                    min_cost_increase = cost_increase
                    best_merge = (i, j)

        # 3. Perform the merge
        MERGE_COST_THRESHOLD = 0.5

        if best_merge and min_cost_increase < MERGE_COST_THRESHOLD:
            i, j = best_merge
            idx_low = min(i, j)
            idx_high = max(i, j)

            groups[idx_low].extend(groups[idx_high])
            del groups[idx_high]
        else:
            break

    return groups
