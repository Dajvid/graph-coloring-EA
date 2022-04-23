import argparse
import random
import sys

import matplotlib.pyplot as plt
import networkx as nx
from deap import creator, base, tools, algorithms


class GraphColorer:
    """TODO"""

    def __init__(self, graph):
        self.graph = graph
        self.chromatic_bounds()
        self.result = None

    def chromatic_bounds(self):
        self.graph.chromatic_number_upper = max(self.graph.degree(), key=lambda x: x[1])[1] + 1

        if len(self.graph) == 1:
            self.graph.chromatic_number_lower = 1
        elif nx.is_bipartite(self.graph):
            self.graph.chromatic_number_lower = 2
        else:
            self.graph.chromatic_number_lower = 3

    def draw_result(self):
        nx.draw(self.graph, node_color=self.result)
        plt.show()

    @staticmethod
    def init_individual(genotype, graph):
        color_range = random.randint(graph.chromatic_number_lower, graph.chromatic_number_upper)

        coloring = [random.randint(0, color_range - 1) for _ in range(len(graph))]
        # coloring = random.sample(range(color_range), graph.number_of_nodes())
        return genotype(coloring)

    @staticmethod
    def gen2colormap(genotype, graph):
        return dict(zip(graph.nodes, genotype))

    @staticmethod
    def fitness(genotype, graph):
        colormap = GraphColorer.gen2colormap(genotype, graph)
        color_count = len(set(genotype))
        conflict_amplification_constant = 5

        conflict_count = 0
        for node in graph.nodes():
            for neighbour in graph.neighbors(node):
                if colormap[node] == colormap[neighbour]:
                    conflict_count += 1

        return conflict_count * conflict_amplification_constant + color_count,

    @staticmethod
    def mutation(graph, genotype):
        mutated_node_ind = random.randint(0, len(graph) - 1)

        genotype[mutated_node_ind] = random.randint(0, graph.chromatic_number_upper - 1)
        return genotype,

    def ea_color(self):
        creator.create("Fitness", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.Fitness, graph=None)

        toolbox = base.Toolbox()
        toolbox.register("individual", GraphColorer.init_individual, creator.Individual, graph=self.graph)

        toolbox.register("mate", tools.cxTwoPoint)
        toolbox.register("mutate", GraphColorer.mutation, self.graph)
        toolbox.register("select", tools.selTournament, tournsize=3)
        toolbox.register("evaluate", GraphColorer.fitness, graph=self.graph)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)

        a = algorithms.eaSimple(toolbox.population(n=100), toolbox, cxpb=0.5, mutpb=0.2, ngen=50)
        print("===")
        self.result = a[0][0]
        self.draw_result()


def parse_args(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i", "--input",
        default="graphs/example0.graphml",
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
    colorer = GraphColorer(graph)
    colorer.ea_color()


if __name__ == '__main__':
    main()