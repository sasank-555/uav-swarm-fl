# Controlled context study

Status: implementation and local pipeline pilots complete; full GPU evaluation pending.
The earlier 432-run benchmark is superseded and cannot establish current defense rankings.

## Question and fixed design

Does BS-observed communication and mobility telemetry improve CCRA beyond handling
missing packets, and does that improvement become larger when the same trace has
worse delivery? This study tests that question within the current simulator. It
cannot establish real-world UAV deployment performance or universal superiority.

The default final study has **720 runs**: 10 seeds (41–50), 100 rounds, six methods,
four attack settings, and three channel conditions. Every run uses 10 clients,
three base stations, synchronization every five rounds, TacticalEdgeCNN, aerial
CIFAR-10, Dirichlet alpha 0.5, and one local epoch. All 49,500 non-root training
images are used. The shared 500-image root set remains disjoint from every client.

| Factor | Levels |
|---|---|
| Defense | FedAvg, coordinate median, FLTrust, CCRA-no-context, CCRA-mask-only, CCRA |
| Attack | Clean, sign flip, ALIE-style, IPM |
| Channel | HFL ideal; measured-relative trace at assumed 15 dB; identical trace at assumed 5 dB |
| Replication | 10 paired seeds, 100 rounds, evaluation every round |

Median is a prespecified conventional comparator, not selected by looking at test
results. FLTrust checks the corrected root-step budget against a trusted-data
baseline. Attack parameters remain fixed at existing defaults: sign-flip scale 5,
ALIE z 1.5, IPM epsilon 0.5. Attack families represent different threat models;
these strengths are not asserted to have equal damage or equal update norms.
The ALIE implementation uses `mean - z * std * sign(mean)` within the serving
cell. Treat it as an ALIE-style directional variant, not an exact reproduction
of every original attack implementation. ALIE/IPM observe honest cell updates;
this is an explicit strong attacker assumption.

Attacker IDs are sampled without replacement from a separate deterministic RNG
stream per seed, with exactly three attackers. The chosen IDs remain the same
across methods, attack types, and channel conditions within that seed. Data splits,
initial weights, training RNG, and trace phases are also paired. Changing seed
changes the split, initialization, trace phase, and placement together; the seed
is the independent replication unit. This is not a separate factorial estimate
of each source of randomness.

## Ablation interpretation

| Contrast | What it isolates |
|---|---|
| CCRA minus mask-only | SINR calibration and operational telemetry in reputation |
| Mask-only minus no-context | Delivered-coordinate scoring, RMS clipping, and averaging |
| CCRA minus no-context | Combined packet-mask and telemetry mechanisms |

The full and mask-only methods use the same packet masks, root-update budget,
norm clipping, staleness weighting, and trust hyperparameters. Mask-only ignores
SINR, PDR, reliability, geometry, speed, and handover telemetry. The original
no-context variant still shares the server's delivery/deadline selection and
staleness weighting. It is not an end-to-end system with all channel information
removed. The CCRA versus mask-only contrast is the primary telemetry comparison.

All study conditions set additive parameter noise to zero. Delivered digital
parameters remain unchanged; the channel introduces packet erasures and deadline
loss. No jammer is used, so the stress intervention changes only the assumed SNR
anchor, preserving the same replay positions and handover behavior. The trusted
telemetry assumption is BS observation or authentication; spoofing is not tested.

Absolute SNR, virtual base stations, PER, upload rate, and latency remain simulated
or derived. The 5/15 dB values are sensitivity settings, not measured calibration.
Two handovers over the 60-round channel validation are insufficient to support a
high-mobility claim. This experiment deliberately isolates delivery severity;
a separate handover-frequency study is still needed for that broader claim.

## Prespecified analysis and decision rule

The primary estimand is the seed-level mean over the three attacks of:

`(CCRA - mask-only) at 5 dB - (CCRA - mask-only) at 15 dB`.

Use final accuracy, expressed in percentage points. Compute each paired
method difference, then each matched stress difference, then average the fixed
attack suite within each seed. Resample the ten seed values with replacement
10,000 times using a fixed analysis RNG, and report the percentile 95% interval.
Rounds, attack cells, and channel cells must not be counted as independent seeds.

The predefined smallest meaningful effect is **1 percentage point**. It is an
engineering decision threshold, not a claim established by earlier results.

- Interval entirely above +1 pp: evidence of a meaningful positive effect.
- Interval entirely below -1 pp: evidence of a meaningful negative effect.
- Interval entirely within [-1, +1] pp: effect bounded within the negligible range.
- Otherwise: inconclusive at this practical threshold; more precision is needed.

A positive interaction does not itself prove positive absolute benefit under
stress: inspect the `attacked_stress_seed_mean` CCRA-minus-mask-only estimate too.
Claim a useful stress-specific telemetry benefit only when both relevant intervals
support a positive practically meaningful effect. A negative interaction is not
necessarily evidence that absolute stressed performance is harmful.

All other comparisons, attack slices, clean-case costs, and mean-round accuracy
are secondary/exploratory. Their intervals have no multiplicity adjustment.
Do not pick a favorable slice as the headline result. Small-sample bootstrap
intervals remain approximate; ten seeds do not guarantee a narrow interval or a
conclusive finding. Do not tune hyperparameters or stop at a favorable partial
result. Record any design changes before rerunning in a new output directory.

Divergence remains an explicit terminal experimental outcome, not a retryable
process failure. Its final accuracy is scored at CIFAR-10 chance (10%). Mean-round
accuracy is the arithmetic mean over rounds 1–100, using chance from divergence
onward, rather than averaging only surviving rounds. This is not a time integral.
Missing jobs are not treated as divergence and block the default analysis.
Communication counts include attempted update payload bits in completed rounds;
protocol overhead, retransmission, and a failed partial round are excluded.
Time-to-40% is reported per run, with blank meaning never reached. It is not
averaged over only successful target-reaching runs.

## Run and reproduce

Prepare `data/cifar10.npz` and `data/channel_traces/deepsense23.npz` first using
the existing preparation tools. Raw DeepSense data must not be committed.

```bash
# Inspect the full design without starting training.
python run_context_study.py --profile final --device cuda --plan-only

# Full evaluation: 720 runs. The default is one process; explicitly choose GPU concurrency.
python run_context_study.py --profile final --device cuda --parallel 4

# Validates full expected completion, computes paired results, writes reports.
python analyze_context_study.py results/context_final
```

The manifest fixes full configurations, source SHA-256, dataset and trace SHA-256,
runtime versions, the primary estimand, and the practical threshold. Resume with
the identical command. Source, design, runtime, or data changes require a new
output directory. Only jobs with matching configuration, terminal summary,
consistent history, and a saved final checkpoint are skipped. A truncated history
alone is not completion. `COMPLETE` is written only when every planned job is
terminal. `--plan-only` never starts training, but prepares pilot data if requested.

The two completed local pilot commands are:

```bash
python run_context_study.py --profile pilot --attacks clean ipm --parallel 2
python run_context_study.py --profile pilot --attacks sign_flip alie \
  --out-dir results/context_attack_pilot --parallel 2
python analyze_context_study.py results/context_pilot
python analyze_context_study.py results/context_attack_pilot
```

They use 2,000 real CIFAR training images, 500 test images, two seeds and two rounds;
the root remains 500 images and client training uses the remaining 1,500. These
144 runs validate the pipeline, not comparative accuracy or scientific hypotheses.
Their recorded source fingerprint predates the later change to final-profile
seed/round defaults. Do not rewrite that provenance to match a newer source tree.
Compact reports are versionable; per-run histories, models, logs, and the full
manifest remain local. Preserve them when copying runs off the GPU.

## Remaining work

1. Run the full fixed GPU study and validate all terminal artifacts and checkpoints.
2. Report the primary interaction, absolute stressed benefit, clean cost, stability,
   and per-cell population violations together, including unfavorable outcomes.
3. If precision is insufficient, plan an additional seed batch before inspecting
   its results; keep its decision separate from this fixed study.
4. Evaluate handover frequency, root-set size, non-IID severity, and local attacker
   concentration before making broader mobility or generalization claims.
