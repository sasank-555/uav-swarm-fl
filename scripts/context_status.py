"""Cheap, read-only progress snapshot; avoids importing the training runtime."""
import argparse
import csv
import json
import statistics
from pathlib import Path


def status(root):
    manifest = json.loads((root / 'study_manifest.json').read_text())
    terminal = diverged = rounds_done = 0
    active, seconds = [], []
    for job in manifest['jobs']:
        cfg = job['config']
        directory = root / f"seed{job['seed']}" / cfg['name']
        summary = directory / 'summary.json'
        if summary.exists():
            try:
                data = json.loads(summary.read_text())
                terminal += 1
                diverged += bool(data.get('diverged'))
                rounds_done += cfg['rounds']
                continue
            except (OSError, ValueError):
                pass
        metrics = directory / 'metrics.csv'
        if metrics.exists():
            with metrics.open() as handle:
                rows = list(csv.DictReader(handle))
            usable = []
            for row in rows:
                try:
                    seconds.append(float(row['round_time_s']))
                    usable.append(int(row['round']))
                except (TypeError, ValueError, KeyError):
                    pass
            current = max(usable, default=0)
            rounds_done += current
            active.append(f"seed{job['seed']}/{cfg['name']}: {current}/{cfg['rounds']}")
    remaining = sum(j['config']['rounds'] for j in manifest['jobs']) - rounds_done
    return {
        'terminal': terminal, 'planned': len(manifest['jobs']), 'diverged': diverged,
        'active_or_interrupted': active,
        'sampled_mean_round_s': round(statistics.fmean(seconds), 2) if seconds else None,
        'remaining_rounds_upper_bound': remaining,
        'complete_marker': (root / 'COMPLETE').exists(),
        'validated': (root / 'ARTIFACT_VALIDATION.json').exists(),
        'analysis_exists': (root / 'context_analysis.json').exists(),
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    print(json.dumps(status(parser.parse_args().root)))
