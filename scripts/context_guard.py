"""Low-cost server watchdog: stop on confirmed mechanical faults, not bad scores."""
from __future__ import annotations

import argparse
import csv
import math
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import torch

from run_context_study import completed, job_directory, read_json, source_digest, write_json


def inspect(root, cache):
    manifest = read_json(root / "study_manifest.json")
    errors, reviews, terminal = [], [], []
    partitions = cache.setdefault("partitions", {})
    validated = cache.setdefault("validated", {})
    rounds = 0
    clean_pdr = {}
    ideal_curves = {}
    for job in manifest["jobs"]:
        cfg = job["config"]
        directory = job_directory(job, root)
        label = f"seed{job['seed']}/{cfg['name']}"
        config_path = directory / "config.json"
        if not config_path.exists():
            continue
        try:
            if read_json(config_path) != cfg:
                errors.append(f"configuration mismatch: {label}")
            partition = read_json(directory / "swarm_partition.json")
            reference = partitions.setdefault(job["seed"], partition)
            if reference != partition:
                errors.append(f"partition mismatch: {label}")
        except FileNotFoundError:
            # Metadata is written during startup, before training begins.
            pass
        except (ValueError, TypeError):
            errors.append(f"invalid metadata: {label}")
        log = Path(cfg["out_dir"]) / (cfg["name"] + ".log")
        if log.exists():
            text = log.read_text(errors="replace")
            if "Traceback (most recent call last)" in text or "CUDA out of memory" in text:
                errors.append(f"process error: {label}")
        metrics = directory / "metrics.csv"
        rows = []
        if metrics.exists():
            with metrics.open() as handle:
                rows = list(csv.DictReader(handle))
            # An appending process can leave the final CSV record incomplete.
            rows = [row for row in rows if row.get("round_time_s") not in (None, "")]
            rounds += len(rows)
            for row in rows:
                try:
                    values = [float(row[k]) for k in ("test_acc", "test_loss", "train_loss", "mean_pdr")]
                    if not all(math.isfinite(v) for v in values) or not 0 <= values[0] <= 1 or not 0 <= values[3] <= 1:
                        errors.append(f"invalid metrics: {label} round {row['round']}")
                        break
                except (ValueError, TypeError, KeyError):
                    errors.append(f"malformed metrics: {label}")
                    break
            if job["scenario"] == "clean_hfl_ideal" and cfg["aggregator"] in {"ccra_noctx", "ccra_maskonly"}:
                ideal_curves[(job["seed"], cfg["aggregator"])] = [r["test_acc"] for r in rows]
        summary_path = directory / "summary.json"
        if not summary_path.exists():
            latest_write = metrics.stat().st_mtime if metrics.exists() else config_path.stat().st_mtime
            if time.time() - latest_write > 900:
                errors.append(f"run has made no progress for 15 minutes: {label}")
            continue
        try:
            if not completed(job, root):
                errors.append(f"invalid terminal artifacts: {label}")
                continue
            terminal.append(job)
            summary = read_json(summary_path)
            if validated.get(label) != summary_path.stat().st_mtime_ns:
                before_validation = len(errors)
                state = torch.load(directory / "final_model.pt", map_location="cpu", weights_only=True)
                if not state or not all(torch.isfinite(v).all().item() for v in state.values()):
                    errors.append(f"non-finite checkpoint: {label}")
                    continue
                history = read_json(directory / "history.json")
                if cfg["aggregator"] == "fltrust":
                    partition = read_json(directory / "swarm_partition.json")
                    for record in history:
                        for cell in record["cells"].values():
                            if not cell.get("received"):
                                continue
                            steps = sorted(cfg["local_epochs"] * math.ceil(partition["drones"][str(cid)]["num_samples"] / cfg["batch_size"]) for cid in cell["client_ids"])
                            middle = len(steps) // 2
                            median = steps[middle] if len(steps) % 2 else (steps[middle-1] + steps[middle]) / 2
                            if cell.get("root_optimizer_steps") != max(1, math.ceil(median)):
                                errors.append(f"FLTrust step-budget mismatch: {label}")
                                break
                if len(errors) == before_validation:
                    validated[label] = summary_path.stat().st_mtime_ns
            if job["scenario"].startswith("clean_") and not summary["diverged"]:
                clean_pdr[(job["seed"], job["scenario"], cfg["aggregator"])] = summary["mean_pdr"]
                # Review cue only: poor accuracy is not proof of an implementation fault.
                if summary["final_test_acc"] <= 0.12:
                    reviews.append(f"clean learning remains near chance; review: {label}")
        except (OSError, ValueError, TypeError, KeyError, RuntimeError) as error:
            errors.append(f"artifact error: {label}: {type(error).__name__}")
    for seed in manifest["seeds"]:
        a = ideal_curves.get((seed, "ccra_noctx"), [])
        b = ideal_curves.get((seed, "ccra_maskonly"), [])
        overlap = min(len(a), len(b))
        if a[:overlap] != b[:overlap]:
            errors.append(f"ideal-link ablation invariant failed: seed{seed}")
    for (seed, scenario, method), pdr in clean_pdr.items():
        if scenario != "clean_hfl_trace_stress":
            continue
        reference = clean_pdr.get((seed, "clean_hfl_trace", method))
        if reference is not None and pdr > reference + 1e-6:
            errors.append(f"stress delivery exceeds control: seed{seed}/{method}")
    per_seed = defaultdict(int)
    expected = defaultdict(int)
    for job in manifest["jobs"]:
        expected[job["seed"]] += 1
    for job in terminal:
        per_seed[job["seed"]] += 1
    return {
        "terminal": len(terminal), "planned": len(manifest["jobs"]), "round_records": rounds,
        "first_batch_complete": len(terminal) >= 8,
        "complete_seeds": [seed for seed, n in per_seed.items() if n == expected[seed]],
        "errors": sorted(set(errors)), "review_cues": sorted(set(reviews)),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--interval", type=int, default=60)
    parser.add_argument("--stop-program", default="uav_context_study")
    args = parser.parse_args()
    cache, previous_errors, progress, progress_time = {}, set(), None, time.monotonic()
    while True:
        report = inspect(args.root, cache)
        expected_source = read_json(args.root / "study_manifest.json")["source_sha256"]
        if source_digest() != expected_source:
            report["errors"].append("training source changed from pinned manifest")
        current = (report["terminal"], report["round_records"])
        if current != progress:
            progress, progress_time = current, time.monotonic()
        elif time.monotonic() - progress_time > 900 and report["terminal"] < report["planned"]:
            report["errors"].append("no training progress for at least 15 minutes")
        write_json(args.root / "EARLY_HEALTH.json", report)
        confirmed = previous_errors.intersection(report["errors"])
        if confirmed:
            report["confirmed_errors"] = sorted(confirmed)
            write_json(args.root / "EARLY_ALERT.json", report)
            subprocess.run(["supervisorctl", "stop", args.stop_program], check=False)
            print("Stopped study after confirmed mechanical error; see EARLY_ALERT.json", flush=True)
            return 1
        previous_errors = set(report["errors"])
        if report["terminal"] == report["planned"] and not report["errors"]:
            print("All jobs terminal; final validation is handled by the study wrapper.", flush=True)
            return 0
        time.sleep(args.interval)


if __name__ == "__main__":
    raise SystemExit(main())
