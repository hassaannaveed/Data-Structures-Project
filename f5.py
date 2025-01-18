import heapq # For priority queue operations (used in Dijkstra's algorithm)
from basic import get_matrix # Import the `get_matrix` function for reading matrices from a file
from graph import Graph
from itertools import combinations
import random

class F5(Graph):
    def __init__(self, graph):
        self.directed = graph.directed
        self.weighted = graph.weighted
        self.graph = graph.graph

        # Initialize the lists for important nodes
        self.deployment_sites = graph.deployment_sites
        self.shelter = graph.shelter
        self.collection_points = graph.collection_points

        self.staging_area =  graph.staging_area

    def add_squad_to_staging_area(self, squad_name, skills, resources, members):
        """
        Adds a squad with specific skills/resources to the staging area.
        """
        self.staging_area[squad_name] = {
            'skills': skills,
            'resources': resources,
            'members': members
        }


    def remove_squad_from_staging_area(self, squad_name):
        """
        Removes a squad from the staging area.
        """
        if squad_name in self.staging_area:
            del self.staging_area[squad_name]

    def deploy_emergency_services(self, deployment_sites):
        """
        Deploys emergency services personnel from the staging area to deployment sites.

        Args:
            deployment_sites (dict): A dictionary where keys are deployment site names,
                                     and values are sets of required skills/resources.

        Returns:
            dict: A mapping of deployment sites to assigned squads.
        """
        # Add staging area squads as temporary nodes
        for squad, squad_info in self.staging_area.items():
            self.add_node(squad)  # Add each squad as a node

        for site, requirements in deployment_sites.items():
            for squad, squad_info in self.staging_area.items():
                # Check if the squad satisfies the site's requirements
                squad_skills = squad_info.get('skills', set())
                squad_resources = squad_info.get('resources', set())
                squad_members = squad_info.get('members', 0)

                required_skills, required_resources = requirements
                if required_skills.issubset(squad_skills) and required_resources.issubset(squad_resources):
                    self.add_edge(squad, site)  # Add an edge if requirements are met

        # Add super source and super sink for max bipartite matching
        super_source, super_sink = self.add_super_source_sink()

        # Calculate maximum flow
        max_flow = self.edmonds_karp(super_source, super_sink)

        # Find the matching from the flow graph
        matching = {}
        for squad in self.staging_area.keys():
            for site, _, _ in self.get_connections(squad):
                if self.get_capacity(squad, site) == 0:  # Fully used edge
                    matching[site] = squad
                    break

        # Cleanup: Remove temporary nodes
        self.remove_node(super_source)
        self.remove_node(super_sink)
        for squad in self.staging_area.keys():
            self.remove_node(squad)

        # Output results
        print("Deployment Plan:")
        for site, squad in matching.items():
            print(f"Deployment Site {site} <- Squad {squad}")
        print(f"Total squads deployed: {len(matching)}")
        print(f"Maximum flow (deployed squads): {max_flow}")

        return matching

    def add_deployment_site(self, site_name, required_skills, required_resources, required_people):
        """
        Adds a deployment site with specific requirements.

        Args:
            site_name (str): Name of the deployment site.
            required_skills (set): Set of skills required for the deployment site.
            required_resources (set): Set of resources required for the deployment site.
            required_people (int): Number of people needed for the deployment.
        """
        # Add deployment site as a node in the graph
        self.add_node(site_name)

        # Add required skills, resources, and number of people to this deployment site
        self.graph[site_name]['required_skills'] = required_skills
        self.graph[site_name]['required_resources'] = required_resources
        self.graph[site_name]['required_people'] = required_people
        self.graph[site_name]['assigned_squad'] = None  # This will store the squad assigned to this site

    def assign_squad_to_deployment(self, site_name, squad_name):
        """
        Assigns a squad from the staging area to the deployment site.

        Args:
            site_name (str): The deployment site to which the squad is assigned.
            squad_name (str): The squad name to assign to the site.
        """
        # Check if the squad has the required skills and resources
        squad = self.staging_area.get(squad_name)

        if not squad:
            print(f"Squad {squad_name} not found in staging area.")
            return

        squad_skills = squad.get("skills", set())
        squad_resources = squad.get("resources", set())
        squad_members = squad.get("members", 0)

        # Check if squad meets the deployment site requirements
        deployment_site = self.graph.get(site_name)

        if not deployment_site:
            print(f"Deployment site {site_name} not found.")
            return

        required_skills = deployment_site.get("required_skills", set())
        required_resources = deployment_site.get("required_resources", set())
        required_people = deployment_site.get("required_people", 0)

        # Validate if squad has required skills, resources, and number of members
        if required_skills.issubset(squad_skills) and required_resources.issubset(
                squad_resources) and squad_members >= required_people:
            self.graph[site_name]['assigned_squad'] = squad_name
            print(f"Squad {squad_name} successfully assigned to {site_name}.")
        else:
            print(f"Squad {squad_name} does not meet the requirements for {site_name}.")
            if not required_skills.issubset(squad_skills):
                print(f"Missing skills: {required_skills - squad_skills}")
            if not required_resources.issubset(squad_resources):
                print(f"Missing resources: {required_resources - squad_resources}")
            if squad_members < required_people:
                print(f"Not enough people: Required {required_people}, but squad has {squad_members} members.")