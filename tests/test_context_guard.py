import csv
from pathlib import Path

import torch

from run_context_study import write_json
from scripts.context_guard import inspect
from test_context_study import save_run


def prepare(tmp_path, method='ccra', diverged=False):
    job = save_run(tmp_path, 41, 'clean_hfl_ideal', method, 0.5, diverged)
    directory = Path(job['config']['out_dir']) / job['config']['name']
    write_json(directory / 'swarm_partition.json', {'drones': {'0': {'num_samples': 100}}})
    torch.save({'weight': torch.ones(3)}, directory / 'final_model.pt')
    write_json(tmp_path / 'study_manifest.json', {'jobs': [job], 'seeds': [41]})
    return job, directory


def test_guard_accepts_recorded_divergence_with_finite_recovery(tmp_path):
    prepare(tmp_path, diverged=True)
    report = inspect(tmp_path, {})
    assert report['terminal'] == 1
    assert report['errors'] == []


def test_guard_rechecks_a_bad_checkpoint_until_fixed(tmp_path):
    _, directory = prepare(tmp_path)
    torch.save({'weight': torch.tensor([float('nan')])}, directory / 'final_model.pt')
    cache = {}
    first = inspect(tmp_path, cache)
    second = inspect(tmp_path, cache)
    assert first['errors'] == second['errors']
    assert 'non-finite checkpoint' in first['errors'][0]
    torch.save({'weight': torch.ones(3)}, directory / 'final_model.pt')
    assert inspect(tmp_path, cache)['errors'] == []


def test_guard_checks_fltrust_steps_before_caching_success(tmp_path):
    _, directory = prepare(tmp_path, 'fltrust')
    rows = [{'round': r, 'test_acc': 0.5, 'cells': {'0': {'received': 1, 'client_ids': [0], 'root_optimizer_steps': 1}}} for r in (1, 2)]
    write_json(directory / 'history.json', rows)
    cache = {}
    first = inspect(tmp_path, cache)
    assert 'FLTrust step-budget mismatch' in first['errors'][0]
    assert inspect(tmp_path, cache)['errors'] == first['errors']


def test_guard_ignores_partial_csv_record_but_flags_nonfinite_complete_record(tmp_path):
    _, directory = prepare(tmp_path)
    fields = ['round', 'test_acc', 'test_loss', 'train_loss', 'mean_pdr', 'round_time_s']
    with (directory / 'metrics.csv').open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerow({'round': 1, 'test_acc': 0.2})
    assert inspect(tmp_path, {})['errors'] == []
    with (directory / 'metrics.csv').open('a', newline='') as handle:
        csv.DictWriter(handle, fieldnames=fields).writerow(dict(zip(fields, [2, 'nan', 2, 2, 1, 1])))
    assert 'invalid metrics' in inspect(tmp_path, {})['errors'][0]


def test_guard_stops_only_after_repeated_confirmed_fault(tmp_path, monkeypatch):
    import scripts.context_guard as guard
    report = {'terminal': 1, 'planned': 1, 'round_records': 1, 'errors': ['configuration mismatch'], 'review_cues': []}
    monkeypatch.setattr(guard, 'inspect', lambda root, cache: dict(report, errors=list(report['errors'])))
    monkeypatch.setattr(guard, 'read_json', lambda path: {'source_sha256': 'fixed'})
    monkeypatch.setattr(guard, 'source_digest', lambda: 'fixed')
    monkeypatch.setattr(guard.sys, 'argv', ['guard', str(tmp_path)])
    sleeps, calls = [], []
    monkeypatch.setattr(guard.time, 'sleep', lambda interval: sleeps.append(interval))
    monkeypatch.setattr(guard.subprocess, 'run', lambda args, **kwargs: calls.append(args))
    assert guard.main() == 1
    assert len(sleeps) == 1
    assert calls == [['supervisorctl', 'stop', 'uav_context_study']]
    assert (tmp_path / 'EARLY_ALERT.json').exists()


def test_transient_fault_does_not_stop_study(tmp_path, monkeypatch):
    import scripts.context_guard as guard
    reports = iter([
        {'terminal': 0, 'planned': 1, 'round_records': 1, 'errors': ['incomplete write'], 'review_cues': []},
        {'terminal': 1, 'planned': 1, 'round_records': 2, 'errors': [], 'review_cues': []},
    ])
    monkeypatch.setattr(guard, 'inspect', lambda root, cache: next(reports))
    monkeypatch.setattr(guard, 'read_json', lambda path: {'source_sha256': 'fixed'})
    monkeypatch.setattr(guard, 'source_digest', lambda: 'fixed')
    monkeypatch.setattr(guard.sys, 'argv', ['guard', str(tmp_path)])
    monkeypatch.setattr(guard.time, 'sleep', lambda interval: None)
    calls = []
    monkeypatch.setattr(guard.subprocess, 'run', lambda args, **kwargs: calls.append(args))
    assert guard.main() == 0
    assert calls == []
