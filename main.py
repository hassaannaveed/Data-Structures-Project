from basic import get_matrix, is_directed, is_weighted
from graph import Graph
from f1 import F1
from f2 import F2
from f3 import F3
from f4 import F4
from f5 import F5


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
f1 = F1(graph)
f2 = F2(graph)
f3 = F3(graph)
f4 = F4(graph)
f5 = F5(graph)
ans = 'y'

while ans=='y':
    print("***** Menu *****")
    print("1. Display the graph and Output to file")
    print("2. Add an edge")
    print("3. Remove an edge")
    print("4. Add a node")
    print("5. Remove a node")
    print("6. Mark a node as important")
    print("7. Mark an edge as impassable/flooded")
    print("8. Find the nearest intersection to a supply point")
    print("9. Show the graph of important nodes only")
    print("10. Enter a collection point for evacuation")
    print("11. Enter the capacity of a road")
    print("12. Enter the capacity of all nodes through a file")
    print("13. Evaluate the evacuation plan")
    print("14. Calculate the fastest route between two nodes")
    print("15. Determine optimal locations for additional supply points")
    print("16. Deployment planning for emergency services")
    print("17. Exit")
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

        if not graph.weighted and weight != 1:
            print("Graph is Unweighted. Cannot carry the operation.")
            ans = input("Do you want to continue? (y/n): ")
            while ans not in ['y', 'n']:
                print("Invalid choice. Please try again.")
                ans = input("Do you want to continue? (y/n): ")
            continue

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
        site_type = input("Enter s for supply point, r for rescue station, h for hospital, g for Govt. building, sh for shelter: ")
        while site_type not in ['s', 'r', 'h', 'g', 'sh']:
            print("Invalid choice. Please try again.")
            site_type = input("Enter s for supply point, r for rescue station, h for hospital, g for Govt. building: ")
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
        mst = f1.basic_network()
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
        #Only works for weighted and directed graphs
        if graph.weighted and graph.directed:
            #The output will only show the number of people that can be evacuated
            #the system assumes that the number os buses are enough for evacuation
            f2.max_flow_collection_to_shelter()
        else:
            print("Graph is either unweighted or undirected. Cannot carry the operation.")

        ans = input("Do you want to continue? (y/n): ")
        while ans not in ['y', 'n']:
            print("Invalid choice. Please try again.")
            ans = input("Do you want to continue? (y/n): ")

    elif choice == '14':
        source = input("Enter the source node: ")
        destination = input("Enter the destination node: ")
        result = f3.calculate_fastest_route(source, destination)
        if result:
            distance, path = result
            print(f"The fastest route from {source} to {destination} is: {' -> '.join(path)}")
            print(f"Total distance: {distance}")
        ans = input("Do you want to continue? (y/n): ")
        while ans not in ['y', 'n']:
            print("Invalid choice. Please try again.")
            ans = input("Do you want to continue? (y/n): ")

    elif choice == '15':
        current_supply_points = input("Enter current supply points (comma-separated): ").split(',')
        k = int(input("Enter the number of additional supply points: "))
        additional_supply_points = f4.optimal_supply_points(current_supply_points, k)
        if additional_supply_points:
            print("Recommended additional supply points:", ", ".join(additional_supply_points))
        ans = input("Do you want to continue? (y/n): ")

    elif choice == '16':
        # Step 1: Get deployment sites from the user
        num_sites = int(input("Enter the number of deployment sites: "))

        for _ in range(num_sites):
            site_name = input("Enter the deployment site name: ")
            required_skills = input("Enter required skills for the site (comma separated): ").split(',')
            required_resources = input("Enter required resources for the site (comma separated): ").split(',')
            required_people = int(input("Enter the number of people needed for the site: "))

            # Clean up input (strip spaces)
            required_skills = {skill.strip() for skill in required_skills}
            required_resources = {resource.strip() for resource in required_resources}

            # Add deployment site
            f5.add_deployment_site(site_name, required_skills, required_resources, required_people)

        # Step 2: Get squads from the user
        num_squads = int(input("Enter the number of squads: "))

        for _ in range(num_squads):
            squad_name = input("Enter the squad name: ")
            squad_skills = input("Enter the skills of the squad (comma separated): ").split(',')
            squad_resources = input("Enter the resources of the squad (comma separated): ").split(',')
            squad_members = int(input("Enter the number of members in the squad: "))

            # Clean up input (strip spaces)
            squad_skills = {skill.strip() for skill in squad_skills}
            squad_resources = {resource.strip() for resource in squad_resources}

            # Add squad to staging area
            f5.add_squad_to_staging_area(squad_name, squad_skills, squad_resources, squad_members)

        # Step 3: Assign squads to deployment sites based on user input
        print("\nAssign squads to deployment sites.")
        for site_name in graph.deployment_sites:  # Only iterate over deployment sites
            squad_name = input(f"Enter the squad name to assign to {site_name}: ")
            f5.assign_squad_to_deployment(site_name, squad_name)

        # Step 4: Deploy emergency services (matching squads to sites)
        print("\nDeploying emergency services...")
        deployment_sites = {}

        for site_name in graph.deployment_sites:  # Use only deployment sites
            required_skills = graph.graph[site_name].get('required_skills', set())
            required_resources = graph.graph[site_name].get('required_resources', set())
            deployment_sites[site_name] = (required_skills, required_resources)

        matching = f5.deploy_emergency_services(deployment_sites)

        # Step 5: Display the deployment plan
        print("\nDeployment Plan:")
        for site, squad in matching.items():
            print(f"Deployment Site {site} <- Squad {squad}")

        print(f"\nTotal squads deployed: {len(matching)}")



    elif choice == '17':
        print("Exiting...")
        break

    else:
        print("Invalid choice. Please try again.")



