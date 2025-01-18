import heapq # For priority queue operations (used in Dijkstra's algorithm)
from basic import get_matrix # Import the `get_matrix` function for reading matrices from a file
from graph import Graph
from itertools import combinations
import random

class F1(Graph):
    def __init__(self, graph):
        self.directed = graph.directed
        self.weighted = graph.weighted
        self.graph = graph.graph

        # Initialize the lists for important nodes
        self.deployment_sites = graph.deployment_sites
        self.shelter = graph.shelter
        self.collection_points = graph.collection_points

        self.staging_area =  graph.staging_area

    def basic_network(self):
        # Create a new graph with only important nodes
        important_nodes = [
            node for node in self.graph
            if self.graph[node]['type_of_node'] in ['s', 'r', 'h', 'g'] or node in self.deployment_sites  or node in self.shelter or node in self.collection_points # Add all important nodes
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