from cpp.graph import Graph

def test_get_odd_nodes(test_graph: Graph):
    assert test_graph.get_odd_nodes() == [1, 2, 3, 4]
    
def test_get_even_nodes(test_graph):
    assert test_graph.get_even_nodes() == [0, 5]