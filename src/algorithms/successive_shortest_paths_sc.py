from collections import defaultdict, deque
from utils.flow_metrics import FlowMetrics
from graph.graph_generator import Edge


class SuccessiveShortestPathsSC:
    @staticmethod
    def compute_metrics(adjacency_list, source, sink, total_flow):
        """
        Compute the minimum-cost flow using Successive Shortest Paths with Scaling.

        :param adjacency_list: Adjacency list of the graph.
        :param source: Source node.
        :param sink: Sink node.
        :param total_flow: Desired total flow to achieve.
        :return: FlowMetrics object containing computed metrics.
        """
        # Initialize FlowMetrics
        total_edges = sum(len(edges) for edges in adjacency_list.values())
        metrics = FlowMetrics(total_edges)

        # Set scaling factor Δ to the maximum capacity in the graph
        delta = SuccessiveShortestPathsSC._get_max_capacity(adjacency_list)

        # Initialize total flow and total cost
        current_flow = 0
        total_cost = 0

        # Outer loop for scaling factor Δ
        while delta >= 1:
            # While there exists an augmenting path with capacity ≥ Δ
            while total_flow > 0:
                # Step 1: Find the shortest path with capacity ≥ Δ
                path, path_cost = SuccessiveShortestPathsSC._find_min_cost_path(
                    adjacency_list, source, sink, delta
                )

                if not path:
                    break  # No augmenting path found

                # Step 2: Find the maximum flow δ that can be pushed along the path
                delta_flow = min(edge.capacity for edge in path)

                # Limit flow to remaining required flow
                delta_flow = min(delta_flow, total_flow)

                # Step 3: Augment the flow along the path
                for edge in path:
                    edge.capacity -= delta_flow
                    SuccessiveShortestPathsSC._augment_reverse_edge(
                        adjacency_list, edge.to_node, edge.from_node, delta_flow
                    )

                # Update metrics
                current_flow += delta_flow
                total_cost += delta_flow * path_cost
                metrics.add_flow(delta_flow)
                metrics.add_cost(delta_flow * path_cost)
                metrics.increment_paths()
                metrics.add_path_length(len(path))

                # Reduce the remaining required flow
                total_flow -= delta_flow

            # Halve the scaling factor Δ
            delta //= 2

        # Final flow validation
        if total_flow > 0:
            metrics.set_total_flow(current_flow)
        else:
            metrics.set_total_flow(current_flow)

        return metrics

    @staticmethod
    def _get_max_capacity(adjacency_list):
        """
        Get the maximum capacity of any edge in the graph.

        :param adjacency_list: Adjacency list of the graph.
        :return: Maximum capacity.
        """
        return max(edge.capacity for edges in adjacency_list.values() for edge in edges)

    @staticmethod
    def _find_min_cost_path(adjacency_list, source, sink, delta):
        """
        Find the minimum-cost path from source to sink with capacity ≥ Δ using Bellman-Ford.

        :param adjacency_list: Adjacency list of the graph.
        :param source: Source node.
        :param sink: Sink node.
        :param delta: Current scaling factor (capacity threshold).
        :return: (path, path_cost) where path is a list of edges and path_cost is the total cost.
        """
        dist = defaultdict(lambda: float('inf'))
        parent = {}
        dist[source] = 0

        # Relax edges |V|-1 times (Bellman-Ford)
        for _ in range(len(adjacency_list) - 1):
            for u, edges in adjacency_list.items():
                for edge in edges:
                    if edge.capacity >= delta:  # Only consider edges with capacity ≥ Δ
                        v = edge.to_node
                        if dist[u] + edge.cost < dist[v]:
                            dist[v] = dist[u] + edge.cost
                            parent[v] = edge

        # If no path to the sink exists, return None
        if sink not in parent:
            return None, 0

        # Reconstruct the path
        path = []
        current = sink
        while current != source:
            edge = parent[current]
            path.append(edge)
            current = edge.from_node
        path.reverse()

        return path, dist[sink]

    @staticmethod
    def _augment_reverse_edge(adjacency_list, from_node, to_node, capacity):
        """
        Augment the reverse edge in the adjacency list.

        :param adjacency_list: Adjacency list of the graph.
        :param from_node: From node of the reverse edge.
        :param to_node: To node of the reverse edge.
        :param capacity: Capacity to add to the reverse edge.
        """
        # Check if the reverse edge exists
        for edge in adjacency_list[from_node]:
            if edge.to_node == to_node:
                edge.capacity += capacity
                return

        # If no reverse edge exists, create one
        adjacency_list[from_node].append(Edge(from_node, to_node, capacity, 0))
