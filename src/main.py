from algorithms.cycle_canceling import CycleCanceling
from utils.file_utils import FileUtils
from utils.graph_metrics import GraphMetrics
from utils.metrics_calculator import MetricsCalculator
from algorithms.edmonds_karp import EdmondsKarp
from algorithms.successive_shortest_paths import SuccessiveShortestPaths
from algorithms.successive_shortest_paths_sc import SuccessiveShortestPathsSC
from algorithms.capacity_scaling import CapacityScaling

def main():
    # Simulation II
    print("Simulation I\n")
    print("Reading graphs, finding the largest SCC, and selecting source/sink...")

    # Define the input graph files and their parameters
    input_files = [
        "output/graph1.txt",
        "output/graph2.txt",
        "output/graph3.txt",
        "output/graph4.txt",
        "output/graph5.txt",
        "output/graph6.txt",
        "output/graph7.txt",
        "output/graph8.txt"
    ]

    graph_params = [
        (100, 0.2, 8, 5),    # Graph 1: (n, r, upperCap, upperCost)
        (200, 0.2, 8, 5),    # Graph 2
        (100, 0.3, 8, 5),    # Graph 3
        (200, 0.3, 8, 5),    # Graph 4
        (100, 0.2, 64, 20),  # Graph 5
        (200, 0.2, 64, 20),  # Graph 6
        (100, 0.3, 64, 20),  # Graph 7
        (200, 0.3, 64, 20)   # Graph 8
    ]

    # Initialize result tables
    graph_characteristics = []  # Table 1 data
    algorithm_results = []  # Table 2 data

    for i, (input_file, params) in enumerate(zip(input_files, graph_params)):
        print(f"\nProcessing file: {input_file} (Graph {i + 1})")

        # Step 1: Read the graph and convert it into an adjacency list
        adjacency_list = FileUtils.read_graph_from_file(input_file)

        # Step 2: Find the largest SCC
        largest_scc = GraphMetrics.find_largest_scc(adjacency_list)

        # Step 3: Select source and sink from the SCC
        source, sink = GraphMetrics.select_source_and_sink(largest_scc)

        # Step 4: Compute maximum flow using Edmonds-Karp
        max_flow = EdmondsKarp.compute_max_flow(largest_scc, source, sink)

        # Step 5: Calculate metrics for the LCC
        node_count = MetricsCalculator.calculate_node_count(largest_scc)
        max_out_degree = MetricsCalculator.calculate_max_out_degree(largest_scc)
        max_in_degree = MetricsCalculator.calculate_max_in_degree(largest_scc)
        average_degree = MetricsCalculator.calculate_average_degree(largest_scc)

        # Record graph characteristics for Table 1
        graph_characteristics.append([
            i + 1,               # Graph number
            params[0],           # n
            params[1],           # r
            params[2],           # upperCap
            params[3],           # upperCost
            max_flow,            # fmax
            node_count,          # |VLCC|
            max_out_degree,      # Δout(LCC)
            max_in_degree,       # Δin(LCC)
            round(average_degree, 2)  # k(LCC)
        ])

        # Step 6: Set required flow as 95% of the maximum flow
        required_flow = int(0.95 * max_flow)

        # Step 7: Run algorithms
        algorithms = [
            ("SSP", SuccessiveShortestPaths),
            ("CS", CapacityScaling),
            ("SSPSC", SuccessiveShortestPathsSC),
            ("CycleCanceling", CycleCanceling)        
            ]

        for algo_name, algo_class in algorithms:
            print(f"Running {algo_name}...")
            metrics = algo_class.compute_metrics(largest_scc, source, sink, required_flow)

            # Record results for Table 2
            algorithm_results.append([
                algo_name,                # Algorithm name
                i + 1,                   # Graph number
                metrics.get_total_flow(),  # f
                metrics.get_min_cost(),    # MC
                metrics.get_num_augmenting_paths(),  # paths
                round(metrics.compute_mean_length(), 4),  # ML
                round(metrics.compute_mean_proportional_length(), 4)  # MPL
            ])

    # Step 8: Display results as tables
    print_results("Table 1: Graph Characteristics", graph_characteristics,
                  ["Graph", "n", "r", "upperCap", "upperCost", "fmax", "|VLCC|", "Δout(LCC)", "Δin(LCC)", "k(LCC)"])
    print_results("Table 2: Algorithm Results", algorithm_results,
                  ["Algorithm", "Graph", "f", "MC", "paths", "ML", "MPL"])
    

    # Simulation II
    print("\n\nSimulation II\n")
    print("Reading graphs, finding the largest SCC, and selecting source/sink...")

    # Define the input graph files and their parameters
    custom_files = [
    "output/custom_graph1.txt",
    "output/custom_graph2.txt"
    ]

    graph_params = [
        (50, 0.1, 10, 50),  
        (200, 0.5, 100, 20)
    ]

    # Initialize result tables
    custom_graph_characteristics = []  # Table 1 data
    custom_algorithm_results = []  # Table 2 data

    for i, (input_file, params) in enumerate(zip(input_files, graph_params)):
        print(f"\nProcessing file: {input_file} (Graph {i + 1})")

        # Step 1: Read the graph and convert it into an adjacency list
        adjacency_list = FileUtils.read_graph_from_file(input_file)

        # Step 2: Find the largest SCC
        largest_scc = GraphMetrics.find_largest_scc(adjacency_list)

        # Step 3: Select source and sink from the SCC
        source, sink = GraphMetrics.select_source_and_sink(largest_scc)

        # Step 4: Compute maximum flow using Edmonds-Karp
        max_flow = EdmondsKarp.compute_max_flow(largest_scc, source, sink)

        # Step 5: Calculate metrics for the LCC
        node_count = MetricsCalculator.calculate_node_count(largest_scc)
        max_out_degree = MetricsCalculator.calculate_max_out_degree(largest_scc)
        max_in_degree = MetricsCalculator.calculate_max_in_degree(largest_scc)
        average_degree = MetricsCalculator.calculate_average_degree(largest_scc)

        # Record graph characteristics for Table 1
        custom_graph_characteristics.append([
            i + 1,               # Graph number
            params[0],           # n
            params[1],           # r
            params[2],           # upperCap
            params[3],           # upperCost
            max_flow,            # fmax
            node_count,          # |VLCC|
            max_out_degree,      # Δout(LCC)
            max_in_degree,       # Δin(LCC)
            round(average_degree, 2)  # k(LCC)
        ])

        # Step 6: Set required flow as 95% of the maximum flow
        required_flow = int(0.95 * max_flow)

        # Step 7: Run algorithms
        algorithms = [
            ("SSP", SuccessiveShortestPaths),
            ("CS", CapacityScaling),
            ("SSPSC", SuccessiveShortestPathsSC),
            ("CycleCanceling", CycleCanceling)        
            ]

        for algo_name, algo_class in algorithms:
            print(f"Running {algo_name}...")
            metrics = algo_class.compute_metrics(largest_scc, source, sink, required_flow)

            # Record results for Table 2
            custom_algorithm_results.append([
                algo_name,                # Algorithm name
                i + 1,                   # Graph number
                metrics.get_total_flow(),  # f
                metrics.get_min_cost(),    # MC
                metrics.get_num_augmenting_paths(),  # paths
                round(metrics.compute_mean_length(), 4),  # ML
                round(metrics.compute_mean_proportional_length(), 4)  # MPL
            ])

    # Step 8: Display results as tables
    print_results("Table 1: Graph Characteristics", custom_graph_characteristics,
                  ["Graph", "n", "r", "upperCap", "upperCost", "fmax", "|VLCC|", "Δout(LCC)", "Δin(LCC)", "k(LCC)"])
    print_results("Table 2: Algorithm Results", custom_algorithm_results,
                  ["Algorithm", "Graph", "f", "MC", "paths", "ML", "MPL"])


def print_results(title, data, headers):
    """
    Print a table with headers and data.
    :param title: Title of the table.
    :param data: List of rows (each row is a list).
    :param headers: List of column headers.
    """
    print(f"\n{title}")
    col_widths = [max(len(str(row[i])) for row in data + [headers]) for i in range(len(headers))]
    format_row = " | ".join("{:<" + str(width) + "}" for width in col_widths)

    print(format_row.format(*headers))
    print("-" * (sum(col_widths) + 3 * (len(headers) - 1)))
    for row in data:
        print(format_row.format(*row))


if __name__ == "__main__":
    main()
