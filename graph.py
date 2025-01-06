import heapq

class Graph:

    deployment_sites = []
    assembly_points = []
    shelter = []
    collection_points = []

    def __init__(self, directed=False, weighted=False):
        self.directed = directed
        self.weighted = weighted
        self.graph = {}

    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = {'connections': [], 'type_of_node': None}
        else:
            print("Node already exists.")

    def add_edge(self, node1, node2, weight=1, capacity=999999999):
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

    def make_important(self, node, type_of_site):
        if node not in self.graph:
            print("The node does not exist.")
            return
        self.graph[node]['type_of_node'] = None

        if type_of_site == 's' or type_of_site == 'r' or type_of_site == 'h' or type_of_site == 'g':
            self.graph[node]['type_of_node'] = type_of_site
        else:
            if type_of_site == 'd':
                Graph.deployment_sites.append(node)
            elif type_of_site == 'a':
                Graph.assembly_points.append(node)
            elif type_of_site == 'c':
                Graph.collection_points.append(node)
            else:
                Graph.shelter.append(node)



    def output_to_file(self, filename="output.txt"):
        nodes = list(self.graph.keys())
        num_nodes = len(nodes)

        adj_matrix = []
        for _ in range(num_nodes):
            adj_matrix.append([0] * num_nodes)

        for node1 in self.graph:
            for connection, weight in self.graph[node1]['connections']:
                row = nodes.index(node1)
                col = nodes.index(connection)
                adj_matrix[row][col] = weight

        with open(filename, "w") as file:
            file.write(" ".join(nodes) + "\n")
            for row in adj_matrix:
                row_string = " ".join([str(item) for item in row])
                file.write(row_string + "\n")

    def mark_impassable(self, node1, node2):
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
        print(f"No edge found between {node1} and {node2}.")
        return None

    def distance_to_nearest_intersection(self, node):
        distances = {n: 9999999 for n in self.graph}
        distances[node] = 0

        visited = set()
        to_visit = [node]

        while to_visit:
            current_node = to_visit.pop(0)

            if current_node in visited:
                continue
            visited.add(current_node)

            # Check if the current node is an intersection
            if current_node != node and len(self.graph[current_node]['connections']) > 0:
                return current_node, distances[current_node]

            # Update distances for neighbors
            for neighbor, weight in self.graph[current_node]['connections']:
                if weight > 0 and neighbor not in visited:
                    new_distance = distances[current_node] + weight
                    if new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        to_visit.append(neighbor)  # Add neighbor to the queue

        print(f"No intersections found for supply point {node}.")
        return

    def basic_network(self):
        important_nodes = [
            node for node in self.graph
            if self.graph[node]['type_of_node'] in ['s', 'r', 'h', 'g']
        ]
        passable_graph = {node: [] for node in important_nodes}
        for node in important_nodes:
            for connection, weight in self.graph[node]['connections']:
                if connection in important_nodes and weight > 0:
                    passable_graph[node].append((connection, weight))

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

        if len(visited) != len(important_nodes):
            print("Graph is not fully connected")
            return []

        return mst

    def dijkstra(self, start_node, target_node):
        # Min-heap priority queue
        pq = [(0, start_node)]  # (distance, node)
        distances = {node: float('inf') for node in self.graph}
        distances[start_node] = 0
        prev_nodes = {node: None for node in self.graph}

        while pq:
            current_dist, current_node = heapq.heappop(pq)

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

        # Reconstruct the path from start to target node
        path = []
        current_node = target_node
        while prev_nodes[current_node] is not None:
            path.insert(0, current_node)
            current_node = prev_nodes[current_node]
        if path:
            path.insert(0, start_node)

        return distances[target_node], path

    def evacuate(self, collection_points, shelter, buses_available, bus_capacity=30):
        total_people = len(collection_points) * 100  # Each collection point has 100 people
        total_buses_needed = total_people // bus_capacity
        if total_people % bus_capacity > 0:
            total_buses_needed += 1

        # Calculate total buses available (adjusted for buses available for each route)
        total_buses_available = buses_available

        print(f"Total people to evacuate: {total_people}")
        print(f"Total buses needed: {total_buses_needed}")
        print(f"Total buses available: {total_buses_available}")

        # Store evacuation paths and check if roads are sufficient
        evacuation_plan = {}
        total_capacity = 0

        for collection_point in collection_points:
            distance, path = self.dijkstra(collection_point, shelter)
            if path:
                print(
                    f"Evacuation path from {collection_point} to shelter: {' -> '.join(path)} with distance {distance}")
                # Calculate the total road capacity for this route
                route_capacity = min([self.graph[path[i]]['connections'][next(
                    (j for j, conn in enumerate(self.graph[path[i]]['connections']) if conn[0] == path[i + 1]), None)][
                                          2]
                                      for i in range(len(path) - 1)])
                print(f"Capacity on this route: {route_capacity}")
                total_capacity += route_capacity
                evacuation_plan[collection_point] = {'path': path, 'distance': distance, 'capacity': route_capacity}
            else:
                print(f"No path found from {collection_point} to shelter.")

        # Check if infrastructure is sufficient
        if total_capacity >= total_buses_needed:
            print("The existing infrastructure is sufficient to evacuate all people.")
        else:
            print("Additional infrastructure is needed to evacuate all people.")

        print("\nEvacuation Plan:")
        for collection_point, plan in evacuation_plan.items():
            print(
                f"{collection_point} -> Path: {' -> '.join(plan['path'])}, Distance: {plan['distance']}, Capacity: {plan['capacity']}")

        return evacuation_plan








