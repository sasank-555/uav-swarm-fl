# Context-Aware Byzantine-Resilient Federated Learning for Tactical UAV Swarms

## Month 1: Foundation & Baseline (weeks 1–4)

This month's goal was a standard federated learning pipeline with **no robustness** in PyTorch,
plus a **FedAvg baseline accuracy**. Months 2–5 are measured against it.

### Setup

```powershell
cd C:\Users\Lenovo\Documents\uav-swarm-fl
pip install -r requirements.txt pyarrow pillow
python prepare_data.py        # CIFAR-10 via fast HF mirror -> data/cifar10.npz
```

The default model is **TacticalEdgeCNN** (about 156k params), which runs well on CPU.
A 50-round, 10-drone run takes about 20 min with 8 threads.
`get_device()` picks CUDA first, then Apple **MPS**, then CPU. To use a GPU, install a CUDA build of PyTorch.
The larger `--model lightcnn` (about 403k params) is about 5x slower on CPU.

### Run

```powershell
# IID baseline: 10 drones, 50 rounds, 2 local epochs
python run_baseline.py --name fedavg_iid

# Non-IID baseline: each drone covers a different "sector" with a skewed class mix
python run_baseline.py --partition dirichlet --dirichlet-alpha 0.5 --name fedavg_noniid

# Plot
python plot_results.py results/fedavg_iid results/fedavg_noniid --out results/baseline_curves.png
```

Every option in `fl/config.py` is also a CLI flag, for example `--num-clients 5 --rounds 100 --local-epochs 1 --lr 0.02`.

### Project layout

| File | Purpose |
|---|---|
| `fl/config.py` | `FLConfig` dataclass. Every field is also a CLI flag. |
| `fl/data.py` | CIFAR-10 loading, the **aerial modification**, and IID/Dirichlet partitioning across drones |
| `fl/models.py` | `TacticalEdgeCNN` (default, about 156k params, no norm layers) and `LightCNN` (about 403k params, GroupNorm) |
| `fl/client.py` | `DroneClient`: local SGD on the drone's own data. Returns a `ClientUpdate`. |
| `fl/server.py` | `FedAvg` aggregator (pluggable), evaluation, and the federated round loop with CSV/JSON logging |
| `run_baseline.py` | Entry point. Writes `results/<name>/{config,metrics.csv,history,summary,swarm_partition}.json` and the model checkpoints. |
| `plot_results.py` | Accuracy and loss curves for one or more runs |
| `prepare_data.py` | Fast CIFAR-10 download (the official server is very slow) |

### "Aerial" CIFAR-10

A nadir (downward-looking) drone camera has no fixed "up" direction, and its effective resolution depends on altitude.
`fl/data.py::aerialize` applies both effects to CIFAR-10:

* **Orientation:** each image gets a fixed random rotation of k×90°. This applies to the train set and to the test set.
* **Altitude:** each image gets a fixed random degradation. It is downsampled to 32 px (50% of images), 24 px (30%) or 16 px (20%) and then upsampled back to 32 px.
* **Training augmentation:** all 8 dihedral orientations (flips plus transpose) and a random crop with 4 px padding.

### FedAvg algorithm (per round)

1. The server broadcasts the global weights *w_t* to the selected drones (`--client-fraction`).
2. Each drone *k* runs `local_epochs` of SGD on its local data *D_k* and gets *w_t^k*.
3. The server aggregates: *w_{t+1} = Σ_k (n_k / n) · w_t^k*. Every update is trusted equally, with no filtering.

### Baseline results

See `results/BASELINE.md`. It is generated after the runs finish.

### Hooks for later months

* **Month 2 (label flipping):** `DroneClient.is_malicious` is available, and `DroneClient.y` holds the local labels, which can be overwritten.
* **Month 3 (NS-3 / EW jamming):** `DroneClient.position` and `DroneClient.link_telemetry` hold SNR and packet-loss values.
* **Month 4 (trust metric):** subclass `Aggregator` in `fl/server.py`, register it in `AGGREGATORS`, then run with `--aggregator trust`.
  `aggregate()` receives every `ClientUpdate` and can read each client's telemetry.
