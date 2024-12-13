import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

#filename is the name of the file to be read
def get_matrix(filename):
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("Sorry! Find not found.")
        return None
    else:
        cleaned_lines = [line for line in lines if line.strip()]

        nodes = cleaned_lines[0].split()

        num_nodes = len(nodes)
        adj_matrix = np.zeros((num_nodes, num_nodes), dtype=int)

        node_to_index = {node: index for index, node in enumerate(nodes)}

        for line in cleaned_lines[1:]:
            parts = line.split()
            node = parts[0]
            edges = list(map(int, parts[1:]))
            row = node_to_index[node]
            for col, weight in enumerate(edges):
                adj_matrix[row][col] = weight

        #Output adjacency matrix
        print("Adjacency Matrix:")
        print(adj_matrix)
        return adj_matrix

#Print the graph
def print_graph(adj_matrix, directed=True, weighted=True):
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
        node_color='red',
        node_size=800,
        font_size=10,
        edge_color='black',
        arrowsize=20
    )

    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    plt.title("Directed Weighted Graph Visualization")
    plt.show()
