import os
import matplotlib.pyplot as plt
import numpy as np


def draw_popsize(variants, input_dir, output_dir):
    fig, axes = plt.subplots(1,len(variants, 3.54,3.54), sharex=True)
    plt.tight_layout(pad=3)
    popsizes=[4, 20, 50, 100, 500, 1000]

    for (variant, ax) in zip(variants, axes):
        x = np.loadtxt(os.path.join(input_dir, variant + ".out"))
        ax.boxplot(x, labels=popsizes)

    plt.savefig(os.path.join(output_dir, "popsizes.svg"))


def draw_cxpb(variants, input_dir):
    pass


def draw_mutpb(variants, input_dir):
    pass


input_dir = "experiments-output-06-05-2022-(03:55:34)"
out_dir_name = "plots"
os.mkdir(out_dir_name)

variants = ["onepoint-repaint", "onepoint-merge", "gpx-repaint", "gpx-merge"]

draw_popsize(variants, input_dir, out_dir_name)
