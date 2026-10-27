"""Audit terminal artifacts and finite checkpoints before interpreting a study."""
from __future__ import annotations

import argparse
import math
from collections import defaultdict
from pathlib import Path

import numpy as np
import torch

from run_context_study import completed, digest, read_json, write_json


def validate(root):
    manifest = read_json(root / "study_manifest.json")
    problems, hashes = [], []
    partitions = {}
    counts = defaultdict(int)
    for job in manifest["jobs"]:
        cfg = job["config"]
        directory = Path(cfg["out_dir"]) / cfg["name"]
        name = f"seed{job['seed']}/{cfg['name']}"
        if not completed(job):
            problems.append(f"incomplete: {name}")
            continue
        summary = read_json(directory / "summary.json")
        history = read_json(directory / "history.json")
        partition = read_json(directory / "swarm_partition.json")
        reference = partitions.setdefault(job["seed"], partition)
        if partition != reference:
            problems.append(f"unpaired partition: {name}")
        if cfg["aggregator"] == "fltrust":
            for row in history:
                for cell in row["cells"].values():
                    if not cell.get("received"):
                        continue
                    steps = [
                        cfg["local_epochs"] * math.ceil(
                            partition["drones"][str(cid)]["num_samples"] / cfg["batch_size"]
                        )
                        for cid in cell["client_ids"]
                    ]
                    expected = max(1, math.ceil(float(np.median(steps))))
                    if cell.get("root_optimizer_steps") != expected:
                        problems.append(f"unmatched FLTrust steps: {name} round {row['round']}")
        try:
            path = directory / "final_model.pt"
            state = torch.load(path, map_location="cpu", weights_only=True)
            if not state or not all(torch.isfinite(value).all().item() for value in state.values()):
                raise ValueError("empty or non-finite checkpoint")
            hashes.append(f"{digest(path)}  {name}/final_model.pt")
        except (OSError, ValueError, RuntimeError) as error:
            problems.append(f"invalid checkpoint: {name}: {error}")
        counts["terminal_runs"] += 1
        counts["diverged_runs"] += summary["diverged"]
    report = {
        "planned_runs": len(manifest["jobs"]), **dict(counts),
        "finite_checkpoints": len(hashes), "paired_seed_partitions": len(partitions),
        "source_sha256": manifest["source_sha256"],
        "dataset_sha256": manifest["dataset_sha256"],
        "trace_sha256": manifest["trace_sha256"],
        "problems": problems,
        "valid": not problems and len(hashes) == len(manifest["jobs"]),
    }
    write_json(root / "ARTIFACT_VALIDATION.json", report)
    (root / "CHECKPOINT_SHA256SUMS.txt").write_text("\n".join(hashes) + "\n")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    args = parser.parse_args()
    report = validate(args.root.resolve())
    print(f"Validated {report.get('terminal_runs', 0)}/{report['planned_runs']} terminal runs; "
          f"{report['finite_checkpoints']} finite checkpoints; {len(report['problems'])} problems")
    if not report["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
