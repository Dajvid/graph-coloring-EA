import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

from optimizer import ea_color, init_individual, gpx, mutation_point_repaint, mutation_color_merge


default_kwargs = {
    "initializer": init_individual,
    "crossover": gpx,
    "mutation": mutation_point_repaint,
    "popsize": 100,
    "cxpb": 0.25,
    "mutpb": 0.2,
    "ngen": 200,
    "visualize": False,
    "verbose": False
}


# crossover, mutace
# popsize, cxpb, mutpb, inciializace
def benchmark_popsize(kwargs, output_path= "o.txt", popsizes=[10, 100, 1000, 10000],
                      iters=[10000, 1000, 100, 10], evaluations=100, visualize=False):
    kwargs = kwargs.copy()
    #results = [np.zeros(evaluations) for _ in range(len(popsizes))]
    results = np.zeros((evaluations, len(popsizes)))
    for i, (popsize, it) in enumerate(zip(popsizes, iters)):
        kwargs["popsize"] = popsize
        kwargs["ngen"] = it
        for j in range(evaluations):
            print(f"Population size benchmark {i * evaluations + j + 1} / {evaluations * len(popsizes)}.")
            results[i][j] = ea_color(**kwargs)[0].fitness.values[0]
    if visualize:
        plt.boxplot(results, labels=popsizes, notch=False)
        plt.show()
    np.savetxt(output_path, results)


def benchmark_param(kwargs,  name, values, value_labels, evaluations=10, visualize=False, output_path="o.txt"):
    kwargs = kwargs.copy()
    # results = [np.zeros(evaluations) for _ in range(len(values))]
    results = np.zeros((evaluations, len(values)))
    for i, value in enumerate(values):
        kwargs[name] = value
        for j in range(evaluations):
            print(f"Param benchmark {i * evaluations + j + 1} / {evaluations * len(values)}.")
            results[j][i] = ea_color(**kwargs)[0].fitness.values[0]
    if visualize:
        plt.boxplot(results, labels=value_labels, notch=False)
        plt.show()

    np.savetxt(output_path, results)


if __name__ == '__main__':
    # input_graph = "graphs/DSJR500.1.graphml"
    input_graph = "graphs/DSJC125.1.graphml"

    g = nx.read_graphml(input_graph)
    default_kwargs["graph"] = g
    benchmark_param(default_kwargs, "mutation", [mutation_point_repaint, mutation_color_merge],
                    ["repaint", "merge"], visualize=True)
