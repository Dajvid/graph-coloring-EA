import argparse
import random
import sys

import matplotlib.pyplot as plt
import networkx as nx
from deap import creator, base, tools, algorithms


def parse_args(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i", "--input",
        default="graphs/example0.graphml",
        help="Path to input graph "
    )

    args = parser.parse_args(argv)
    return args


def draw(colormap, graph):
    nx.draw(graph, node_color=colormap)


def init_individual(genotype, graph):
    color_range = random.randint(graph.chromatic_number_lower, graph.chromatic_number_upper)

    coloring = [random.randint(0, color_range - 1) for _ in range(len(graph))]
    # coloring = random.sample(range(color_range), graph.number_of_nodes())
    return genotype(coloring)


def gen2colormap(genotype, graph):
    return dict(zip(graph.nodes, genotype))


def fitness(genotype, graph):
    colormap = gen2colormap(genotype, graph)
    color_count = len(set(genotype))
    conflict_amplification_constant = 5

    conflict_count = 0
    for node in graph.nodes():
        for neighbour in graph.neighbors(node):
            if colormap[node] == colormap[neighbour]:
                conflict_count += 1

    return conflict_count * conflict_amplification_constant + color_count,


def mutation(graph, genotype):
    mutated_node_ind = random.randint(0, len(graph) - 1)

    genotype[mutated_node_ind] = random.randint(0, graph.chromatic_number_upper - 1)
    return genotype,


def main(argv=None):
    args = parse_args(argv)
    graph = nx.read_graphml(args.input)

    seed = random.randrange(sys.maxsize)
    random.seed(seed)
    print(f"Seed: {seed}")

    graph.chromatic_number_lower = max(graph.degree(), key=lambda x: x[1])[1]
    graph.chromatic_number_upper = max(graph.degree(), key=lambda x: x[1])[1] + 1

    creator.create("Fitness", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.Fitness, graph=None)

    toolbox = base.Toolbox()
    toolbox.register("individual", init_individual, creator.Individual, graph=graph)

    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", mutation, graph)
    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("evaluate", fitness, graph=graph)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    top = None
    a = algorithms.eaSimple(toolbox.population(n=100), toolbox, cxpb=0.5, mutpb=0.2, ngen=50, halloffame=top)
    print("===")
    print(top)
    draw(a[0][0], graph)
    plt.show()


if __name__ == '__main__':
    main()
