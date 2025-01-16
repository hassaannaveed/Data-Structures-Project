from b1 import get_matrix, is_directed, is_weighted
from graph import Graph

filename = input("Enter the filename to be read: ")

adj_matrix = get_matrix(filename)

# Check if the adjacency matrix is None (i.e., file not found or error reading file)
if adj_matrix is None:
    print("Exiting...")
    exit()

if is_directed(adj_matrix) and is_weighted(adj_matrix):
    graph = Graph(directed=True, weighted=True)
elif is_directed(adj_matrix) and not is_weighted(adj_matrix):
    graph = Graph(directed=True, weighted=False)
elif not is_directed(adj_matrix) and is_weighted(adj_matrix):
    graph = Graph(directed=False, weighted=True)
else:
    graph = Graph(directed=False, weighted=False)


graph.add_from_adj_matrix(adj_matrix)

print("Graph has been created successfully.")
print("Graph is directed: ", graph.directed)
print("Graph is weighted: ", graph.weighted)
ans = 'y'

total_buses = 0


while ans=='y':
    print("***** Menu *****")
    print("1. Display the graph and Output to file")
    print("2. Add an edge")
    print("3. Remove an edge")
    print("4. Add a node")
    print("5. Remove a node")
    print("6. Mark a node as important")
    print("7. Mark an edge as impassable")
    print("8. Find the nearest intersection to a supply point")
    print("9. Show the graph of important nodes only")
    print("10. Enter a collection point for evacuation")
    print("11. Enter the capacity of a road")
    print("12. Enter the capacity of all nodes through a file")
    print ("13. Enter the Total number of buses available")
    print("14. Evaluate the evacuation plan")
    print("15. Exit")
    print("******************")

    choice = input("Enter your choice: ")

    if choice == '1':
        print("Note: Negative weights represent flooded roads.")
        graph.display()
        graph.output_to_file()
        print("Graph has been written to a file successfully.")
        ans = input("Do you want to continue? (y/n): ")
        while ans not in ['y', 'n']:
            print("Invalid choice. Please try again.")
            ans = input("Do you want to continue? (y/n): ")

    elif choice == '2':
        node1 = input("Enter the starting node: ")
        node2 = input("Enter the ending node: ")
        weight = int(input("Enter the weight (or enter 1 if unweighted): "))

        graph.add_edge(node1, node2, weight)

        print(f"Edge between {node1} and {node2} has been added.")
        ans = input("Do you want to continue? (y/n): ")
        while ans not in ['y', 'n']:
            print("Invalid choice. Please try again.")
            ans = input("Do you want to continue? (y/n): ")

    elif choice == '3':
        node1 = input("Enter the starting node: ")
        node2 = input("Enter the ending node: ")
        graph.remove_edge(node1, node2)
        print(f"Edge between {node1} and {node2} has been removed.")
        ans = input("Do you want to continue? (y/n): ")
        while ans not in ['y', 'n']:
            print("Invalid choice. Please try again.")
            ans = input("Do you want to continue? (y/n): ")

    elif choice == '4':
        node = input("Enter the node to be added: ")
        graph.add_node(node)
        print(f"{node} has been added")
        ans = input("Do you want to continue? (y/n): ")
        while ans not in ['y', 'n']:
            print("Invalid choice. Please try again.")
            ans = input("Do you want to continue? (y/n): ")

    elif choice == '5':
        node = input("Enter the node to be removed: ")
        graph.remove_node(node)
        print(f"{node} has been removed.")
        ans = input("Do you want to continue? (y/n): ")
        while ans not in ['y', 'n']:
            print("Invalid choice. Please try again.")
            ans = input("Do you want to continue? (y/n): ")

    elif choice == '6':
        node = input("Enter the node to be marked as important: ")
        site_type = input("Enter d for deployment site, a for assembly point, s for supply point, r for rescue station, h for hospital, g for Govt. building, sh for shelter: ")
        while site_type not in ['d', 'a', 's', 'r', 'h', 'g', 'sh']:
            print("Invalid choice. Please try again.")
            site_type = input("Enter d for deployment site, a for assembly point, s for supply point, r for rescue station, h for hospital, g for Govt. building: ")
        graph.set_important(node, site_type)
        ans = input("Do you want to continue? (y/n): ")
        while ans not in ['y', 'n']:
            print("Invalid choice. Please try again.")
            ans = input("Do you want to continue? (y/n): ")

    elif choice == '7':
        node1 = input("Enter the starting node: ")
        node2 = input("Enter the ending node: ")
        graph.set_impassable(node1, node2)
        ans = input("Do you want to continue? (y/n): ")
        while ans not in ['y', 'n']:
            print("Invalid choice. Please try again.")
            ans = input("Do you want to continue? (y/n): ")

    elif choice == '8':
        if not graph.weighted:
            print("Graph is Unweighted. Cannot carry the operation.")
            ans = input("Do you want to continue? (y/n): ")
            while ans not in ['y', 'n']:
                print("Invalid choice. Please try again.")
                ans = input("Do you want to continue? (y/n): ")
            continue
        node = input("Enter the supply point to find the nearest intersection: ")
        graph.set_important(node, 's')
        result = graph.distance_to_nearest_intersection(node)
        if result:
            nearest_node, distance = result
            print(f"The nearest intersection to {node} is {nearest_node} at a distance of {distance}.")
        ans = input("Do you want to continue? (y/n): ")
        while ans not in ['y', 'n']:
            print("Invalid choice. Please try again.")
            ans = input("Do you want to continue? (y/n): ")

    elif choice == '9':
        if not graph.weighted:
            print("Graph is Unweighted. Cannot carry the operation.")
            ans = input("Do you want to continue? (y/n): ")
            while ans not in ['y', 'n']:
                print("Invalid choice. Please try again.")
                ans = input("Do you want to continue? (y/n): ")
            continue
        mst = graph.basic_network()
        print("The Basic Network:")
        for node1, node2, weight in mst:
            print(f"{node1} - {node2} (Cost: {weight})")
        ans = input("Do you want to continue? (y/n): ")
        while ans not in ['y', 'n']:
            print("Invalid choice. Please try again.")
            ans = input("Do you want to continue? (y/n): ")

    elif choice == '10':
        node = input("Enter the collection point for evacuation: ")
        graph.set_important(node, 'c')
        print(f"{node} has been set as the evacuation point.")
        ans = input("Do you want to continue? (y/n): ")
        while ans not in ['y', 'n']:
            print("Invalid choice. Please try again.")
            ans = input("Do you want to continue? (y/n): ")

    elif choice == '11':
        node1 = input("Enter the starting node: ")
        node2 = input("Enter the ending node: ")
        capacity = int(input("Enter the capacity of the road (in number of people): "))
        graph.set_capacity(node1, node2, capacity)
        ans = input("Do you want to continue? (y/n): ")
        while ans not in ['y', 'n']:
            print("Invalid choice. Please try again.")
            ans = input("Do you want to continue? (y/n): ")

    elif choice == '12':
        filename = input("Enter the filename to read the capacity of all nodes: ")
        graph.set_capacity_from_file(filename)
        ans = input("Do you want to continue? (y/n): ")
        while ans not in ['y', 'n']:
            print("Invalid choice. Please try again.")
            ans = input("Do you want to continue? (y/n): ")

    elif choice == '13':
        total_buses = int(input("Enter the total number of buses available (each bus carry 30 people): "))
        ans = input("Do you want to continue? (y/n): ")
        while ans not in ['y', 'n']:
            print("Invalid choice. Please try again.")
            ans = input("Do you want to continue? (y/n): ")

    elif choice == '14':
        graph.evacuate(total_buses)


    elif choice == '15':
        print("Exiting...")
        break

    else:
        print("Invalid choice. Please try again.")



