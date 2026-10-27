"""Paired, seed-clustered context-ablation estimates from a study manifest."""
from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path

import numpy as np

from run_context_study import completed, read_json, write_json

COMPARISONS = [
    ("ccra", "ccra_maskonly", "telemetry"),
    ("ccra_maskonly", "ccra_noctx", "packet_mask"),
    ("ccra", "ccra_noctx", "full_context"),
]


def interval(values, samples=10_000):
    """Resample independent seeds, never individual rounds or attack cells."""
    values = np.asarray(values, dtype=float)
    if not len(values):
        return {"n_seeds": 0, "mean_pp": None, "ci95_pp": None}
    result = {"n_seeds": len(values), "mean_pp": float(values.mean() * 100), "ci95_pp": None}
    if len(values) >= 2:
        rng = np.random.default_rng(501_927)
        means = values[rng.integers(len(values), size=(samples, len(values)))].mean(axis=1)
        result["ci95_pp"] = (np.quantile(means, [0.025, 0.975]) * 100).tolist()
    return result


def classify(estimate, threshold_pp):
    ci = estimate.get("ci95_pp")
    if ci is None or estimate["n_seeds"] < 10:
        return "insufficient replication"
    low, high = ci
    if low > threshold_pp:
        return "meaningful positive effect supported"
    if high < -threshold_pp:
        return "meaningful negative effect supported"
    if low > -threshold_pp and high < threshold_pp:
        return "effect bounded within the predefined negligible range"
    return "inconclusive at the predefined practical threshold"


def run_metrics(job, chance):
    cfg = job["config"]
    directory = Path(cfg["out_dir"]) / cfg["name"]
    summary = read_json(directory / "summary.json")
    history = read_json(directory / "history.json")
    acc = {row["round"]: row["test_acc"] for row in history if "test_acc" in row}
    diverged = summary["diverged"]
    if not diverged and len(acc) != cfg["rounds"]:
        raise ValueError("study analysis requires evaluation every round")
    # Divergence is scored at chance from its failure round through the fixed horizon.
    curve = [acc.get(rnd, chance) for rnd in range(1, cfg["rounds"] + 1)]
    if not all(math.isfinite(x) and 0 <= x <= 1 for x in curve):
        raise ValueError(f"invalid accuracy curve in {directory}")
    final = chance if diverged else summary["final_test_acc"]
    return {
        "seed": job["seed"], "scenario": job["scenario"], "aggregator": cfg["aggregator"],
        "diverged": diverged, "final_accuracy": final,
        "mean_round_accuracy": sum(curve) / cfg["rounds"],
        "mean_pdr": summary["mean_pdr"], "mean_latency_s": summary["mean_latency_s"],
        "total_handovers": summary["total_handovers"],
        "honest_rejection": summary["mean_honest_rejection_rate"],
        "attacker_acceptance": summary["mean_attacker_acceptance_rate"],
        "bound_violating_cells": summary["total_robustness_bound_violating_cells"],
        "attempted_upload_mib": sum(
            drone.get("model_bits", 0) for row in history for drone in row.get("drones", {}).values()
        ) / 8 / 2**20,
        "rounds_to_40pct": next((r for r, value in sorted(acc.items()) if value >= 0.4), None),
    }


def analyze(root, chance=0.1, allow_incomplete=False):
    manifest = read_json(root / "study_manifest.json")
    rows, missing, configs = [], [], {}
    for job in manifest["jobs"]:
        cfg = job["config"]
        key = (job["seed"], job["scenario"], cfg["aggregator"])
        if key in configs:
            raise ValueError(f"duplicate study job: {key}")
        configs[key] = cfg
        if not completed(job):
            missing.append(list(key))
            continue
        rows.append(run_metrics(job, chance))
    if missing and not allow_incomplete:
        raise ValueError(f"{len(missing)} missing/incomplete jobs; finish the study or use --allow-incomplete")
    if not rows:
        raise ValueError("no terminal study runs")
    by_key = {(r["seed"], r["scenario"], r["aggregator"]): r for r in rows}
    scenarios = sorted({j["scenario"] for j in manifest["jobs"]})
    estimates, primary = [], []
    for method, baseline, label in COMPARISONS:
        for metric in ("final_accuracy", "mean_round_accuracy"):
            per_scenario = {}
            for scenario in scenarios:
                differences = {}
                for seed in manifest["seeds"]:
                    keys = [(seed, scenario, name) for name in (method, baseline)]
                    if any(key not in by_key for key in keys):
                        continue
                    # Method is the only permitted input difference within a pair.
                    pair_configs = [
                        {k: v for k, v in configs[key].items() if k not in {"name", "aggregator"}}
                        for key in keys
                    ]
                    if pair_configs[0] != pair_configs[1]:
                        raise ValueError(f"unpaired configurations: {keys}")
                    differences[seed] = by_key[keys[0]][metric] - by_key[keys[1]][metric]
                per_scenario[scenario] = differences
                estimates.append({
                    "comparison": label, "metric": metric, "scope": scenario,
                    **interval(list(differences.values())),
                })
            # First average the fixed attack suite within each seed; resample seeds.
            attacked = [s for s in scenarios if not s.startswith("clean_")]
            pooled = [
                np.mean([per_scenario[s][seed] for s in attacked])
                for seed in manifest["seeds"]
                if attacked and all(seed in per_scenario[s] for s in attacked)
            ]
            estimates.append({
                "comparison": label, "metric": metric, "scope": "attacked_suite_seed_mean",
                **interval(pooled),
            })
            stress_scenarios = [s for s in attacked if s.endswith("_hfl_trace_stress")]
            stressed = [
                np.mean([per_scenario[s][seed] for s in stress_scenarios])
                for seed in manifest["seeds"]
                if stress_scenarios and all(seed in per_scenario[s] for s in stress_scenarios)
            ]
            estimates.append({
                "comparison": label, "metric": metric, "scope": "attacked_stress_seed_mean",
                **interval(stressed),
            })
            interactions = defaultdict(list)
            for seed in manifest["seeds"]:
                for reference in ("hfl_trace", "hfl_ideal"):
                    diffs = []
                    attacks = sorted({s.split("_hfl_")[0] for s in attacked})
                    for attack in attacks:
                        base = per_scenario.get(f"{attack}_{reference}", {})
                        stress = per_scenario.get(f"{attack}_hfl_trace_stress", {})
                        if seed in base and seed in stress:
                            diffs.append(stress[seed] - base[seed])
                    if attacks and len(diffs) == len(attacks):
                        interactions[reference].append(float(np.mean(diffs)))
            for reference, differences in interactions.items():
                estimate = {
                    "comparison": label, "metric": metric,
                    "scope": f"interaction_stress_minus_{reference}",
                    **interval(differences),
                }
                estimates.append(estimate)
                if label == "telemetry" and metric == "final_accuracy" and reference == "hfl_trace":
                    primary.append(estimate)
    threshold = manifest.get("meaningful_effect_pp", 1.0)
    for estimate in primary:
        estimate["assessment"] = (
            "pilot only; no inferential conclusion" if manifest["profile"] == "pilot"
            else "incomplete study; no inferential conclusion" if missing
            else classify(estimate, threshold)
        )
    report = {
        "profile": manifest["profile"], "planned_runs": len(configs), "terminal_runs": len(rows),
        "missing_jobs": missing, "chance_accuracy": chance,
        "meaningful_effect_pp": threshold,
        "primary": primary, "estimates": estimates,
        "interpretation": (
            "Pipeline pilot only; no defense-ranking or significance claims."
            if manifest["profile"] == "pilot" else
            "Paired percentile bootstrap over seeds. Primary contrast: telemetry gain under stress "
            "minus telemetry gain on the same unstressed trace, averaged over attacks per seed. "
            "Other contrasts are exploratory; intervals have no multiplicity adjustment."
        ),
    }
    write_json(root / "context_analysis.json", report)
    with (root / "context_runs.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    lines = ["# Controlled context study", "", report["interpretation"], "",
             f"Terminal runs: {len(rows)}/{len(configs)}. Diverged final accuracy is scored at {100*chance:.1f}%.",
             "Mean-round accuracy uses the fixed requested horizon, with chance from divergence onward.",
             "Intervals resample seeds; rounds and attack/condition cells are not independent replicates.",
             "The final design uses at least ten paired seeds and 100 rounds by default.", "",
             f"Predefined practical threshold: {threshold:.2f} percentage points.",
             "Primary assessment: " + (primary[0]["assessment"] if primary else "primary comparison unavailable"),
             "A positive stress interaction alone does not establish positive absolute benefit under stress; inspect both contrasts.", "",
             "| Contrast | Metric | Scope | Seeds | Gain (pp) | Paired bootstrap 95% interval (pp) |",
             "|---|---|---|---:|---:|---|"]
    for row in estimates:
        mean = "—" if row["mean_pp"] is None else f"{row['mean_pp']:+.3f}"
        ci = "—" if row["ci95_pp"] is None else f"[{row['ci95_pp'][0]:+.3f}, {row['ci95_pp'][1]:+.3f}]"
        lines.append(f"| {row['comparison']} | {row['metric']} | {row['scope']} | {row['n_seeds']} | {mean} | {ci} |")
    lines.extend(["", "## Run outcomes", "",
                  "| Method | Terminal | Diverged | All-run final accuracy (%) |",
                  "|---|---:|---:|---:|"])
    for method in sorted({r["aggregator"] for r in rows}):
        subset = [r for r in rows if r["aggregator"] == method]
        lines.append(f"| {method} | {len(subset)} | {sum(r['diverged'] for r in subset)} | {100*np.mean([r['final_accuracy'] for r in subset]):.2f} |")
    (root / "CONTEXT_ANALYSIS.md").write_text("\n".join(lines) + "\n")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--chance-accuracy", type=float, default=0.1)
    parser.add_argument("--allow-incomplete", action="store_true")
    args = parser.parse_args()
    if not 0 <= args.chance_accuracy <= 1:
        parser.error("chance accuracy must be in [0, 1]")
    report = analyze(args.root.resolve(), args.chance_accuracy, args.allow_incomplete)
    print(f"Analyzed {report['terminal_runs']}/{report['planned_runs']} runs; wrote CONTEXT_ANALYSIS.md")


if __name__ == "__main__":
    main()
