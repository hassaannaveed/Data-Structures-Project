import heapq # For priority queue operations (used in Dijkstra's algorithm)
from basic import get_matrix # Import the `get_matrix` function for reading matrices from a file
from graph import Graph
from itertools import combinations
import random

class F4(Graph):
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

    def optimal_supply_points(self, current_supply_points, k):

        all_nodes = list(self.graph.keys())  # Get all nodes in the graph
        candidate_nodes = [node for node in all_nodes if node not in current_supply_points]

        if len(candidate_nodes) < k:
            print("Not enough nodes to place additional supply points.")
            return None

        # Initialize k random medoids
        medoids = random.sample(candidate_nodes, k)

        def calculate_cost(medoids):
            """Calculate the average distance cost of nodes to the nearest medoid."""
            total_distance = 0
            for node in all_nodes:
                if node in medoids or node in current_supply_points:
                    continue
                min_distance = float('inf')
                for medoid in medoids + current_supply_points:
                    result = self.djikstra(node, medoid)
                    if result:
                        distance, _ = result
                        min_distance = min(min_distance, distance)
                total_distance += min_distance
            return total_distance / len(all_nodes)

        # Iterative medoids optimization
        best_medoids = medoids[:]
        best_cost = calculate_cost(best_medoids)
        improvement = True

        while improvement:
            improvement = False
            for medoid in best_medoids:
                for candidate in candidate_nodes:
                    if candidate in best_medoids:
                        continue
                    new_medoids = best_medoids[:]
                    new_medoids.remove(medoid)
                    new_medoids.append(candidate)
                    new_cost = calculate_cost(new_medoids)
                    if new_cost < best_cost:
                        best_cost = new_cost
                        best_medoids = new_medoids
                        improvement = True

        print(f"Optimal supply points: {best_medoids}")
        print(f"Average distance cost: {best_cost}")
        return best_medoids