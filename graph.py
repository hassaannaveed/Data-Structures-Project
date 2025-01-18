import heapq # For priority queue operations (used in Dijkstra's algorithm)
from basic import get_matrix # Import the `get_matrix` function for reading matrices from a file
from itertools import combinations
import random

class Graph:

    def __init__(self, directed=False, weighted=False):
        self.directed = directed
        self.weighted = weighted
        self.graph = {}


        # Initialize the lists for important nodes
        self.deployment_sites = []
        self.shelter = []
        self.collection_points = []

        self.staging_area = {}  # Holds squads and their skills/resources




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
            if type_of_site == 'c':
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

    def dijkstra(self, start_node, target_node):
        # Min-heap priority queue
        pq = [(0, start_node)]  # (distance, node)
        distances = {node: float('inf') for node in self.graph}
        distances[start_node] = 0
        prev_nodes = {node: None for node in self.graph}

        while pq:
            current_dist, current_node = heapq.heappop(pq)

            # Skip processing if a better distance is already found
            if current_dist > distances[current_node]:
                continue

            # Explore neighbors
            for neighbor, weight in self.graph[current_node]:
                new_dist = current_dist + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    prev_nodes[neighbor] = current_node
                    heapq.heappush(pq, (new_dist, neighbor))

            if distances[target_node] == float('inf'):
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

    def display_important_nodes(self):
        print("Important Nodes:")
        for node in self.graph:
            if self.graph[node]['type_of_node'] in ['s', 'r', 'h', 'g'] or node in self.deployment_sites or  node in self.shelter or node in self.collection_points:
                print(f"{node}: {self.graph[node]['type_of_node']}")
        print()

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