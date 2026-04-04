# Baggage QC Labeling Guide

Create labels in YOLO format for each image in `images/all`.

## Classes
- `0`: intact_bag
- `1`: damaged_bag
- `2`: mishandled_bag

## Label file format
One text file per image with same stem, extension `.txt`:

```
class x_center y_center width height
```

All coordinates are normalized to [0,1].

## Folder convention
- Images: `08_CNN/data/baggage_qc/images/all`
- Labels: `08_CNN/data/baggage_qc/labels/all`

After labeling, run:

```bash
python 08_CNN/scripts/prepare_baggage_dataset.py
```
