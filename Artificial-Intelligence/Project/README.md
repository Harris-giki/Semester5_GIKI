# Hybrid AI-Based Breast Tumor Diagnosis and Decision Support System

A comprehensive medical decision support system that combines **Custom CNN-based tumor classification** with **Traditional AI decision-making** to produce medically meaningful, explainable, and integrated diagnostic support.

## Project Overview

This system addresses the challenge of early and accurate breast tumor detection by combining:

- **Machine Learning (Custom CNN):** Deep learning model with custom architecture for tumor classification
- **Rule-Based Expert System:** IF-THEN rules based on oncology guidelines
- **Fuzzy Logic System:** Handles uncertainty in predictions and provides nuanced risk assessment
- **Web Interface:** Modern React frontend for image upload and result visualization

## Features

- **Tumor Classification:** Classifies mammogram images as benign or malignant
- **Confidence Scoring:** Provides probability scores for predictions
- **Risk Assessment:** Multi-level risk evaluation (very_low to very_high)
- **Expert Recommendations:** Clinical recommendations based on oncology guidelines
- **Explainable AI:** Grad-CAM visualization for model interpretability
- **Fuzzy Analysis:** Handles borderline cases and uncertainty
- **Patient Context:** Incorporates patient metadata for comprehensive analysis
- **Apple Silicon Optimized:** GPU acceleration for M1/M2/M3/M4 Macs via PyTorch MPS

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interface                          │
│                    (React + Next.js Frontend)                   │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                         FastAPI Backend                         │
│                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │   ML Module     │  │  Expert System  │  │  Fuzzy Logic    │  │
│  │  (Custom CNN)   │─▶│  (Rule-Based)   │─▶│    System       │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
│           │                    │                    │           │
│           └────────────────────┴────────────────────┘           │
│                                │                                │
│                    ┌───────────▼───────────┐                    │
│                    │  Integration Pipeline  │                    │
│                    │  (Combined Analysis)   │                    │
│                    └───────────────────────┘                    │
└─────────────────────────────────────────────────────────────────┘
```

## CNN Model Architecture

Custom 5-block convolutional neural network designed for mammogram classification:

```
┌──────────────────────────────────────────────────────────────┐
│  Input: 224 × 224 × 3 (RGB Image)                            │
├──────────────────────────────────────────────────────────────┤
│  Block 1: Conv2D(32) → BN → Conv2D(32) → BN → Pool → Drop    │
│  Block 2: Conv2D(64) → BN → Conv2D(64) → BN → Pool → Drop    │
│  Block 3: Conv2D(128) → BN → Conv2D(128) → BN → Pool → Drop  │
│  Block 4: Conv2D(256) × 3 → BN × 3 → Pool → Drop             │
│  Block 5: Conv2D(128) → BN → Conv2D(128) → BN → Pool → Drop  │
├──────────────────────────────────────────────────────────────┤
│  GlobalAveragePooling2D                                       │
│  Dense(128) → BN → Dropout(0.5)                               │
│  Dense(1, sigmoid) → Output (Benign/Malignant)               │
└──────────────────────────────────────────────────────────────┘

Features:
• L2 regularization (0.001) on all Conv layers
• BatchNormalization for training stability
• Progressive dropout (0.3 → 0.4 → 0.5)
• ~1.2M trainable parameters
```

## Project Structure

```
Project/
├── backend/
│   ├── main.py                 # FastAPI application entry point
│   ├── train.py                # Model training script
│   ├── prepare_dataset.py      # Dataset preparation script
│   ├── requirements.txt        # Python dependencies
│   ├── models/                 # Saved model weights
│   └── src/
│       ├── ml/                 # Machine Learning module
│       │   ├── cnn_classifier.py    # Custom CNN model
│       │   └── preprocessing.py     # Image preprocessing
│       ├── traditional_ai/     # Traditional AI module
│       │   ├── expert_system.py     # Rule-based expert system
│       │   └── fuzzy_logic.py       # Fuzzy inference system
│       └── api/                # API routes
│           └── routes.py            # FastAPI endpoints
├── frontend/
│   ├── src/
│   │   ├── app/               # Next.js app router
│   │   ├── components/        # React components
│   │   └── lib/               # Utilities and types
│   └── package.json
├── datasets/                   # Dataset placeholder
│   └── README.md              # Dataset instructions
└── README.md                   # This file
```

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- pnpm (or npm/yarn)
- Mac with Apple Silicon (M1/M2/M3/M4) recommended for GPU acceleration

### Backend Setup

1. Navigate to the backend directory:
```bash
cd Project/backend
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

> **Note for Apple Silicon:** TensorFlow Metal is included for GPU acceleration. If you encounter issues, ensure you have the latest macOS and run:
> ```bash
> pip install tensorflow-metal
> ```

4. Start the server:
```bash
python3 main.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd Project/frontend
```

2. Install dependencies:
```bash
pnpm install
```

3. Start the development server:
```bash
pnpm dev
```

The frontend will be available at `http://localhost:3001`

## Training the Model

### 1. Prepare the Dataset

```bash
cd backend
python3 prepare_dataset.py
```

This organizes the CBIS-DDSM dataset into:
```
datasets/mammograms/
├── train/
│   ├── benign/
│   └── malignant/
├── val/
│   ├── benign/
│   └── malignant/
└── test/
    ├── benign/
    └── malignant/
```

### 2. Train the Model

```bash
python3 train.py --data-dir ../datasets/mammograms --epochs 50
```

**Training options:**
| Argument | Default | Description |
|----------|---------|-------------|
| `--data-dir` | `../datasets/mammograms` | Path to dataset |
| `--epochs` | `50` | Number of training epochs |
| `--batch-size` | `32` | Batch size |
| `--input-size` | `224` | Input image size |
| `--learning-rate` | `0.001` | Initial learning rate |
| `--dropout` | `0.5` | Dropout rate |
| `--patience` | `10` | Early stopping patience |

### 3. Using the Trained Model

```python
from src.ml.cnn_classifier import BreastTumorClassifier

# Load trained model
classifier = BreastTumorClassifier(model_path="models/best_model.pth")

# Predict
with open("mammogram.jpg", "rb") as f:
    result = classifier.predict(f.read())
    print(result)
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/predict` | POST | Basic CNN prediction |
| `/api/diagnose` | POST | Full diagnosis with ML + Expert + Fuzzy |
| `/api/gradcam` | POST | Generate Grad-CAM visualization |
| `/api/preprocess` | POST | Image preprocessing |
| `/api/rules` | GET | List expert system rules |

## Traditional AI Component

### Rule-Based Expert System
- 10+ rules based on oncology guidelines
- Forward chaining inference
- Priority-based rule evaluation
- Patient context integration

### Fuzzy Logic System
- Mamdani inference system
- Membership functions for confidence, severity, age, pain
- Handles uncertainty and borderline cases
- Provides interpretable risk scores

## Example Rules

```python
# High Confidence Malignant
IF predicted_class == "malignant" AND confidence > 0.85
THEN risk = VERY_HIGH AND recommend = "Immediate biopsy"

# Borderline Case
IF confidence in [0.55, 0.75]
THEN uncertainty = MEDIUM AND recommend = "Additional imaging"

# Family History Consideration
IF family_history == True AND confidence > 0.50
THEN recommend = "Genetic counseling"
```

## Technologies Used

### Backend
- **FastAPI:** Modern Python web framework
- **PyTorch:** Deep learning framework
- **PyTorch MPS:** GPU acceleration for Apple Silicon
- **scikit-fuzzy:** Fuzzy logic library
- **OpenCV:** Image processing

### Frontend
- **Next.js 15:** React framework
- **TypeScript:** Type safety
- **Tailwind CSS 4:** Styling
- **Radix UI:** UI components
- **Motion:** Animations

## Authors

- Muhammad Haris (2023428)
- Mumtaz Ali (2023559)

## Course

CS351 - Artificial Intelligence

## References

1. S. A. Hussain et al., "Breast Cancer Classification using Deep Learning Techniques," IEEE Access, 2020.
2. J. Arevalo et al., "Representation learning for mammography mass lesion classification," Pattern Recognition, 2016.
3. L. Shen et al., "End-to-end training for whole-image breast cancer diagnosis using Deep CNNs," J. Biomed. Imaging, 2019.
4. E. H. Shortliffe, "MYCIN: A Knowledge-Based Expert System," Addison-Wesley, 1985.
5. K. Doi, "Computer-Aided Diagnosis in Medical Imaging," Academic Radiology, 2007.
6. Russell & Norvig, Artificial Intelligence: A Modern Approach, 4th Ed., Prentice Hall.

## License

This project is for educational purposes as part of CS351 AI course.

## Disclaimer

This system is designed for educational and research purposes only. It should not be used as a substitute for professional medical diagnosis. Always consult with qualified healthcare professionals for medical decisions.
