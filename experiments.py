import networkx as nx

from optimizer import ea_color


def benchmark_param(graph, name, values):
    for value in values:
        ea_color(graph, *(name, value))
# inciializace, crossover, mutace
# popsize, cxpb, mutpb


if __name__ == '__main__':
    input_graph = "graphs/example0.graphml"

    colorer = GraphColorer(nx.read_graphml(input_graph))
    colorer.ea_color()
