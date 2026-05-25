from collections import defaultdict
from heapq import heappush, heappop
from utils.flow_metrics import FlowMetrics
from graph.graph_generator import Edge



class CapacityScaling:
    @staticmethod
    def compute_metrics(adjacency_list, source, sink, required_flow):
        """
        Computes metrics for the Capacity Scaling algorithm.

        :param adjacency_list: Adjacency list of the graph.
        :param source: Source node.
        :param sink: Sink node.
        :param required_flow: The required flow.
        :return: FlowMetrics object containing computed metrics.
        """
        # Calculate the total number of edges in the graph
        total_edges = sum(len(edges) for edges in adjacency_list.values())

        # Initialize FlowMetrics
        metrics = FlowMetrics(total_edges)

        # Determine the maximum capacity (scaling factor Δ)
        delta = CapacityScaling._get_max_capacity(adjacency_list)

        while delta >= 1:
            # While there exists an augmenting path with residual capacity ≥ Δ
            while required_flow > 0:
                path = CapacityScaling._find_augmenting_path(adjacency_list, source, sink, delta)
                if not path:
                    break  # No augmenting path found

                # Determine the maximum flow δ that can be pushed along the path
                delta_flow = CapacityScaling._get_min_capacity(path)

                # Limit flow by the remaining required flow
                delta_flow = min(delta_flow, required_flow)

                # Augment the flow along the path
                CapacityScaling._augment_flow(adjacency_list, path, delta_flow)

                # Update metrics
                metrics.add_flow(delta_flow)
                metrics.add_cost(delta_flow * CapacityScaling._compute_path_cost(path))
                metrics.increment_paths()
                metrics.add_path_length(len(path))

                # Reduce the remaining required flow
                required_flow -= delta_flow

            # Reduce the scaling factor Δ by halving
            delta //= 2

        # If the required flow is not met, return failure
        if required_flow > 0:
            metrics.set_total_flow(-1)  # Indicate failure
            return metrics

        return metrics

    @staticmethod
    def _find_augmenting_path(adjacency_list, source, sink, delta):
        """
        Find the shortest augmenting path with residual capacity ≥ Δ using Dijkstra's algorithm.

        :param adjacency_list: Adjacency list of the graph.
        :param source: Source node.
        :param sink: Sink node.
        :param delta: Current scaling factor.
        :return: List of edges representing the augmenting path.
        """
        pq = []  # Priority queue for Dijkstra's algorithm
        heappush(pq, (0, source))
        dist = defaultdict(lambda: float('inf'))
        dist[source] = 0
        parent_map = {}

        while pq:
            current_dist, u = heappop(pq)

            # Skip stale entries
            if current_dist > dist[u]:
                continue

            for edge in adjacency_list.get(u, []):
                if edge.capacity >= delta:  # Consider edges with residual capacity ≥ Δ
                    v = edge.to_node
                    new_dist = dist[u] + edge.cost

                    if new_dist < dist[v]:
                        dist[v] = new_dist
                        parent_map[v] = edge
                        heappush(pq, (new_dist, v))

        # If no path to the sink exists, return None
        if sink not in parent_map:
            return None

        # Reconstruct the path from source to sink
        return CapacityScaling._reconstruct_path(parent_map, source, sink)

    @staticmethod
    def _reconstruct_path(parent_map, source, sink):
        """
        Reconstruct the augmenting path from the parent map.

        :param parent_map: Dictionary mapping nodes to their incoming edges.
        :param source: Source node.
        :param sink: Sink node.
        :return: List of edges representing the path.
        """
        path = []
        current = sink
        while current != source:
            edge = parent_map[current]
            path.append(edge)
            current = edge.from_node
        path.reverse()
        return path

    @staticmethod
    def _augment_flow(adjacency_list, path, delta_flow):
        """
        Augment the flow along the path.

        :param adjacency_list: Adjacency list of the graph.
        :param path: List of edges in the augmenting path.
        :param delta_flow: The flow to augment.
        """
        for edge in path:
            edge.capacity -= delta_flow  # Decrease forward edge capacity

            # Find or create the reverse edge
            reverse_edge = CapacityScaling._find_reverse_edge(adjacency_list, edge.to_node, edge.from_node)
            if reverse_edge:
                reverse_edge.capacity += delta_flow
            else:
                # Add a reverse edge if it doesn't exist
                adjacency_list[edge.to_node].append(Edge(edge.to_node, edge.from_node, delta_flow, 0))

    @staticmethod
    def _find_reverse_edge(adjacency_list, from_node, to_node):
        """
        Find the reverse edge in the adjacency list.

        :param adjacency_list: Adjacency list of the graph.
        :param from_node: Start node of the reverse edge.
        :param to_node: End node of the reverse edge.
        :return: The reverse edge if it exists, otherwise None.
        """
        for edge in adjacency_list.get(from_node, []):
            if edge.to_node == to_node:
                return edge
        return None

    @staticmethod
    def _get_min_capacity(path):
        """
        Get the minimum capacity along the path.

        :param path: List of edges.
        :return: Minimum capacity along the path.
        """
        return min(edge.capacity for edge in path)

    @staticmethod
    def _get_max_capacity(adjacency_list):
        """
        Get the maximum capacity in the graph.

        :param adjacency_list: Adjacency list of the graph.
        :return: Maximum capacity.
        """
        return max(edge.capacity for edges in adjacency_list.values() for edge in edges)

    @staticmethod
    def _compute_path_cost(path):
        """
        Compute the total cost of a path.

        :param path: List of edges.
        :return: Total cost of the path.
        """
        return sum(edge.cost for edge in path)
