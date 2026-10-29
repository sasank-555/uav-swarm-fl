#!/usr/bin/env bash
set -euo pipefail
UAV_STUDY_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
UAV_STUDY_PYTHON="${UAV_STUDY_PYTHON:-/venv/main/bin/python}"
UAV_STUDY_PARALLEL="${UAV_STUDY_PARALLEL:-8}"
cd "$UAV_STUDY_ROOT"
export CUBLAS_WORKSPACE_CONFIG=:4096:8
export OMP_NUM_THREADS=2
export MKL_NUM_THREADS=2
export OPENBLAS_NUM_THREADS=1
export PYTHONUNBUFFERED=1
"$UAV_STUDY_PYTHON" -c 'import torch; assert torch.cuda.is_available(), "CUDA is required"; print(torch.__version__, torch.version.cuda, torch.cuda.get_device_name())'
"$UAV_STUDY_PYTHON" -m pip freeze > GPU_REQUIREMENTS.txt
nvidia-smi > GPU_ENVIRONMENT.txt
"$UAV_STUDY_PYTHON" run_context_study.py --profile final --device cuda --parallel "$UAV_STUDY_PARALLEL"
"$UAV_STUDY_PYTHON" validate_context_study.py results/context_final
"$UAV_STUDY_PYTHON" analyze_context_study.py results/context_final
printf 'Study, artifact validation, and analysis completed.\n'
