import argparse
import random
import sys
import networkx as nx

from optimizer import ea_color, mutation_change_conflicting, mutation_point_repaint


def parse_args(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i", "--input",
        default="graphs/DSJC125.1.graphml",
        help="Path to input graph "
    )

    args = parser.parse_args(argv)
    return args


def main(argv=None):
    args = parse_args(argv)
    graph = nx.read_graphml(args.input)

    seed = random.randrange(sys.maxsize)
    random.seed(seed)
    print(f"Seed: {seed}")

    ea_color(graph, mutation=mutation_change_conflicting, visualize=True)


if __name__ == '__main__':
    main()
