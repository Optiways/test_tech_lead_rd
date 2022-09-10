from graph import Graph
from test_tech_lead_rd.core.path_functions import (
    construct_vertices_dict,
    get_optimal_goal,
    get_shortest_path
)


class Path():
    def __init__(self, starting_vertice: tuple, edges: list[tuple],):
        """
        Parameters
        ----------
        starting_vertice : tuple
            vertice coordinates where the path begin
        edges : list[tuple]
            list of edges as tuple (edge order, id 1, id 2)
        """
        self.starting_vertice = starting_vertice
        self.edges = edges

    def get_path(self, starting_vertice: tuple, graph: Graph):
        self.starting_vertice = starting_vertice
        vertices_dict = construct_vertices_dict(graph.edges)
        remaining_edges = self.edges
        current_vertice = starting_vertice
        path = []
        while remaining_edges:
            optimal_goal = get_optimal_goal()
            path += get_shortest_path(current_vertice, optimal_goal, vertices_dict)
            for edge in path:
                remaining_edges.remove(edge)
        return path
