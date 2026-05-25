import heapq
from collections import defaultdict
from utils.flow_metrics import FlowMetrics


class SuccessiveShortestPaths:
    @staticmethod
    def compute_metrics(adjacency_list, source, sink, required_flow):
        """
        Computes metrics for the Successive Shortest Paths algorithm.

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

        # Residual capacities and flow
        capacity = defaultdict(int)
        cost = defaultdict(int)
        flow = defaultdict(int)

        # Build capacity and cost from the input graph
        for u, edges in adjacency_list.items():
            for edge in edges:
                capacity[(u, edge.to_node)] = edge.capacity
                cost[(u, edge.to_node)] = edge.cost
                flow[(u, edge.to_node)] = 0  # Initialize flow to 0

        while required_flow > 0:
            # Step 1: Find the shortest path using Dijkstra's algorithm
            dist, parent = SuccessiveShortestPaths._dijkstra(adjacency_list, source, sink, capacity, cost, flow)

            if sink not in parent:
                break  # No augmenting path found

            # Step 2: Find the bottleneck capacity (δ) along the shortest path
            path_flow = float('inf')
            path_length = 0  # Count the number of edges in this path
            current = sink

            while current != source:
                prev = parent[current]
                path_flow = min(path_flow, capacity[(prev, current)] - flow[(prev, current)])
                current = prev
                path_length += 1

            # Limit path flow to the remaining required flow
            path_flow = min(path_flow, required_flow)

            # Step 3: Augment the flow along the shortest path
            current = sink
            while current != source:
                prev = parent[current]
                forward_edge = (prev, current)
                reverse_edge = (current, prev)

                # Update forward and reverse flows
                flow[forward_edge] += path_flow
                flow[reverse_edge] -= path_flow

                # Update the cost
                metrics.add_cost(path_flow * cost[forward_edge])

                current = prev

            # Update metrics
            metrics.add_flow(path_flow)
            metrics.increment_paths()
            metrics.add_path_length(path_length)

            # Reduce the remaining required flow
            required_flow -= path_flow

        # If the total flow is less than the required flow, return failure
        if required_flow > 0:
            metrics.set_total_flow(-1)  # Indicate failure

        return metrics

    @staticmethod
    def _dijkstra(adjacency_list, source, sink, capacity, cost, flow):
        """
        Dijkstra's algorithm for shortest path with unit costs.

        :param adjacency_list: Adjacency list of the graph.
        :param source: Source node.
        :param sink: Sink node.
        :param capacity: Residual capacities of edges.
        :param cost: Cost of edges.
        :param flow: Current flow along edges.
        :return: A tuple (dist, parent) where dist is a dictionary of shortest distances
                 and parent is a dictionary of node predecessors.
        """
        dist = defaultdict(lambda: float('inf'))
        parent = {}
        dist[source] = 0

        # Priority queue for Dijkstra's algorithm
        pq = [(0, source)]  # (distance, node)

        while pq:
            current_dist, u = heapq.heappop(pq)

            # If this distance is stale, skip
            if current_dist > dist[u]:
                continue

            for edge_key in capacity.keys():
                if edge_key[0] != u:  # Skip edges not starting from u
                    continue

                v = edge_key[1]
                residual_capacity = capacity[edge_key] - flow[edge_key]

                if residual_capacity > 0:
                    new_dist = dist[u] + cost[edge_key]
                    if new_dist < dist[v]:
                        dist[v] = new_dist
                        parent[v] = u
                        heapq.heappush(pq, (new_dist, v))

        return dist, parent
