#!/usr/bin/env python3
from __future__ import annotations

import argparse
import random
import shutil
from pathlib import Path


def split_indices(items: list[Path], train_ratio: float, val_ratio: float, seed: int) -> tuple[list[Path], list[Path], list[Path]]:
    random.seed(seed)
    items = items[:]
    random.shuffle(items)
    n = len(items)
    n_train = int(n * train_ratio)
    n_val = int(n * val_ratio)
    train = items[:n_train]
    val = items[n_train:n_train + n_val]
    test = items[n_train + n_val:]
    return train, val, test


def copy_group(files: list[Path], dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    for f in files:
        shutil.copy2(f, dest / f.name)


def split_detection(images_dir: Path, labels_dir: Path, output_root: Path, train_ratio: float, val_ratio: float, seed: int) -> None:
    images = sorted([p for p in images_dir.glob("*") if p.suffix.lower() in {".jpg", ".jpeg", ".png"}])
    train, val, test = split_indices(images, train_ratio, val_ratio, seed)

    for split_name, group in [("train", train), ("val", val), ("test", test)]:
        img_dest = output_root / "images" / split_name
        lbl_dest = output_root / "labels" / split_name
        img_dest.mkdir(parents=True, exist_ok=True)
        lbl_dest.mkdir(parents=True, exist_ok=True)
        for img in group:
            shutil.copy2(img, img_dest / img.name)
            lbl = labels_dir / f"{img.stem}.txt"
            if lbl.exists():
                shutil.copy2(lbl, lbl_dest / lbl.name)
            else:
                (lbl_dest / f"{img.stem}.txt").write_text("", encoding="utf-8")

    print(f"Detection split complete: train={len(train)} val={len(val)} test={len(test)}")


def split_classification(data_root: Path, output_root: Path, train_ratio: float, val_ratio: float, seed: int) -> None:
    classes = [d.name for d in data_root.iterdir() if d.is_dir()]
    for cls in classes:
        cls_files = sorted([p for p in (data_root / cls).glob("*") if p.suffix.lower() in {".jpg", ".jpeg", ".png"}])
        train, val, test = split_indices(cls_files, train_ratio, val_ratio, seed)
        copy_group(train, output_root / "train" / cls)
        copy_group(val, output_root / "val" / cls)
        copy_group(test, output_root / "test" / cls)
        print(f"{cls}: train={len(train)} val={len(val)} test={len(test)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Split datasets for detection/classification.")
    parser.add_argument("--task", choices=["detection", "classification"], required=True)
    parser.add_argument("--train-ratio", type=float, default=0.7)
    parser.add_argument("--val-ratio", type=float, default=0.15)
    parser.add_argument("--seed", type=int, default=42)

    parser.add_argument("--images-dir", type=Path)
    parser.add_argument("--labels-dir", type=Path)
    parser.add_argument("--data-root", type=Path)
    parser.add_argument("--output-root", type=Path, required=True)

    args = parser.parse_args()

    if args.task == "detection":
        if not args.images_dir or not args.labels_dir:
            raise ValueError("For detection, provide --images-dir and --labels-dir")
        split_detection(args.images_dir, args.labels_dir, args.output_root, args.train_ratio, args.val_ratio, args.seed)
    else:
        if not args.data_root:
            raise ValueError("For classification, provide --data-root")
        split_classification(args.data_root, args.output_root, args.train_ratio, args.val_ratio, args.seed)


if __name__ == "__main__":
    main()
