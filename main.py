import logging
import sys
from cpp.algorithms import chinese_postman
from cpp.input import parse_cmd_line, parse_file
from cpp.graph import Graph

handler = logging.StreamHandler(sys.stdout)
root_logger = logging.getLogger()
root_logger.addHandler(handler)

def main():
    in_file, plot_graph = parse_cmd_line()
    vertices, edges = parse_file(in_file)
    print(f"#E={len(edges)}, #V={len(vertices)}")
    graph = Graph(vertices, edges)
    if plot_graph:
        graph.plot()
    result = chinese_postman(graph, 1)
    if len(result) > 1:
        for i, r in enumerate(result):
            print(f"Path #{i+1}/{len(result)} > {r}")
    else:
        print(result[0])


if __name__ == "__main__":
    main()
