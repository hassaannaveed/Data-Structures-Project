from b1 import get_matrix, visual_graph
from b2 import Graph

name = input("What is the name of the file? ")
directed = input("Is it directed? (yes/no) ")
weighted = input("Is it weighted? (yes/no) ")
if directed == "yes" and weighted == "yes":
    adjacency_matrix = get_matrix(name)
    visual_graph(adjacency_matrix, True, True)
    Graph = Graph(True, True)
    for i in range(len(adjacency_matrix)):
        Graph.add_node(i)
        for j in range(len(adjacency_matrix)):
            if adjacency_matrix[i][j] != 0:
                Graph.add_edge(i, j, adjacency_matrix[i][j])

    Graph.display()
elif directed == "yes" and weighted == "no":
    adjacency_matrix = get_matrix(name)
    visual_graph(adjacency_matrix, True, False)
    Graph = Graph(True, False)
    for i in range(len(adjacency_matrix)):
        Graph.add_node(i)
        for j in range(len(adjacency_matrix)):
            if adjacency_matrix[i][j] != 0:
                Graph.add_edge(i, j)
    Graph.display()
elif directed == "no" and weighted == "yes":
    adjacency_matrix = get_matrix(name)
    visual_graph(adjacency_matrix, False, True)
    Graph = Graph(False, True)
    for i in range(len(adjacency_matrix)):
        Graph.add_node(i)
        for j in range(len(adjacency_matrix)):
            if adjacency_matrix[i][j] != 0:
                Graph.add_edge(i, j, adjacency_matrix[i][j])
    Graph.display()
elif directed == "no" and weighted == "no":
    adjacency_matrix = get_matrix(name)
    visual_graph(adjacency_matrix, False, False)
    Graph = Graph(False, False)
    for i in range(len(adjacency_matrix)):
        Graph.add_node(i)
        for j in range(len(adjacency_matrix)):
            if adjacency_matrix[i][j] != 0:
                Graph.add_edge(i, j)
    Graph.display()
else:
    print ("Invalid input. Please try again.")
    exit()