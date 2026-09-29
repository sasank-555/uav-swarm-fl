"""Plot test accuracy / loss curves for one or more runs.

    python plot_results.py results/fedavg_iid results/fedavg_noniid --out results/baseline.png
"""
from __future__ import annotations

import argparse
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


def load(run_dir):
    with open(os.path.join(run_dir, "history.json")) as f:
        hist = [h for h in json.load(f) if "test_acc" in h]
    return os.path.basename(os.path.normpath(run_dir)), hist


def main():
    p = argparse.ArgumentParser()
    p.add_argument("runs", nargs="+")
    p.add_argument("--out", default="results/baseline_curves.png")
    p.add_argument("--title", default="FedAvg baseline — UAV swarm (aerial CIFAR-10)")
    args = p.parse_args()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))
    for run in args.runs:
        name, hist = load(run)
        rounds = [h["round"] for h in hist]
        ax1.plot(rounds, [h["test_acc"] * 100 for h in hist], label=name, linewidth=2)
        ax2.plot(rounds, [h["test_loss"] for h in hist], label=name, linewidth=2)

    ax1.set(xlabel="Communication round", ylabel="Global test accuracy (%)", title="Accuracy")
    ax2.set(xlabel="Communication round", ylabel="Global test loss", title="Loss")
    for ax in (ax1, ax2):
        ax.grid(alpha=0.3)
        ax.legend()
    fig.suptitle(args.title)
    fig.tight_layout()
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    fig.savefig(args.out, dpi=150)
    print(f"Saved {args.out}")


if __name__ == "__main__":
    main()
