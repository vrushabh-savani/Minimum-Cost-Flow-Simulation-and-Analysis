class FlowMetrics:
    def __init__(self, total_edges):
        """
        Initializes the FlowMetrics object.

        :param total_edges: Total number of edges in the graph.
        """
        self.total_flow = 0
        self.min_cost = 0
        self.num_augmenting_paths = 0
        self.total_edges_in_paths = 0  
        self.total_edges = total_edges 

    def add_flow(self, flow):
        """
        Increment total flow.

        :param flow: The flow to add.
        """
        self.total_flow += flow

    def add_cost(self, cost):
        """
        Increment total cost.

        :param cost: The cost to add.
        """
        self.min_cost += cost

    def increment_paths(self):
        """
        Increment the number of augmenting paths.
        """
        self.num_augmenting_paths += 1

    def add_path_length(self, length):
        """
        Add path length (number of edges in the augmenting path).

        :param length: The length of the augmenting path to add.
        """
        self.total_edges_in_paths += length

    def set_total_flow(self, total_flow):
        """
        Set total flow (e.g., for failure cases).

        :param total_flow: The total flow to set.
        """
        self.total_flow = total_flow

    def get_total_flow(self):
        """
        Get total flow.

        :return: Total flow.
        """
        return self.total_flow

    def get_min_cost(self):
        """
        Get minimum cost.

        :return: Minimum cost.
        """
        return self.min_cost

    def get_num_augmenting_paths(self):
        """
        Get the number of augmenting paths.

        :return: Number of augmenting paths.
        """
        return self.num_augmenting_paths

    def compute_mean_length(self):
        """
        Compute mean length (ML), the average length of augmenting paths.

        :return: Mean length of augmenting paths.
        """
        return self.total_edges_in_paths / self.num_augmenting_paths if self.num_augmenting_paths > 0 else 0.0

    def compute_mean_proportional_length(self):
        """
        Compute mean proportional length (MPL).

        :return: Mean proportional length, rounded to 4 decimal places.
        """
        mpl = self.compute_mean_length() / self.total_edges if self.total_edges > 0 else 0.0
        return round(mpl, 4)

    def __str__(self):
        """
        String representation of the FlowMetrics object.
        """
        return (f"FlowMetrics{{"
                f"totalFlow={self.total_flow}, "
                f"minCost={self.min_cost}, "
                f"numAugmentingPaths={self.num_augmenting_paths}, "
                f"meanLength={self.compute_mean_length():.4f}, "
                f"meanProportionalLength={self.compute_mean_proportional_length():.4f}"
                f"}}")
