#!/usr/bin/env python3
from __future__ import annotations

import argparse
import random
from pathlib import Path
import cv2


def augment_once(img):
    out = img.copy()

    if random.random() < 0.5:
        out = cv2.flip(out, 1)

    if random.random() < 0.7:
        alpha = random.uniform(0.8, 1.2)
        beta = random.randint(-20, 20)
        out = cv2.convertScaleAbs(out, alpha=alpha, beta=beta)

    if random.random() < 0.4:
        k = random.choice([3, 5])
        out = cv2.GaussianBlur(out, (k, k), 0)

    return out


def run(input_dir: Path, output_dir: Path, copies: int) -> int:
    output_dir.mkdir(parents=True, exist_ok=True)
    image_files = [p for p in input_dir.glob("*") if p.suffix.lower() in {".jpg", ".jpeg", ".png"}]

    saved = 0
    for img_path in image_files:
        img = cv2.imread(str(img_path))
        if img is None:
            continue
        for i in range(copies):
            aug = augment_once(img)
            out_name = f"{img_path.stem}_aug{i+1}{img_path.suffix.lower()}"
            cv2.imwrite(str(output_dir / out_name), aug)
            saved += 1
    return saved


def main() -> None:
    parser = argparse.ArgumentParser(description="Simple image augmentation utility.")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--copies", default=3, type=int)
    args = parser.parse_args()

    total = run(args.input, args.output, args.copies)
    print(f"Saved {total} augmented images to {args.output}")


if __name__ == "__main__":
    main()
