import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

#Reads the graph from the file and returns the adjacency matrix
def get_matrix(filename):
    try:
        # Open the file and read all lines
        with open(filename, "r") as file:
            lines = file.readlines()
    # Handle exception for file not found
    except FileNotFoundError:
        print("Sorry! File not found.")
        return None
    # Handle exception for any other error
    except Exception as e:
        print("An error occurred: ", e)
        return None

    # Initialize the adjacency matrix
    adj_matrix = []

    # Loop through the lines and append the rows to the matrix
    for line in lines[1:]: # Skip the first line
        if not line.strip(): # Skip empty lines
            continue
        row = list(map(int, line.split()[1:])) # Skip the first element
        adj_matrix.append(row) # Append the row to the matrix

    # Check if the matrix is square
    num_rows = len(adj_matrix) # Get the number of rows
    for row in adj_matrix: # Loop through the rows
        if len(row) != num_rows:  # Check if each row has the same number of columns as rows
            print("Error: The matrix is not square.") # Print an error message if not square
            return None

    return adj_matrix


def visual_graph(adj_matrix, directed=True):
    adj_matrix_np = np.array(adj_matrix)
    if directed:
        g = nx.from_numpy_array(adj_matrix_np, create_using=nx.DiGraph)
    else:
        g = nx.from_numpy_array(adj_matrix_np, create_using=nx.Graph)

    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(g)
    nx.draw(
        g,
        pos,
        with_labels=True,
        node_color='yellow',
        node_size=800,
        font_size=10,
        edge_color='black',
        arrowsize=20
    )

    edge_labels = nx.get_edge_attributes(g, 'weight')
    nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels, font_size=8)

    plt.title("Directed Weighted Graph Visualization")
    plt.show()

# Check if the graph is directed
def is_directed(adj_matrix):
    num_nodes = len(adj_matrix) # Get the number of nodes
    for i in range(num_nodes): # Loop through the rows
        for j in range(num_nodes): # Loop through the columns
            if adj_matrix[i][j] != adj_matrix[j][i]: # Check if the matrix is symmetric
                return True # If not symmetric, it is directed
    return False # If symmetric, it is undirected

# Check if the graph is weighted
def is_weighted(adj_matrix):
    for row in adj_matrix: # Loop through the rows
        for weight in row: # Loop through the elements in the row
            if weight > 1: # If any element is greater than 1 then it is weighted
                return True
    return False # If all elements are 0 or 1, it is unweighted