"""Download CIFAR-10 from the HuggingFace mirror and cache it as data/cifar10.npz.

The official Toronto server is often very slow; this mirror is much faster.
If data/cifar10.npz exists, fl.data uses it instead of torchvision's downloader.

    python prepare_data.py
"""
from __future__ import annotations

import io
import os
import urllib.request

import numpy as np

BASE = "https://huggingface.co/datasets/uoft-cs/cifar10/resolve/main/plain_text/"
FILES = {"train": "train-00000-of-00001.parquet", "test": "test-00000-of-00001.parquet"}


def load_split(path: str):
    import pyarrow.parquet as pq
    from PIL import Image

    table = pq.read_table(path).to_pydict()
    imgs = np.stack([np.array(Image.open(io.BytesIO(d["bytes"])).convert("RGB")) for d in table["img"]])
    labels = np.array(table["label"], dtype=np.int64)
    return imgs.astype(np.uint8), labels


def main(data_dir: str = "data"):
    os.makedirs(data_dir, exist_ok=True)
    arrays = {}
    for split, fname in FILES.items():
        path = os.path.join(data_dir, fname)
        if not os.path.exists(path):
            print(f"Downloading {split} split ...")
            urllib.request.urlretrieve(BASE + fname, path)
        x, y = load_split(path)
        arrays[f"x_{split}"], arrays[f"y_{split}"] = x, y
        print(f"{split}: {x.shape} labels={np.bincount(y).tolist()}")
    out = os.path.join(data_dir, "cifar10.npz")
    np.savez_compressed(out, **arrays)
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
