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


if __name__ == "__main__":
    main()
