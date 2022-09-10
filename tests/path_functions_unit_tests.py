from core.path_functions import get_shortest_path, construct_vertices_dict
import pytest


@pytest.mark.parametrize(
    (
        "starting_vertice",
        "goal_vertice",
        "graph",
        "expected"
    ),
    [
        (
            (0,0),
            (1,1),
            {
                (0,0): [((0,1), 2), ((1,0), 1)],
                (0,1): [((0,0), 2), ((1,1), 1)],
                (1,0): [((0,0), 1), ((1,1), 1)],
                (1,1): [((0,1), 1), ((1,0), 1)]
            },
            [(0,0), (1,0), (1,1)]
        ),
        (
            (0,0),
            (0,0),
            {
                (0,0): [((0,1), 2), ((1,0), 1)],
                (0,1): [((0,0), 2), ((1,1), 1)],
                (1,0): [((0,0), 1), ((1,1), 1)],
                (1,1): [((0,1), 1), ((1,0), 1)]
            },
            [(0,0)]
        ),
    ]
)
def test_get_shortest_path(starting_vertice, goal_vertice, graph, expected):
    assert get_shortest_path(starting_vertice, goal_vertice, graph) == expected

@pytest.mark.parametrize(
    (
        "edges",
        "expected"
    ),
    [
        (
            [
                ("A", "B", 1, (0,0), (0,1)),
                ("A", "C", 1, (0,0), (1,0)),
                ("B", "D", 1, (0,1), (1,1)),
                ("C", "D", 1, (1,0), (1,1)),
            ],
            {
                (0,0): [((0,1), 1), ((1,0), 1)],
                (0,1): [((0,0), 1), ((1,1), 1)],
                (1,0): [((0,0), 1), ((1,1), 1)],
                (1,1): [((0,1), 1), ((1,0), 1)],
            }
        )
    ]
)
def test_construct_vertice_dict(edges, expected):
    assert construct_vertices_dict(edges) == expected