class Graph:
    def __init__(self, directed=False, weighted=False):
        self.directed = directed
        self.weighted = weighted
        self.adjacency_list = {}  # Stores the graph as an adjacency list

    def add_node(self, node):
        if node not in self.adjacency_list:
            self.adjacency_list[node] = []

    def add_edge(self, src, dest, weight=1):
        if self.weighted:
            edge = (dest, weight)
        else:
            edge = dest

        self.adjacency_list[src].append(edge)

        if not self.directed:  # For undirected graphs, add the reverse edge
            reverse_edge = (src, weight) if self.weighted else src
            self.adjacency_list[dest].append(reverse_edge)

    def remove_node(self, node):
        if node in self.adjacency_list:
            del self.adjacency_list[node]
            for edges in self.adjacency_list.values():
                edges[:] = [edge for edge in edges if edge != node and (isinstance(edge, tuple) and edge[0] != node)]

    def remove_edge(self, src, dest):
        self.adjacency_list[src] = [
            edge for edge in self.adjacency_list[src] if edge != dest and (isinstance(edge, tuple) and edge[0] != dest)
        ]
        if not self.directed:
            self.adjacency_list[dest] = [
                edge for edge in self.adjacency_list[dest] if
                edge != src and (isinstance(edge, tuple) and edge[0] != src)
            ]

    def get_neighbors(self, node):
        return self.adjacency_list.get(node, [])

    def display(self):
        for node, edges in self.adjacency_list.items():
            print(f"{node} -> {edges}")