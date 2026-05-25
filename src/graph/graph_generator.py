import random
import math

class Node:
    def __init__(self, node_id, x, y):
        self.id = node_id  # Unique ID for the node
        self.x = x         # Cartesian x-coordinate
        self.y = y         # Cartesian y-coordinate


class Edge:
    def __init__(self, from_node, to_node, capacity, cost):
        self.from_node = from_node  # Start node of the edge
        self.to_node = to_node      # End node of the edge
        self.capacity = capacity    # Capacity of the edge
        self.cost = cost            # Cost of the edge

    def __str__(self):
        return f"{self.from_node} {self.to_node} {self.capacity} {self.cost}"


class Graph:
    def __init__(self):
        self.nodes = []  # List of Node objects
        self.edges = []  # List of Edge objects


class GraphGenerator:
    @staticmethod
    def generate_graph(n, r, upper_cap, upper_cost):
        """
        Generate a random graph based on the given parameters.

        :param n: Number of nodes
        :param r: Distance threshold for edge creation
        :param upper_cap: Maximum capacity of any edge
        :param upper_cost: Maximum cost of any edge
        :return: A Graph object containing nodes and edges
        """
        graph = Graph()
        random.seed()

        # Step 1: Generate nodes with random (x, y) coordinates
        for i in range(n):
            x = random.uniform(0, 1)  # Random x-coordinate in [0, 1]
            y = random.uniform(0, 1)  # Random y-coordinate in [0, 1]
            graph.nodes.append(Node(i, x, y))

        # Step 2: Generate edges based on the distance threshold 'r'
        for u in graph.nodes:
            for v in graph.nodes:
                if u.id != v.id:  # Avoid self-loops
                    distance = math.sqrt((u.x - v.x) ** 2 + (u.y - v.y) ** 2)
                    if distance <= r:
                        rand_prob = random.random()  # Random probability
                        if rand_prob < 0.3 and not GraphGenerator.edge_exists(graph, u.id, v.id) and not GraphGenerator.edge_exists(graph, v.id, u.id):
                            # Add edge (u -> v) with a probability of 30%
                            graph.edges.append(Edge(u.id, v.id, random.randint(1, upper_cap),
                                                    random.randint(1, upper_cost)))
                        elif rand_prob < 0.6 and not GraphGenerator.edge_exists(graph, v.id, u.id) and not GraphGenerator.edge_exists(graph, u.id, v.id):
                            # Add edge (v -> u) with a probability of 30%
                            graph.edges.append(Edge(v.id, u.id, random.randint(1, upper_cap),
                                                    random.randint(1, upper_cost)))
        return graph

    @staticmethod
    def edge_exists(graph, from_node, to_node):
        """
        Check if an edge already exists in the graph.

        :param graph: The Graph object
        :param from_node: Start node of the edge
        :param to_node: End node of the edge
        :return: True if the edge exists, False otherwise
        """
        return any(edge.from_node == from_node and edge.to_node == to_node for edge in graph.edges)

    @staticmethod
    def save_graph_to_file(graph, file_name):
        """
        Save the graph's edges to a file.

        :param graph: The Graph object
        :param file_name: Name of the file to save the graph
        """
        try:
            with open(file_name, 'w') as f:
                for edge in graph.edges:
                    f.write(str(edge) + "\n")
            print(f"Graph saved to file: {file_name}")
        except IOError as e:
            print(f"Error saving graph to file: {e}")


if __name__ == "__main__":
    # Define graph configurations (n, r, upperCap, upperCost)
    configurations = [
        (100, 0.2, 8, 5),  # Example: n=100 nodes, r=0.2 distance, upperCap=8, upperCost=5
        (200, 0.2, 8, 5),
        (100, 0.3, 8, 5),
        (200, 0.3, 8, 5),
        (100, 0.2, 64, 20),
        (200, 0.2, 64, 20),
        (100, 0.3, 64, 20),
        (200, 0.3, 64, 20)
    ]

    # Generate and save graphs
    for idx, (n, r, upper_cap, upper_cost) in enumerate(configurations, start=1):
        graph = GraphGenerator.generate_graph(n, r, upper_cap, upper_cost)
        GraphGenerator.save_graph_to_file(graph, f"output/graph{idx}.txt")

    # Custom configurations for Simulations II
    custom_configurations = [
        (50, 0.1, 10, 50),  # Set 1: Sparse graph
        (200, 0.5, 100, 20)  # Set 2: Dense graph
    ]

    # Generate and save graphs
    for idx, (n, r, upper_cap, upper_cost) in enumerate(custom_configurations, start=1):
        graph = GraphGenerator.generate_graph(n, r, upper_cap, upper_cost)
        GraphGenerator.save_graph_to_file(graph, f"output/custom_graph{idx}.txt")