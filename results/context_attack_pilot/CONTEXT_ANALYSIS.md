# Controlled context study

Pipeline pilot only; no defense-ranking or significance claims.

Terminal runs: 72/72. Diverged final accuracy is scored at 10.0%.
Mean-round accuracy uses the fixed requested horizon, with chance from divergence onward.
Intervals resample seeds; rounds and attack/condition cells are not independent replicates.
The final design uses at least ten paired seeds and 100 rounds by default.

Predefined practical threshold: 1.00 percentage points.
Primary assessment: pilot only; no inferential conclusion
A positive stress interaction alone does not establish positive absolute benefit under stress; inspect both contrasts.

| Contrast | Metric | Scope | Seeds | Gain (pp) | Paired bootstrap 95% interval (pp) |
|---|---|---|---:|---:|---|
| telemetry | final_accuracy | alie_hfl_ideal | 2 | +0.000 | [+0.000, +0.000] |
| telemetry | final_accuracy | alie_hfl_trace | 2 | +0.000 | [+0.000, +0.000] |
| telemetry | final_accuracy | alie_hfl_trace_stress | 2 | +0.000 | [+0.000, +0.000] |
| telemetry | final_accuracy | sign_flip_hfl_ideal | 2 | +0.000 | [+0.000, +0.000] |
| telemetry | final_accuracy | sign_flip_hfl_trace | 2 | +0.100 | [+0.000, +0.200] |
| telemetry | final_accuracy | sign_flip_hfl_trace_stress | 2 | -0.200 | [-0.400, +0.000] |
| telemetry | final_accuracy | attacked_suite_seed_mean | 2 | -0.017 | [-0.033, +0.000] |
| telemetry | final_accuracy | attacked_stress_seed_mean | 2 | -0.100 | [-0.200, +0.000] |
| telemetry | final_accuracy | interaction_stress_minus_hfl_trace | 2 | -0.150 | [-0.300, +0.000] |
| telemetry | final_accuracy | interaction_stress_minus_hfl_ideal | 2 | -0.100 | [-0.200, +0.000] |
| telemetry | mean_round_accuracy | alie_hfl_ideal | 2 | +0.000 | [+0.000, +0.000] |
| telemetry | mean_round_accuracy | alie_hfl_trace | 2 | +0.000 | [+0.000, +0.000] |
| telemetry | mean_round_accuracy | alie_hfl_trace_stress | 2 | +0.000 | [+0.000, +0.000] |
| telemetry | mean_round_accuracy | sign_flip_hfl_ideal | 2 | +0.000 | [+0.000, +0.000] |
| telemetry | mean_round_accuracy | sign_flip_hfl_trace | 2 | +0.050 | [+0.000, +0.100] |
| telemetry | mean_round_accuracy | sign_flip_hfl_trace_stress | 2 | -0.100 | [-0.200, +0.000] |
| telemetry | mean_round_accuracy | attacked_suite_seed_mean | 2 | -0.008 | [-0.017, +0.000] |
| telemetry | mean_round_accuracy | attacked_stress_seed_mean | 2 | -0.050 | [-0.100, +0.000] |
| telemetry | mean_round_accuracy | interaction_stress_minus_hfl_trace | 2 | -0.075 | [-0.150, +0.000] |
| telemetry | mean_round_accuracy | interaction_stress_minus_hfl_ideal | 2 | -0.050 | [-0.100, +0.000] |
| packet_mask | final_accuracy | alie_hfl_ideal | 2 | +0.000 | [+0.000, +0.000] |
| packet_mask | final_accuracy | alie_hfl_trace | 2 | -0.100 | [-0.200, +0.000] |
| packet_mask | final_accuracy | alie_hfl_trace_stress | 2 | +0.000 | [+0.000, +0.000] |
| packet_mask | final_accuracy | sign_flip_hfl_ideal | 2 | +0.000 | [+0.000, +0.000] |
| packet_mask | final_accuracy | sign_flip_hfl_trace | 2 | +0.000 | [+0.000, +0.000] |
| packet_mask | final_accuracy | sign_flip_hfl_trace_stress | 2 | -0.200 | [-0.400, +0.000] |
| packet_mask | final_accuracy | attacked_suite_seed_mean | 2 | -0.050 | [-0.100, +0.000] |
| packet_mask | final_accuracy | attacked_stress_seed_mean | 2 | -0.100 | [-0.200, +0.000] |
| packet_mask | final_accuracy | interaction_stress_minus_hfl_trace | 2 | -0.050 | [-0.100, +0.000] |
| packet_mask | final_accuracy | interaction_stress_minus_hfl_ideal | 2 | -0.100 | [-0.200, +0.000] |
| packet_mask | mean_round_accuracy | alie_hfl_ideal | 2 | +0.000 | [+0.000, +0.000] |
| packet_mask | mean_round_accuracy | alie_hfl_trace | 2 | -0.050 | [-0.100, +0.000] |
| packet_mask | mean_round_accuracy | alie_hfl_trace_stress | 2 | +0.000 | [+0.000, +0.000] |
| packet_mask | mean_round_accuracy | sign_flip_hfl_ideal | 2 | +0.000 | [+0.000, +0.000] |
| packet_mask | mean_round_accuracy | sign_flip_hfl_trace | 2 | +0.000 | [+0.000, +0.000] |
| packet_mask | mean_round_accuracy | sign_flip_hfl_trace_stress | 2 | -0.100 | [-0.200, +0.000] |
| packet_mask | mean_round_accuracy | attacked_suite_seed_mean | 2 | -0.025 | [-0.050, +0.000] |
| packet_mask | mean_round_accuracy | attacked_stress_seed_mean | 2 | -0.050 | [-0.100, +0.000] |
| packet_mask | mean_round_accuracy | interaction_stress_minus_hfl_trace | 2 | -0.025 | [-0.050, +0.000] |
| packet_mask | mean_round_accuracy | interaction_stress_minus_hfl_ideal | 2 | -0.050 | [-0.100, +0.000] |
| full_context | final_accuracy | alie_hfl_ideal | 2 | +0.000 | [+0.000, +0.000] |
| full_context | final_accuracy | alie_hfl_trace | 2 | -0.100 | [-0.200, +0.000] |
| full_context | final_accuracy | alie_hfl_trace_stress | 2 | +0.000 | [+0.000, +0.000] |
| full_context | final_accuracy | sign_flip_hfl_ideal | 2 | +0.000 | [+0.000, +0.000] |
| full_context | final_accuracy | sign_flip_hfl_trace | 2 | +0.100 | [+0.000, +0.200] |
| full_context | final_accuracy | sign_flip_hfl_trace_stress | 2 | -0.400 | [-0.800, +0.000] |
| full_context | final_accuracy | attacked_suite_seed_mean | 2 | -0.067 | [-0.133, +0.000] |
| full_context | final_accuracy | attacked_stress_seed_mean | 2 | -0.200 | [-0.400, +0.000] |
| full_context | final_accuracy | interaction_stress_minus_hfl_trace | 2 | -0.200 | [-0.400, +0.000] |
| full_context | final_accuracy | interaction_stress_minus_hfl_ideal | 2 | -0.200 | [-0.400, +0.000] |
| full_context | mean_round_accuracy | alie_hfl_ideal | 2 | +0.000 | [+0.000, +0.000] |
| full_context | mean_round_accuracy | alie_hfl_trace | 2 | -0.050 | [-0.100, +0.000] |
| full_context | mean_round_accuracy | alie_hfl_trace_stress | 2 | +0.000 | [+0.000, +0.000] |
| full_context | mean_round_accuracy | sign_flip_hfl_ideal | 2 | +0.000 | [+0.000, +0.000] |
| full_context | mean_round_accuracy | sign_flip_hfl_trace | 2 | +0.050 | [+0.000, +0.100] |
| full_context | mean_round_accuracy | sign_flip_hfl_trace_stress | 2 | -0.200 | [-0.400, +0.000] |
| full_context | mean_round_accuracy | attacked_suite_seed_mean | 2 | -0.033 | [-0.067, +0.000] |
| full_context | mean_round_accuracy | attacked_stress_seed_mean | 2 | -0.100 | [-0.200, +0.000] |
| full_context | mean_round_accuracy | interaction_stress_minus_hfl_trace | 2 | -0.100 | [-0.200, +0.000] |
| full_context | mean_round_accuracy | interaction_stress_minus_hfl_ideal | 2 | -0.100 | [-0.200, +0.000] |

## Run outcomes

| Method | Terminal | Diverged | All-run final accuracy (%) |
|---|---:|---:|---:|
| ccra | 12 | 0 | 10.00 |
| ccra_maskonly | 12 | 0 | 10.02 |
| ccra_noctx | 12 | 0 | 10.07 |
| fedavg | 12 | 0 | 10.10 |
| fltrust | 12 | 0 | 10.18 |
| median | 12 | 0 | 10.00 |
