# 08_CNN Starter Pipeline

This folder contains a starter vision pipeline for:
- Baggage Handling QC (detection + incident reports)
- Airport Crowd Analytics (YOLO person counting)
- Cabin Cleanliness Detection (CNN classification)

## Quick Start

1. Install dependencies
```bash
pip install -r 08_CNN/requirements.txt
```

2. Put media in raw folders
- `08_CNN/data/baggage_qc/raw`
- `08_CNN/data/crowd_analytics/raw`
- `08_CNN/data/cabin_cleanliness/raw`

3. Extract frames (if using videos)
```bash
python 08_CNN/scripts/extract_frames.py --input 08_CNN/data/crowd_analytics/raw --output 08_CNN/data/crowd_analytics/images/all --every-n 10
```

4. Split dataset
```bash
python 08_CNN/scripts/split_dataset.py --task detection --images-dir 08_CNN/data/crowd_analytics/images/all --labels-dir 08_CNN/data/crowd_analytics/labels/all --output-root 08_CNN/data/crowd_analytics
```

5. Train YOLO
```bash
python 08_CNN/scripts/train_yolo.py --data 08_CNN/configs/yolo_crowd.yaml --model yolo11n.pt --epochs 30 --imgsz 640 --project 08_CNN/runs --name crowd_yolo
```

6. Train cabin cleanliness CNN
```bash
python 08_CNN/scripts/train_cabin_cleanliness.py --data-root 08_CNN/data/cabin_cleanliness --epochs 15 --img-size 224 --batch-size 16 --output-dir 08_CNN/models
```

7. Generate incident report from detections
```bash
python 08_CNN/scripts/generate_incident_report.py --detections-csv 08_CNN/reports/baggage_detections.csv --output 08_CNN/reports/incident_report.csv
```

## Notes
- For empty folders in git, add a `.gitkeep` file if needed.
- YOLO labels must follow YOLO txt format: `class x_center y_center width height` normalized in [0,1].
