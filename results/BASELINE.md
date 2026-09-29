# Month 1: FedAvg Baseline Results

Setup: aerial-modified CIFAR-10, 10 drones, TacticalEdgeCNN (156k params), FedAvg, 50 rounds,
2 local epochs, SGD (lr 0.01, momentum 0.9), batch 64, seed 42, CPU.

| Run | Partition | Final test acc | Best test acc |
|---|---|---|---|
| `fedavg_iid` | IID (5,000 balanced images/drone) | **62.62%** | 62.65% (round 49) |
| `fedavg_noniid` | Dirichlet α=0.5 (skewed classes/drone) | **60.23%** | 60.58% (round 49) |

Accuracy curves are in `baseline_curves.png`. Neither curve had fully plateaued by round 50.
More rounds would add a few more points of accuracy.

These numbers are the reference for Month 2 (label-flipping attacks).
