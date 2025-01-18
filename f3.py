import heapq # For priority queue operations (used in Dijkstra's algorithm)
from basic import get_matrix # Import the `get_matrix` function for reading matrices from a file
from graph import Graph
from itertools import combinations
import random

class F3(Graph):
    def __init__(self, graph):
        self.directed = graph.directed
        self.weighted = graph.weighted
        self.graph = graph.graph

        # Initialize the lists for important nodes
        self.deployment_sites = graph.deployment_sites
        self.assembly_points = graph.assembly_points
        self.shelter = graph.shelter
        self.collection_points = graph.collection_points

        self.staging_area =  graph.staging_area

    def calculate_fastest_route(self, source, destination):

        if source not in self.graph or destination not in self.graph:
            print(f"One or both nodes ({source}, {destination}) do not exist.")
            return None

        # Priority queue for Dijkstra's algorithm
        pq = [(0, source)]  # (distance, current_node)
        distances = {node: float('inf') for node in self.graph}
        distances[source] = 0
        prev_nodes = {node: None for node in self.graph}

        while pq:
            current_distance, current_node = heapq.heappop(pq)

            # Skip if a better path has already been found
            if current_distance > distances[current_node]:
                continue

            # Explore neighbors
            for neighbor, weight, _ in self.graph[current_node]['connections']:
                if weight < 0:  # Skip impassable roads
                    continue

                new_distance = current_distance + weight

                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    prev_nodes[neighbor] = current_node
                    heapq.heappush(pq, (new_distance, neighbor))

        # Reconstruct the path
        path = []
        current_node = destination

        while current_node is not None:
            path.insert(0, current_node)
            current_node = prev_nodes[current_node]

        if distances[destination] == float('inf'):
            print(f"No path exists between {source} and {destination}.")
            return None

        return distances[destination], path