import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

#filename is the name of the file to be read
def task1(filename, directed=True, weighted=True):
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("Sorry! Find not found.")
        return None
    else:
        cleaned_lines = [line for line in lines if line.strip()]

        nodes = cleaned_lines[0].split()

        adj_matrix = [[0 for _ in range(len(nodes))] for _ in range(len(nodes))]
        node_to_index = {node: i for i, node in enumerate(nodes)}
        for line in cleaned_lines[1:]:
            parts = line.split()
            node = parts[0]
            edges = list(map(int, parts[1:]))

            row = node_to_index[node]
            for col, weight in enumerate(edges):
                adj_matrix[row][col] = weight

        #Create a figure from adjacency matrix
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
            node_color='skyblue',
            node_size=800,
            font_size=10,
            edge_color='black',
            arrowsize=20
        )


        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

        plt.title("Directed Weighted Graph Visualization")
        plt.show()

        return adj_matrix


name = input("What is the name of the file? ")
directed = input("Is it directed? (yes/no) ")
weighted = input("Is it weighted? (yes/no) ")
if directed == "yes" and weighted == "yes":
    adjacency_matrix = task1(name)
elif directed == "yes" and weighted == "no":
    adjacency_matrix = task1(name, True, False)
elif directed == "no" and weighted == "yes":
    adjacency_matrix = task1(name, False, True)
elif directed == "no" and weighted == "no":
    adjacency_matrix = task1(name, False, False)
else:
    print ("Invalid input. Please try again.")
    exit()