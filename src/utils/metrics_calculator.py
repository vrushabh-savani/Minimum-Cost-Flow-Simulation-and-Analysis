from collections import defaultdict


class MetricsCalculator:
    @staticmethod
    def calculate_node_count(lcc):
        """
        Calculates the number of nodes in the largest connected component (LCC).

        :param lcc: The adjacency list of the largest connected component.
        :return: The number of nodes in the LCC.
        """
        return len(lcc)

    @staticmethod
    def calculate_max_out_degree(lcc):
        """
        Calculates the maximum out-degree of any node in the LCC.

        :param lcc: The adjacency list of the largest connected component.
        :return: The maximum out-degree of any node.
        """
        return max(len(edges) for edges in lcc.values())

    @staticmethod
    def calculate_max_in_degree(lcc):
        """
        Calculates the maximum in-degree of any node in the LCC.

        :param lcc: The adjacency list of the largest connected component.
        :return: The maximum in-degree of any node.
        """
        in_degree_map = MetricsCalculator._calculate_in_degrees(lcc)
        return max(in_degree_map.values(), default=0)

    @staticmethod
    def calculate_average_degree(lcc):
        """
        Calculates the average degree of nodes in the LCC.

        :param lcc: The adjacency list of the largest connected component.
        :return: The average degree of the nodes.
        """
        total_degree = 0

        # Calculate total degrees (in-degree + out-degree)
        in_degree_map = MetricsCalculator._calculate_in_degrees(lcc)
        for node, edges in lcc.items():
            out_degree = len(edges)
            in_degree = in_degree_map.get(node, 0)
            total_degree += (out_degree + in_degree)

        return total_degree / len(lcc)

    @staticmethod
    def _calculate_in_degrees(lcc):
        """
        Helper function to calculate in-degrees for all nodes in the graph.

        :param lcc: The adjacency list of the largest connected component.
        :return: A dictionary of nodes to their in-degree counts.
        """
        in_degree_map = defaultdict(int)

        # Count in-degrees
        for edges in lcc.values():
            for edge in edges:
                in_degree_map[edge.to_node] += 1

        return in_degree_map
