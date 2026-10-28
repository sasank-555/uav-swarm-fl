# Controlled context study

Paired percentile bootstrap over seeds. Primary contrast: telemetry gain under stress minus telemetry gain on the same unstressed trace, averaged over attacks per seed. Other contrasts are exploratory; intervals have no multiplicity adjustment.

Terminal runs: 720/720. Diverged final accuracy is scored at 10.0%.
Mean-round accuracy uses the fixed requested horizon, with chance from divergence onward.
Intervals resample seeds; rounds and attack/condition cells are not independent replicates.
The final design uses at least ten paired seeds and 100 rounds by default.

Predefined practical threshold: 1.00 percentage points.
Primary assessment: meaningful negative effect supported
A positive stress interaction alone does not establish positive absolute benefit under stress; inspect both contrasts.

| Contrast | Metric | Scope | Seeds | Gain (pp) | Paired bootstrap 95% interval (pp) |
|---|---|---|---:|---:|---|
| telemetry | final_accuracy | alie_hfl_ideal | 10 | -0.107 | [-0.794, +0.731] |
| telemetry | final_accuracy | alie_hfl_trace | 10 | -0.832 | [-2.053, +0.341] |
| telemetry | final_accuracy | alie_hfl_trace_stress | 10 | -3.881 | [-5.429, -2.464] |
| telemetry | final_accuracy | clean_hfl_ideal | 10 | -1.690 | [-3.233, -0.262] |
| telemetry | final_accuracy | clean_hfl_trace | 10 | -0.882 | [-1.414, -0.422] |
| telemetry | final_accuracy | clean_hfl_trace_stress | 10 | -2.112 | [-2.736, -1.474] |
| telemetry | final_accuracy | ipm_hfl_ideal | 10 | -0.752 | [-1.606, +0.024] |
| telemetry | final_accuracy | ipm_hfl_trace | 10 | -0.720 | [-1.442, -0.021] |
| telemetry | final_accuracy | ipm_hfl_trace_stress | 10 | -3.214 | [-5.142, -1.364] |
| telemetry | final_accuracy | sign_flip_hfl_ideal | 10 | -1.690 | [-3.198, -0.413] |
| telemetry | final_accuracy | sign_flip_hfl_trace | 10 | -0.779 | [-1.637, +0.048] |
| telemetry | final_accuracy | sign_flip_hfl_trace_stress | 10 | -3.397 | [-5.429, -1.635] |
| telemetry | final_accuracy | attacked_suite_seed_mean | 10 | -1.708 | [-2.574, -1.050] |
| telemetry | final_accuracy | attacked_stress_seed_mean | 10 | -3.497 | [-5.085, -2.140] |
| telemetry | final_accuracy | interaction_stress_minus_hfl_trace | 10 | -2.720 | [-3.899, -1.508] |
| telemetry | final_accuracy | interaction_stress_minus_hfl_ideal | 10 | -2.648 | [-3.945, -1.399] |
| telemetry | mean_round_accuracy | alie_hfl_ideal | 10 | -0.651 | [-1.124, -0.183] |
| telemetry | mean_round_accuracy | alie_hfl_trace | 10 | -0.550 | [-1.156, -0.015] |
| telemetry | mean_round_accuracy | alie_hfl_trace_stress | 10 | -2.722 | [-3.494, -1.907] |
| telemetry | mean_round_accuracy | clean_hfl_ideal | 10 | -0.879 | [-1.172, -0.640] |
| telemetry | mean_round_accuracy | clean_hfl_trace | 10 | -0.620 | [-1.139, -0.016] |
| telemetry | mean_round_accuracy | clean_hfl_trace_stress | 10 | -2.017 | [-2.635, -1.389] |
| telemetry | mean_round_accuracy | ipm_hfl_ideal | 10 | -0.370 | [-0.859, +0.145] |
| telemetry | mean_round_accuracy | ipm_hfl_trace | 10 | -0.838 | [-1.174, -0.502] |
| telemetry | mean_round_accuracy | ipm_hfl_trace_stress | 10 | -1.666 | [-2.183, -1.227] |
| telemetry | mean_round_accuracy | sign_flip_hfl_ideal | 10 | -0.987 | [-1.676, -0.433] |
| telemetry | mean_round_accuracy | sign_flip_hfl_trace | 10 | -1.094 | [-1.619, -0.555] |
| telemetry | mean_round_accuracy | sign_flip_hfl_trace_stress | 10 | -2.765 | [-3.804, -1.793] |
| telemetry | mean_round_accuracy | attacked_suite_seed_mean | 10 | -1.294 | [-1.696, -0.899] |
| telemetry | mean_round_accuracy | attacked_stress_seed_mean | 10 | -2.385 | [-3.020, -1.735] |
| telemetry | mean_round_accuracy | interaction_stress_minus_hfl_trace | 10 | -1.557 | [-2.267, -0.852] |
| telemetry | mean_round_accuracy | interaction_stress_minus_hfl_ideal | 10 | -1.715 | [-2.255, -1.162] |
| packet_mask | final_accuracy | alie_hfl_ideal | 10 | +0.000 | [+0.000, +0.000] |
| packet_mask | final_accuracy | alie_hfl_trace | 10 | +0.136 | [-0.976, +1.470] |
| packet_mask | final_accuracy | alie_hfl_trace_stress | 10 | +4.770 | [+2.529, +7.114] |
| packet_mask | final_accuracy | clean_hfl_ideal | 10 | +0.000 | [+0.000, +0.000] |
| packet_mask | final_accuracy | clean_hfl_trace | 10 | +0.767 | [+0.096, +1.629] |
| packet_mask | final_accuracy | clean_hfl_trace_stress | 10 | +3.660 | [+1.850, +5.426] |
| packet_mask | final_accuracy | ipm_hfl_ideal | 10 | +0.000 | [+0.000, +0.000] |
| packet_mask | final_accuracy | ipm_hfl_trace | 10 | -0.554 | [-1.244, +0.043] |
| packet_mask | final_accuracy | ipm_hfl_trace_stress | 10 | +4.132 | [+2.021, +5.712] |
| packet_mask | final_accuracy | sign_flip_hfl_ideal | 10 | +0.000 | [+0.000, +0.000] |
| packet_mask | final_accuracy | sign_flip_hfl_trace | 10 | -0.201 | [-1.044, +0.507] |
| packet_mask | final_accuracy | sign_flip_hfl_trace_stress | 10 | +3.785 | [+0.945, +6.319] |
| packet_mask | final_accuracy | attacked_suite_seed_mean | 10 | +1.341 | [+0.647, +1.922] |
| packet_mask | final_accuracy | attacked_stress_seed_mean | 10 | +4.229 | [+2.158, +5.876] |
| packet_mask | final_accuracy | interaction_stress_minus_hfl_trace | 10 | +4.435 | [+2.373, +6.052] |
| packet_mask | final_accuracy | interaction_stress_minus_hfl_ideal | 10 | +4.229 | [+2.158, +5.876] |
| packet_mask | mean_round_accuracy | alie_hfl_ideal | 10 | +0.000 | [+0.000, +0.000] |
| packet_mask | mean_round_accuracy | alie_hfl_trace | 10 | -0.128 | [-0.369, +0.106] |
| packet_mask | mean_round_accuracy | alie_hfl_trace_stress | 10 | +2.251 | [+1.372, +3.168] |
| packet_mask | mean_round_accuracy | clean_hfl_ideal | 10 | +0.000 | [+0.000, +0.000] |
| packet_mask | mean_round_accuracy | clean_hfl_trace | 10 | -0.117 | [-0.244, +0.006] |
| packet_mask | mean_round_accuracy | clean_hfl_trace_stress | 10 | +2.016 | [+1.485, +2.618] |
| packet_mask | mean_round_accuracy | ipm_hfl_ideal | 10 | +0.000 | [+0.000, +0.000] |
| packet_mask | mean_round_accuracy | ipm_hfl_trace | 10 | +0.043 | [-0.121, +0.208] |
| packet_mask | mean_round_accuracy | ipm_hfl_trace_stress | 10 | +2.802 | [+1.948, +3.711] |
| packet_mask | mean_round_accuracy | sign_flip_hfl_ideal | 10 | +0.000 | [+0.000, +0.000] |
| packet_mask | mean_round_accuracy | sign_flip_hfl_trace | 10 | +0.099 | [-0.098, +0.331] |
| packet_mask | mean_round_accuracy | sign_flip_hfl_trace_stress | 10 | +1.548 | [+0.677, +2.375] |
| packet_mask | mean_round_accuracy | attacked_suite_seed_mean | 10 | +0.735 | [+0.456, +1.012] |
| packet_mask | mean_round_accuracy | attacked_stress_seed_mean | 10 | +2.200 | [+1.382, +3.011] |
| packet_mask | mean_round_accuracy | interaction_stress_minus_hfl_trace | 10 | +2.196 | [+1.389, +3.016] |
| packet_mask | mean_round_accuracy | interaction_stress_minus_hfl_ideal | 10 | +2.200 | [+1.382, +3.011] |
| full_context | final_accuracy | alie_hfl_ideal | 10 | -0.107 | [-0.794, +0.731] |
| full_context | final_accuracy | alie_hfl_trace | 10 | -0.696 | [-1.376, -0.060] |
| full_context | final_accuracy | alie_hfl_trace_stress | 10 | +0.889 | [-1.098, +2.566] |
| full_context | final_accuracy | clean_hfl_ideal | 10 | -1.690 | [-3.233, -0.262] |
| full_context | final_accuracy | clean_hfl_trace | 10 | -0.115 | [-0.854, +0.863] |
| full_context | final_accuracy | clean_hfl_trace_stress | 10 | +1.548 | [+0.148, +2.959] |
| full_context | final_accuracy | ipm_hfl_ideal | 10 | -0.752 | [-1.606, +0.024] |
| full_context | final_accuracy | ipm_hfl_trace | 10 | -1.274 | [-1.946, -0.612] |
| full_context | final_accuracy | ipm_hfl_trace_stress | 10 | +0.918 | [-0.925, +2.709] |
| full_context | final_accuracy | sign_flip_hfl_ideal | 10 | -1.690 | [-3.198, -0.413] |
| full_context | final_accuracy | sign_flip_hfl_trace | 10 | -0.980 | [-1.797, -0.169] |
| full_context | final_accuracy | sign_flip_hfl_trace_stress | 10 | +0.388 | [-1.631, +2.556] |
| full_context | final_accuracy | attacked_suite_seed_mean | 10 | -0.367 | [-1.061, +0.272] |
| full_context | final_accuracy | attacked_stress_seed_mean | 10 | +0.732 | [-0.903, +2.127] |
| full_context | final_accuracy | interaction_stress_minus_hfl_trace | 10 | +1.715 | [+0.044, +3.075] |
| full_context | final_accuracy | interaction_stress_minus_hfl_ideal | 10 | +1.581 | [+0.052, +2.886] |
| full_context | mean_round_accuracy | alie_hfl_ideal | 10 | -0.651 | [-1.124, -0.183] |
| full_context | mean_round_accuracy | alie_hfl_trace | 10 | -0.678 | [-1.252, -0.157] |
| full_context | mean_round_accuracy | alie_hfl_trace_stress | 10 | -0.472 | [-1.260, +0.382] |
| full_context | mean_round_accuracy | clean_hfl_ideal | 10 | -0.879 | [-1.172, -0.640] |
| full_context | mean_round_accuracy | clean_hfl_trace | 10 | -0.737 | [-1.227, -0.182] |
| full_context | mean_round_accuracy | clean_hfl_trace_stress | 10 | -0.001 | [-0.716, +0.747] |
| full_context | mean_round_accuracy | ipm_hfl_ideal | 10 | -0.370 | [-0.859, +0.145] |
| full_context | mean_round_accuracy | ipm_hfl_trace | 10 | -0.795 | [-1.120, -0.426] |
| full_context | mean_round_accuracy | ipm_hfl_trace_stress | 10 | +1.136 | [+0.349, +2.087] |
| full_context | mean_round_accuracy | sign_flip_hfl_ideal | 10 | -0.987 | [-1.676, -0.433] |
| full_context | mean_round_accuracy | sign_flip_hfl_trace | 10 | -0.995 | [-1.527, -0.497] |
| full_context | mean_round_accuracy | sign_flip_hfl_trace_stress | 10 | -1.217 | [-2.453, -0.082] |
| full_context | mean_round_accuracy | attacked_suite_seed_mean | 10 | -0.559 | [-0.935, -0.139] |
| full_context | mean_round_accuracy | attacked_stress_seed_mean | 10 | -0.184 | [-0.949, +0.580] |
| full_context | mean_round_accuracy | interaction_stress_minus_hfl_trace | 10 | +0.638 | [-0.253, +1.429] |
| full_context | mean_round_accuracy | interaction_stress_minus_hfl_ideal | 10 | +0.485 | [-0.339, +1.187] |

## Run outcomes

| Method | Terminal | Diverged | All-run final accuracy (%) |
|---|---:|---:|---:|
| ccra | 120 | 0 | 51.13 |
| ccra_maskonly | 120 | 0 | 52.80 |
| ccra_noctx | 120 | 0 | 51.43 |
| fedavg | 120 | 41 | 37.27 |
| fltrust | 120 | 0 | 50.64 |
| median | 120 | 26 | 29.25 |
