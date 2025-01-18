import heapq # For priority queue operations (used in Dijkstra's algorithm)
from basic import get_matrix # Import the `get_matrix` function for reading matrices from a file

class Graph:

    def __init__(self, directed=False, weighted=False):
        self.directed = directed
        self.weighted = weighted
        self.graph = {}


        # Initialize the lists for important nodes
        self.deployment_sites = []
        self.assembly_points = []
        self.shelter = []
        self.collection_points = []

        #variables
        self.total_policemen = 0
        self.total_firefighters = 0
        self.total_medics = 0

        self.staging_personnel = []  # To store emergency services personnel
        self.deployed_personnel = {site: {'policemen': 0, 'firefighters': 0, 'medics': 0} for site in self.deployment_sites}
        self.waiting_for_personnel = {site: {'policemen': 0, 'firefighters': 0, 'medics': 0} for site in
                                   self.deployment_sites}




    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = {'connections': [], 'type_of_node': None}
        else:
            print("Node already exists.")

    def add_edge(self, node1, node2, weight=1, capacity=99):
        """
            Adds an edge between two nodes with an optional weight and capacity.
            If the graph is undirected, the edge is bidirectional.

            Args:
                node1 (str): The starting node.
                node2 (str): The ending node.
                weight (int): The weight of the edge (default is 1).
                capacity (int): The capacity of the edge (default is 99).
            """
        if node1 not in self.graph:
            self.add_node(node1)
        if node2 not in self.graph:
            self.add_node(node2)


        self.graph[node1]['connections'].append((node2, weight, capacity))

        if not self.directed:
            self.graph[node2]['connections'].append((node1, weight, capacity))

    def set_capacity(self, node1, node2, capacity):
        if node1 not in self.graph or node2 not in self.graph:
            print("One or both nodes do not exist.")
            return

        found = False
        for connection in self.graph[node1]['connections']:
            if connection[0] == node2:
                connection_index = self.graph[node1]['connections'].index(connection)
                self.graph[node1]['connections'][connection_index] = (connection[0], connection[1], capacity)
                found = True
                break


        if not self.directed:
            for connection  in self.graph[node2]['connections']:
                if connection[0] == node1:
                    connection_index = self.graph[node2]['connections'].index(connection)
                    self.graph[node2]['connections'][connection_index] = (connection[0], connection[1], capacity)
                    found = True
                    break

        if found:
            print(f"Capacity between {node1} and {node2} set to {capacity}.")
        else:
            print(f"No edge found between {node1} and {node2} to update capacity.")

    def get_connections(self, node):
        return self.graph.get(node, {}).get('connections', [])

    def has_edge(self, node1, node2):
        for connection, _, _ in self.graph.get(node1, {}).get('connections', []):
            if connection == node2:
                return True
        return False

    def remove_edge(self, node1, node2):
        if node1 in self.graph:
            self.graph[node1]['connections'] = [n for n in self.graph[node1]['connections'] if n[0] != node2]

        if not self.directed and node2 in self.graph:
            self.graph[node2]['connections'] = [n for n in self.graph[node2]['connections'] if n[0] != node1]

    def remove_node(self, node):
        if node in self.graph:
            # Remove edges from other nodes to this node
            for connections in self.graph.values():
                connections['connections'] = [n for n in connections['connections'] if n[0] != node]
            del self.graph[node]

    def display(self):
        print("Graph:")
        displayed_edges = set()  # To track edges in undirected graphs and prevent duplication

        for node, data in self.graph.items():
            # Determine the type of node
            if data['type_of_node'] == 's':
                node_type = "Supply Point"
            elif data['type_of_node'] == 'r':
                node_type = "Rescue Station"
            elif data['type_of_node'] == 'h':
                node_type = "Hospital"
            elif data['type_of_node'] == 'g':
                node_type = "Govt. Building"
            else:
                node_type = None

            connections = []
            for connection_data in data['connections']:
                connection, weight, capacity = connection_data
                if self.directed:
                    # For directed graphs, add the edge directly
                    connections.append(f"{connection} (Weight: {weight}, Capacity: {capacity})")
                else:
                    # For undirected graphs, avoid duplicate edges
                    edge = tuple(sorted([node, connection]))
                    if edge not in displayed_edges:
                        connections.append(f"{connection} (Weight: {weight}, Capacity: {capacity})")
                        displayed_edges.add(edge)

            # Prepare connections data for output
            connections_data = ", ".join(connections) if connections else "No connections"

            # Print node and its connections
            if node_type is not None:
                print(f"{node} ({node_type}): {connections_data}")
            else:
                print(f"{node}: {connections_data}")


    def add_from_adj_matrix(self, adj_matrix):
        num_rows = len(adj_matrix)
        for row in adj_matrix:
            if len(row) != num_rows:
                print("Invalid adjacency matrix.")
                return

        nodes = [chr(65 + i) for i in range(len(adj_matrix))]

        for node in nodes:
            self.add_node(node)

        for i in range(len(adj_matrix)):
            for j in range(len(adj_matrix[i])):
                if adj_matrix[i][j] != 0:
                    self.add_edge(nodes[i], nodes[j], adj_matrix[i][j])

    def set_important(self, node, type_of_site):
        if node not in self.graph:
            print("The node does not exist.")
            return
        self.graph[node]['type_of_node'] = None

        if type_of_site == 's' or type_of_site == 'r' or type_of_site == 'h' or type_of_site == 'g':
            self.graph[node]['type_of_node'] = type_of_site
        else:
            if type_of_site == 'd':
                self.deployment_sites.append(node)
            elif type_of_site == 'a':
                self.assembly_points.append(node)
            elif type_of_site == 'c':
                self.collection_points.append(node)
            elif type_of_site == 'sh':
                self.shelter.append(node)



    def output_to_file(self, filename="output.txt"):
        nodes = list(self.graph.keys())
        num_nodes = len(nodes)

        adj_matrix = []
        for _ in range(num_nodes):
            adj_matrix.append([0] * num_nodes)

        for node1 in self.graph:
            for connection, weight, _ in self.graph[node1]['connections']:
                row = nodes.index(node1)
                col = nodes.index(connection)
                adj_matrix[row][col] = weight

        with open(filename, "w") as file:
            file.write(" ".join(nodes) + "\n")
            for row in adj_matrix:
                row_string = " ".join([str(item) for item in row])
                file.write(row_string + "\n")

    def set_impassable(self, node1, node2):
        if node1 not in self.graph:
            print(f"Node {node1} does not exist.")
            return
        if node2 not in self.graph:
            print(f"Node {node2} does not exist.")
            return

        connections = []
        found = False
        for connected_node, weight, capacity in self.graph[node1]['connections']:
            if connected_node == node2 and weight > 0:
                connections.append((connected_node, -weight, capacity))
                found = True
            else:
                connections.append((connected_node, weight, capacity))

        if found:
            self.graph[node1]['connections'] = connections
            print(f"Edge between {node1} and {node2} has been marked impassable.")
        else:
            print(f"No edge found between {node1} and {node2}.")
            return

        # If the graph is undirected, do the same for the reverse connection
        if not self.directed:
            connections = []
            for connected_node, weight, capacity in self.graph[node2]['connections']:
                if connected_node == node1 and weight > 0:
                    connections.append((connected_node, -weight, capacity))
                else:
                    connections.append((connected_node, weight, capacity))
            self.graph[node2]['connections'] = connections

    def get_capacity(self, node1, node2):
        for connection, weight, capacity in self.graph.get(node1, {}).get('connections', []):
            if connection == node2:
                return capacity
        return None

    def set_capacity_from_file(self, filename):
        capacity_matrix = get_matrix(filename)
        num_rows = len(capacity_matrix)
        for row in capacity_matrix:
            if len(row) != num_rows:
                print("Invalid capacity matrix.")
                return

        nodes = [chr(65 + i) for i in range(len(capacity_matrix))]

        for i in range(len(capacity_matrix)):
            for j in range(len(capacity_matrix[i])):
                if capacity_matrix[i][j] > 0:
                    self.set_capacity(nodes[i], nodes[j], capacity_matrix[i][j])


    def distance_to_nearest_intersection(self, supply_point):
        if supply_point not in self.graph:
            print(f"Node {supply_point} does not exist.")
            return

        nearest_intersection = None
        shortest_distance = 999999999999999
        best_path = []

        print(f"\nCalculating distances from supply point: {supply_point}\n")

        # Iterate through all nodes
        for node in self.graph:
            # Check if the node is an intersection
            if node != supply_point and len(self.graph[node]['connections']) > 1:
                # Use the pre-defined djikstra function
                distance, path = self.djikstra(supply_point, node)

                # Update nearest intersection if a shorter path is found
                if distance < shortest_distance:
                    nearest_intersection = node
                    shortest_distance = distance
                    best_path = path

                print(f"  {node}: Distance = {distance}, Path = {' -> '.join(path) if path else 'No path'}")

        # Display the nearest intersection and details
        if nearest_intersection:
            print(f"\nNearest intersection: {nearest_intersection}")
            print(f"Shortest distance: {shortest_distance}")
            print(f"Path: {' -> '.join(best_path)}")
        else:
            print("\nNo intersection found.")


    def basic_network(self):
        # Create a new graph with only important nodes
        important_nodes = [
            node for node in self.graph
            if self.graph[node]['type_of_node'] in ['s', 'r', 'h', 'g'] or node in self.deployment_sites or node in self.assembly_points or node in self.shelter or node in self.collection_points # Add all important nodes
        ]
        # Check if there are any important nodes
        if not important_nodes:
            print("No important nodes found.")
            return []
        # Initialize passable graph for important nodes
        passable_graph = {node: [] for node in important_nodes}

        # Iterate through all pairs of important nodes
        for node1 in important_nodes:
            #Checks every other important node in the graph
            for node2 in important_nodes:
                if node1 == node2:
                    continue  # Skip self-loops

                direct_connection = False
                #check the connections of the node
                for connection, weight, _ in self.graph[node1]['connections']:
                    if connection == node2 and weight > 0:  # Ensure positive weight for passable connections
                        passable_graph[node1].append((node2, weight))
                        if (not self.directed) and (node2, node1) not in passable_graph[node2]:
                            passable_graph[node2].append((node1, weight))
                        direct_connection = True
                        break  # No need to continue checking for this pair

                    # If no direct connection exists, use Dijkstra to find the shortest path
                    if not direct_connection:
                        result = self.djikstra(node1, node2)
                        if result:  # If a path exists
                            distance, _ = result
                            passable_graph[node1].append((node2, distance))
                            if (not self.directed) and (node2, node1) not in passable_graph[node2]:
                                passable_graph[node2].append((node1, distance))

        mst = []
        visited = set()
        start_node = important_nodes[0]
        min_heap = []

        for connections, weight in passable_graph[start_node]:
            heapq.heappush(min_heap, (weight, start_node, connections))

        visited.add(start_node)

        while min_heap:
            weight, node1, node2 = heapq.heappop(min_heap)

            if node2 not in visited:
                visited.add(node2)
                mst.append((node1, node2, weight))

                for connections, weight in passable_graph[node2]:
                    if connections not in visited:
                        heapq.heappush(min_heap, (weight, node2, connections))
            else:
                continue

        # Check if all important nodes are connected
        if len(visited) != len(important_nodes):
            print("Graph is not fully connected")
            return []

        return mst

    def djikstra(self, start_node, target_node):
        # Min-heap priority queue
        pq = [(0, start_node)]  # (distance, node)
        distances = {node: 999999999 for node in self.graph}
        distances[start_node] = 0
        prev_nodes = {node: None for node in self.graph}

        while pq:
            current_dist, current_node = heapq.heappop(pq)
            # Skip processing if a better distance is already found
            if current_dist > distances[current_node]:
                continue

            # Explore neighbors
            for neighbor, weight, capacity in self.graph[current_node]['connections']:
                if weight < 0:  # Skip impassable roads
                    continue

                new_dist = current_dist + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    prev_nodes[neighbor] = current_node
                    heapq.heappush(pq, (new_dist, neighbor))

        if distances[target_node] == 999999999:
            return None

        # Reconstruct the path from start to target node
        path = []
        current_node = target_node
        while prev_nodes[current_node] is not None:
            path.insert(0, current_node)
            current_node = prev_nodes[current_node]
        if path:
            path.insert(0, start_node)

        return distances[target_node], path

    def add_super_source_sink(self):
        """
        Adds a super source and super sink to the graph, connecting to all collection points and shelters.
        """
        super_source = "super_source"
        super_sink = "super_sink"

        self.add_node(super_source)
        self.add_node(super_sink)

        # Connect the super source to all collection points
        for node in self.collection_points:
            capacity = sum(conn[2] for conn in self.graph[node]['connections'])
            self.add_edge(super_source, node, capacity)

        # Connect all shelters to the super sink
        for node in self.shelter:
            capacity = sum(conn[2] for conn in self.graph[node]['connections'])
            self.add_edge(node, super_sink, capacity)

        return super_source, super_sink

    def bfs(self, source, sink, parent):
        """
        Breadth-First Search to find an augmenting path.
        """
        visited = {node: False for node in self.graph}
        queue = [source]
        visited[source] = True

        while queue:
            u = queue.pop(0)

            for v, capacity, _ in self.graph[u]['connections']:
                if not visited[v] and capacity > 0:  # Only consider nodes with available capacity
                    queue.append(v)
                    visited[v] = True
                    parent[v] = u
                    if v == sink:
                        return True

        return False

    def edmonds_karp(self, source, sink):
        """
        Implements the Edmonds-Karp algorithm to calculate max flow and outputs the flow graph.
        """
        parent = {node: None for node in self.graph}
        max_flow = 0

        # Flow graph to track actual flows
        flow_graph = {node: {} for node in self.graph}

        while self.bfs(source, sink, parent):
            # Find the bottleneck capacity along the path
            path_flow = float("Inf")
            s = sink
            while s != source:
                u = parent[s]
                for v, capacity, _ in self.graph[u]['connections']:
                    if v == s:
                        path_flow = min(path_flow, capacity)
                        break
                s = u

            # Update capacities and store flows in the flow graph
            v = sink
            while v != source:
                u = parent[v]
                # Update residual capacity in the forward edge
                for i, (connection, capacity, _) in enumerate(self.graph[u]['connections']):
                    if connection == v:
                        self.graph[u]['connections'][i] = (connection, capacity - path_flow, _)
                        break
                # Update residual capacity in the reverse edge
                for i, (connection, capacity, _) in enumerate(self.graph[v]['connections']):
                    if connection == u:
                        self.graph[v]['connections'][i] = (connection, capacity + path_flow, _)
                        break

                # Update the flow graph
                flow_graph[u][v] = flow_graph[u].get(v, 0) + path_flow
                flow_graph[v][u] = flow_graph[v].get(u, 0) - path_flow

                v = u

            # Add the path flow to the total max flow
            max_flow += path_flow

        # Output the flow graph
        print("\nFlow Graph (Node -> Node: Flow):")
        for u, connections in flow_graph.items():
            for v, flow in connections.items():
                if flow > 0:  # Only print positive flows
                    print(f"{u} -> {v}: {flow}")

        return max_flow

    def max_flow_collection_to_shelter(self):
        """
        Calculates the max flow from collection points to shelters using a super source and super sink.
        """
        # Add super source and super sink
        super_source, super_sink = self.add_super_source_sink()

        # Calculate the max flow
        max_flow = self.edmonds_karp(super_source, super_sink)

        # Remove the super source and super sink after calculation
        self.remove_node(super_source)
        self.remove_node(super_sink)

        print(f"Maximum flow from collection points to shelters: {max_flow}")
        return max_flow


    def display_important_nodes(self):
        print("Important Nodes:")
        for node in self.graph:
            if self.graph[node]['type_of_node'] in ['s', 'r', 'h', 'g'] or node in self.deployment_sites or node in self.assembly_points or node in self.shelter or node in self.collection_points:
                print(f"{node}: {self.graph[node]['type_of_node']}")
        print()

    def add_personnel(self, personnel_type, amount, resources):
        """
        Adds personnel to the available pool, including their resources.
        personnel_type: str ('policemen', 'firefighters', or 'medics')
        amount: int (number of personnel to add)
        resources: list of str (resources available with the personnel)
        """
        for _ in range(amount):
            person = {'type': personnel_type, 'resources': resources}
            self.staging_personnel.append(person)

        if personnel_type == 'policemen':
            self.total_policemen += amount
        elif personnel_type == 'firefighters':
            self.total_firefighters += amount
        elif personnel_type == 'medics':
            self.total_medics += amount
        else:
            print(f"Invalid personnel type: {personnel_type}")

    def _get_group_size(self, personnel_type):
        """
        Returns the group size based on the personnel type.
        Policemen work in groups of 2, firefighters in groups of 4, and medics in groups of 3.
        """
        if personnel_type == 'policemen':
            return 2
        elif personnel_type == 'firefighters':
            return 4
        elif personnel_type == 'medics':
            return 3
        else:
            raise ValueError(f"Invalid personnel type: {personnel_type}")

    def assign_personnel(self, site_name, personnel_type, numofgroups, required_resources):
        """
        Assign personnel to a site if resources match; otherwise, update the waiting list.
        """
        if site_name not in self.deployment_sites:
            print(f"Site {site_name} is not a deployment site.")
            return

        if personnel_type not in self.staging_personnel:
            print(f"No personnel of type {personnel_type} available in the staging area.")
            return

        # Filter personnel groups by required resources
        available_groups = [
            group for group in self.staging_personnel[personnel_type]
            if all(resource in group['resources'] for resource in required_resources)
        ]

        if len(available_groups) < numofgroups:
            print(f"Not enough qualified personnel groups. Updating waiting list for {site_name}.")
            self.waiting_for_personnel[site_name][personnel_type] += numofgroups
            return

        # Deploy personnel to the site
        for _ in range(numofgroups):
            deployed_group = available_groups.pop(0)
            self.staging_personnel[personnel_type].remove(deployed_group)

        self.deployed_personnel[site_name][personnel_type] += numofgroups
        print(f"Assigned {numofgroups} group(s) of {personnel_type} to {site_name}.")

    def release_personnel(self, site_name, personnel_type, numofgroups):
        """
        Release personnel from a deployment site and check the waiting list for reassignment.
        site_name: str (the deployment site name)
        personnel_type: str ('policemen', 'firefighters', or 'medics')
        numofgroups: int (number of groups to release)
        """
        group_size = self._get_group_size(personnel_type)
        total_personnel_to_release = group_size * numofgroups

        # Check if there are enough personnel to release
        if self.deployed_personnel[site_name][personnel_type] >= total_personnel_to_release:
            self.deployed_personnel[site_name][personnel_type] -= total_personnel_to_release
            for _ in range(total_personnel_to_release):
                # Add released personnel back to the staging area
                self.staging_personnel.append(
                    {'type': personnel_type, 'resources': []})  # User defines resources when adding

            print(f"Released {total_personnel_to_release} {personnel_type}(s) from {site_name}.")

            # Re-check the waiting list for deployment
            self.check_waiting_sites()
        else:
            print(
                f"Error: Not enough {personnel_type}(s) deployed at {site_name} to release {total_personnel_to_release}.")

    def check_waiting_sites(self):
        """
        Check if any waiting deployment sites can now be fulfilled.
        """
        for site_name, waiting in self.waiting_for_personnel.items():
            for personnel_type, required in waiting.items():
                if required > 0:
                    group_size = self._get_group_size(personnel_type)
                    num_of_groups = (required + group_size - 1) // group_size  # Calculate required groups
                    required_resources = []  # Resources are entered when personnel are added by the user

                    self.assign_personnel(site_name, personnel_type, num_of_groups, required_resources)

                    # Reduce the waiting list if personnel were assigned
                    assigned_personnel = min(required, num_of_groups * group_size)
                    waiting[personnel_type] -= assigned_personnel


    def display_waiting_status(self):
        """
        Display the current waiting status for each deployment site.
        """
        print("Waiting for personnel:")
        for site, waiting in self.waiting_for_personnel.items():
            for personnel_type, count in waiting.items():
                if count > 0:
                    print(f"{site} is waiting for {count} {personnel_type}(s) in groups.")

    def display_staging_area(self):
        """Display the available emergency services in the staging area."""
        if not self.staging_personnel:
            print("No emergency services available in the staging area.")
            return

        print("Staging Area Personnel:")
        for person in self.staging_personnel:
            print(
                f"Type: {person['type']}, Resources: {', '.join(person['resources'])}")

    def display_total_personnel(self):
        """Display the total number of available personnel."""
        print(f"Total Policemen: {self.total_policemen}")
        print(f"Total Firefighters: {self.total_firefighters}")
        print(f"Total Medics: {self.total_medics}")


