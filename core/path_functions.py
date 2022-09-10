from typing import Dict, List, Tuple


def construct_vertices_dict(edges: list[tuple]) -> Dict[tuple, List]:
    """
    Parameters
    ----------
    edges : list[tuple]
        list of edges as tuple (coord 1, coord 2, weight)
    
    Returns
    -------
    tuple(str, bool)
        path to input graph file, whether to plot the graph.
    """
    vertice_dict = {}
    for edge in edges:
        if edge[3] in vertice_dict:
            vertice_dict[edge[3]].append((edge[4], edge[2]))
        else:
            vertice_dict[edge[3]] = [(edge[4], edge[2])]
        if edge[4] in vertice_dict:
            vertice_dict[edge[4]].append((edge[3], edge[2]))
        else:
            vertice_dict[edge[4]] = [(edge[3], edge[2])]
    return vertice_dict


def get_shortest_path(starting_vertice: tuple, goal_vertice: tuple, graph: Dict[tuple, List]) -> list:
    """
    Shortest path using Dijsktra method
    """
    shortest_paths = {starting_vertice: (None, 0)}
    current_vertice = starting_vertice
    visited = set()

    while current_vertice != goal_vertice:
        visited.add(current_vertice)
        neighbours = graph[current_vertice]
        weight_to_current_node = shortest_paths[current_vertice][1]

        for neighbour in neighbours:
            weight = neighbour[1] + weight_to_current_node
            if neighbour[0] not in shortest_paths:
                shortest_paths[neighbour[0]] = (current_vertice, weight)
            else:
                current_shortest_weight = shortest_paths[neighbour[0]][1]
                if current_shortest_weight > weight:
                    shortest_paths[neighbour[0]] = (current_vertice, weight)

        next_vertices = {vertice: shortest_paths[vertice] for vertice in shortest_paths if vertice not in visited}
        if not next_vertices:
            raise ValueError("No path possible")
        current_vertice = min(next_vertices, key=lambda k: next_vertices[k][1])
    
    path = []
    while current_vertice is not None:
        path.append(current_vertice)
        next_vertice = shortest_paths[current_vertice][0]
        current_vertice = next_vertice
    path = path[::-1]
    return path

def get_optimal_goal() -> Tuple:
    # TODO
    return ()
