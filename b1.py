import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def get_matrix(filename):
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("Sorry! Find not found.")
        return None
    except Exception as e:
        print("An error occurred: ", e)
        return None
    else:

        nodes = lines[0].split()

        num_nodes = len(nodes)

        adj_matrix = np.zeros((num_nodes, num_nodes), dtype=int)

        node_to_index = {node: index for index, node in enumerate(nodes)}

        for line in lines[1:]:
            parts = line.split()
            node = parts[0]
            edges = list(map(int, parts[1:]))
            row = node_to_index[node]
            for col, weight in enumerate(edges):
                adj_matrix[row][col] = weight

        return adj_matrix

def visual_graph(adj_matrix, directed=True, weighted=True):
    adj_matrix_np = np.array(adj_matrix)
    if directed:
        G = nx.from_numpy_array(adj_matrix_np, create_using=nx.DiGraph)
    else:
        G = nx.from_numpy_array(adj_matrix_np, create_using=nx.Graph)

    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G)
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color='yellow',
        node_size=800,
        font_size=10,
        edge_color='black',
        arrowsize=20
    )

    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    plt.title("Directed Weighted Graph Visualization")
    plt.show()

def print_matrix(adj_matrix):
    for row in adj_matrix:
        print(" ".join(map(str, row)))

def is_directed(adj_matrix):
    return not np.array_equal(adj_matrix, adj_matrix.T)

def is_weighted(adj_matrix):
    for i in range(len(adj_matrix)):
        for j in range(len(adj_matrix[i])):
            if adj_matrix[i][j] > 1:
                return True
    return False

def output_to_file(self, filename = "output.txt"):

        nodes = list(self.graph.keys())

        # Step 2: Initialize an adjacency matrix with zeros
        adj_matrix = [[0] * len(nodes) for _ in range(len(nodes))]

        # Step 3: Fill the adjacency matrix with edge weights
        for i, node1 in enumerate(nodes):
            for j, node2 in enumerate(nodes):
                for connection, weight in self.graph.get(node1, []):
                    if connection == node2:
                        adj_matrix[i][j] = weight

        # Step 4: Write the matrix to a text file
        with open(filename, "w") as file:
            # Write node labels in the first row
            file.write(" ".join(nodes) + "\n")

            # Write the adjacency matrix
            for row in adj_matrix:
                file.write(" ".join(map(str, row)) + "\n")