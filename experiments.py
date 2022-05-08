import datetime
import os

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from deap import tools

from optimizer import ea_color, gpx, mutation_point_repaint, mutation_color_merge, mutation_change_conflicting

default_kwargs = {
    "crossover": gpx,
    "mutation": mutation_point_repaint,
    "popsize": 50,
    "cxpb": 0.25,
    "mutpb": 0.2,
    "ngen": 200,
    "visualize": False,
    "verbose": False
}


# crossover, mutace,
# popsize, cxpb, mutpb, selection
def benchmark_popsize(kwargs, output_path="o.txt", popsizes=[10, 20, 50, 100, 500, 1000, 5000],
                      evaluations=50, visualize=False):
    eval_count = 100000
    kwargs = kwargs.copy()
    results = np.zeros((evaluations, len(popsizes)))
    for i, popsize in enumerate(popsizes):
        kwargs["popsize"] = popsize
        kwargs["ngen"] = eval_count // popsize
        for j in range(evaluations):
            print(f"Population size benchmark {i * evaluations + j + 1} / {evaluations * len(popsizes)}.")
            results[j][i] = ea_color(**kwargs)[0].fitness.values[0]
    plt.figure()
    plt.boxplot(results, labels=popsizes, notch=False)
    plt.xlabel = "popuation size"
    plt.ylabel = "fitness"
    plt.savefig(output_path + ".svg")
    if visualize:
        plt.show()
    np.savetxt(output_path + ".out", results)
    with open(output_path + ".meta", "w+") as f:
        f.write(f"popsizes: {popsizes}")
        f.write(f"kwargs: {kwargs}")


def benchmark_param(kwargs,  name, values, evaluations=50, visualize=False, output_path="o.txt",
                    xlabel="variants", ylabel="values", labels=None):
    labels = labels if labels else values
    kwargs = kwargs.copy()
    results = np.zeros((evaluations, len(values)))
    for i, value in enumerate(values):
        kwargs[name] = value
        for j in range(evaluations):
            print(f"Param benchmark {i * evaluations + j + 1} / {evaluations * len(values)}.")
            results[j][i] = ea_color(**kwargs)[0].fitness.values[0]
    plt.figure()
    plt.boxplot(results, labels=labels, notch=False)
    plt.xlabel = xlabel
    plt.ylabel = ylabel
    plt.savefig(f"{output_path}-{name}.svg")
    if visualize:
        plt.show()

    np.savetxt(f"{output_path}-{name}.out", results)
    with open(output_path + ".meta", "w+") as f:
        f.write(f"{name}: {values}")
        f.write(f"kwargs: {kwargs}")


def experiment_onepoint_repaint(out):
    kwargs = default_kwargs.copy()
    kwargs.update({"crossover": tools.cxOnePoint,
                   "mutation": mutation_point_repaint})
    benchmark_popsize(kwargs, output_path=os.path.join(out, "onepoint-repaint-popsize"))
    benchmark_param(kwargs, output_path=os.path.join(out, "onepoint-repaint"), name="cxpb", values=[0.1, 0.2, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
    benchmark_param(kwargs, output_path=os.path.join(out, "onepoint-repaint"), name="mutpb", values=[0.1, 0.2, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])


def experiment_onepoint_merge(out):
    kwargs = default_kwargs.copy()
    kwargs.update({"crossover": tools.cxOnePoint,
                   "mutation": mutation_color_merge})
    benchmark_popsize(kwargs, os.path.join(out, "onepoint-merge-popsize"))
    benchmark_param(kwargs, output_path=os.path.join(out, "onepoint-merge"), name="cxpb", values=[0.1, 0.2, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
    benchmark_param(kwargs, output_path=os.path.join(out, "onepoint-merge"), name="mutpb", values=[0.1, 0.2, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])


def experiment_onepoint_conflicting(out):
    kwargs = default_kwargs.copy()
    kwargs.update({"crossover": tools.cxOnePoint,
                   "mutation": mutation_change_conflicting})
    benchmark_popsize(kwargs, os.path.join(out, "onepoint-conflicting-popsize"))
    benchmark_param(kwargs, output_path=os.path.join(out, "onepoint-conflicting"), name="cxpb", values=[0.1, 0.2, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
    benchmark_param(kwargs, output_path=os.path.join(out, "onepoint-conflicting"), name="mutpb", values=[0.1, 0.2, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])


def experiment_gpx_repaint(out):
    kwargs = default_kwargs.copy()
    kwargs.update({"crossover": gpx,
                   "mutation": mutation_point_repaint})
    benchmark_popsize(kwargs, os.path.join(out, "gpx-repaint-popsize"))
    benchmark_param(kwargs, output_path=os.path.join(out, "gpx-repaint"), name="cxpb", values=[0.1, 0.2, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
    benchmark_param(kwargs, output_path=os.path.join(out, "gpx-repaint"), name="mutpb", values=[0.1, 0.2, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])


def experiment_gpx_merge(out):
    kwargs = default_kwargs.copy()
    kwargs.update({"crossover": gpx,
                   "mutation": mutation_color_merge})
    benchmark_popsize(kwargs, os.path.join(out, "gpx-merge-popsize"))
    benchmark_param(kwargs, output_path=os.path.join(out, "gpx-merge"), name="cxpb", values=[0.1, 0.2, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
    benchmark_param(kwargs, output_path=os.path.join(out, "gpx-merge"), name="mutpb", values=[0.1, 0.2, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])


def experiment_gpx_conflicting(out):
    kwargs = default_kwargs.copy()
    kwargs.update({"crossover": gpx,
                   "mutation": mutation_change_conflicting})
    benchmark_popsize(kwargs, os.path.join(out, "gpx-conflicting-popsize"))
    benchmark_param(kwargs, output_path=os.path.join(out, "gpx-conflicting"), name="cxpb", values=[0.1, 0.2, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
    benchmark_param(kwargs, output_path=os.path.join(out, "gpx-conflicting"), name="mutpb", values=[0.1, 0.2, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])


def benchmark_variant(g, name, crossover, mutation, popsize, cxpb, mutpb, output_dir, iters=50):
    eval_count = 100000
    kwargs = {
        "crossover": crossover,
        "mutation": mutation,
        "popsize": popsize,
        "cxpb": cxpb,
        "mutpb": mutpb,
        "ngen": eval_count // popsize,
        "graph": g,
        "visualize": False,
        "verbose": False
    }
    results = np.zeros(iters)

    for i in range(iters):
        print(f"{name} best setting iteration {i} / {iters}")
        results[i] = ea_color(**kwargs)[0].fitness.values[0]

    np.savetxt(os.path.join(output_dir, f"{name}-best.out"), results)


if __name__ == '__main__':
    # input_graph = "graphs/DSJR500.1.graphml"
    input_graph = "graphs/DSJC125.1.graphml"
    g = nx.read_graphml(input_graph)
    out_dir = f"experiments-output-" + datetime.datetime.now().strftime("%d-%m-%Y-(%H:%M:%S)")
    os.mkdir(out_dir)
    default_kwargs["graph"] = g

    # experiment_onepoint_repaint(out_dir)
    # experiment_onepoint_merge(out_dir)
    # experiment_onepoint_conflicting(out_dir)
    #
    # experiment_gpx_repaint(out_dir)
    # experiment_gpx_merge(out_dir)
    # experiment_gpx_conflicting(out_dir)

    # benchmark_variant(g, "onepoint_repaint", tools.cxOnePoint, mutation_point_repaint, popsize=20, cxpb=0.7, mutpb=0.8,
    #                   output_dir=out_dir, iters=50)
    #
    # benchmark_variant(g, "onepoint_merge", tools.cxOnePoint, mutation_color_merge, popsize=1000, cxpb=0.9, mutpb=0.7,
    #                   output_dir=out_dir, iters=50)

    benchmark_variant(g, "onepoint_conflicting", tools.cxOnePoint, mutation_change_conflicting, popsize=20, cxpb=0.6, mutpb=0.7,
                      output_dir=out_dir, iters=50)

    # benchmark_variant(g, "gpx_repaint", gpx, mutation_point_repaint, popsize=50, cxpb=0.4, mutpb=0.5,
    #                   output_dir=out_dir, iters=50)

    # benchmark_variant(g, "gpx_merge", gpx, mutation_color_merge, popsize=5000, cxpb=0.7, mutpb=0.4,
    #                   output_dir=out_dir, iters=50)

    benchmark_variant(g, "gpx_conflicting", gpx, mutation_change_conflicting, popsize=20, cxpb=0.2, mutpb=0.5,
                      output_dir=out_dir, iters=50)