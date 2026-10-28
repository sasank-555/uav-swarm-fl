# Controlled context study: final findings

The fixed 720-run A100 study finished on 28 October 2026. All 720 runs have terminal
records, all 720 final checkpoints are finite, and the ten paired client partitions
match. There were 67 explicitly recorded numerical divergences; no process failures
or unexpected CUDA errors were found. The [full local analysis](context_final_gpu/CONTEXT_ANALYSIS.md),
[validation report](context_final_gpu/ARTIFACT_VALIDATION.json), and
[study protocol](../docs/CONTEXT_STUDY.md) contain the detailed evidence.

## Prespecified result

The primary comparison isolates CCRA's telemetry from its handling of missing
packets. For each of the ten seeds and three attacks, it compares CCRA with
`ccra_maskonly` at the assumed 5 dB and 15 dB anchors of the *same* DeepSense
trace. The primary estimate is the extra telemetry benefit under stress.

| Measure | Estimate (percentage points) | Seed-bootstrap 95% interval |
|---|---:|---:|
| Extra telemetry benefit at 5 dB versus 15 dB (primary) | **−2.72** | **[−3.90, −1.51]** |
| CCRA versus mask-only, attacked 5 dB conditions | **−3.50** | **[−5.08, −2.14]** |

The primary interval lies entirely below the prespecified −1 percentage point
practical threshold. In this simulator and fixed study, **the current telemetry
mechanism made CCRA meaningfully worse as packet delivery deteriorated**. It also
reduced absolute attacked accuracy in the stressed condition: CCRA averaged
45.98%, versus 49.48% for mask-only. This rejects the proposed positive
channel-context claim for the present implementation and conditions.

## Other findings

| Exploratory paired contrast | Attacked 5 dB gain (pp) | Seed-bootstrap 95% interval |
|---|---:|---:|
| Mask-only versus no-context | +4.23 | [+2.16, +5.88] |
| Full CCRA versus no-context | +0.73 | [−0.90, +2.13] |

The mask-only result suggests that using delivered-coordinate masks in scoring,
clipping, and averaging is valuable under packet loss. The full CCRA-versus-
no-context interval is inconclusive at the 1 pp threshold. These are secondary
contrasts with no adjustment for multiple comparisons; they must not replace the
prespecified primary result.

At 5 dB under attack, full CCRA rejected 41.2% of received honest updates on
average, versus 13.8% for mask-only. It accepted 8.8% of received attacker updates,
versus 13.5% for mask-only. This is a plausible *mechanism* for its lower accuracy:
telemetry made the gate stricter for both attackers and honest clients. These rates
are descriptive and do not by themselves establish causal mediation.

Across all attacked conditions, chance-scored final accuracy was 51.58% for
mask-only, 50.24% for no-context, 50.08% for FLTrust, and 49.88% for full CCRA.
FedAvg and coordinate median diverged in 41 and 26 runs respectively; FLTrust and
all three CCRA variants had zero divergences. These are descriptive comparisons,
not a post hoc claim that mask-only universally beats every baseline. Diverged
runs contribute 10% to all-run final accuracy rather than disappearing from means.

## Interpretation and limits

This is a strong negative finding for the *specific telemetry update rule* tested.
It does not establish that channel context can never help. DeepSense Scenario 23
has one measured base station, uncalibrated beam power, virtual additional base
stations, and few simulated handovers. Absolute 5/15 dB SNR anchors, packet errors,
and upload behavior are assumptions or derived quantities. The study uses aerial
CIFAR-10, one CNN, fixed attack strengths, 100 rounds, and ten seeds. The ALIE
implementation is a directional variant. The seed-bootstrap intervals describe
variation over the paired seeds in this design; broader datasets, hardware,
mobility, and adversarial telemetry are outside their scope.

The next algorithm study should diagnose why weak-link evidence suppresses honest
trust recovery, then freeze a modified rule and test it on **new seeds and
conditions**. Retuning on these ten evaluation seeds and treating the same results
as confirmation would invalidate the fixed-study inference. A separate mobility
study is needed before claiming an advantage under frequent handovers.

The training source was pinned at `485fa9f3fda70cc7b54a1871f677654ce95469d5`.
Its SHA-256 training-code digest, full dataset digest, and trace digest are recorded
in the [run state](../docs/GPU_RUN_STATE.md) and the preserved local study manifest.
The local analysis and checkpoint hash list match their validated remote copies.
