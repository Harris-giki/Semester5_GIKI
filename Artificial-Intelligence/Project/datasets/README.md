# Datasets Directory

## Recommended Datasets for Breast Tumor Classification

This directory is a placeholder for mammogram datasets. Below are the recommended datasets for training and testing the CNN classifier.

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

**Structure:**
```
datasets/
└── INbreast/
    ├── images/
    └── annotations/
```

### 3. Mini-MIAS (Mammographic Image Analysis Society)

**Description:** Digitized mammograms with verified annotations.

**Download:** https://www.kaggle.com/datasets/kmader/mias-mammography

**Structure:**
```
datasets/
└── mini-MIAS/
    ├── images/
    └── info.txt
```

## Dataset Preparation

### Directory Structure for Training

Organize your dataset in the following structure for training:

```
datasets/
└── mammograms/
    ├── train/
    │   ├── benign/
    │   │   ├── image001.png
    │   │   ├── image002.png
    │   │   └── ...
    │   └── malignant/
    │       ├── image001.png
    │       ├── image002.png
    │       └── ...
    ├── val/
    │   ├── benign/
    │   └── malignant/
    └── test/
        ├── benign/
        └── malignant/
```

### Preprocessing Recommendations

1. **Resize:** All images should be resized to 224x224 pixels (or 256x256 for cropping)
2. **Format:** Convert to PNG or JPEG format
3. **Normalization:** Will be handled by the preprocessing module
4. **Augmentation:** The training module includes data augmentation

### Sample Training Script

After placing your data, you can train the model using:

```python
from src.ml.cnn_classifier import BreastTumorClassifier, TumorClassifierTrainer
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

# Define transforms
train_transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.RandomCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.RandomVerticalFlip(),
    transforms.RandomRotation(15),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Load dataset
train_dataset = datasets.ImageFolder('datasets/mammograms/train', transform=train_transform)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

# Initialize and train
classifier = BreastTumorClassifier(model_type="resnet50")
trainer = TumorClassifierTrainer(classifier)

# Training loop
for epoch in range(50):
    train_loss, train_acc = trainer.train_epoch(train_loader)
    print(f"Epoch {epoch+1}: Loss={train_loss:.4f}, Acc={train_acc:.4f}")

# Save model
classifier.save_model('models/tumor_classifier.pth')
```

## Notes

- Ensure proper ethical use of medical imaging data
- Follow data usage agreements for each dataset
- Keep patient data anonymized
- Do not commit actual datasets to version control

