"""
CBIS-DDSM Dataset Preparation Script
=====================================

This script processes the CBIS-DDSM dataset and organizes it into a structure
suitable for training the breast tumor classifier.

Key insight: The dicom_info.csv contains the actual JPEG paths and PatientName
that can be parsed to match with case descriptions for labels.

PatientName format: Mass-Training_P_00001_LEFT_CC_1
                    [Type]-[Split]_P_[ID]_[Laterality]_[View]_[AbnormalityID]
"""

import os
import pandas as pd
import shutil
from pathlib import Path
from sklearn.model_selection import train_test_split
import re
from typing import Dict, Tuple
import argparse


def parse_patient_name(patient_name: str) -> Dict:
    """
    Parse the PatientName to extract case information.
    
    Example: Mass-Training_P_01265_RIGHT_MLO_1
    Returns: {
        'case_type': 'Mass',
        'split': 'Training',
        'patient_id': 'P_01265',
        'laterality': 'RIGHT',
        'view': 'MLO',
        'abnormality_id': '1'
    }
    """
    if pd.isna(patient_name):
        return None
    
    # Pattern with abnormality ID
    # (Mass|Calc)-(Training|Test)_P_(\d+)_(LEFT|RIGHT)_(CC|MLO)_(\d+)
    pattern = r'(Mass|Calc)-(Training|Test)_P_(\d+)_(LEFT|RIGHT)_(CC|MLO)_(\d+)'
    match = re.match(pattern, patient_name)
    
    if match:
        return {
            'case_type': match.group(1),
            'split': match.group(2),
            'patient_id': f'P_{match.group(3)}',
            'laterality': match.group(4),
            'view': match.group(5),
            'abnormality_id': match.group(6)
        }
    
    # Try pattern without abnormality ID (for full mammograms)
    pattern2 = r'(Mass|Calc)-(Training|Test)_P_(\d+)_(LEFT|RIGHT)_(CC|MLO)$'
    match2 = re.match(pattern2, patient_name)
    if match2:
        return {
            'case_type': match2.group(1),
            'split': match2.group(2),
            'patient_id': f'P_{match2.group(3)}',
            'laterality': match2.group(4),
            'view': match2.group(5),
            'abnormality_id': '1'
        }
    
    return None


def load_case_descriptions(csv_dir: Path) -> pd.DataFrame:
    """Load all case description CSVs and combine them."""
    all_cases = []
    
    csv_files = [
        'mass_case_description_train_set.csv',
        'mass_case_description_test_set.csv',
        'calc_case_description_train_set.csv',
        'calc_case_description_test_set.csv',
    ]
    
    for csv_name in csv_files:
        csv_path = csv_dir / csv_name
        if csv_path.exists():
            df = pd.read_csv(csv_path)
            
            # Normalize column names (some CSVs have 'breast_density' vs 'breast density')
            df.columns = [col.lower().replace(' ', '_') for col in df.columns]
            
            # Add source info
            if 'mass' in csv_name:
                df['case_type'] = 'Mass'
            else:
                df['case_type'] = 'Calc'
            
            if 'train' in csv_name:
                df['source_split'] = 'Training'
            else:
                df['source_split'] = 'Test'
            
            all_cases.append(df)
            print(f"  Loaded {len(df)} cases from {csv_name}")
    
    combined = pd.concat(all_cases, ignore_index=True)
    return combined


def create_lookup_key(row) -> str:
    """Create a unique key for matching cases."""
    # Key format: CaseType_Split_PatientID_Laterality_View_AbnormalityID
    laterality = row.get('left_or_right_breast', '').upper()
    view = row.get('image_view', '').upper()
    patient_id = row.get('patient_id', '')
    abnormality_id = str(row.get('abnormality_id', '1'))
    case_type = row.get('case_type', '')
    split = row.get('source_split', '')
    
    return f"{case_type}_{split}_{patient_id}_{laterality}_{view}_{abnormality_id}"


def normalize_pathology(pathology: str) -> str:
    """Normalize pathology labels to benign/malignant."""
    if pd.isna(pathology):
        return None
    
    pathology = str(pathology).upper().strip()
    
    if 'MALIGNANT' in pathology:
        return 'malignant'
    elif 'BENIGN' in pathology:
        return 'benign'
    else:
        return None


def prepare_dataset(
    archive_dir: Path,
    output_dir: Path,
    val_split: float = 0.2
) -> Dict[str, Dict[str, int]]:
    """
    Prepare the CBIS-DDSM dataset for training.
    """
    csv_dir = archive_dir / 'csv'
    jpeg_dir = archive_dir / 'jpeg'
    
    print("=" * 60)
    print("CBIS-DDSM Dataset Preparation")
    print("=" * 60)
    print(f"Archive directory: {archive_dir}")
    print(f"Output directory: {output_dir}")
    print()
    
    # Step 1: Load dicom_info.csv to get JPEG paths
    print("Step 1: Loading DICOM info...")
    dicom_info = pd.read_csv(csv_dir / 'dicom_info.csv')
    
    # Filter to only cropped images (these are the tumor ROIs)
    cropped_images = dicom_info[dicom_info['SeriesDescription'] == 'cropped images'].copy()
    print(f"  Found {len(cropped_images)} cropped images")
    
    # Parse patient names to extract case info
    print("\nStep 2: Parsing image metadata...")
    parsed_info = []
    for _, row in cropped_images.iterrows():
        parsed = parse_patient_name(row['PatientName'])
        if parsed:
            parsed['image_path'] = row['image_path']
            parsed['full_patient_name'] = row['PatientName']
            parsed_info.append(parsed)
    
    images_df = pd.DataFrame(parsed_info)
    print(f"  Successfully parsed {len(images_df)} images")
    
    # Create lookup key for images
    images_df['lookup_key'] = images_df.apply(
        lambda r: f"{r['case_type']}_{r['split']}_{r['patient_id']}_{r['laterality']}_{r['view']}_{r['abnormality_id']}", 
        axis=1
    )
    
    # Step 3: Load case descriptions for pathology labels
    print("\nStep 3: Loading case descriptions...")
    cases_df = load_case_descriptions(csv_dir)
    
    # Create lookup key for cases
    cases_df['lookup_key'] = cases_df.apply(create_lookup_key, axis=1)
    
    # Create pathology lookup dictionary
    pathology_lookup = {}
    for _, row in cases_df.iterrows():
        key = row['lookup_key']
        pathology = normalize_pathology(row.get('pathology'))
        if pathology:
            pathology_lookup[key] = pathology
    
    print(f"  Created pathology lookup with {len(pathology_lookup)} entries")
    
    # Step 4: Match images with pathology
    print("\nStep 4: Matching images with pathology labels...")
    images_df['label'] = images_df['lookup_key'].map(pathology_lookup)
    
    # Report matching stats
    matched = images_df['label'].notna().sum()
    print(f"  Matched {matched}/{len(images_df)} images with pathology labels")
    
    # Filter to only matched images
    labeled_df = images_df[images_df['label'].notna()].copy()
    
    print(f"\nLabel distribution:")
    print(f"  {labeled_df['label'].value_counts().to_dict()}")
    
    # Step 5: Create train/val/test splits
    print("\nStep 5: Creating train/val/test splits...")
    
    # Use original splits from CSV
    train_data = labeled_df[labeled_df['split'] == 'Training']
    test_data = labeled_df[labeled_df['split'] == 'Test']
    
    # Split training into train/val
    if len(train_data) > 0:
        train_df, val_df = train_test_split(
            train_data,
            test_size=val_split,
            stratify=train_data['label'],
            random_state=42
        )
    else:
        train_df = pd.DataFrame()
        val_df = pd.DataFrame()
    
    test_df = test_data
    
    print(f"  Train: {len(train_df)} images")
    print(f"  Val: {len(val_df)} images")
    print(f"  Test: {len(test_df)} images")
    
    # Step 6: Copy files to output directory
    print("\nStep 6: Copying files to output directory...")
    
    # Create output directories
    for split in ['train', 'val', 'test']:
        for label in ['benign', 'malignant']:
            (output_dir / split / label).mkdir(parents=True, exist_ok=True)
    
    stats = {
        'train': {'benign': 0, 'malignant': 0},
        'val': {'benign': 0, 'malignant': 0},
        'test': {'benign': 0, 'malignant': 0}
    }
    
    def copy_files(df: pd.DataFrame, split_name: str):
        copied = 0
        for idx, row in df.iterrows():
            # Construct source path
            # image_path is like: CBIS-DDSM/jpeg/1.3.../1-172.jpg
            # We need: archive/jpeg/1.3.../1-172.jpg
            relative_path = row['image_path'].replace('CBIS-DDSM/jpeg/', '')
            src_path = jpeg_dir / relative_path
            
            if src_path.exists():
                label = row['label']
                dst_name = f"{row['full_patient_name']}_{idx}.jpg"
                dst_path = output_dir / split_name / label / dst_name
                
                shutil.copy2(src_path, dst_path)
                stats[split_name][label] += 1
                copied += 1
            else:
                # Try with just the filename
                parts = row['image_path'].split('/')
                if len(parts) >= 2:
                    folder = parts[-2]
                    filename = parts[-1]
                    src_path = jpeg_dir / folder / filename
                    if src_path.exists():
                        label = row['label']
                        dst_name = f"{row['full_patient_name']}_{idx}.jpg"
                        dst_path = output_dir / split_name / label / dst_name
                        
                        shutil.copy2(src_path, dst_path)
                        stats[split_name][label] += 1
                        copied += 1
        
        print(f"    Copied {copied} files to {split_name}/")
    
    copy_files(train_df, 'train')
    copy_files(val_df, 'val')
    copy_files(test_df, 'test')
    
    # Print final statistics
    print(f"\n{'=' * 60}")
    print("DATASET PREPARATION COMPLETE")
    print("=" * 60)
    print(f"\nOutput directory: {output_dir}")
    print("\nFinal statistics:")
    
    total_all = 0
    for split in ['train', 'val', 'test']:
        total = stats[split]['benign'] + stats[split]['malignant']
        total_all += total
        print(f"  {split.upper():6s}: {total:4d} images "
              f"(benign: {stats[split]['benign']}, malignant: {stats[split]['malignant']})")
    
    print(f"\n  TOTAL: {total_all} images")
    
    print("\n" + "=" * 60)
    print("HOW THIS DATA WAS PROCESSED")
    print("=" * 60)
    print("""
1. SOURCE: CBIS-DDSM dataset (Curated Breast Imaging Subset of DDSM)
   
2. IMAGE TYPE: Cropped images (ROI regions around tumors)
   - NOT full mammograms (too large, tumor is small region)
   - NOT ROI masks (binary masks, not useful for classification)

3. LABELS: Extracted from case description CSVs
   - 'pathology' column: BENIGN, MALIGNANT, BENIGN_WITHOUT_CALLBACK
   - BENIGN_WITHOUT_CALLBACK treated as BENIGN

4. MATCHING: Images matched to labels via PatientName parsing
   - Format: Mass-Training_P_00001_LEFT_CC_1
   - Contains: CaseType, Split, PatientID, Laterality, View, AbnormalityID

5. SPLITS:
   - Training/Test: From original CBIS-DDSM splits (CSV names)
   - Validation: 20% split from Training data

6. OUTPUT STRUCTURE:
   mammograms/
   ├── train/
   │   ├── benign/     (for training)
   │   └── malignant/
   ├── val/
   │   ├── benign/     (for validation during training)
   │   └── malignant/
   └── test/
       ├── benign/     (for final evaluation)
       └── malignant/
""")
    
    return stats


def main():
    parser = argparse.ArgumentParser(description='Prepare CBIS-DDSM dataset for training')
    parser.add_argument('--archive-dir', type=str,
                        default='../datasets/archive',
                        help='Path to archive directory')
    parser.add_argument('--output-dir', type=str,
                        default='../datasets/mammograms',
                        help='Path to output directory')
    parser.add_argument('--val-split', type=float, default=0.2,
                        help='Fraction of training data for validation')
    
    args = parser.parse_args()
    
    # Convert to absolute paths
    script_dir = Path(__file__).parent
    archive_dir = Path(args.archive_dir)
    output_dir = Path(args.output_dir)
    
    if not archive_dir.is_absolute():
        archive_dir = script_dir / archive_dir
    if not output_dir.is_absolute():
        output_dir = script_dir / output_dir
    
    if not archive_dir.exists():
        print(f"Error: Archive directory not found: {archive_dir}")
        return 1
    
    prepare_dataset(archive_dir, output_dir, args.val_split)
    return 0


if __name__ == '__main__':
    exit(main())
