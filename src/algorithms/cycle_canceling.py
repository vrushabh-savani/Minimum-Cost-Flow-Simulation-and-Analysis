from collections import defaultdict, deque
from utils.flow_metrics import FlowMetrics
from graph.graph_generator import Edge

class CycleCanceling:
    @staticmethod
    def compute_metrics(adjacency_list, source, sink, required_flow):
        """
        Compute the minimum-cost flow using the Cycle Canceling Algorithm.

        :param adjacency_list: Adjacency list of the graph.
        :param source: Source node.
        :param sink: Sink node.
        :param required_flow: Desired flow to achieve.
        :return: FlowMetrics object containing computed metrics.
        """
        # Initialize FlowMetrics
        total_edges = sum(len(edges) for edges in adjacency_list.values())
        metrics = FlowMetrics(total_edges)

        # Step 1: Create residual graph with capacities and costs
        residual_capacity = defaultdict(lambda: defaultdict(int))
        edge_cost = defaultdict(lambda: defaultdict(int))

        for u, edges in adjacency_list.items():
            for edge in edges:
                residual_capacity[edge.from_node][edge.to_node] += edge.capacity
                edge_cost[edge.from_node][edge.to_node] = edge.cost
                # Add reverse edge with zero capacity and negative cost
                residual_capacity[edge.to_node][edge.from_node] += 0
                edge_cost[edge.to_node][edge.from_node] = -edge.cost

        # Step 2: Push initial feasible flow using a modified Ford-Fulkerson
        flow_sent = CycleCanceling._initialize_feasible_flow(
            residual_capacity, source, sink, required_flow
        )

        metrics.set_total_flow(flow_sent)

        # Step 3: Cancel negative-cost cycles iteratively
        path_count = 0
        cycle_lengths = []

        while True:
            # Detect a negative-cost cycle using Bellman-Ford
            cycle = CycleCanceling._find_negative_cycle(residual_capacity, edge_cost)
            if cycle is None:
                break  # No negative-cost cycles, algorithm terminates

            # Find the minimum residual capacity along the cycle
            cycle_capacity = float('inf')
            for u, v in zip(cycle, cycle[1:] + [cycle[0]]):
                cycle_capacity = min(cycle_capacity, residual_capacity[u][v])

            # Augment the flow along the cycle
            for u, v in zip(cycle, cycle[1:] + [cycle[0]]):
                residual_capacity[u][v] -= cycle_capacity
                residual_capacity[v][u] += cycle_capacity

            # Update metrics
            path_count += 1
            cycle_lengths.append(len(cycle))
            metrics.add_cost(cycle_capacity * sum(edge_cost[u][v] for u, v in zip(cycle, cycle[1:] + [cycle[0]])))

        # Step 4: Finalize metrics
        metrics.increment_paths()
        metrics.add_path_length(sum(cycle_lengths) / path_count if path_count > 0 else 0.0)
        metrics.compute_mean_proportional_length()

        return metrics

    @staticmethod
    def _initialize_feasible_flow(residual_capacity, source, sink, required_flow):
        """
        Push initial feasible flow using a simple Ford-Fulkerson approach.

        :param residual_capacity: Residual capacity graph.
        :param source: Source node.
        :param sink: Sink node.
        :param required_flow: Desired flow to achieve.
        :return: The amount of flow sent.
        """
        flow_sent = 0
        while flow_sent < required_flow:
            # BFS to find an augmenting path
            parent_map = {}
            queue = deque([source])
            visited = {source}

            while queue:
                current = queue.popleft()
                for neighbor, capacity in residual_capacity[current].items():
                    if neighbor not in visited and capacity > 0:
                        parent_map[neighbor] = current
                        visited.add(neighbor)
                        queue.append(neighbor)
                        if neighbor == sink:
                            # Augment flow along the path
                            path_flow = float('inf')
                            node = sink
                            while node != source:
                                prev = parent_map[node]
                                path_flow = min(path_flow, residual_capacity[prev][node])
                                node = prev

                            # Adjust residual capacities
                            node = sink
                            while node != source:
                                prev = parent_map[node]
                                residual_capacity[prev][node] -= path_flow
                                residual_capacity[node][prev] += path_flow
                                node = prev

                            flow_sent += path_flow
                            if flow_sent >= required_flow:
                                return flow_sent

                            break
            else:
                break  # No augmenting path found

        return flow_sent

    @staticmethod
    def _find_negative_cycle(residual_capacity, edge_cost):
        """
        Find a negative-cost cycle using Bellman-Ford.

        :param residual_capacity: Residual capacity graph.
        :param edge_cost: Edge costs for the graph.
        :return: List of nodes forming the negative-cost cycle, or None if no cycle exists.
        """
        nodes = list(residual_capacity.keys())
        dist = {node: float('inf') for node in nodes}
        parent = {node: None for node in nodes}
        dist[nodes[0]] = 0

        # Relax edges |V|-1 times
        for _ in range(len(nodes) - 1):
            for u in nodes:
                for v in residual_capacity[u]:
                    if residual_capacity[u][v] > 0 and dist[u] + edge_cost[u][v] < dist[v]:
                        dist[v] = dist[u] + edge_cost[u][v]
                        parent[v] = u

        # Check for negative cycles
        for u in nodes:
            for v in residual_capacity[u]:
                if residual_capacity[u][v] > 0 and dist[u] + edge_cost[u][v] < dist[v]:
                    # Negative cycle detected, reconstruct the cycle
                    cycle = []
                    visited = set()
                    x = v
                    while x not in visited:
                        visited.add(x)
                        x = parent[x]

                    # Reconstruct cycle
                    start = x
                    cycle.append(start)
                    x = parent[start]
                    while x != start:
                        cycle.append(x)
                        x = parent[x]
                    cycle.reverse()
                    return cycle

        return None
