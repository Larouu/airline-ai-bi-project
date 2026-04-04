#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import zipfile
from pathlib import Path
from urllib.request import urlretrieve


def load_config(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def download_zip(url: str, destination_zip: Path) -> None:
    ensure_dir(destination_zip.parent)
    urlretrieve(url, destination_zip)


def extract_zip(zip_path: Path, target_dir: Path) -> None:
    ensure_dir(target_dir)
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(target_dir)


def run_kaggle_download(dataset: str, target_dir: Path, unzip: bool = True) -> None:
    ensure_dir(target_dir)
    cmd = ["kaggle", "datasets", "download", "-d", dataset, "-p", str(target_dir)]
    if unzip:
        cmd.append("--unzip")
    subprocess.run(cmd, check=True)


def process_sources(config: dict, repo_root: Path, dry_run: bool = False) -> None:
    sources = config.get("sources", [])
    if not sources:
        print("No sources found in config.")
        return

    for src in sources:
        if not src.get("enabled", False):
            continue

        src_type = src.get("type", "")
        name = src.get("name", "unnamed_source")
        task = src.get("task", "unknown")

        print(f"[INFO] Source: {name} | task={task} | type={src_type}")

        if src_type == "direct_zip":
            url = src["url"]
            target = repo_root / src["target_dir"]
            zip_path = target / f"{name}.zip"
            if dry_run:
                print(f"  DRY-RUN download: {url} -> {zip_path}")
                print(f"  DRY-RUN extract to: {target}")
                continue

            download_zip(url, zip_path)
            if src.get("extract", True):
                extract_zip(zip_path, target)
            print(f"  DONE direct zip: {target}")

        elif src_type == "kaggle":
            dataset = src["dataset"]
            target = repo_root / src["target_dir"]
            if "replace-with-valid-kaggle-dataset-slug" in dataset:
                print("  SKIP kaggle source: set a valid dataset slug first.")
                continue
            if dry_run:
                print(f"  DRY-RUN kaggle download: {dataset} -> {target}")
                continue

            try:
                run_kaggle_download(dataset, target, unzip=src.get("extract", True))
                print(f"  DONE kaggle source: {target}")
            except Exception as exc:
                print(f"  ERROR kaggle download failed: {exc}")

        elif src_type == "manual_note":
            print(f"  NOTE: {src.get('message', '')}")

        else:
            print(f"  SKIP unknown source type: {src_type}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Download/bootstrap public datasets for 08_CNN tasks.")
    parser.add_argument(
        "--config",
        default="08_CNN/configs/public_data_sources.json",
        type=str,
        help="Path to data sources config JSON",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print actions without downloading")
    args = parser.parse_args()

    script_path = Path(__file__).resolve()
    repo_root = script_path.parents[2]
    config_path = repo_root / args.config

    if not config_path.exists():
        raise FileNotFoundError(f"Config not found: {config_path}")

    config = load_config(config_path)
    process_sources(config, repo_root, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
