# Datasets Directory

## Recommended Datasets for Breast Tumor Classification

This directory is a placeholder for mammogram datasets. Below are the recommended datasets for training and testing the Custom CNN classifier.

### 1. CBIS-DDSM (Curated Breast Imaging Subset of DDSM)

**Description:** A curated and standardized subset of the Digital Database for Screening Mammography.

**Download:** https://wiki.cancerimagingarchive.net/display/Public/CBIS-DDSM

**Structure:**
```
datasets/
└── CBIS-DDSM/
    ├── train/
    │   ├── benign/
    │   └── malignant/
    └── test/
        ├── benign/
        └── malignant/
```

### 2. INbreast Database

**Description:** Full-field digital mammography database with well-annotated lesions.

**Download:** https://www.kaggle.com/datasets/martholi/inbreast (requires access)

### 3. Mini-MIAS (Mammographic Image Analysis Society)

**Description:** Digitized mammograms with verified annotations.

**Download:** https://www.kaggle.com/datasets/kmader/mias-mammography

## Dataset Preparation

### Using the Automatic Preparation Script

If you've downloaded the CBIS-DDSM dataset (archive folder), run:

```bash
cd backend
python3 prepare_dataset.py
```

This will:
1. Parse the CSV files for pathology labels (BENIGN/MALIGNANT)
2. Find the corresponding cropped tumor images (ROI regions)
3. Organize into train/val/test splits (80/20 for train/val, test from original)
4. Copy images to the proper folder structure

### Manual Directory Structure

If preparing manually, organize your dataset as:

```
datasets/
└── mammograms/
    ├── train/
    │   ├── benign/
    │   │   ├── image001.jpg
    │   │   ├── image002.jpg
    │   │   └── ...
    │   └── malignant/
    │       ├── image001.jpg
    │       ├── image002.jpg
    │       └── ...
    ├── val/
    │   ├── benign/
    │   └── malignant/
    └── test/
        ├── benign/
        └── malignant/
```

### Preprocessing Recommendations

1. **Resize:** Images are automatically resized to 224x224 pixels during training
2. **Format:** PNG or JPEG format supported
3. **Normalization:** Handled automatically (rescaled to [0, 1])
4. **Augmentation:** Applied during training:
   - Rotation (±20°)
   - Width/Height shift (20%)
   - Shear (20%)
   - Zoom (20%)
   - Horizontal/Vertical flip

## Training Commands

After preparing the dataset:

```bash
cd backend
source venv/bin/activate

# Train with default settings
python3 train.py --data-dir ../datasets/mammograms

# Train with custom settings
python3 train.py \
    --data-dir ../datasets/mammograms \
    --epochs 100 \
    --batch-size 32 \
    --input-size 224 \
    --learning-rate 0.001
```

## Model Output

After training, models are saved to `backend/models/`:
- `best_model.h5` - Best model based on validation accuracy
- `final_model.h5` - Model from the last epoch
- `logs/` - TensorBoard training logs

## Apple Silicon (M1/M2/M3/M4) Optimization

The training script automatically uses TensorFlow Metal for GPU acceleration:

```bash
# Verify GPU is detected
python3 -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
```

Expected output for Apple Silicon:
```
[PhysicalDevice(name='/physical_device:GPU:0', device_type='GPU')]
```

If GPU is not detected, ensure tensorflow-metal is installed:
```bash
pip install tensorflow-metal
```

## Notes

- Ensure proper ethical use of medical imaging data
- Follow data usage agreements for each dataset
- Keep patient data anonymized
- Do not commit actual datasets to version control

## Recommended Dataset Sizes

| Split | Minimum | Recommended |
|-------|---------|-------------|
| Train | 200/class | 1000+/class |
| Val | 50/class | 200+/class |
| Test | 50/class | 200+/class |

Larger datasets generally improve model accuracy and generalization.
