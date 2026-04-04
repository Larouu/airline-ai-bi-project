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

2. Bootstrap public starter data
```bash
python 08_CNN/scripts/download_public_datasets.py --dry-run
python 08_CNN/scripts/download_public_datasets.py
```

You can edit `08_CNN/configs/public_data_sources.json` to enable Kaggle sources by setting a valid dataset slug.

3. Put additional media in raw folders
- `08_CNN/data/baggage_qc/raw`
- `08_CNN/data/crowd_analytics/raw`
- `08_CNN/data/cabin_cleanliness/raw`

4. Extract frames (if using videos)
```bash
python 08_CNN/scripts/extract_frames.py --input 08_CNN/data/crowd_analytics/raw --output 08_CNN/data/crowd_analytics/images/all --every-n 10
```

5. Split dataset
```bash
python 08_CNN/scripts/split_dataset.py --task detection --images-dir 08_CNN/data/crowd_analytics/images/all --labels-dir 08_CNN/data/crowd_analytics/labels/all --output-root 08_CNN/data/crowd_analytics
```

Alternative for crowd bootstrap from COCO128 (person-only):
```bash
python 08_CNN/scripts/prepare_crowd_person_dataset.py --images-dir 08_CNN/data/crowd_analytics/raw/coco128/images/train2017 --labels-dir 08_CNN/data/crowd_analytics/raw/coco128/labels/train2017 --output-root 08_CNN/data/crowd_analytics
```

6. Train YOLO
```bash
python 08_CNN/scripts/train_yolo.py --data 08_CNN/configs/yolo_crowd.yaml --model yolo11n.pt --epochs 30 --imgsz 640 --project 08_CNN/runs --name crowd_yolo
```

7. Train cabin cleanliness CNN
```bash
python 08_CNN/scripts/train_cabin_cleanliness.py --data-root 08_CNN/data/cabin_cleanliness --epochs 15 --img-size 224 --batch-size 16 --output-dir 08_CNN/models
```

8. Generate incident report from detections
```bash
python 08_CNN/scripts/generate_incident_report.py --detections-csv 08_CNN/reports/baggage_detections.csv --output 08_CNN/reports/incident_report.csv
```

## Notes
- For empty folders in git, add a `.gitkeep` file if needed.
- YOLO labels must follow YOLO txt format: `class x_center y_center width height` normalized in [0,1].

## Start the Other Two Tasks

### Baggage Handling QC
1. Put images in `08_CNN/data/baggage_qc/images/all`
2. Label YOLO txt files in `08_CNN/data/baggage_qc/labels/all`
3. Build split:
```bash
python 08_CNN/scripts/prepare_baggage_dataset.py
```
4. Train:
```bash
python 08_CNN/scripts/train_yolo.py --data 08_CNN/configs/yolo_baggage.yaml --model yolo11n.pt --epochs 30 --imgsz 640 --project 08_CNN/runs --name baggage_yolo
```

### Cabin Cleanliness Detection
1. Put class folders in `08_CNN/data/cabin_cleanliness/raw` with names:
	- `Clean`
	- `Needs_Attention`
	- `Dirty`
2. Build split:
```bash
python 08_CNN/scripts/prepare_cabin_dataset.py
```
3. Train:
```bash
python 08_CNN/scripts/train_cabin_cleanliness.py --data-root 08_CNN/data/cabin_cleanliness --epochs 15 --img-size 224 --batch-size 16 --output-dir 08_CNN/models
```
