import random
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


def chromatic_bounds(graph):
    graph.chromatic_number_upper = max(graph.degree(), key=lambda x: x[1])[1] + 1

    if len(graph) == 1:
        graph.chromatic_number_lower = 1
    elif nx.is_bipartite(graph):
        graph.chromatic_number_lower = 2
    else:
        graph.chromatic_number_lower = 3


def draw_result(graph, colormap):
    nx.draw(graph, node_color=colormap)
    plt.show()


def init_individual(genotype, graph):
    color_range = random.randint(graph.chromatic_number_lower, graph.chromatic_number_upper)

    coloring = [random.randint(0, color_range - 1) for _ in range(len(graph))]
    return genotype(coloring)


def init_individual_heuristic(genotype, graph):
    colormap = nx.greedy_color(graph, 'largest_first')
    result = genotype()

    for node in graph.nodes:
        result.append(colormap[node])

    return result


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


def mutation_point_repaint(graph, genotype):
    """Change color of randomly chosen node to randomly picked color"""
    mutated_node_ind = random.randint(0, len(graph) - 1)

    genotype[mutated_node_ind] = random.randint(0, graph.chromatic_number_upper - 1)
    return genotype,


def mutation_color_merge(graph, genotype):
    """Merge two randomly chosen colors into one color"""
    x = random.choice(genotype)
    y = random.choice(genotype)

    for i in range(len(genotype)):
        if genotype[i] == x:
            genotype[i] = y

    return genotype,


def mutation_change_conflicting(graph, genotype):
    colormap = dict(zip(graph.nodes, genotype))
    color_range = random.randint(graph.chromatic_number_lower, graph.chromatic_number_upper)

    conflicting = set()
    for node in graph.nodes():
        for neighbour in graph.neighbors(node):
            if colormap[node] == colormap[neighbour]:
                conflicting.add(node)
                conflicting.add(neighbour)

    for i, node in enumerate(graph.nodes):
        if node in conflicting:
            genotype[i] = random.randint(0, color_range - 1)

    return genotype,


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


def gpx(parent1, parent2):
    """Greedy partition crossover"""
    return gpx_helper(parent1, parent2), gpx_helper(parent2, parent1)


def ea_color(graph, selection=(tools.selTournament, {"tournsize": 3}), crossover=gpx, mutation=mutation_point_repaint,
             popsize=100, cxpb=0.25, mutpb=0.2, ngen=1000, visualize=False, verbose=True):
    chromatic_bounds(graph)
    creator.create("Fitness", base.Fitness, weights=(-1.0,))
    creator.create("Individual", IndividualT, fitness=creator.Fitness, graph=None)

    toolbox = base.Toolbox()

    toolbox.register("individual", init_individual, creator.Individual, graph=graph)
    toolbox.register("mate", crossover)
    toolbox.register("mutate", mutation, graph)
    toolbox.register("select", selection[0], **(selection[1]))
    toolbox.register("evaluate", fitness, graph=graph)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    stats = tools.Statistics(key=lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    hof = tools.HallOfFame(1)

    algorithms.eaSimple(toolbox.population(n=popsize), toolbox, cxpb=cxpb, mutpb=mutpb, ngen=ngen,
                        stats=stats, verbose=verbose, halloffame=hof)
    if visualize:
        draw_result(graph, hof)

    return hof
