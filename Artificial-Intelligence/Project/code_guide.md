# 📚 Code Guide: Understanding Your Breast Tumor Diagnosis System

**Welcome!** This guide will help you understand every part of your project, even if you're new to coding. We'll start from the basics and work our way up.

---

## 🎯 **Where to Start? (Reading Order)**

If you're completely new, follow this order:

### **Step 1: Understand the Big Picture**
1. Read `README.md` - Overview of the entire project
2. Read this file (`CODE_GUIDE.md`) - You're here! ✅

### **Step 2: Backend (Python) - Start Here!**
1. `backend/main.py` - The entry point (where the server starts)
2. `backend/src/api/routes.py` - How the API receives requests
3. `backend/src/ml/cnn_classifier.py` - The AI model that analyzes images
4. `backend/src/traditional_ai/expert_system.py` - Rule-based AI system
5. `backend/src/traditional_ai/fuzzy_logic.py` - Handles uncertainty
6. `backend/train.py` - How the model was trained

### **Step 3: Frontend (React/Next.js) - Then This!**
1. `frontend/src/app/page.tsx` - Main page (where everything happens)
2. `frontend/src/lib/types.ts` - Data structures (what data looks like)
3. `frontend/src/components/ImageUploader.tsx` - Image upload component
4. `frontend/src/components/DiagnosisResults.tsx` - Shows results
5. `frontend/src/components/StatsOverview.tsx` - Dashboard stats
6. Other components in `frontend/src/components/`

---

## 🏗️ **Project Structure Overview**

```
Project/
├── backend/          # Python server (AI brain)
├── frontend/         # React website (user interface)
└── datasets/         # Training images
```

**Think of it like a restaurant:**
- **Frontend** = The dining room (what customers see)
- **Backend** = The kitchen (where the work happens)
- **Datasets** = The ingredients (training data)

---

## 🔧 **Backend Files Explained**

### **1. `backend/main.py`** ⭐ START HERE
**What it does:** This is where your Python server starts. It's like the main door of your application.

**Key concepts:**
- **FastAPI**: A Python framework for building APIs (like a waiter that takes orders)
- **CORS**: Allows the frontend to talk to the backend
- **Routes**: Different endpoints (like different menu items)

**What happens:**
1. Creates a FastAPI application
2. Sets up CORS (so frontend can connect)
3. Includes all API routes from `routes.py`
4. Starts the server on port 8000

**Key code:**
```python
app = FastAPI(...)  # Creates the app
app.include_router(router, prefix="/api")  # Adds routes
uvicorn.run(...)  # Starts the server
```

---

### **2. `backend/src/api/routes.py`** 🛣️
**What it does:** Defines the API endpoints. When the frontend sends a request, this file handles it.

**Main endpoints:**
- `GET /api/health` - Checks if server is running
- `POST /api/diagnose` - Analyzes a mammogram image
- `POST /api/gradcam` - Generates heatmap visualization

**What happens when you upload an image:**
1. Receives the image file from frontend
2. Preprocesses the image (resizes, enhances)
3. Calls the CNN classifier to predict (benign/malignant)
4. Calls expert system for rule-based analysis
5. Calls fuzzy logic system for uncertainty handling
6. Combines all results and sends back to frontend

**Key functions:**
- `full_diagnosis()` - Main diagnosis function
- `get_classifier()` - Loads the AI model
- `get_expert_system()` - Loads expert system
- `get_fuzzy_system()` - Loads fuzzy logic system

---

### **3. `backend/src/ml/cnn_classifier.py`** 🤖
**What it does:** Contains the deep learning model that analyzes mammogram images.

**Key concepts:**
- **CNN (Convolutional Neural Network)**: A type of AI that's good at analyzing images
- **Transfer Learning**: Using a pre-trained model (ResNet50) and adapting it
- **ResNet50**: A powerful image recognition model trained on millions of images

**What happens:**
1. Loads the trained model (`best_model.pth`)
2. Preprocesses the image (resize to 224x224, normalize)
3. Runs the image through the neural network
4. Gets probabilities: "80% benign, 20% malignant"
5. Returns the prediction with confidence

**Key classes:**
- `TransferLearningCNN`: The neural network architecture
- `BreastTumorClassifier`: Wrapper that handles prediction

**Model architecture:**
```
Input Image (224x224)
    ↓
ResNet50 (pre-trained backbone)
    ↓
Custom layers (512 neurons → 2 classes)
    ↓
Output: [benign_probability, malignant_probability]
```

---

### **4. `backend/src/ml/preprocessing.py`** 🖼️
**What it does:** Prepares images before feeding them to the AI model.

**Functions:**
- `enhance_contrast()` - Makes images clearer
- `get_image_stats()` - Calculates image statistics (brightness, contrast, etc.)

**Why it matters:** Better image quality = better predictions

---

### **5. `backend/src/traditional_ai/expert_system.py`** 🧠
**What it does:** Implements rule-based AI using medical guidelines. Like a doctor following a checklist.

**How it works:**
- Has a set of IF-THEN rules based on medical knowledge
- Example: "IF confidence > 0.8 AND severity > 7 THEN recommend immediate biopsy"
- Fires rules based on the ML prediction and patient data

**Key concepts:**
- **Rules**: Medical guidelines encoded as logic
- **Rules Fired**: Which rules were triggered
- **Recommendations**: Clinical advice based on rules

**Example rule:**
```python
IF (confidence is high) AND (severity is high)
THEN (risk = very_high) AND (recommend immediate biopsy)
```

---

### **6. `backend/src/traditional_ai/fuzzy_logic.py`** 🌫️
**What it does:** Handles uncertainty and vague information. Unlike yes/no logic, fuzzy logic deals with "maybe" and "somewhat".

**Why it's needed:** Medical diagnosis isn't always black and white. Fuzzy logic helps with:
- "High confidence" vs "Very high confidence"
- "Moderate risk" vs "High risk"
- Uncertainty in predictions

**Key concepts:**
- **Membership Functions**: How much something belongs to a category (0 to 1)
- **Fuzzy Rules**: Rules that work with degrees of truth
- **Defuzzification**: Converting fuzzy results to clear numbers

**Example:**
- Instead of "confidence = 0.75" (exact)
- Fuzzy: "confidence is 60% 'medium' and 40% 'high'"

---

### **7. `backend/train.py`** 🎓
**What it does:** Script to train the AI model on your dataset.

**What happens during training:**
1. Loads images from `datasets/mammograms/train/`
2. Applies data augmentation (flip, rotate, etc.)
3. Trains the model for multiple epochs
4. Validates on validation set
5. Saves the best model to `models/best_model.pth`

**Key concepts:**
- **Epoch**: One complete pass through all training data
- **Loss**: How wrong the model is (lower is better)
- **Accuracy**: How often the model is correct
- **Validation**: Testing on unseen data

**Training process:**
```
For each epoch:
  1. Train on training images
  2. Calculate loss and accuracy
  3. Validate on validation images
  4. Save best model
  5. Adjust learning rate
```

---

### **8. `backend/requirements.txt`** 📦
**What it does:** Lists all Python packages needed to run the backend.

**Key packages:**
- `fastapi` - Web framework
- `torch` - PyTorch (deep learning library)
- `torchvision` - Image processing for PyTorch
- `pillow` - Image handling
- `opencv-python` - Computer vision
- `scikit-fuzzy` - Fuzzy logic library

---

## 🎨 **Frontend Files Explained**

### **1. `frontend/src/app/page.tsx`** ⭐ MAIN PAGE
**What it does:** The main page of your website. This is where everything happens.

**Key concepts:**
- **React Hooks**: `useState` manages component state (like variables)
- **Tabs**: Different views (Overview, Upload, Results, etc.)
- **API Calls**: Sends requests to backend

**What happens:**
1. User sees the page
2. User uploads an image
3. Page sends image to backend API
4. Backend analyzes and returns results
5. Page displays results

**Key state variables:**
- `results` - Stores diagnosis results
- `selectedImage` - The uploaded image
- `isLoading` - Shows loading spinner
- `activeTab` - Which tab is visible

**Main functions:**
- `analyzeMammogram()` - Sends image to backend
- `handleImageSelect()` - Handles file upload
- `generateGradCAM()` - Gets heatmap visualization

---

### **2. `frontend/src/app/layout.tsx`** 🎨
**What it does:** Wraps all pages. Sets up the theme, fonts, and global structure.

**Key concepts:**
- **Theme Provider**: Manages dark/light mode
- **Fonts**: Inter and JetBrains Mono

---

### **3. `frontend/src/app/globals.css`** 🎨
**What it does:** Global styles for the entire website. Defines colors, animations, and design system.

**Key concepts:**
- **CSS Variables**: Reusable color values (like `--accent-cyan`)
- **Dark Theme**: All the color definitions
- **Animations**: Smooth transitions and effects

**Color system:**
- `--accent-cyan`: Primary accent color
- `--accent-purple`: Secondary accent
- `--danger`: Red for warnings
- `--success`: Green for positive results

---

### **4. `frontend/src/components/ImageUploader.tsx`** 📤
**What it does:** Component for uploading mammogram images.

**Features:**
- Drag and drop
- Click to browse
- Image preview
- File validation

**What happens:**
1. User drags or selects an image
2. Validates file type (must be image)
3. Shows preview
4. Calls parent's `onImageSelect` function

---

### **5. `frontend/src/components/PatientForm.tsx`** 📝
**What it does:** Form to collect patient information (age, pain level, symptoms).

**Fields:**
- Age (optional)
- Pain level (0-10 slider)
- Family history (checkbox)
- Lump detected (checkbox)
- Nipple discharge (checkbox)

**Why it matters:** This data is used by the expert system and fuzzy logic for better diagnosis.

---

### **6. `frontend/src/components/DiagnosisResults.tsx`** 📊
**What it does:** Displays the diagnosis results in a beautiful, organized way.

**Shows:**
- Main result (Benign/Malignant)
- Risk category badge
- Score cards (ML prediction, Expert analysis, Fuzzy analysis)
- Recommendations
- Follow-up information

**Key features:**
- Color-coded by risk level
- Animated appearance
- Clear visual hierarchy

---

### **7. `frontend/src/components/StatsOverview.tsx`** 📈
**What it does:** Shows key statistics in a dashboard format.

**Stats displayed:**
- Prediction Confidence (from ML model)
- Risk Score (composite score)
- Rules Fired (how many expert rules triggered)
- Analysis Status (Complete/Ready)

**Note:** This shows "—" when no analysis is done (no fake data!)

---

### **8. `frontend/src/components/GradCAMViewer.tsx`** 🔥
**What it does:** Displays the Grad-CAM heatmap visualization.

**What is Grad-CAM?**
- Shows which parts of the image the AI focused on
- Red areas = important for the prediction
- Helps explain why the AI made its decision

**How it works:**
1. User clicks "Generate Heatmap"
2. Frontend requests heatmap from backend
3. Backend generates heatmap using Grad-CAM
4. Frontend displays overlay on original image

---

### **9. `frontend/src/components/Header.tsx`** 🎯
**What it does:** Top navigation bar with logo and title.

---

### **10. `frontend/src/components/Sidebar.tsx`** 📑
**What it does:** Left sidebar navigation menu.

**Tabs:**
- Overview
- Upload
- Results
- Details
- Explainability

---

### **11. `frontend/src/lib/types.ts`** 📋
**What it does:** Defines TypeScript interfaces (data structures).

**Why it matters:** Ensures data consistency. Like a blueprint for what data should look like.

**Key interfaces:**
- `DiagnosisResponse` - Full diagnosis result
- `MLPrediction` - ML model output
- `ExpertAnalysis` - Expert system output
- `FuzzyAnalysis` - Fuzzy logic output
- `PatientData` - Patient information

---

### **12. `frontend/src/lib/utils.ts`** 🛠️
**What it does:** Utility functions used throughout the frontend.

**Functions:**
- `cn()` - Combines CSS classes
- `getRiskColor()` - Returns color based on risk level
- `getUrgencyColor()` - Returns color based on urgency
- `API_BASE_URL` - Backend API URL

---

### **13. `frontend/package.json`** 📦
**What it does:** Lists all JavaScript/TypeScript packages needed.

**Key packages:**
- `next` - Next.js framework
- `react` - React library
- `@phosphor-icons/react` - Icons
- `motion` - Animations
- `sonner` - Toast notifications

---

## 🔄 **How Data Flows Through the System**

### **Complete Flow: Image Upload to Results**

```
1. USER ACTION
   User uploads image in frontend
   ↓
2. FRONTEND (page.tsx)
   - User selects image
   - Fills patient form (optional)
   - Clicks analyze
   ↓
3. API REQUEST
   POST /api/diagnose
   - Image file
   - Patient data (age, symptoms, etc.)
   ↓
4. BACKEND (routes.py)
   - Receives request
   - Validates image
   - Preprocesses image
   ↓
5. ML MODEL (cnn_classifier.py)
   - Loads trained model
   - Predicts: benign/malignant
   - Returns confidence and probabilities
   ↓
6. EXPERT SYSTEM (expert_system.py)
   - Applies medical rules
   - Generates recommendations
   - Determines risk level
   ↓
7. FUZZY LOGIC (fuzzy_logic.py)
   - Handles uncertainty
   - Calculates fuzzy risk score
   - Provides interpretation
   ↓
8. COMBINE RESULTS (routes.py)
   - Merges all three analyses
   - Creates final recommendation
   - Calculates composite risk score
   ↓
9. API RESPONSE
   Returns JSON with all results
   ↓
10. FRONTEND (page.tsx)
    - Receives results
    - Updates state
    - Switches to Results tab
    ↓
11. DISPLAY (DiagnosisResults.tsx)
    - Shows main result
    - Displays scores
    - Lists recommendations
    - Shows risk category
```

---

## 🧠 **Technical Concepts Explained Simply**

### **1. What is Transfer Learning?**
Instead of training a model from scratch (which needs millions of images), we use a pre-trained model (ResNet50) that already knows how to recognize images. We then fine-tune it for mammograms.

**Analogy:** Like learning to drive. You don't start from zero - you already know how to use your hands and feet. You just learn the specific skills for driving.

### **2. What is an API?**
API (Application Programming Interface) is like a waiter in a restaurant:
- Frontend (customer) makes a request
- API (waiter) takes it to the backend (kitchen)
- Backend (kitchen) prepares the response
- API (waiter) brings it back to frontend (customer)

### **3. What is State in React?**
State is like the memory of a component. When you upload an image, the component "remembers" it using state.

**Example:**
```typescript
const [results, setResults] = useState(null);
// results = current value (null initially)
// setResults = function to update it
```

### **4. What is CORS?**
CORS (Cross-Origin Resource Sharing) allows your frontend (localhost:3000) to talk to your backend (localhost:8000). Without it, browsers block the requests for security.

### **5. What is Grad-CAM?**
Grad-CAM (Gradient-weighted Class Activation Mapping) creates a heatmap showing which parts of the image the AI focused on. It's like highlighting the important parts of a text.

---

## 🎓 **Key Technologies Used**

### **Backend:**
- **Python 3.14** - Programming language
- **FastAPI** - Web framework (creates the API)
- **PyTorch** - Deep learning library
- **PIL/Pillow** - Image processing
- **OpenCV** - Computer vision

### **Frontend:**
- **TypeScript** - JavaScript with types
- **Next.js** - React framework
- **React** - UI library
- **Tailwind CSS** - Styling
- **Framer Motion** - Animations

---

## 🔍 **How to Debug/Understand Issues**

### **If backend doesn't start:**
1. Check if port 8000 is already in use
2. Verify virtual environment is activated
3. Check if all packages are installed (`pip install -r requirements.txt`)

### **If frontend doesn't connect:**
1. Check if backend is running on port 8000
2. Check CORS settings in `main.py`
3. Verify `API_BASE_URL` in `utils.ts`

### **If predictions are wrong:**
1. Check model file exists (`models/best_model.pth`)
2. Verify image preprocessing matches training
3. Check model was trained on similar images

---

## 📝 **Important Notes for Your Presentation**

1. **Model Accuracy:** Your model has ~78% validation accuracy (from training logs)
2. **No Fake Data:** All displayed values come from actual predictions
3. **Three AI Systems:**
   - **ML (CNN)**: Deep learning for image classification
   - **Expert System**: Rule-based medical guidelines
   - **Fuzzy Logic**: Handles uncertainty
4. **Explainability:** Grad-CAM shows why the AI made its decision

---

## 🚀 **Quick Reference: File Purposes**

| File | Purpose | When to Look |
|------|---------|--------------|
| `backend/main.py` | Server entry point | Starting the backend |
| `backend/src/api/routes.py` | API endpoints | Understanding API flow |
| `backend/src/ml/cnn_classifier.py` | AI model | Understanding predictions |
| `backend/src/traditional_ai/expert_system.py` | Rule-based AI | Understanding recommendations |
| `backend/src/traditional_ai/fuzzy_logic.py` | Uncertainty handling | Understanding risk scores |
| `frontend/src/app/page.tsx` | Main page | Understanding user flow |
| `frontend/src/components/DiagnosisResults.tsx` | Results display | Understanding UI |
| `frontend/src/lib/types.ts` | Data structures | Understanding data format |

---

## 💡 **Tips for Understanding Code**

1. **Start with the flow:** Follow one complete request from frontend to backend
2. **Read comments:** Code has comments explaining what it does
3. **Print statements:** Add `print()` in Python or `console.log()` in TypeScript to see what's happening
4. **Break it down:** Don't try to understand everything at once. Focus on one file at a time
5. **Use the browser dev tools:** Press F12 to see network requests and console logs

---

## 🎯 **Summary**

**Your system works like this:**
1. User uploads mammogram image
2. Frontend sends it to backend
3. Backend uses three AI systems:
   - CNN model predicts benign/malignant
   - Expert system applies medical rules
   - Fuzzy logic handles uncertainty
4. Results are combined and sent back
5. Frontend displays beautiful results

**The code is organized into:**
- **Backend**: Python code that does the AI work
- **Frontend**: React code that shows the user interface
- **Components**: Reusable UI pieces

**Remember:** You don't need to understand everything perfectly. Focus on the main flow and the key files. The rest will make sense as you explore!

---

**Good luck with your project! 🎉**

