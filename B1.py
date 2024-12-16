from tabulate import tabulate

#filename is the name of the file to be read
def task1(filename):
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("Sorry! Find not found.")
        return None
    else:
        cleaned_lines = [line for line in lines if line.strip()]

        nodes = cleaned_lines[0].split()

        #Edited by Hassaan


        adj_matrix = [[0 for _ in range(len(nodes))] for _ in range(len(nodes))]
        node_to_index = {node: i for i, node in enumerate(nodes)}
        for line in cleaned_lines[1:]:
            parts = line.split()
            node = parts[0]
            edges = list(map(int, parts[1:]))

            row = node_to_index[node]
            for col, weight in enumerate(edges):
                adj_matrix[row][col] = weight



        #Edited by Mo Elsobky from row 29 till row 110



        return nodes, adj_matrix

# Function to display the city map in table format
def display_city_map(nodes, adj_matrix):
    data = [[nodes[i]] + adj_matrix[i] for i in range(len(nodes))]
    headers = ["Node"] + nodes
    print(tabulate(data, headers=headers, tablefmt="fancy_grid"))

# Function to modify the city map
def modify_city_map(nodes, adj_matrix):
    print("\nAvailable nodes:", nodes)

    while True:
        print("\nOptions:")
        print("1. Add an important point")
        print("2. Mark a road as impassable")
        print("3. Add a waterway")
        print("4. Exit and display updated city map")
        
        choice = input("Enter your choice: ")

        if choice == "1":
            # Add an important point
            point = input("Enter the name of the new important point: ")
            if point not in nodes:
                nodes.append(point)
                for row in adj_matrix:
                    row.append(0)  # Add column with zeros
                adj_matrix.append([0] * len(nodes))  # Add row with zeros
                print(f"Added '{point}' as an important point.")
            else:
                print("This point already exists!")

        elif choice == "2":
            # Mark a road as impassable
            node1 = input("Enter the starting node: ")
            node2 = input("Enter the destination node: ")
            if node1 in nodes and node2 in nodes:
                adj_matrix[nodes.index(node1)][nodes.index(node2)] = 0
                print(f"Marked road from '{node1}' to '{node2}' as impassable.")
            else:
                print("One or both nodes do not exist!")

        elif choice == "3":
            # Add a waterway
            node1 = input("Enter the starting node: ")
            node2 = input("Enter the destination node: ")
            weight = int(input("Enter the weight (distance) of the waterway: "))
            if node1 in nodes and node2 in nodes:
                adj_matrix[nodes.index(node1)][nodes.index(node2)] = weight
                print(f"Added waterway from '{node1}' to '{node2}' with weight {weight}.")
            else:
                print("One or both nodes do not exist!")

        elif choice == "4":
            print("Exiting modification menu.")
            break

        else:
            print("Invalid choice. Please try again.")

# Main program
fn = "graph_directed_weighted.txt"
nodes, adjacency_matrix = task1(fn)

if nodes and adjacency_matrix:
    print("\nOriginal City Map:")
    display_city_map(nodes, adjacency_matrix)

    # Modify the city map
    modify_city_map(nodes, adjacency_matrix)

    # Display updated city map
    print("\nUpdated City Map:")
    display_city_map(nodes, adjacency_matrix)