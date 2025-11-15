# routes/run_experiments.py
# Main script to run the case study from Chapter 2, now including Fairness metrics.

import route_generator as gen
import similarity
import static_matching
import greedy_mathcing
import metrics

# --- Simulation Parameters ---
ALPHA = 0.5
BETA = 0.5
NUM_ROUTES = 10

def print_results(scenario_name, groups, all_routes):
    """Helper function to print formatted results, including new Fairness metric."""

    num_groups = len(groups)
    avg_size = metrics.calculate_avg_group_size(groups)
    travel_gain = metrics.calculate_travel_gain(groups, all_routes)

    max_relative_detour = metrics.calculate_fairness(groups)

    print(f"  Groups formed: {num_groups}")
    print(f"  Avg. group size: {avg_size:.2f}")
    print(f"  Travel Gain: {travel_gain:.2%}")
    print(f"  Max Relative Detour (MRD): {max_relative_detour:.2%}")


def main():
    """
    Runs the full experiment for Chapter 2.
    """
    print("Initializing experiment...")
    print(f"Parameters: ALPHA={ALPHA}, BETA={BETA}, NUM_ROUTES={NUM_ROUTES}\n")

    graph = gen.generate_graph()

    scenarios = ['identical', 'partial', 'different']

    for scenario in scenarios:
        print(f"--- Running Scenario: {scenario.upper()} ---")

        # 1. Generate routes for this scenario
        routes = gen.generate_routes(graph, scenario, NUM_ROUTES)

        # 2. Run Static Matching (Experiment 1)
        print("\n  Running Static Matching (Partition Merging)...")
        static_groups = static_matching.run_static_matching(routes, graph, ALPHA, BETA)
        print_results(f"Static ({scenario})", static_groups, routes)

        # 3. Run Greedy Matching (Experiment 1)
        print("\n  Running Greedy Matching (Dynamic)...")
        greedy_groups = greedy_mathcing.run_greedy_matching(routes, graph, ALPHA, BETA)
        print_results(f"Greedy ({scenario})", greedy_groups, routes)
        print("-" * 40 + "\n")

    # 4. Run Experiment 2: Impact of Alpha/Beta
    print(f"--- Running Experiment 2: Impact of Parameters ---")
    print("  (Using 'partial' scenario as testbed)\n")
    routes = gen.generate_routes(graph, 'partial', NUM_ROUTES)

    for alpha in [0.1, 0.5, 0.9]:
        beta = 1.0 - alpha
        print(f"  Testing with Alpha = {alpha:.1f}, Beta = {beta:.1f}")

        # Static Match
        static_groups = static_matching.run_static_matching(routes, graph, alpha, beta)
        travel_gain = metrics.calculate_travel_gain(static_groups, routes)
        mrd = metrics.calculate_fairness(static_groups)  # NEW MRD CALCULATION
        print(f"    Static Match Travel Gain: {travel_gain:.2%}, MRD: {mrd:.2%}")  # UPDATED PRINT

        # Greedy Match
        greedy_groups = greedy_mathcing.run_greedy_matching(routes, graph, alpha, beta)
        travel_gain_greedy = metrics.calculate_travel_gain(greedy_groups, routes)
        mrd_greedy = metrics.calculate_fairness(greedy_groups)  # NEW MRD CALCULATION
        print(f"    Greedy Match Travel Gain: {travel_gain_greedy:.2%}, MRD: {mrd_greedy:.2%}\n")  # UPDATED PRINT


if __name__ == "__main__":
    main()