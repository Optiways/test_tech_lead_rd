import itertools
import logging
from typing import List, Tuple
from cpp.graph import Graph
import networkx as nx


logger = logging.getLogger("algo")


def _flatten_circuit_edge(edge: dict):
    origin = edge[0]
    destination = edge[1]
    weight = edge[3]["weight"]
    if "subpath" in edge[3]:
        subpath: List = edge[3]["subpath"]
        if origin == subpath[-1]:
            subpath.reverse()
        subpath = [(subpath[i], subpath[i + 1]) for i in range(len(subpath) - 1)]
    else:
        subpath = [(origin, destination)]
    return subpath, weight


def _create_eulerian_circuit(graph_augmented, graph_original, start_node=None):
    """
    networkx.eulerian_circuit only returns the order in which we hit each node.  It does not return the attributes of the
    edges needed to complete the circuit.  This is necessary for the postman problem where we need to keep track of which
    edges have been covered already when multiple edges exist between two nodes.
    We also need to annotate the edges added to make the eulerian to follow the actual shortest path trails (not
    the direct shortest path pairings between the odd nodes for which there might not be a direct trail)

    Args:
        graph_augmented (networkx graph): graph w links between odd degree nodes created from `add_augmenting_path_to_graph`.
        graph_original (networkx graph): orginal graph
        start_node (str): name of starting (and ending) node for CPP solution.

    Returns:
        networkx graph (`graph_original`) augmented with edges directly between the odd nodes
    """

    euler_circuit = list(
        nx.eulerian_circuit(graph_augmented, source=start_node, keys=True)
    )
    assert len(graph_augmented.edges()) == len(
        euler_circuit
    ), "graph and euler_circuit do not have equal number of edges."

    for edge in euler_circuit:
        aug_path = nx.shortest_path(graph_original, edge[0], edge[1], weight="weight")
        edge_attr = graph_augmented[edge[0]][edge[1]][edge[2]]
        if not edge_attr.get("augmented"):
            yield edge + (edge_attr,)
        else:
            for edge_aug in list(zip(aug_path[:-1], aug_path[1:])):
                # find edge with shortest distance (if there are two parallel edges between the same nodes)
                edge_aug_dict = graph_original[edge_aug[0]][edge_aug[1]]
                edge_key = min(
                    edge_aug_dict.keys(), key=(lambda k: edge_aug_dict[k]["weight"])
                )  # index with min distance
                edge_aug_shortest = edge_aug_dict[edge_key]
                edge_aug_shortest["augmented"] = True
                edge_aug_shortest["id"] = edge_aug_dict[edge_key]["id"]
                yield edge_aug + (
                    edge_key,
                    edge_aug_shortest,
                )


def _add_augmenting_path_to_graph(graph, min_weight_pairs):
    """
    Add the min weight matching edges to the original graph
    Note the resulting graph could (and likely will) have edges that didn't exist on the original graph.  To get the
    true circuit, we must breakdown these augmented edges into the shortest path through the edges that do exist.  This
    is done with `create_eulerian_circuit`.

    Args:
        graph (networkx graph):
        min_weight_pairs (list[2tuples): output of `dedupe_matching` specifying the odd degree nodes to link together

    Returns:
        networkx graph: `graph` augmented with edges between the odd nodes specified in `min_weight_pairs`
    """
    graph_aug = graph.copy()
    for pair in min_weight_pairs:
        shortest_path = nx.shortest_path(
            graph, pair[0], pair[1], weight="weight"
        )  # TODO: already computed earlier. Should be memoized somewhere to avoid some computation
        shortest_path_weight = nx.path_weight(graph, shortest_path, weight="weight")
        graph_aug.add_edge(
            pair[0],
            pair[1],
            weight=shortest_path_weight,
            subpath=shortest_path,
        )
    return graph_aug


def _create_complete_graph(pair_weights) -> nx.Graph:
    """
    Create a fully connected graph from a list of node pairs and the distances between them.

    Args:
        pair_weights (dict): mapping between node pairs and distance calculated in `get_shortest_paths_distances`.

    Returns:
        complete networkx graph using the node pairs and distances provided in `pair_weights`
    """
    g = nx.Graph()
    for k, v in pair_weights.items():
        g.add_edge(k[0], k[1], weight=v)
    return g


def _get_shortest_paths_distances(graph: Graph, pairs: List[Tuple[int]]):
    """
    Compute shortest distance between each pair of nodes in a graph

    Args:
        graph (Graph)
        pairs (list[2tuple]): List of length 2 tuples containing node pairs to calculate shortest path between

    Returns:
        dict: mapping of each pair in `pairs` to the shortest path.
    """
    print("get_shortest_paths_distances")
    distances = {}
    for pair in pairs:
        distances[pair] = nx.shortest_path_length(
            graph, pair[0], pair[1], weight="weight"
        )
    return distances


def chinese_postman(graph: Graph, start_node: int = 0) -> Tuple[list[int], float]:
    """Will compute the minimum weight path that gets through all edged of a positively weighted graph.

    Args:
        graph (Graph): the input graph from which we want the minimal path
        start_node (int, optional): the starting node id. Defaults to 0.

    Returns:
        Tuple[list[int], float]: list of nodes travelled, total sum of trip
    """
    print("Starting chinese postman problem search")
    if nx.is_eulerian(graph.nxgraph):
        path = list(nx.eulerian_circuit(graph.nxgraph))
        weight = nx.path_weight(graph.nxgraph, [u for u, _ in path] + [path[0][0]], weight="weight")
        return path, weight
    odd_nodes = graph.get_odd_nodes()
    odd_node_pairs = list(itertools.combinations(odd_nodes, 2))
    logger.info("get augmenting path for odd nodes")
    print("get augmenting path for odd nodes")
    odd_node_pairs_shortest_paths = _get_shortest_paths_distances(
        graph.nxgraph, odd_node_pairs
    )
    g_odd_complete = _create_complete_graph(odd_node_pairs_shortest_paths)

    print("Find min weight matching")
    odd_matching = nx.algorithms.min_weight_matching(g_odd_complete)

    print("add the min weight matching edges to g")
    graph_aug = _add_augmenting_path_to_graph(graph.nxgraph, odd_matching)

    print("get eulerian circuit route")
    circuit = _create_eulerian_circuit(graph_aug, graph.nxgraph, start_node)
    result = []
    total_weight = 0
    for edge in circuit:
        subpath, weight = _flatten_circuit_edge(edge)
        result.extend(subpath)
        total_weight += weight

    return result, total_weight
