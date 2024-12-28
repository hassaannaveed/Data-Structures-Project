from b1 import get_matrix, print_matrix, is_directed, is_weighted
from b2andf1 import Graph

filename = input("Enter the filename to be read: ")
adj_matrix = get_matrix(filename)


if is_directed(adj_matrix):
    graph = Graph(directed=True)
else:
    graph = Graph(directed=False)

graph.add_from_adj_matrix(adj_matrix)

print("Graph has been created successfully.")
ans = 'y'

while ans=='y':
    print("***** Menu *****")
    print("1. Display the graph and Output to file")
    print("2. Add an edge")
    print("3. Remove an edge")
    print("4. Add a node")
    print("5. Remove a node")
    print("6. Mark a node as important")
    print("7. Show the graph of important nodes only")
    print("8. Exit")
    print("******************")

    choice = input("Enter your choice: ")

    if choice == '1':
        graph.display()
        graph.output_to_file()
        ans = input("Do you want to continue? (y/n): ")

    elif choice == '2':
        node1 = input("Enter the starting node: ")
        node2 = input("Enter the ending node: ")
        weight = int(input("Enter the weight (or enter 1 if unweighted): "))
        graph.add_edge(node1, node2, weight)
        print(f"Edge between {node1} and {node2} has been added.")
        ans = input("Do you want to continue? (y/n): ")

    elif choice == '3':
        node1 = input("Enter the starting node: ")
        node2 = input("Enter the ending node: ")
        graph.remove_edge(node1, node2)
        print(f"Edge between {node1} and {node2} has been removed.")
        ans = input("Do you want to continue? (y/n): ")

    elif choice == '4':
        node = input("Enter the node to be added: ")
        graph.add_node(node)
        print(f"{node} has been added")
        ans = input("Do you want to continue? (y/n): ")

    elif choice == '5':
        node = input("Enter the node to be removed: ")
        graph.remove_node(node)
        print(f"{node} has been removed.")
        ans = input("Do you want to continue? (y/n): ")

    elif choice == '6':
        node = input("Enter the node to be marked as important: ")
        graph.make_important(node)
        ans = input("Do you want to continue? (y/n): ")

    elif choice == '7':
        if not is_weighted(adj_matrix):
            print("Graph is unweighted. Cannot show important nodes.")
            ans = input("Do you want to continue? (y/n): ")
            continue
        graph.prim_algo()
        ans = input("Do you want to continue? (y/n): ")

    elif choice == '8':
        print("Exiting...")
        break

    else:
        print("Invalid choice. Please try again.")



