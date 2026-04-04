#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import csv
from ultralytics import YOLO


def estimate_queue_length(person_count: int, factor: float) -> int:
    return int(round(person_count * factor))


def main() -> None:
    parser = argparse.ArgumentParser(description="Run YOLO inference and estimate queue length from person count.")
    parser.add_argument("--model", required=True, type=str, help="Path to trained YOLO model")
    parser.add_argument("--source", required=True, type=str, help="Image/video folder or file")
    parser.add_argument("--output-csv", required=True, type=Path)
    parser.add_argument("--queue-factor", default=0.6, type=float, help="Queue estimate factor")
    args = parser.parse_args()

    model = YOLO(args.model)
    results = model.predict(source=args.source, save=False, stream=True)

    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["image_name", "person_count", "estimated_queue_length"])
        for r in results:
            path = Path(r.path).name if r.path else "unknown"
            classes = r.boxes.cls.tolist() if r.boxes is not None else []
            person_count = sum(1 for c in classes if int(c) == 0)
            queue_len = estimate_queue_length(person_count, args.queue_factor)
            writer.writerow([path, person_count, queue_len])

    print(f"Saved queue analytics to: {args.output_csv}")


if __name__ == "__main__":
    main()
