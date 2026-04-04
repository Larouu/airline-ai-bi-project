#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import cv2

VIDEO_EXTS = {".mp4", ".avi", ".mov", ".mkv", ".wmv"}


def extract_frames(input_dir: Path, output_dir: Path, every_n: int = 10, prefix: str = "frame") -> int:
    output_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for media in sorted(input_dir.rglob("*")):
        if media.suffix.lower() not in VIDEO_EXTS:
            continue
        cap = cv2.VideoCapture(str(media))
        if not cap.isOpened():
            continue
        frame_idx = 0
        base = media.stem
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            if frame_idx % every_n == 0:
                out_name = f"{prefix}_{base}_{frame_idx:06d}.jpg"
                cv2.imwrite(str(output_dir / out_name), frame)
                count += 1
            frame_idx += 1
        cap.release()
    return count


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract frames from videos.")
    parser.add_argument("--input", required=True, type=Path, help="Input folder containing videos")
    parser.add_argument("--output", required=True, type=Path, help="Output folder for extracted frames")
    parser.add_argument("--every-n", default=10, type=int, help="Save one frame every N frames")
    parser.add_argument("--prefix", default="frame", type=str, help="Filename prefix")
    args = parser.parse_args()

    total = extract_frames(args.input, args.output, args.every_n, args.prefix)
    print(f"Extracted {total} frames to {args.output}")


if __name__ == "__main__":
    main()
