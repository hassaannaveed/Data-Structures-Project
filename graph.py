import heapq # For priority queue operations (used in Dijkstra's algorithm)


from b1 import get_matrix # Import the `get_matrix` function for reading matrices from a file


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


    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = {'connections': [], 'type_of_node': None}
        else:
            print("Node already exists.")

    def add_edge(self, node1, node2, weight=1, capacity=99):
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
            for connection in self.graph[node2]['connections']:
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
            node_type = None
            if data['type_of_node'] == 's':
                node_type = "Supply Point"
            elif data['type_of_node'] == 'r':
                node_type = "Rescue Station"
            elif data['type_of_node'] == 'h':
                node_type = "Hospital"
            elif data['type_of_node'] == 'g':
                node_type = "Govt. Building"

            connections = []
            for connection, weight, capacity in data['connections']:
                if self.directed:
                    # For directed graphs, add the edge directly
                    connections.append(f"{connection} (Weight: {weight}), Capacity: {capacity})")
                else:
                    # For undirected graphs, avoid duplicate edges
                    edge = tuple(sorted([node, connection]))
                    if edge not in displayed_edges:
                        connections.append(f"{connection} (Weight: {weight}), Capacity: {capacity})")
                        displayed_edges.add(edge)

            connections_data = ", ".join(connections) if connections else "No connections"
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

        connections = []
        found = False
        for connected_node, weight in self.graph[node1]['connections']:
            if connected_node == node2 and weight > 0:
                connections.append((connected_node, -weight))
                found = True
            else:
                connections.append((connected_node, weight))

        if found:
            self.graph[node1]['connections'] = connections
            print(f"Edge between {node1} and {node2} has been marked impassable.")
        else:
            print(f"No edge found between {node1} and {node2}.")
            return

        # If the graph is undirected, do the same for the reverse connection
        if not self.directed:
            connections = []
            for connected_node, weight in self.graph[node2]['connections']:
                if connected_node == node1 and weight > 0:
                    connections.append((connected_node, -weight))
                else:
                    connections.append((connected_node, weight))
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
            #Checks every node in the graph
            for node2 in self.graph:
                if node1 == node2:
                    continue  # Skip self-loops

                direct_connection = False
                #check the connections of the node
                for connection, weight, _ in self.graph[node1]['connections']:
                    if connection == node2 and weight > 0:  # Ensure positive weight for passable connections
                        passable_graph[node1].append((node2, weight))
                        direct_connection = True
                        break  # No need to continue checking for this pair

                        # If no direct connection exists, use Dijkstra to find the shortest path
                    if not direct_connection:
                        result = self.djikstra(node1, node2)
                        if result:  # If a path exists
                            distance, _ = result
                            passable_graph[node1].append((node2, distance))

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

    def evacuate(self, buses_available, bus_capacity=30):

        # First, find the shelter node in the graph

        if not self.shelter:
            print("No shelter node found.")
            return

        shelter_node = self.shelter[0] # Assume there's only one shelter node

        # Step 1: Calculate shortest paths from each collection point to the shelter using Dijkstra's algorithm
        collection_points = self.collection_points
        shortest_paths = {}

        for collection_point in collection_points:
            distance, path = self.djikstra(collection_point, shelter_node)
            shortest_paths[collection_point] = (distance, path)
            print(f"Shortest path from {collection_point} to shelter: {path} with distance {distance}")

        # Step 2: Prepare the graph for Ford-Fulkerson
        # Create a new graph for the Ford-Fulkerson algorithm to find maximum flow
        capacity_graph = {node: {} for node in self.graph}

        # Populate the capacity graph with the actual capacities
        for node in self.graph:
            for connection, weight, capacity in self.graph[node]['connections']:
                capacity_graph[node][connection] = capacity  # Use capacity, not weight

        # Ford-Fulkerson algorithm (Edmonds-Karp implementation for maximum flow)
        def bfs(source, sink, parent):
            visited = {node: False for node in self.graph}
            queue = [source]
            visited[source] = True

            while queue:
                node = queue.pop(0)

                for neighbor in capacity_graph[node]:
                    if not visited[neighbor] and capacity_graph[node][neighbor] > 0:
                        queue.append(neighbor)
                        visited[neighbor] = True
                        parent[neighbor] = node
                        if neighbor == sink:
                            return True
            return False

        def edmonds_karp(source, sink):
            total_flow = 0
            parent = {}
            while bfs(source, sink, parent):
                path_flow = 999999999
                s = sink
                while s != source:
                    path_flow = min(path_flow, capacity_graph[parent[s]][s])
                    s = parent[s]

                total_flow += path_flow

                v = sink
                while v != source:
                    u = parent[v]
                    capacity_graph[u][v] -= path_flow
                    capacity_graph[v][u] += path_flow
                    v = parent[v]

            return total_flow

        # Step 3: Check the maximum flow from collection points to the shelter
        total_buses_needed = 0
        for collection_point in collection_points:
            # Assume that each path can accommodate `bus_capacity` passengers at a time.
            flow_capacity = edmonds_karp(collection_point, shelter_node)
            buses_needed = flow_capacity // bus_capacity
            if flow_capacity % bus_capacity != 0:
                buses_needed += 1  # If there's any remainder, we need one more bus

            print(f"From {collection_point}, we can evacuate {flow_capacity} people, requiring {buses_needed} buses.")
            total_buses_needed += buses_needed

        # Step 4: Check if the number of buses is sufficient
        if total_buses_needed <= buses_available:
            print(
                f"Evacuation is possible! We need {total_buses_needed} buses and have {buses_available} buses available.")
            return True
        else:
            print(
                f"Evacuation is not possible. We need {total_buses_needed} buses, but only {buses_available} buses are available.")
            return False