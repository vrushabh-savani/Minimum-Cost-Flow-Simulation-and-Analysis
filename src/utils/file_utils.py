from collections import defaultdict
from graph.graph_generator import Edge


class FileUtils:
    @staticmethod
    def read_graph_from_file(file_name):
        """
        Reads a graph from a file and returns it as an adjacency list.

        :param file_name: The file containing the graph in the specified format.
        :return: A dictionary representing the adjacency list of the graph.
        """
        adjacency_list = defaultdict(list)

        try:
            with open(file_name, 'r') as file:
                for line in file:
                    # Split each line into parts: from, to, capacity, cost
                    parts = line.strip().split()
                    if len(parts) != 4:
                        raise ValueError(f"Invalid line format: {line}")

                    from_node = int(parts[0])
                    to_node = int(parts[1])
                    capacity = int(parts[2])
                    cost = int(parts[3])

                    # Create the Edge object
                    edge = Edge(from_node, to_node, capacity, cost)

                    # Add the edge to the adjacency list
                    adjacency_list[from_node].append(edge)

        except FileNotFoundError:
            print(f"Error: File not found: {file_name}")
        except IOError as e:
            print(f"Error reading graph from file: {e}")
        except ValueError as ve:
            print(f"Value error while reading graph: {ve}")

        return adjacency_list

    @staticmethod
    def print_adjacency_list(adjacency_list):
        """
        Prints the adjacency list representation of the graph for debugging.

        :param adjacency_list: The graph in adjacency list form.
        """
        for node, edges in adjacency_list.items():
            print(f"Node {node} -> ", end="")
            for edge in edges:
                print(f"(To: {edge.to_node}, Cap: {edge.capacity}, Cost: {edge.cost}) ", end="")
            print()
