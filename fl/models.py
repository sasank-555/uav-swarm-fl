"""Lightweight CNN suitable for on-board (edge) training on a drone."""
from __future__ import annotations

import torch.nn as nn


def _block(c_in: int, c_out: int) -> nn.Sequential:
    # GroupNorm instead of BatchNorm: BN running statistics are known to break
    # under FedAvg with non-IID data, GN has no cross-batch state.
    return nn.Sequential(
        nn.Conv2d(c_in, c_out, 3, padding=1, bias=False),
        nn.GroupNorm(8, c_out),
        nn.ReLU(inplace=True),
    )


class LightCNN(nn.Module):
    """~0.4M parameter CNN: 3 conv stages (32-64-128) + small classifier."""

    def __init__(self, num_classes: int = 10, in_channels: int = 3):
        super().__init__()
        self.features = nn.Sequential(
            _block(in_channels, 32), _block(32, 32), nn.MaxPool2d(2),  # 16x16
            _block(32, 64), _block(64, 64), nn.MaxPool2d(2),           # 8x8
            _block(64, 128), nn.MaxPool2d(2),                          # 4x4
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Dropout(0.3),
            nn.Linear(128 * 4 * 4, 128),
            nn.ReLU(inplace=True),
            nn.Linear(128, num_classes),
        )

    def forward(self, x):
        return self.classifier(self.features(x))


class TacticalEdgeCNN(nn.Module):
    """~156k parameter CNN (16-32-64) with no normalisation layers.

    Sized for on-board training on a drone's embedded CPU: ~5x faster per
    epoch than LightCNN, and having no norm layers means the whole model state
    is plain weights (clean for FedAvg and for the Month 4 update statistics).
    """

    def __init__(self, num_classes: int = 10, in_channels: int = 3):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(in_channels, 16, 3, padding=1), nn.ReLU(inplace=True), nn.MaxPool2d(2),  # 16x16
            nn.Conv2d(16, 32, 3, padding=1), nn.ReLU(inplace=True), nn.MaxPool2d(2),           # 8x8
            nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(inplace=True), nn.MaxPool2d(2),           # 4x4
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64 * 4 * 4, 128),
            nn.ReLU(inplace=True),
            nn.Linear(128, num_classes),
        )

    def forward(self, x):
        return self.classifier(self.features(x))


MODELS = {"tacticaledge": TacticalEdgeCNN, "lightcnn": LightCNN}


def build_model(name: str = "tacticaledge", num_classes: int = 10) -> nn.Module:
    if name not in MODELS:
        raise ValueError(f"Unknown model '{name}'. Available: {list(MODELS)}")
    return MODELS[name](num_classes)
