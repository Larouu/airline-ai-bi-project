"""
Extract and convert Roboflow OpenAI Vision format datasets to YOLO format.
Downloads images from URLs and converts bounding boxes to normalized YOLO format.
"""

import argparse
import hashlib
import io
import json
import logging
import re
import shutil
import zipfile
from collections import defaultdict
from pathlib import Path
from urllib.request import urlopen

from PIL import Image

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# images getting from https://universe.roboflow.com/
class RoboflowExtractor:
    """Extract Roboflow OpenAI Vision format datasets."""
    
    def __init__(self, extract_dir, output_dir, cache_dir=None):
        self.extract_dir = Path(extract_dir)
        self.output_dir = Path(output_dir)
        self.cache_dir = Path(cache_dir) if cache_dir else self.output_dir / '.image_cache'
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _resolve_zip_path(self, zip_name):
        return self.extract_dir / 'temp' / zip_name

    def _ensure_extracted(self, zip_name, temp_folder):
        """Extract a Roboflow zip archive into its temp folder if needed."""
        source_zip = self._resolve_zip_path(zip_name)
        target_dir = self.extract_dir / 'temp' / temp_folder

        if not source_zip.exists():
            raise FileNotFoundError(f"Missing archive: {source_zip}")

        target_dir.mkdir(parents=True, exist_ok=True)
        if not list(target_dir.glob('*.jsonl')):
            logger.info(f"Extracting {source_zip.name} to {target_dir}")
            with zipfile.ZipFile(source_zip) as archive:
                archive.extractall(target_dir)

        return target_dir

    def _normalize_label(self, label, classes_list):
        label = label.strip()
        if not label:
            return None

        if label in classes_list:
            return label

        if label.isdigit() and label in classes_list:
            return label

        if label.isdigit():
            label_index = int(label)
            if 0 <= label_index < len(classes_list):
                return classes_list[label_index]

        fixes = {
            'luggege': 'luggage',
            'plastick_bag': 'plastic_bag',
        }
        fixed_label = fixes.get(label, label)
        if fixed_label in classes_list:
            return fixed_label

        return label

    def _parse_annotation_items(self, assistant_content, classes_list):
        """Return ordered (box, label) pairs from one assistant response."""
        items = []
        segments = [segment.strip() for segment in assistant_content.split(';') if segment.strip()]

        for segment in segments:
            locations = re.findall(r'<loc(\d{4})>', segment)
            if len(locations) < 4:
                continue

            box = [int(value) / 1000.0 for value in locations[:4]]
            label = re.sub(r'<loc\d{4}>', '', segment).strip()
            label = self._normalize_label(label, classes_list)

            if label:
                items.append((box, label))

        return items
        
    def parse_location_boxes(self, loc_string):
        """
        Convert OpenAI Vision location format <loc0490><loc0800><loc0969><loc0823> to boxes.
        Format: <locYYYY> represents 1000-normalized coordinates (0-1000 scale).
        Returns list of boxes as [x1, y1, x2, y2] in 0-1 normalized format.
        """
        # Find all <locXXXX> patterns
        pattern = r'<loc(\d{4})>'
        matches = re.findall(pattern, loc_string)
        
        boxes = []
        # Group into sets of 4 (x1, y1, x2, y2)
        for i in range(0, len(matches) - 3, 4):
            x1 = int(matches[i]) / 1000.0
            y1 = int(matches[i+1]) / 1000.0
            x2 = int(matches[i+2]) / 1000.0
            y2 = int(matches[i+3]) / 1000.0
            boxes.append([x1, y1, x2, y2])
        
        return boxes
    
    def box_to_yolo_format(self, box, img_width=640, img_height=640):
        """
        Convert [x1, y1, x2, y2] normalized (0-1) to YOLO format.
        YOLO format: x_center y_center width height (all normalized 0-1)
        """
        x1, y1, x2, y2 = box
        x_center = (x1 + x2) / 2
        y_center = (y1 + y2) / 2
        width = x2 - x1
        height = y2 - y1
        
        # Clamp to valid range
        x_center = max(0.0, min(1.0, x_center))
        y_center = max(0.0, min(1.0, y_center))
        width = max(0.0, min(1.0, width))
        height = max(0.0, min(1.0, height))
        
        return x_center, y_center, width, height
    
    def download_image(self, url, max_retries=3):
        """Download image from URL with retry logic."""
        url_hash = hashlib.md5(url.encode()).hexdigest()
        cache_path = self.cache_dir / f"{url_hash}.jpg"
        
        if cache_path.exists():
            logger.debug(f"Cache hit for {url[:60]}...")
            try:
                return Image.open(cache_path)
            except Exception as e:
                logger.warning(f"Failed to load cached image: {e}")
                cache_path.unlink()
        
        for attempt in range(max_retries):
            try:
                logger.debug(f"Downloading {url[:60]}... (attempt {attempt+1}/{max_retries})")
                response = urlopen(url, timeout=10)
                img = Image.open(io.BytesIO(response.read())).convert('RGB')
                img.load()
                
                # Cache the image
                img.save(cache_path, 'JPEG')
                return img
            except Exception as e:
                logger.warning(f"Attempt {attempt+1} failed: {e}")
                if attempt == max_retries - 1:
                    return None
        
        return None
    
    def extract_dataset(self, dataset_name, source_dir, jsonl_files):
        """
        Extract a single dataset.
        
        Args:
            dataset_name: Name of dataset (luggage, crowd, cabin)
            jsonl_files: List of JSONL files (train, valid, test)
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"Extracting {dataset_name.upper()} dataset")
        logger.info(f"{'='*60}")
        
        stats = defaultdict(int)
        all_labels = set()
        class_order = []
        
        # Parse all JSONL files to extract annotations
        annotations_by_split = {}
        
        for split_file in jsonl_files:
            split_file = Path(split_file)
            split_name = split_file.stem.split('.')[-1]  # train, valid, test
            split_path = source_dir / split_file
            
            if not split_path.exists():
                logger.warning(f"File not found: {split_path}")
                continue
            
            logger.info(f"\nParsing {split_name} split ({split_file})...")
            
            annotations = []
            with open(split_path, 'r', encoding='utf-8') as f:
                for line_idx, line in enumerate(f):
                    try:
                        data = json.loads(line)
                        messages = data.get('messages', [])
                        
                        # Extract image URL
                        img_url = None
                        classes_list = []
                        assistant_content = ''
                        
                        for msg in messages:
                            if msg.get('role') == 'user':
                                content = msg.get('content')
                                
                                # If content is a string, extract classes
                                if isinstance(content, str):
                                    if 'detect' in content:
                                        text = content
                                        match = re.search(r'detect (.+)', text)
                                        if match:
                                            classes_str = match.group(1)
                                            classes_list = [c.strip() for c in classes_str.split(';') if c.strip()]
                                
                                # If content is array, extract image URL
                                elif isinstance(content, list):
                                    for content_item in content:
                                        if content_item.get('type') == 'image_url':
                                            img_url = content_item.get('image_url', {}).get('url')
                            
                            elif msg.get('role') == 'assistant':
                                assistant_content = msg.get('content', '')

                        if classes_list:
                            for class_name in classes_list:
                                if class_name not in class_order:
                                    class_order.append(class_name)

                        if assistant_content and img_url:
                            items = self._parse_annotation_items(assistant_content, classes_list)

                            if items:
                                annotations.append({
                                    'url': img_url,
                                    'items': items,
                                    'content': assistant_content,
                                })
                                for _, label in items:
                                    all_labels.add(label)
                    except json.JSONDecodeError as e:
                        logger.warning(f"Failed to parse line {line_idx}: {e}")
                        continue
            
            annotations_by_split[split_name] = annotations
            logger.info(f"Parsed {len(annotations)} annotations from {split_name}")
            stats[f"{split_name}_annotations"] = len(annotations)
        
        if not annotations_by_split:
            logger.error(f"No annotations found for {dataset_name}")
            return stats
        
        # Create output directories
        output_base = self.output_dir / dataset_name
        output_base.mkdir(parents=True, exist_ok=True)

        for stale_dir in [output_base / 'images', output_base / 'labels']:
            if stale_dir.exists():
                shutil.rmtree(stale_dir)
        
        # Determine class to ID mapping
        if not class_order:
            class_order = sorted(list(all_labels))
        else:
            for label in sorted(all_labels):
                if label not in class_order:
                    class_order.append(label)

        class_to_id = {label: idx for idx, label in enumerate(class_order)}
        
        logger.info(f"\nFound {len(class_order)} classes: {class_order}")
        
        # Save classes.txt
        classes_file = output_base / 'classes.txt'
        with open(classes_file, 'w') as f:
            for class_name in class_order:
                f.write(f"{class_name}\n")
        logger.info(f"Saved classes to {classes_file}")
        
        # Download images and create labels
        successful_images = 0
        
        for split_name, annotations in annotations_by_split.items():
            images_dir = output_base / 'images' / split_name
            labels_dir = output_base / 'labels' / split_name
            images_dir.mkdir(parents=True, exist_ok=True)
            labels_dir.mkdir(parents=True, exist_ok=True)
            
            logger.info(f"\nProcessing {split_name} images...")
            
            for ann_idx, annotation in enumerate(annotations):
                url = annotation['url']
                items = annotation['items']
                
                # Download image
                img = self.download_image(url)
                if img is None:
                    logger.warning(f"Failed to download image {ann_idx} from {url[:60]}")
                    stats[f"{split_name}_failed"] += 1
                    continue
                
                # Save image
                img_name = f"{dataset_name}_{split_name}_{ann_idx:05d}.jpg"
                img_path = images_dir / img_name
                img.save(img_path, 'JPEG', quality=95)
                
                # Create labels file in YOLO format
                label_path = labels_dir / img_name.replace('.jpg', '.txt')
                with open(label_path, 'w') as f:
                    for box, label in items:
                        if label in class_to_id:
                            class_id = class_to_id[label]
                            x_center, y_center, width, height = self.box_to_yolo_format(box)
                            f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")
                
                successful_images += 1
                
                if (ann_idx + 1) % 10 == 0:
                    logger.info(f"  Processed {ann_idx + 1}/{len(annotations)} {split_name} images")
            
            stats[f"{split_name}_downloaded"] = len([d for d in (images_dir).glob('*.jpg')])
            logger.info(f"Downloaded {stats[f'{split_name}_downloaded']} {split_name} images")

            split_names = [name for name, items in annotations_by_split.items() if items]
            val_split = 'valid' if 'valid' in split_names else ('test' if 'test' in split_names else 'train')

        # Create dataset.yaml for YOLO
            yaml_content = f"""path: {output_base}
        train: images/train
        val: images/{val_split}
        test: images/test

        nc: {len(class_order)}
        names: {class_order}
        """
        yaml_path = output_base / 'dataset.yaml'
        with open(yaml_path, 'w') as f:
            f.write(yaml_content)
        logger.info(f"Created YOLO config: {yaml_path}")
        
        return stats
    
    def run(self):
        """Run extraction for all datasets."""
        all_stats = {}
        
        datasets = [
            ('luggage', 'luggage.v1i.openai.zip', 'temp_extract_luggage', ['_annotations.train.jsonl']),
            ('crowd', 'crowd.v1i.openai.zip', 'temp_extract_crowd', ['_annotations.train.jsonl', '_annotations.valid.jsonl', '_annotations.test.jsonl']),
            ('cabin', 'Cabin Detection.v4-ultimate.openai.zip', 'temp_extract_cabin', ['_annotations.train.jsonl', '_annotations.valid.jsonl', '_annotations.test.jsonl']),
        ]
        
        for dataset_name, zip_name, temp_folder, jsonl_files in datasets:
            source_dir = self._ensure_extracted(zip_name, temp_folder)
            all_stats[dataset_name] = self.extract_dataset(dataset_name, source_dir, jsonl_files)
        
        # Print summary
        logger.info(f"\n{'='*60}")
        logger.info("EXTRACTION SUMMARY")
        logger.info(f"{'='*60}")
        
        for dataset_name, stats in all_stats.items():
            logger.info(f"\n{dataset_name.upper()}:")
            for key, value in sorted(stats.items()):
                logger.info(f"  {key}: {value}")
        
        logger.info(f"\nAll datasets extracted to: {self.output_dir}")
        logger.info(f"Image cache: {self.cache_dir}")
        
        return all_stats


def main():
    parser = argparse.ArgumentParser(description='Extract Roboflow OpenAI Vision datasets to YOLO format')
    parser.add_argument('--extract-dir', 
                        default=r'c:\Users\achre\Downloads\Esprit\DL\Ailines project\08_CNN',
                        help='Directory containing extracted zip folders')
    parser.add_argument('--output-dir',
                        default=r'c:\Users\achre\Downloads\Esprit\DL\Ailines project\08_CNN\data',
                        help='Output directory for converted datasets')
    parser.add_argument('--cache-dir',
                        help='Cache directory for downloaded images')
    
    args = parser.parse_args()
    
    extractor = RoboflowExtractor(args.extract_dir, args.output_dir, args.cache_dir)
    extractor.run()


if __name__ == '__main__':
    main()
