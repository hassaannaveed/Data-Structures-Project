import networkx as nx
from collections import deque
import heapq
from itertools import combinations
from basic import get_matrix  # Importing a custom function for reading matrix from a file
from graph import Graph


class F5(Graph):
    def __init__(self, graph):
        self.directed = graph.directed
        self.weighted = graph.weighted
        self.graph = graph.graph

        # Initialize the lists for important nodes
        self.deployment_sites = graph.deployment_sites
        self.shelter = graph.shelter
        self.collection_points = graph.collection_points
        self.staging_area = graph.staging_area


class F5Deployment:
    def __init__(self, f5_graph: F5):
        self.f5_graph = f5_graph  # The graph structure is now based on the F5 class
        self.teams = {}
        self.sites = {}
        self.disaster_types = {
            'flood': {'pump', 'boat', 'divers'},
            'forest fire': {'chainsaw', 'firetruck', 'water hose'},
            'earthquake': {'crane', 'medical kit', 'rescue dogs'}
        }
        self.priority = []

    # Get user input for the number of teams, their capacities, skills, and the required units, skills, and priority for each site
    def get_user_input(self):
        print("Available skills:", ", ".join(sorted(set(skill for skills in self.disaster_types.values() for skill in skills))))

        num_teams = int(input("Enter the number of emergency rescue teams: "))
        for i in range(num_teams):
            capacity = int(input(f"Enter the capacity of Team {i + 1} (number of units they can deploy): "))
            skills = input(f"Enter the skills of Team {i + 1} (comma-separated, e.g., chainsaw, pump): ").split(',')
            self.teams[f'Team_{i + 1}'] = {'capacity': capacity, 'skills': set(skills)}

        num_sites = len(self.f5_graph.deployment_sites)
        for j, site in enumerate(self.f5_graph.deployment_sites, start=1):
            required_units = int(input(f"Enter the required number of units for Site {site} (Site {j}): "))
            disaster_type = input(f"Enter the type of disaster for Site {site} (e.g., flood, forest fire, earthquake): ").strip().lower()
            priority = int(input(f"Enter the priority for Site {site} (lower number = higher priority): "))
            if disaster_type not in self.disaster_types:
                print(f"Invalid disaster type. Available options: {', '.join(self.disaster_types.keys())}")
                return
            self.sites[site] = {'required_units': required_units, 'required_skills': self.disaster_types[disaster_type], 'priority': priority}

        self.priority = sorted(self.sites.keys(), key=lambda site: self.sites[site]['priority'])

    # Create a flow network based on the user input
    def create_flow_graph(self):
        # Use the F5 graph structure to create a flow network
        self.f5_graph.graph.add_node("source")
        self.f5_graph.graph.add_node("sink")

        for team, team_data in self.teams.items():
            self.f5_graph.graph.add_edge("source", team, capacity=team_data['capacity'])

        for site, site_data in self.sites.items():
            self.f5_graph.graph.add_edge(site, "sink", capacity=site_data['required_units'])

            for team, team_data in self.teams.items():
                if team_data['skills'] & site_data['required_skills']:
                    self.f5_graph.graph.add_edge(team, site, capacity=min(team_data['capacity'], site_data['required_units']))

    # Implement the Ford-Fulkerson algorithm to find the maximum flow in the flow network
    def ford_fulkerson(self, source, sink):
        residual_graph = {edge: self.f5_graph.graph.edges[edge]['capacity'] for edge in self.f5_graph.graph.edges}
        max_flow = 0

        def bfs_find_path():
            visited = set()
            queue = deque([(source, [])])
            while queue:
                current_node, path = queue.popleft()
                if current_node == sink:
                    return path

                for neighbor in self.f5_graph.graph.neighbors(current_node):
                    if neighbor not in visited and residual_graph.get((current_node, neighbor), 0) > 0:
                        visited.add(neighbor)
                        queue.append((neighbor, path + [(current_node, neighbor)]))

            return None

        while True:
            path = bfs_find_path()
            if not path:
                break

            bottleneck = min(residual_graph[edge] for edge in path)
            for u, v in path:
                residual_graph[(u, v)] -= bottleneck
                residual_graph[(v, u)] = residual_graph.get((v, u), 0) + bottleneck

            max_flow += bottleneck

        return max_flow

    # Assign teams to sites based on the maximum flow in the flow network
    def assign_teams_to_sites(self):
        self.create_flow_graph()
        max_flow = self.ford_fulkerson("source", "sink")
        print(f"\nMaximum units deployed: {max_flow}")

        assigned_teams = set()
        for site in self.priority:
            site_data = self.sites[site]
            required_units = site_data['required_units']

            for team, team_data in self.teams.items():
                if team in assigned_teams:
                    continue

                if required_units > 0 and team_data['capacity'] > 0:
                    if team_data['skills'] & site_data['required_skills']:
                        deployed_units = min(team_data['capacity'], required_units)
                        team_data['capacity'] -= deployed_units
                        required_units -= deployed_units

                        print(f"{deployed_units} units from {team} deployed to {site}")

                        if team_data['capacity'] == 0:
                            assigned_teams.add(team)

                        if required_units == 0:
                            break

            if required_units > 0:
                print(f"Error: Not enough personnel to fully handle {site}. {required_units} units still needed. Help is on its way.")

    # Display the deployment summary
    def display(self):
        print("\n--- Deployment Summary ---")
        print("Teams and their remaining capacities:")
        for team, data in self.teams.items():
            print(f"{team}: {data['capacity']} units left")

        print("\nSites and their statuses:")
        for site, data in self.sites.items():
            print(f"Site {site}: {data['required_units']} units still needed, priority {data['priority']}")

        print("\nGraph details:")
        print("Nodes:", self.f5_graph.graph.nodes())
        print("Edges and capacities:")
        for u, v, capacity in self.f5_graph.graph.edges(data='capacity'):
            print(f"{u} -> {v}: {capacity}")

    def run(self):
        self.get_user_input()
        self.assign_teams_to_sites()
        self.display()
