class Graph:

    def __init__(self, directed=False):
        # Initialize the graph as either directed or undirected
        self.directed = directed
        self.graph = {}

    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = {'important': False, 'connections': []}

    def add_edge(self, node1, node2, weight=1):
        if node1 not in self.graph:
            self.add_node(node1)
        if node2 not in self.graph:
            self.add_node(node2)

        self.graph[node1]['connections'].append((node2, weight))

        # If the graph is undirected, add the reverse edge as well
        if not self.directed:
            self.graph[node2]['connections'].append((node1, weight))

    def get_connections(self, node):
        # Get the connections of a node
        return self.graph.get(node, {}).get('connections', [])

    def has_edge(self, node1, node2):
        # Check if there is an edge between node1 and node2
        for connection, _ in self.graph.get(node1, {}).get('connections', []):
            if connection == node2:
                return True
        return False

    def remove_edge(self, node1, node2):
        # Remove an edge from node1 to node2
        if node1 in self.graph:
            self.graph[node1]['connections'] = [n for n in self.graph[node1]['connections'] if n[0] != node2]

        # For undirected graph, remove the reverse edge
        if not self.directed and node2 in self.graph:
            self.graph[node2]['connections'] = [n for n in self.graph[node2]['connections'] if n[0] != node1]

    def remove_node(self, node):
        # Remove a node and all its edges
        if node in self.graph:
            # Remove edges from other nodes to this node
            for connections in self.graph.values():
                connections['connections'] = [n for n in connections['connections'] if n[0] != node]
            del self.graph[node]

    def display(self):
        # Display the graph
        print("Graph:")
        for node, data in self.graph.items():
            connection_list = [f"{connection} ({weight})" for connection, weight in data['connections']]
            important_status = "Important" if data['important'] else "Not Important"
            print(f"{node}: {', '.join(connection_list)} - {important_status}")

    def add_from_adj_matrix(self, adj_matrix):
        nodes = [chr(65 + i) for i in range(len(adj_matrix))]

        for node in nodes:
            self.add_node(node)

        for i in range(len(adj_matrix)):
            for j in range(len(adj_matrix[i])):
                if adj_matrix[i][j] != 0:
                    self.add_edge(nodes[i], nodes[j], adj_matrix[i][j])

    def make_important(self, node):
        if node in self.graph:
            self.graph[node]['important'] = True
            print("The node has been made important.")
        else:
            print("The node does not exist.")

    def output_to_file(self, filename="output.txt"):

        nodes = list(self.graph.keys())

        # Initialize an adjacency matrix with zeros
        adj_matrix = [[0] * len(nodes) for _ in range(len(nodes))]

        # Fill the adjacency matrix with edge weights
        for i, node1 in enumerate(nodes):
            for j, node2 in enumerate(nodes):
                for connection, weight in self.graph[node1]['connections']:
                    if connection == node2:
                        adj_matrix[i][j] = weight

        # Write the matrix to a text file
        with open(filename, "w") as file:
            # Write node labels in the first row
            file.write(" ".join(nodes) + "\n")

            # Write the adjacency matrix
            for row in adj_matrix:
                file.write(" ".join(map(str, row)) + "\n")