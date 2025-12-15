# Hybrid AI-Based Breast Tumor Diagnosis and Decision Support System

A comprehensive medical decision support system that combines **CNN-based tumor classification** with **Traditional AI decision-making** to produce medically meaningful, explainable, and integrated diagnostic support.

## Project Overview

This system addresses the challenge of early and accurate breast tumor detection by combining:

- **Machine Learning (CNN):** Deep learning model for tumor classification using transfer learning
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
│  │   (CNN/ResNet)  │─▶│  (Rule-Based)   │─▶│    System       │  │
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

## Project Structure

```
AI-project/
├── backend/
│   ├── main.py                 # FastAPI application entry point
│   ├── requirements.txt        # Python dependencies
│   └── src/
│       ├── ml/                 # Machine Learning module
│       │   ├── cnn_classifier.py    # CNN model (ResNet50)
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

### Backend Setup

1. Navigate to the backend directory:
```bash
cd Project/backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start the server:
```bash
python main.py
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

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/predict` | POST | Basic CNN prediction |
| `/api/diagnose` | POST | Full diagnosis with ML + Expert + Fuzzy |
| `/api/gradcam` | POST | Generate Grad-CAM visualization |
| `/api/preprocess` | POST | Image preprocessing |
| `/api/rules` | GET | List expert system rules |

## Machine Learning Component

### Model Architecture
- **Base Model:** ResNet50 (pretrained on ImageNet)
- **Transfer Learning:** Fine-tuned for binary classification
- **Output:** Benign/Malignant classification with confidence scores

### Preprocessing
- Resizing to 224x224
- Normalization with ImageNet statistics
- CLAHE contrast enhancement (optional)
- Noise removal via bilateral filtering

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

## Training Your Own Model

1. Prepare dataset following `datasets/README.md` instructions
2. Use the `TumorClassifierTrainer` class
3. Save trained weights to `models/`

```python
from src.ml.cnn_classifier import BreastTumorClassifier

# Initialize with custom weights
classifier = BreastTumorClassifier(
    model_type="resnet50",
    model_path="models/my_trained_model.pth"
)
```

## Technologies Used

### Backend
- **FastAPI:** Modern Python web framework
- **PyTorch:** Deep learning framework
- **torchvision:** Computer vision models
- **scikit-fuzzy:** Fuzzy logic library
- **OpenCV:** Image processing

### Frontend
- **Next.js 15:** React framework
- **TypeScript:** Type safety
- **Tailwind CSS 4:** Styling
- **Radix UI:** UI components
- **Recharts:** Data visualization
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

