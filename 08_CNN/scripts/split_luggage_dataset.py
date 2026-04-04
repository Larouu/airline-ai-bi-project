#!/usr/bin/env python3
from __future__ import annotations

import argparse
import random
import shutil
from pathlib import Path


IMG_EXTS = {".jpg", ".jpeg", ".png"}


def split_items(items: list[Path], train_ratio: float, val_ratio: float, seed: int) -> tuple[list[Path], list[Path], list[Path]]:
    rng = random.Random(seed)
    seq = items[:]
    rng.shuffle(seq)

    total = len(seq)
    train_count = int(total * train_ratio)
    val_count = int(total * val_ratio)
    test_count = total - train_count - val_count

    train = seq[:train_count]
    valid = seq[train_count : train_count + val_count]
    test = seq[train_count + val_count : train_count + val_count + test_count]
    return train, valid, test


def copy_pair(src_img: Path, src_lbl_dir: Path, dst_img_dir: Path, dst_lbl_dir: Path) -> None:
    dst_img_dir.mkdir(parents=True, exist_ok=True)
    dst_lbl_dir.mkdir(parents=True, exist_ok=True)

    shutil.copy2(src_img, dst_img_dir / src_img.name)
    src_label = src_lbl_dir / f"{src_img.stem}.txt"
    if src_label.exists():
        shutil.copy2(src_label, dst_lbl_dir / src_label.name)
    else:
        (dst_lbl_dir / f"{src_img.stem}.txt").write_text("", encoding="utf-8")


def rewrite_dataset_yaml(dataset_root: Path) -> None:
    classes_path = dataset_root / "classes.txt"
    names = [line.strip() for line in classes_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    yaml_text = (
        f"path: {dataset_root}\n"
        "train: images/train\n"
        "val: images/valid\n"
        "test: images/test\n\n"
        f"nc: {len(names)}\n"
        f"names: {names}\n"
    )
    (dataset_root / "dataset.yaml").write_text(yaml_text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Split luggage dataset from one train pool into train/valid/test.")
    parser.add_argument("--dataset-root", type=Path, default=Path("08_CNN/data/luggage"))
    parser.add_argument("--train-ratio", type=float, default=0.7)
    parser.add_argument("--val-ratio", type=float, default=0.15)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--overwrite", action="store_true", help="Delete existing valid/test splits before writing")
    args = parser.parse_args()

    if args.train_ratio <= 0 or args.val_ratio < 0 or (args.train_ratio + args.val_ratio) >= 1:
        raise ValueError("Ratios must satisfy: train_ratio > 0, val_ratio >= 0, train_ratio + val_ratio < 1")

    dataset_root = args.dataset_root
    images_train = dataset_root / "images" / "train"
    labels_train = dataset_root / "labels" / "train"

    if not images_train.exists() or not labels_train.exists():
        raise FileNotFoundError("Expected source folders: images/train and labels/train")

    source_images = sorted([p for p in images_train.iterdir() if p.is_file() and p.suffix.lower() in IMG_EXTS])
    if not source_images:
        raise RuntimeError("No source images found in images/train")

    if args.overwrite:
        for split_name in ("valid", "test"):
            for branch in ("images", "labels"):
                split_dir = dataset_root / branch / split_name
                if split_dir.exists():
                    shutil.rmtree(split_dir)

    train_items, valid_items, test_items = split_items(
        source_images,
        train_ratio=args.train_ratio,
        val_ratio=args.val_ratio,
        seed=args.seed,
    )

    temp_root = dataset_root / ".split_tmp"
    if temp_root.exists():
        shutil.rmtree(temp_root)

    for split_name, items in (("train", train_items), ("valid", valid_items), ("test", test_items)):
        for img_path in items:
            copy_pair(
                src_img=img_path,
                src_lbl_dir=labels_train,
                dst_img_dir=temp_root / "images" / split_name,
                dst_lbl_dir=temp_root / "labels" / split_name,
            )

    for branch in ("images", "labels"):
        target_root = dataset_root / branch
        if target_root.exists():
            shutil.rmtree(target_root)
        shutil.move(str(temp_root / branch), str(target_root))

    if temp_root.exists():
        shutil.rmtree(temp_root)

    rewrite_dataset_yaml(dataset_root)

    print("Luggage split complete")
    print(f"train={len(train_items)} valid={len(valid_items)} test={len(test_items)}")
    print(f"dataset={dataset_root}")


if __name__ == "__main__":
    main()