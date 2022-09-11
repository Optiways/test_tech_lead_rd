import os
import re

import pytest
from cpp.algorithms import chinese_postman, _get_odd_nodes
from cpp.graph import Graph
from cpp.input import parse_file


def _load_graph_file(file):
    vertices, edges = parse_file(file)
    return Graph(vertices, edges)


def _load_expected_path_file(input_string):
    input_string = input_string.replace(" ", "")
    path_data = re.findall(r"(\d+,\d+)", input_string)
    path = [tuple(map(lambda x: int(x), item.split(","))) for item in path_data]
    weight_data = int(re.findall(r"(\d+)\)$", input_string)[0])
    return (path, weight_data)


testset = {}
for item in os.scandir("tests/fixtures/chinese_postman"):
    if item.is_dir():
        try:
            graph = _load_graph_file(os.path.join(item, "graph.txt"))
            with open(os.path.join(item, "expected.txt"), "r") as content:
                str_expected_output = content.readline()
            expected_output = _load_expected_path_file(str_expected_output)
            testset[str(item)] = (graph, expected_output)
        except:
            print(f"Could not load test graph {item}")
            raise


@pytest.mark.parametrize("test_case", testset.keys())
def test_chinese_postman(test_case):
    g, expected = testset[test_case]
    output = chinese_postman(g)
    assert output == [expected]


def test_get_odd_nodes(test_graph: Graph):
    assert _get_odd_nodes(test_graph.nxgraph) == [1, 2, 3, 4]
