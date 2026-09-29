"""Aggregator + federated training loop.

The aggregation rule is pluggable: Month 1 uses plain FedAvg (McMahan et al.,
2017); Month 4 adds the Multi-Dimensional Trust aggregator that gates each
update using network telemetry (SNR, packet loss) and update statistics.
"""
from __future__ import annotations

import csv
import json
import os
import time

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from .client import ClientUpdate, DroneClient


class Aggregator:
    name = "base"

    def aggregate(self, global_state: dict, updates: list[ClientUpdate]) -> tuple[dict, dict]:
        """Return (new_global_state, info). `info` is logged each round."""
        raise NotImplementedError


class FedAvg(Aggregator):
    """Sample-size-weighted average of client models. No robustness at all:
    every update is trusted equally, which is exactly what Month 2 will break."""
    name = "fedavg"

    def aggregate(self, global_state, updates):
        total = sum(u.num_samples for u in updates)
        weights = {u.client_id: u.num_samples / total for u in updates}
        new_state = {}
        for key, ref in global_state.items():
            if not torch.is_floating_point(ref):
                new_state[key] = updates[0].state_dict[key].clone()
                continue
            acc = torch.zeros_like(ref, dtype=torch.float32)
            for u in updates:
                acc += weights[u.client_id] * u.state_dict[key].float()
            new_state[key] = acc.to(ref.dtype)
        return new_state, {"weights": weights}


AGGREGATORS = {"fedavg": FedAvg}


def build_aggregator(name: str) -> Aggregator:
    if name not in AGGREGATORS:
        raise ValueError(f"Unknown aggregator '{name}'. Available: {list(AGGREGATORS)}")
    return AGGREGATORS[name]()


@torch.no_grad()
def evaluate(model: nn.Module, dataset, device, batch_size: int = 512, num_classes: int = 10):
    model.eval()
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=False)
    loss_fn = nn.CrossEntropyLoss(reduction="sum")
    total_loss, correct, n = 0.0, 0, 0
    class_correct = torch.zeros(num_classes)
    class_total = torch.zeros(num_classes)
    for xb, yb in loader:
        xb, yb = xb.to(device), yb.to(device)
        out = model(xb)
        total_loss += loss_fn(out, yb).item()
        pred = out.argmax(1)
        correct += (pred == yb).sum().item()
        n += len(yb)
        class_total += torch.bincount(yb.cpu(), minlength=num_classes).float()
        class_correct += torch.bincount(yb[pred == yb].cpu(), minlength=num_classes).float()
    per_class = (class_correct / class_total.clamp(min=1)).tolist()
    return {"test_loss": total_loss / n, "test_acc": correct / n, "per_class_acc": per_class}


class FederatedServer:
    def __init__(self, model: nn.Module, clients: list[DroneClient], test_ds, cfg, device):
        self.model = model.to(device)
        self.clients = clients
        self.test_ds = test_ds
        self.cfg = cfg
        self.device = device
        self.aggregator = build_aggregator(cfg.aggregator)
        self.rng = np.random.default_rng(cfg.seed)
        self.history: list[dict] = []

    def sample_clients(self) -> list[DroneClient]:
        m = max(1, int(round(self.cfg.client_fraction * len(self.clients))))
        idx = self.rng.choice(len(self.clients), size=m, replace=False)
        return [self.clients[i] for i in sorted(idx)]

    def run(self, run_dir: str) -> list[dict]:
        cfg = self.cfg
        csv_path = os.path.join(run_dir, "metrics.csv")
        fields = ["round", "test_acc", "test_loss", "train_loss", "train_acc", "num_clients", "round_time_s"]
        with open(csv_path, "w", newline="") as f:
            csv.DictWriter(f, fieldnames=fields).writeheader()

        best_acc = 0.0
        for rnd in range(1, cfg.rounds + 1):
            t0 = time.time()
            selected = self.sample_clients()
            updates = [c.local_train(self.model) for c in selected]

            global_state = {k: v.detach().cpu() for k, v in self.model.state_dict().items()}
            new_state, agg_info = self.aggregator.aggregate(global_state, updates)
            self.model.load_state_dict(new_state)

            w = np.array([u.num_samples for u in updates], dtype=float)
            train_loss = float(np.average([u.metrics["train_loss"] for u in updates], weights=w))
            train_acc = float(np.average([u.metrics["train_acc"] for u in updates], weights=w))

            record = {"round": rnd, "train_loss": train_loss, "train_acc": train_acc,
                      "num_clients": len(updates)}
            if rnd % cfg.eval_every == 0 or rnd == cfg.rounds:
                record.update(evaluate(self.model, self.test_ds, self.device, cfg.eval_batch_size))
            record["round_time_s"] = time.time() - t0
            self.history.append(record)

            with open(csv_path, "a", newline="") as f:
                csv.DictWriter(f, fieldnames=fields, extrasaction="ignore").writerow(record)

            acc = record.get("test_acc")
            if acc is not None and acc > best_acc:
                best_acc = acc
                torch.save(self.model.state_dict(), os.path.join(run_dir, "best_model.pt"))
            acc_str = f"{acc * 100:6.2f}%" if acc is not None else "   -   "
            print(f"[round {rnd:3d}/{cfg.rounds}] test_acc={acc_str} "
                  f"train_loss={train_loss:.4f} train_acc={train_acc * 100:5.2f}% "
                  f"({record['round_time_s']:.1f}s)", flush=True)

        torch.save(self.model.state_dict(), os.path.join(run_dir, "final_model.pt"))
        with open(os.path.join(run_dir, "history.json"), "w") as f:
            json.dump(self.history, f, indent=2)
        return self.history
