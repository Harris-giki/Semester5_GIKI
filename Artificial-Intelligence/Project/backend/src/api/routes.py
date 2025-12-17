"""
FastAPI Routes for Breast Tumor Diagnosis System
Handles image upload, prediction, and diagnosis
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from pydantic import BaseModel
from typing import Optional
import io
import base64
from PIL import Image

from ..ml.cnn_classifier import BreastTumorClassifier
from ..ml.preprocessing import enhance_contrast, get_image_stats
from ..traditional_ai.expert_system import BreastTumorExpertSystem
from ..traditional_ai.fuzzy_logic import FuzzyDiagnosisSystem


router = APIRouter()

# Initialize models (loaded once at startup)
classifier = None
expert_system = None
fuzzy_system = None


def get_classifier():
    """Lazy initialization of classifier."""
    global classifier
    if classifier is None:
        import os
        model_path = os.path.join(os.path.dirname(__file__), "../../models/best_model.pth")
        classifier = BreastTumorClassifier(
            model_path=model_path,
            model_type="transfer",
            backbone="resnet50"
        )
    return classifier


def get_expert_system():
    """Lazy initialization of expert system."""
    global expert_system
    if expert_system is None:
        expert_system = BreastTumorExpertSystem()
    return expert_system


def get_fuzzy_system():
    """Lazy initialization of fuzzy system."""
    global fuzzy_system
    if fuzzy_system is None:
        fuzzy_system = FuzzyDiagnosisSystem()
    return fuzzy_system




@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Breast Tumor Diagnosis API",
        "version": "1.0.0",
        "model_accuracy": "94.0%"
    }


@router.post("/diagnose")
async def full_diagnosis(
    image: UploadFile = File(...),
    age: Optional[int] = Form(None),
    pain_level: Optional[int] = Form(None),
    family_history: bool = Form(False),
    lump_detected: bool = Form(False),
    nipple_discharge: bool = Form(False),
    enhance: bool = Form(False)
):
    """
    Perform complete diagnosis combining ML and Traditional AI.
    
    Args:
        image: Mammogram image file
        age: Patient age
        pain_level: Pain level (0-10)
        family_history: Family history of breast cancer
        lump_detected: Whether lump was detected
        nipple_discharge: Whether nipple discharge is present
        enhance: Apply contrast enhancement
    
    Returns:
        Complete diagnosis with ML predictions, expert analysis, and recommendations
    """
    try:
        # Validate file type
        if not image.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read image bytes
        image_bytes = await image.read()
        
        # Optional contrast enhancement
        if enhance:
            image_bytes = enhance_contrast(image_bytes)
        
        # Get image statistics
        stats = get_image_stats(image_bytes)
        
        # Step 1: ML Prediction
        clf = get_classifier()
        ml_prediction = clf.predict(image_bytes)
        
        # Step 2: Expert System Analysis
        patient_data = {}
        if age is not None:
            patient_data["age"] = age
        if pain_level is not None:
            patient_data["pain_level"] = pain_level
        patient_data["family_history"] = family_history
        patient_data["lump_detected"] = lump_detected
        patient_data["nipple_discharge"] = nipple_discharge
        
        expert = get_expert_system()
        expert_analysis = expert.analyze(ml_prediction, patient_data)
        
        # Step 3: Fuzzy Logic Analysis
        fuzzy = get_fuzzy_system()
        fuzzy_analysis = fuzzy.analyze(
            confidence=ml_prediction["confidence"],
            severity_score=ml_prediction["severity_score"],
            age=age,
            pain_level=pain_level
        )
        
        # Step 4: Combine results for final recommendation
        combined = _combine_analyses(ml_prediction, expert_analysis, fuzzy_analysis)
        
        return {
            "success": True,
            "ml_prediction": ml_prediction,
            "expert_analysis": expert_analysis,
            "fuzzy_analysis": fuzzy_analysis,
            "combined_recommendation": combined,
            "image_stats": stats
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/gradcam")
async def generate_gradcam(
    image: UploadFile = File(...)
):
    """
    Generate Grad-CAM visualization for model explainability.
    
    Args:
        image: Mammogram image file
    
    Returns:
        Base64 encoded heatmap overlay image and prediction
    """
    try:
        # Validate file type
        if not image.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read image bytes
        image_bytes = await image.read()
        
        # Generate Grad-CAM
        clf = get_classifier()
        heatmap, prediction = clf.generate_gradcam(image_bytes)
        
        # Convert heatmap to base64
        pil_image = Image.fromarray(heatmap)
        buffer = io.BytesIO()
        pil_image.save(buffer, format="PNG")
        buffer.seek(0)
        
        heatmap_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        return {
            "success": True,
            "prediction": prediction,
            "heatmap": heatmap_base64,
            "heatmap_format": "png"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def _combine_analyses(
    ml_prediction: dict,
    expert_analysis: dict,
    fuzzy_analysis: dict
) -> dict:
    """
    Combine all analyses into a unified recommendation.
    """
    # Get risk levels from each system
    ml_severity = ml_prediction.get("severity_score", 50)
    expert_risk = expert_analysis.get("diagnosis_summary", {}).get("risk_level", "moderate")
    fuzzy_risk = fuzzy_analysis.get("fuzzy_risk_score", 50)
    
    # Calculate composite risk score (weighted average)
    risk_map = {
        "very_low": 10,
        "low": 30,
        "moderate": 50,
        "high": 70,
        "very_high": 90
    }
    expert_risk_score = risk_map.get(expert_risk, 50)
    
    composite_score = (
        0.4 * ml_severity +
        0.35 * expert_risk_score +
        0.25 * fuzzy_risk
    )
    
    # Determine final risk category
    if composite_score >= 75:
        final_risk = "very_high"
        action = "immediate"
    elif composite_score >= 55:
        final_risk = "high"
        action = "urgent"
    elif composite_score >= 35:
        final_risk = "moderate"
        action = "soon"
    elif composite_score >= 15:
        final_risk = "low"
        action = "routine"
    else:
        final_risk = "very_low"
        action = "routine"
    
    # Get top recommendations
    recommendations = expert_analysis.get("recommendations", [])[:5]
    
    # Build summary
    summary = _generate_summary(
        ml_prediction.get("predicted_class"),
        ml_prediction.get("confidence"),
        final_risk,
        fuzzy_analysis.get("uncertainty_level", "low")
    )
    
    return {
        "composite_risk_score": round(composite_score, 2),
        "final_risk_category": final_risk,
        "recommended_action": action,
        "confidence_level": "high" if ml_prediction.get("confidence", 0) > 0.8 else "moderate" if ml_prediction.get("confidence", 0) > 0.6 else "low",
        "top_recommendations": recommendations,
        "summary": summary,
        "needs_immediate_attention": composite_score >= 70
    }


def _generate_summary(
    predicted_class: str,
    confidence: float,
    risk_level: str,
    uncertainty: str
) -> str:
    """Generate a human-readable summary of the diagnosis."""
    
    if predicted_class == "malignant":
        if confidence > 0.85:
            base = f"The analysis indicates a HIGH PROBABILITY of malignant tumor with {confidence:.1%} confidence."
        elif confidence > 0.70:
            base = f"The analysis suggests POSSIBLE malignant tumor with {confidence:.1%} confidence."
        else:
            base = f"The analysis shows INCONCLUSIVE results leaning towards malignant with {confidence:.1%} confidence."
    else:
        if confidence > 0.90:
            base = f"The analysis indicates the tumor is likely BENIGN with {confidence:.1%} confidence."
        elif confidence > 0.75:
            base = f"The analysis suggests the tumor is probably benign with {confidence:.1%} confidence."
        else:
            base = f"The analysis shows INCONCLUSIVE results leaning towards benign with {confidence:.1%} confidence."
    
    risk_descriptions = {
        "very_high": "Immediate medical consultation is strongly recommended.",
        "high": "Prompt medical evaluation is advised within the next few days.",
        "moderate": "Follow-up evaluation should be scheduled within the next few weeks.",
        "low": "Continue routine monitoring with regular check-ups.",
        "very_low": "No immediate concern. Maintain regular screening schedule."
    }
    
    base += f" {risk_descriptions.get(risk_level, '')}"
    
    if uncertainty == "high":
        base += " Note: There is some uncertainty in this assessment. Additional testing is recommended for confirmation."
    
    return base

