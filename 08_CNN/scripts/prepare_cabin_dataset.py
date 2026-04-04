#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from split_dataset import split_classification


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare cabin cleanliness classification split from raw class folders.")
    parser.add_argument("--raw-root", type=Path, default=Path("08_CNN/data/cabin_cleanliness/raw"), help="Folder with class subfolders")
    parser.add_argument("--output-root", type=Path, default=Path("08_CNN/data/cabin_cleanliness"))
    parser.add_argument("--train-ratio", type=float, default=0.7)
    parser.add_argument("--val-ratio", type=float, default=0.15)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    if not args.raw_root.exists():
        raise FileNotFoundError(f"Raw root not found: {args.raw_root}")

    split_classification(
        data_root=args.raw_root,
        output_root=args.output_root,
        train_ratio=args.train_ratio,
        val_ratio=args.val_ratio,
        seed=args.seed,
    )


if __name__ == "__main__":
    main()
