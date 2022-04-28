import argparse
import networkx as nx
import matplotlib.pyplot as plt


def parse_args(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i", "--input",
        help="Path to input graph"
    )

    parser.add_argument(
        "-o", "--output",
        help="Name for the output file"
    )

    args = parser.parse_args(argv)
    return args


def main(argv=None):
    args = parse_args(argv)
    edges = []
    num_vertices = 0
    num_edges = 0

    with open(args.input, "r") as f:
        for line in f:
            splitted = line.split()
            if splitted[0] == 'e':
                edges.append((int(splitted[1]), int(splitted[2])))
            elif splitted[0] == 'c':
                pass
            elif splitted[0] == 'p':
                if splitted[1] != "edge":
                    raise SyntaxError(f"Unknown problem type {splitted[1]}")
                num_vertices = int(splitted[2])
                num_edges = int(splitted[3])
            else:
                raise SyntaxError(f"Unknown line type {splitted[0]}")

    g = nx.Graph(edges)
    # TODO compare expected and actual vertex/node count...
    nx.draw(g)
    nx.write_graphml(g, args.output)
    plt.show()


if __name__ == '__main__':
    main()