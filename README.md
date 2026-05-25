# Minimum-Cost Flow Algorithms

## Department of Computer Science and Software Engineering  
**Concordia University**  
**COMP 6651 Algorithm Design Techniques**  
**Fall 2024**

### Project Description

This project aims to solve the minimum-cost flow problem in directed graphs, extending the Ford-Fulkerson algorithm to include cost considerations for each unit of flow. The project involves implementing and analyzing various adaptations of the Ford-Fulkerson algorithm, including:

- Successive Shortest Path Algorithm
- Capacity Scaling Algorithm
- Integration of Successive Shortest Path and Capacity Scaling Algorithms
- **Cycle-Cancelling Algorithm** (as the fourth algorithm)

The goal is to send a given flow between a source and sink while minimizing the total cost, taking into account both the flow capacities and unit costs. The project includes the following tasks:

1. Implement a random graph generator to create directed, weighted, Euclidean source-sink graphs.
2. Generate random graphs with specified properties and store them in an external file in the EDGES format.
3. Select the largest connected component (LCC) of each graph, and identify source-sink pairs for flow calculations.
4. Run and compare the performance of three algorithms on these LCCs.
5. Implement and analyze the **Cycle-Cancelling Algorithm** as the fourth algorithm, comparing it against the others.
6. Measure and record key metrics, such as total cost and flow, for each algorithm.

### Installation and Setup

1. **Ensure Python is installed (Python 3.6+ is required):**

    To verify if Python is installed on your system, run the following command:

    ```bash
    python --version
    ```

    If you do not have Python installed or the version is below 3.6, you can download and install the latest version of Python from the [official Python website](https://www.python.org/downloads/).

2. **Run the project:**

    - Generate and process graphs:

    ```bash
    python main.py
    ```

### Contributors

- Vrushabh Savani (SID: 40291740)
- Fatema Gajipurwala (SID: 40269575)
- Sahil Khunt (SID: 40279373)
- Khushi Parikh (SID: 40292715)
- Vishwas Tomar (SID: 40254026)

