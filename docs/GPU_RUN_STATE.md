# Full GPU study run state

Completed and validated on 28 October 2026: 720/720 terminal runs, 720 finite
checkpoints, ten paired partitions, zero artifact problems, 67 explicit numerical
divergences, and no unexpected process failure logs. The local copy passed the
same validation and analysis; the remote and local reports/checkpoint hash lists
match. The GPU instance is idle and can be stopped after review.

Launched 27 October 2026 on the supplied NVIDIA A100-SXM4-40GB instance.
Initial throughput indicates approximately 20–30 hours; this is preliminary and
not an uptime or completion guarantee. Eight workers are active under supervisor.

- SSH: `ssh -p 13378 root@212.13.234.23`
- Project: `/workspace/uav-context-study`
- Python: `/venv/main/bin/python`
- Supervisor: `uav_context_study`
- Remote outputs: `/workspace/uav-context-study/results/context_final`
- Local recovery: `results/context_final_gpu`
- Pinned training source: `485fa9f3fda70cc7b54a1871f677654ce95469d5`
- Training source SHA-256: `98a13e85169f56b05e627add6720b9f57cfc9b0bc88fc9137cd4325114947116`
- Full dataset SHA-256: `ebd37adf1cdd972d382b420ebefd070c9db63116626c24338ab1489af78f37ee`
- Prepared trace SHA-256: `68785bd1d5c03ef6e08b0bb46595aca785498f461ee0e48c40fbbeb921381a60`

The source archive and dependency/hardware records are backed up locally. The
small `context_status.py` helper was added after pinning and is read-only; it is
not training code. Both machines passed 37 tests. All 144 CPU pilot checkpoints
and all 12 CUDA preflight checkpoints passed artifact validation, with matching
paired client partitions and FLTrust optimizer-step checks where applicable.

A server-side supervisor process, `uav_context_guard`, checks mechanical health
once per minute without AI calls. It checks frozen configuration/source, matched
partitions, finite metrics/checkpoints, FLTrust root steps, progress, process errors,
and the ideal-link equality of mask-only versus no-context. The same fault must
appear in two consecutive checks before it stops the study process group and
writes `EARLY_ALERT.json`. It does not stop the rented instance. Recorded numerical
divergence is valid, and poor accuracy is a review cue rather than an automatic
stop. `EARLY_HEALTH.json` records the current state and completion milestones.

A quiet thread heartbeat, `monitor-uav-context-study`, performs the next startup
review on a 30-minute schedule, then checks every two hours until the first full
seed is complete, and every four hours thereafter. It reviews the first completed
batch and the first complete seed. Only clean-control learning
sanity checks are allowed at interim review: do not rank methods, tune parameters,
or alter the fixed design from partial results. It should notify only on an
actionable failure or final completion, and disable itself after recovery and
analysis. Local scheduling requires the computer and app to remain available.
Training and the per-minute mechanical guard run independently on the server.
The six guard regression tests include confirmation-before-stop, transient writes,
finite recovery from numerical divergence, and FLTrust step-budget mismatches.

The instance has no persistent workspace volume. Incremental backups omit model
checkpoints during training; final recovery includes all checkpoints. Preserve
the original study manifest unchanged. Analysis and artifact-validation scripts
support copied directories without rewriting their original remote paths.
Final results have been safely copied and locally validated. The instance can
be stopped to end GPU charges; do not destroy it without a separate decision.

The supervisor entry point runs the fixed final design, validates artifacts,
then computes the prespecified analysis. Completion means all 720 runs have a
terminal summary (including explicit numerical divergence), and validation
reports `valid: true` with 720 finite final checkpoints. An unexpected process
failure is distinct from scientific numerical divergence.

Laptop disconnection, sleep, closing Codex, or reaching the AI usage limit does
not stop server-side training or the health guard. Local AI reviews and backups
need the laptop/app/network; the next successful check reads continued progress
and syncs it. Failed SSH checks make one bounded attempt, rather than retrying
repeatedly. The GPU instance must remain running. AI reviews use allowance even
when silent; server training and the mechanical guard do not.
