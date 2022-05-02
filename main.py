import argparse
import random
import sys

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from deap import creator, base, tools, algorithms


class IndividualT(list):

    def color_sets(self):
        colors = set(self)
        result = {color: set() for color in colors}

        for i in range(len(self)):
            result[self[i]].add(i)

        return result


class GraphColorer:
    """TODO"""

    def __init__(self, graph):
        self.graph = graph
        self.chromatic_bounds()
        self.result = None
        self.toolbox = None

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
        return genotype(coloring)

    @staticmethod
    def fitness(genotype, graph):
        colormap = dict(zip(graph.nodes, genotype))
        color_count = len(set(genotype))
        conflict_amplification_constant = 100

        conflict_count = 0
        for node in graph.nodes():
            for neighbour in graph.neighbors(node):
                if colormap[node] == colormap[neighbour]:
                    conflict_count += 1

        return conflict_count * conflict_amplification_constant + color_count,

    @staticmethod
    def mutation_point_repaint(graph, genotype):
        """Change color of randomly chosen node to randomly picked color"""
        mutated_node_ind = random.randint(0, len(graph) - 1)

        genotype[mutated_node_ind] = random.randint(0, graph.chromatic_number_upper - 1)
        return genotype,

    @staticmethod
    def mutation_color_merge(graph, genotype):
        """Merge two randomly chosen colors into one color"""
        x = random.choice(genotype)
        y = random.choice(genotype)

        for i in range(len(genotype)):
            if genotype[i] == x:
                genotype[i] = y

        return genotype,

    @staticmethod
    def gpx_helper(parent1, parent2):
        parents = [parent1, parent2]
        parent_sets = [parent1.color_sets(), parent2.color_sets()]
        # p1_max = max(parent1_color_sets.values, key=len)
        child = [None] * len(parent1)

        # a = [max(parent_set.values(), key=len) for parent_set in parent_sets]
        # class_index = 0 if len(a[0]) > len(a[1]) else 1
        class_index = 0
        while child.count(None) == 0:
            vertices = max(parent_sets[class_index], key=len)
            color = parents[vertices[0]]

            # save color class in the child
            for vertex in vertices:
                child[vertex] = color
                # delete used vertices from the other parent set
                parent_sets[(class_index + 1) % 2][parents[(class_index + 1) % 2][vertex]].remove(vertex)

            # And finally delete the whole used color class from current parent
            parent_sets[class_index].pop(color)

            class_index = (class_index + 1) % 2

        return creator.Individual(child)

    @staticmethod
    def gpx(parent1, parent2):
        """Greedy partition crossover"""
        return GraphColorer.gpx_helper(parent1, parent2), GraphColorer.gpx_helper(parent2, parent1)

    # TODO another smart crossover

    def ea_color(self, popsize=100, cxpb=0.25, mutpb=0.2, ngen=1000):
        creator.create("Fitness", base.Fitness, weights=(-1.0,))
        creator.create("Individual", IndividualT, fitness=creator.Fitness, graph=None)

        self.toolbox = base.Toolbox()
        self.toolbox.register("individual", GraphColorer.init_individual, creator.Individual, graph=self.graph)
        # self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("mutate", GraphColorer.mutation_point_repaint, self.graph)
        self.toolbox.register("select", tools.selTournament, tournsize=3)
        self.toolbox.register("evaluate", GraphColorer.fitness, graph=self.graph)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        self.toolbox.register("mate", GraphColorer.gpx)

        stats = tools.Statistics(key=lambda ind: ind.fitness.values)
        stats.register("avg", np.mean)
        stats.register("std", np.std)
        stats.register("min", np.min)
        stats.register("max", np.max)

        hof = tools.HallOfFame(1)

        algorithms.eaSimple(self.toolbox.population(n=popsize), self.toolbox, cxpb=cxpb, mutpb=mutpb, ngen=ngen,
                            stats=stats, verbose=True, halloffame=hof)

        self.result = hof
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
