import heapq # For priority queue operations (used in Dijkstra's algorithm)
from basic import get_matrix # Import the `get_matrix` function for reading matrices from a file
from graph import Graph
from itertools import combinations
import random

class F2(Graph):
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