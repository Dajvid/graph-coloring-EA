import os
import matplotlib.pyplot as plt
import numpy as np


def draw_parameter_tuning(input_dir, output_dir):
    variants = ["onepoint-conflicting", "onepoint-merge", "onepoint-repaint"]
    param = "mutpb"
    fig, axes = plt.subplots(len(variants), 1,  sharex=True)
    plt.tight_layout(pad=2)
    labels = [0.1, 0.2, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

    for (variant, ax) in zip(variants, axes):
        x = np.loadtxt(os.path.join(input_dir, variant + f"-{param}.out"))
        ax.boxplot(x, labels=labels)
        ax.set_title(variant)

    plt.savefig(os.path.join(output_dir, f"{param}.png"),)


def draw_cx(input_dir, output_dir):
    fig, axes = plt.subplots(3, 1)
    plt.tight_layout(pad=2)

    for i, mut_variant in enumerate(["repaint", "merge", "conflicting"]):
        data = []
        labels = []
        for j, cx_variant in enumerate(["onepoint", "gpx"]):
            data.append(np.loadtxt(os.path.join(input_dir,  f"{cx_variant}_{mut_variant}-best.out")))
            labels.append(f"{cx_variant}-{mut_variant}")
        axes[i].boxplot(data, labels=labels)

    plt.savefig(os.path.join(output_dir, "cx-best.png"))


def draw_mut(input_dir, output_dir):
    fig, axes = plt.subplots(2, 1)
    plt.tight_layout(pad=2)

    for i, cx_variant in enumerate(["onepoint", "gpx"]):
        data = []
        labels = []
        for j, mut_variant in enumerate(["repaint", "merge", "conflicting"]):
            data.append(np.loadtxt(os.path.join(input_dir,  f"{cx_variant}_{mut_variant}-best.out")))
            labels.append(f"{cx_variant}-{mut_variant}")
        axes[i].boxplot(data, labels=labels)

    plt.savefig(os.path.join(output_dir, "mut-best.png"))


def draw_variants(input_dir, output_dir):
    variants = ["onepoint_repaint", "onepoint_merge", "onepoint_conflicting", "gpx_repaint", "gpx_merge", "gpx_conflicting"]

    plt.figure(figsize=(15, 10))

    data = []
    for variant in variants:
        data.append(np.loadtxt(os.path.join(input_dir,  f"{variant}-best.out")))
    plt.boxplot(data, labels=variants)
    plt.savefig(os.path.join(output_dir, "variants-best.png"))


if __name__ == '__main__':
    input_dir = "experiments-output-06-05-2022-(03:55:34)"
    out_dir_name = "plots"
    try:
        os.mkdir(out_dir_name)
    except FileExistsError:
        pass

    draw_parameter_tuning(input_dir, out_dir_name)
    draw_cx(input_dir, out_dir_name)
    draw_mut(input_dir, out_dir_name)
    draw_variants(input_dir, out_dir_name)