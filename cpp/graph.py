from __future__ import annotations
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import sys
import networkx as nx


class Graph:
    def __init__(self, vertices: list[tuple], edges: list[tuple]):
        """
        Parameters
        ----------
        vertices : list[tuple]
            list of vertices coordinates.
        edges : list[tuple]
            list of edges as tuple (id 1, id 2, weight, coordinates 1, coordinates 2).
        """
        self.vertices = vertices
        self.edges = edges

        g = nx.MultiGraph()
        for edge in enumerate(self.edges):
            g.add_edge(edge[1][0], edge[1][1], weight=edge[1][2])
        self.nxgraph = g

    def plot(self):
        """
        Plot the graph.
        """
        weights = list(set(edge[2] for edge in self.edges))
        colors = plt.cm.get_cmap("viridis", len(weights))
        _, ax = plt.subplots()
        for i, weight in enumerate(weights):
            lines = [
                [edge[-2][::-1], edge[-1][::-1]]
                for edge in self.edges
                if edge[2] == weight
            ]
            ax.add_collection(
                LineCollection(
                    lines, colors=colors(i), alpha=0.7, label=f"weight {weight}"
                )
            )
        ax.plot()
        ax.legend()
        plt.title(f"#E={len(self.edges)}, #V={len(self.vertices)}")
        plt.show()
        plt.savefig(sys.stdout.buffer)

    def _get_even_or_odd_nodes(self, mod):
        """
        Helper function for get_even_nodes. Return names of the odd or even nodes
        Args:
            mod (int): 0 for even, 1 for odd

        Returns:
            list[str]: list of node names of odd or even degree
        """
        degree_nodes = []
        for v, d in self.nxgraph.degree():
            if d % 2 == mod:
                degree_nodes.append(v)
        return degree_nodes

    def get_odd_nodes(self):
        """
        Return nodes whose degree is odd.

        Returns:
            list[str]: names of nodes with odd degree
        """
        return self._get_even_or_odd_nodes(1)

    def get_even_nodes(self):
        """
        Return nodes whose degree is even.

        Returns:
            list[str]: names of nodes with even degree

        """
        return self._get_even_or_odd_nodes(0)
