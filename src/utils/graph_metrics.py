from collections import defaultdict, deque
from graph.graph_generator import Edge


class GraphMetrics:
    @staticmethod
    def find_largest_scc(adjacency_list):
        """
        Finds the largest strongly connected component (LCC) of a directed graph.

        :param adjacency_list: The adjacency list representation of the graph.
        :return: The adjacency list of the largest strongly connected component (LCC).
        """
        # Step 1: Perform a DFS to get the finishing order of nodes
        finish_order = []
        visited = set()

        for node in adjacency_list.keys():
            if node not in visited:
                GraphMetrics._dfs(adjacency_list, node, visited, finish_order)

        # Step 2: Transpose the graph
        transposed_graph = GraphMetrics._transpose_graph(adjacency_list)

        # Step 3: Perform DFS on the transposed graph in the order of finish_order
        visited.clear()
        components = []
        while finish_order:
            node = finish_order.pop()
            if node not in visited:
                component = []
                GraphMetrics._dfs_on_transposed(transposed_graph, node, visited, component)
                components.append(component)

        # Step 4: Find the largest component
        largest_scc = max(components, key=len, default=[])

        # Step 5: Extract the adjacency list for the largest SCC
        return GraphMetrics._extract_subgraph(adjacency_list, largest_scc)

    @staticmethod
    def _dfs(graph, node, visited, finish_order):
        """
        Perform a DFS and populate the finish order stack.
        """
        visited.add(node)
        for edge in graph.get(node, []):
            if edge.to_node not in visited:
                GraphMetrics._dfs(graph, edge.to_node, visited, finish_order)
        finish_order.append(node)

    @staticmethod
    def _transpose_graph(adjacency_list):
        """
        Transpose the graph (reverse the direction of all edges).
        """
        transposed = defaultdict(list)
        for node, edges in adjacency_list.items():
            for edge in edges:
                transposed[edge.to_node].append(Edge(edge.to_node, edge.from_node, edge.capacity, edge.cost))
        return transposed

    @staticmethod
    def _dfs_on_transposed(graph, node, visited, component):
        """
        Perform a DFS on the transposed graph.
        """
        visited.add(node)
        component.append(node)
        for edge in graph.get(node, []):
            if edge.to_node not in visited:
                GraphMetrics._dfs_on_transposed(graph, edge.to_node, visited, component)

    @staticmethod
    def _extract_subgraph(graph, nodes):
        """
        Extract the adjacency list for a subgraph containing only the given nodes.
        """
        subgraph = defaultdict(list)
        node_set = set(nodes)

        for node in nodes:
            edges = [
                edge for edge in graph.get(node, [])
                if edge.to_node in node_set
            ]
            subgraph[node].extend(edges)

        return subgraph

    @staticmethod
    def select_source_and_sink(scc_adjacency_list):
        """
        Select the source and sink nodes from the largest SCC.

        :param scc_adjacency_list: The adjacency list of the SCC.
        :return: A tuple (source, sink).
        """
        if not scc_adjacency_list:
            raise ValueError("SCC adjacency list cannot be null or empty")

        # Step 1: Select the starting node of the DFS as the source (s)
        source = next(iter(scc_adjacency_list.keys()))  # Start with the first node in the SCC

        # Step 2: Perform BFS from the source to determine distances
        distances = GraphMetrics._bfs(scc_adjacency_list, source)

        # Step 3: Find the node with the maximum distance as the sink (t)
        sink = max(distances, key=distances.get)

        return source, sink

    @staticmethod
    def _bfs(graph, start_node):
        """
        Perform BFS and return distances from the start node to all other nodes.

        :param graph: The adjacency list representation of the graph.
        :param start_node: The node to start BFS from.
        :return: A dictionary of distances from the start_node to all reachable nodes.
        """
        queue = deque([start_node])
        distances = {start_node: 0}

        while queue:
            current_node = queue.popleft()
            for edge in graph.get(current_node, []):
                if edge.to_node not in distances:  # Node not visited yet
                    distances[edge.to_node] = distances[current_node] + 1
                    queue.append(edge.to_node)

        return distances
