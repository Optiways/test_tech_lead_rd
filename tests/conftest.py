
import pytest

from cpp.graph import Graph

@pytest.fixture(scope="function")
def test_graph():
    vertices = [(0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0)]
    edges =[(0, 1, 1), (0, 2, 2), (1, 2, 5), (1, 3, 3), (2, 4, 4), (3, 4, 6), (3, 5, 1), (4, 5, 1)]
    return Graph(vertices=vertices, edges=edges)

