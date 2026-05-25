from collections import deque, defaultdict


class EdmondsKarp:
    @staticmethod
    def compute_max_flow(adjacency_list, source, sink):
        """
        Computes the maximum flow between source and sink using the Edmonds-Karp algorithm.

        :param adjacency_list: The adjacency list representation of the graph.
        :param source: The source node.
        :param sink: The sink node.
        :return: The maximum flow in the graph.
        """
        # Adjacency list representation for residual capacities
        residual_graph = defaultdict(lambda: defaultdict(int))

        # Step 1: Initialize residual graph based on the adjacency list
        for from_node, edges in adjacency_list.items():
            for edge in edges:
                residual_graph[from_node][edge.to_node] += edge.capacity  # Add forward capacity
                residual_graph[edge.to_node][from_node] += 0             # Reverse edge with 0 capacity initially


        max_flow = 0

        # Step 2: Loop until no more augmenting paths exist
        while True:
            # Find augmenting path using BFS
            parent = {}
            if not EdmondsKarp._bfs(residual_graph, source, sink, parent):
                break

            # Find bottleneck capacity along the augmenting path
            path_flow = float('inf')
            current = sink
            while current != source:
                prev = parent[current]
                path_flow = min(path_flow, residual_graph[prev][current])
                current = prev

            # Update residual capacities along the augmenting path
            current = sink
            while current != source:
                prev = parent[current]
                residual_graph[prev][current] -= path_flow
                residual_graph[current][prev] += path_flow
                current = prev

            # Add path flow to overall maximum flow
            max_flow += path_flow



        return max_flow

    @staticmethod
    def _bfs(residual_graph, source, sink, parent):
        """
        Helper method to perform BFS and find an augmenting path in the residual graph.

        :param residual_graph: The residual graph.
        :param source: The source node.
        :param sink: The sink node.
        :param parent: Dictionary to store the augmenting path.
        :return: True if an augmenting path exists, False otherwise.
        """
        queue = deque([source])
        visited = set([source])

        while queue:
            current = queue.popleft()

            for next_node, capacity in residual_graph[current].items():
                if next_node not in visited and capacity > 0:  # Check if the edge has residual capacity
                    queue.append(next_node)
                    visited.add(next_node)
                    parent[next_node] = current

                    # If we reach the sink, the path is found
                    if next_node == sink:
                        return True

        return False
