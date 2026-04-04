#!/usr/bin/env python3
from __future__ import annotations

import argparse
import random
import shutil
from pathlib import Path

IMG_EXTS = {".jpg", ".jpeg", ".png"}


def read_person_only_labels(label_path: Path) -> list[str]:
    if not label_path.exists():
        return []
    person_lines: list[str] = []
    for line in label_path.read_text(encoding="utf-8").splitlines():
        parts = line.strip().split()
        if not parts:
            continue
        if parts[0] == "0":
            person_lines.append(line)
    return person_lines


def split_items(items: list[Path], train_ratio: float, val_ratio: float, seed: int) -> tuple[list[Path], list[Path], list[Path]]:
    random.seed(seed)
    seq = items[:]
    random.shuffle(seq)
    n = len(seq)
    n_train = int(n * train_ratio)
    n_val = int(n * val_ratio)
    train = seq[:n_train]
    val = seq[n_train:n_train + n_val]
    test = seq[n_train + n_val:]
    return train, val, test


def copy_split(group: list[Path], split_name: str, src_lbl_dir: Path, out_root: Path) -> int:
    out_img = out_root / "images" / split_name
    out_lbl = out_root / "labels" / split_name
    out_img.mkdir(parents=True, exist_ok=True)
    out_lbl.mkdir(parents=True, exist_ok=True)

    count = 0
    for img in group:
        src_lbl = src_lbl_dir / f"{img.stem}.txt"
        person_lines = read_person_only_labels(src_lbl)
        if not person_lines:
            continue

        shutil.copy2(img, out_img / img.name)
        (out_lbl / f"{img.stem}.txt").write_text("\n".join(person_lines) + "\n", encoding="utf-8")
        count += 1
    return count


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare crowd analytics dataset (person-only) from COCO-style labels.")
    parser.add_argument("--images-dir", type=Path, required=True, help="Source images directory")
    parser.add_argument("--labels-dir", type=Path, required=True, help="Source labels directory")
    parser.add_argument("--output-root", type=Path, default=Path("08_CNN/data/crowd_analytics"))
    parser.add_argument("--train-ratio", type=float, default=0.7)
    parser.add_argument("--val-ratio", type=float, default=0.15)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    if not args.images_dir.exists():
        raise FileNotFoundError(f"Images dir not found: {args.images_dir}")
    if not args.labels_dir.exists():
        raise FileNotFoundError(f"Labels dir not found: {args.labels_dir}")

    images = sorted([p for p in args.images_dir.glob("*") if p.suffix.lower() in IMG_EXTS])
    train, val, test = split_items(images, args.train_ratio, args.val_ratio, args.seed)

    train_n = copy_split(train, "train", args.labels_dir, args.output_root)
    val_n = copy_split(val, "val", args.labels_dir, args.output_root)
    test_n = copy_split(test, "test", args.labels_dir, args.output_root)

    total = train_n + val_n + test_n
    print(f"Prepared crowd dataset with person labels only.")
    print(f"train={train_n} val={val_n} test={test_n} total={total}")
    print(f"Output: {args.output_root}")


if __name__ == "__main__":
    main()
