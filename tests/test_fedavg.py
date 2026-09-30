from types import SimpleNamespace

import pytest
import torch

from fl.client import ClientUpdate
from fl.server import FedAvg, build_aggregator


def make_update(client_id, state, num_samples):
    return ClientUpdate(
        client_id=client_id,
        state_dict=state,
        delta={},
        num_samples=num_samples,
    )


def test_fedavg_computes_sample_weighted_average():
    cfg = SimpleNamespace(aggregator="fedavg")
    aggregator = FedAvg(cfg)

    global_state = {
        "weight": torch.tensor([0.0, 0.0]),
        "counter": torch.tensor(0, dtype=torch.int64),
    }

    update_1 = make_update(
        client_id=0,
        state={
            "weight": torch.tensor([1.0, 2.0]),
            "counter": torch.tensor(5, dtype=torch.int64),
        },
        num_samples=1,
    )

    update_2 = make_update(
        client_id=1,
        state={
            "weight": torch.tensor([3.0, 4.0]),
            "counter": torch.tensor(9, dtype=torch.int64),
        },
        num_samples=3,
    )

    new_state, info = aggregator.aggregate(
        global_state,
        [update_1, update_2],
    )

    # Weighted average:
    # (1/4) * [1, 2] + (3/4) * [3, 4] = [2.5, 3.5]
    assert torch.allclose(
        new_state["weight"],
        torch.tensor([2.5, 3.5]),
    )

    assert info["weights"] == {
        0: pytest.approx(0.25),
        1: pytest.approx(0.75),
    }

    # Existing FedAvg behaviour for non-floating buffers is preserved.
    assert new_state["counter"].item() == 5


def test_build_aggregator_passes_configuration():
    cfg = SimpleNamespace(aggregator="fedavg")

    aggregator = build_aggregator("fedavg", cfg)

    assert isinstance(aggregator, FedAvg)
    assert aggregator.cfg is cfg


def test_build_aggregator_rejects_unknown_name():
    cfg = SimpleNamespace(aggregator="unknown")

    with pytest.raises(ValueError, match="Unknown aggregator"):
        build_aggregator("unknown", cfg)