from b1 import get_matrix, visual_graph
from b2 import Graph

name = input("What is the name of the file? ")
directed = input("Is it directed? (yes/no) ")
weighted = input("Is it weighted? (yes/no) ")
adjacency_matrix = get_matrix(name)
if directed == "yes" and weighted == "yes":

    visual_graph(adjacency_matrix, True, True)
elif directed == "yes" and weighted == "no":

    visual_graph(adjacency_matrix, True, False)
elif directed == "no" and weighted == "yes":

    visual_graph(adjacency_matrix, False, True)
elif directed == "no" and weighted == "no":

    visual_graph(adjacency_matrix, False, False)
else:
    print ("Invalid input. Please try again.")
    exit()