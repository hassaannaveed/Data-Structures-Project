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

        adj_matrix = [[0 for _ in range(num_nodes)] for _ in range(num_nodes)]


        node_to_index = {}
        index = 0
        for i in nodes:
            node_to_index[i] = index
            index = index + 1


        for line in lines[1:]:
            parts = line.split()
            node = parts[0]
            edges = [int(weight) for weight in parts[1:]]
            row = node_to_index[node]
            for col in range(len(edges)):
                adj_matrix[row][col] = edges[col]

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

def is_directed(adj_matrix):
    num_nodes = len(adj_matrix)
    for i in range(num_nodes):
        for j in range(num_nodes):
            if adj_matrix[i][j] != adj_matrix[j][i]:
                return True
    return False

def is_weighted(adj_matrix):
    for row in adj_matrix:
        for weight in row:
            if weight > 1:
                return True
    return False