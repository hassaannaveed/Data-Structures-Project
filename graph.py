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
        if node2 not in self.graph:
            print(f"Node {node2} does not exist.")
            return

        connections = []
        found = False
        for connected_node, weight, _ in self.graph[node1]['connections']:
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
            for connected_node, weight, _ in self.graph[node2]['connections']:
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
            #Checks every other important node in the graph
            for node2 in important_nodes:

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

        # Assuming that every collection point ahs 100 people to evacuate
        total_people = 100 * len(self.collection_points)
        if (buses_available * bus_capacity) < total_people:
            more_buses_needed = ((total_people - (buses_available * bus_capacity)) % bus_capacity) + 1


        # Create a new graph for the flow problem
        flow_graph = {}
        for node in self.graph:
            flow_graph[node] = {}
            for connection, weight, capacity in self.graph[node]['connections']:
                if weight >= 0:  # Only consider passable roads
                    flow_graph[node][connection] = capacity

        # Add super-source and super-sink
        super_source = "SuperSource"
        super_sink = "SuperSink"

        flow_graph[super_source] = {}
        flow_graph[super_sink] = {}

        # Connect super-source to all collection points
        for collection_point in self.collection_points:
            flow_graph[super_source][collection_point] = float('inf')  # Unlimited capacity from super-source

        # Connect all shelters to the super-sink
        for shelter_point in self.shelter:
            if shelter_point not in flow_graph:
                flow_graph[shelter_point] = {}
            flow_graph[shelter_point][super_sink] = float('inf')  # Unlimited capacity to super-sink

        # Helper function: BFS to find an augmenting path
        def bfs(residual_graph, source, sink, parent):
            visited = set()
            queue = [source]
            visited.add(source)

            while queue:
                current_node = queue.pop(0)

                for neighbor,capacity in residual_graph[current_node].items():
                    if neighbor not in visited and capacity > 0:  # Unvisited and has capacity
                        queue.append(neighbor)
                        visited.add(neighbor)
                        parent[neighbor] = current_node

                        if neighbor == sink:
                            return True
            return False

        # Ford-Fulkerson method to calculate max flow
        def ford_fulkerson(graph, source, sink):
            residual_graph = {node: edges.copy() for node, edges in graph.items()}
            parent = {}
            max_flow = 0

            while bfs(residual_graph, source, sink, parent):
                # Find the bottleneck capacity along the path found by BFS
                path_flow = float('inf')
                current_node = sink

                while current_node != source:
                    path_flow = min(path_flow, residual_graph[parent[current_node]][current_node])
                    current_node = parent[current_node]

                # Update residual capacities of the edges and reverse edges
                current_node = sink
                while current_node != source:
                    prev_node = parent[current_node]
                    residual_graph[prev_node][current_node] -= path_flow
                    if current_node not in residual_graph:
                        residual_graph[current_node] = {}
                    residual_graph[current_node][prev_node] = residual_graph[current_node].get(prev_node, 0) + path_flow
                    current_node = prev_node

                max_flow += path_flow

            return max_flow

        # Calculate max flow
        max_flow = ford_fulkerson(flow_graph, super_source, super_sink)

        # Check if the maximum flow is enough to evacuate all people
        if max_flow >= total_people:
            return True
        else:
            print(f"{more_buses_needed} more buses are needed to evacuate all people.")
            return False
