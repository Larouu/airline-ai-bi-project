#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd


SEVERITY_MAP = {
    "damaged_bag": "high",
    "mishandled_bag": "medium",
    "intact_bag": "low",
}


def build_report(df: pd.DataFrame) -> pd.DataFrame:
    required = {"timestamp", "camera_id", "image_name", "predicted_class", "confidence"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    incidents = df[df["predicted_class"].isin(["damaged_bag", "mishandled_bag"])].copy()
    incidents["severity"] = incidents["predicted_class"].map(SEVERITY_MAP).fillna("medium")
    incidents["incident_type"] = incidents["predicted_class"].replace(
        {"damaged_bag": "Damage", "mishandled_bag": "Mishandling"}
    )
    incidents["action"] = incidents["severity"].map(
        {
            "high": "Dispatch supervisor and isolate baggage",
            "medium": "Flag to operations desk for review",
            "low": "No action",
        }
    )

    cols = [
        "timestamp",
        "camera_id",
        "image_name",
        "incident_type",
        "predicted_class",
        "confidence",
        "severity",
        "action",
    ]
    return incidents[cols].sort_values(["timestamp", "severity"], ascending=[True, False])


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate baggage incident report from detections CSV.")
    parser.add_argument("--detections-csv", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    df = pd.read_csv(args.detections_csv)
    report = build_report(df)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    report.to_csv(args.output, index=False)
    print(f"Incident report generated: {args.output}")
    print(f"Incidents found: {len(report)}")


if __name__ == "__main__":
    main()
