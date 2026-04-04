#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from split_dataset import split_detection


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare baggage detection dataset from all/ folders.")
    parser.add_argument("--images-dir", type=Path, default=Path("08_CNN/data/baggage_qc/images/all"))
    parser.add_argument("--labels-dir", type=Path, default=Path("08_CNN/data/baggage_qc/labels/all"))
    parser.add_argument("--output-root", type=Path, default=Path("08_CNN/data/baggage_qc"))
    parser.add_argument("--train-ratio", type=float, default=0.7)
    parser.add_argument("--val-ratio", type=float, default=0.15)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    if not args.images_dir.exists():
        raise FileNotFoundError(f"Images dir not found: {args.images_dir}")
    if not args.labels_dir.exists():
        raise FileNotFoundError(f"Labels dir not found: {args.labels_dir}")

    split_detection(
        images_dir=args.images_dir,
        labels_dir=args.labels_dir,
        output_root=args.output_root,
        train_ratio=args.train_ratio,
        val_ratio=args.val_ratio,
        seed=args.seed,
    )


if __name__ == "__main__":
    main()
