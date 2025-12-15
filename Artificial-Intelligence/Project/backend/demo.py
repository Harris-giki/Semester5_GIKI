"""
Demo Script for Breast Tumor Diagnosis System
Run this to test the system components without the API.
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.ml.cnn_classifier import BreastTumorClassifier
from src.traditional_ai.expert_system import BreastTumorExpertSystem
from src.traditional_ai.fuzzy_logic import FuzzyDiagnosisSystem


def demo_expert_system():
    """Demonstrate the Rule-Based Expert System."""
    print("\n" + "=" * 60)
    print("RULE-BASED EXPERT SYSTEM DEMO")
    print("=" * 60)
    
    expert = BreastTumorExpertSystem()
    
    # Test Case 1: High confidence malignant
    print("\n--- Test Case 1: High Confidence Malignant ---")
    ml_prediction = {
        "predicted_class": "malignant",
        "confidence": 0.92,
        "severity_score": 85.0
    }
    patient_data = {
        "age": 55,
        "family_history": True
    }
    
    result = expert.analyze(ml_prediction, patient_data)
    print_expert_result(result)
    
    # Test Case 2: Moderate confidence benign
    print("\n--- Test Case 2: Moderate Confidence Benign ---")
    ml_prediction = {
        "predicted_class": "benign",
        "confidence": 0.78,
        "severity_score": 22.0
    }
    patient_data = {
        "age": 42
    }
    
    result = expert.analyze(ml_prediction, patient_data)
    print_expert_result(result)
    
    # Test Case 3: Borderline case
    print("\n--- Test Case 3: Borderline Case ---")
    ml_prediction = {
        "predicted_class": "malignant",
        "confidence": 0.58,
        "severity_score": 58.0
    }
    patient_data = {
        "age": 35,
        "pain_level": 6,
        "lump_detected": True
    }
    
    result = expert.analyze(ml_prediction, patient_data)
    print_expert_result(result)


def print_expert_result(result):
    """Pretty print expert system results."""
    summary = result["diagnosis_summary"]
    print(f"  Classification: {summary['predicted_class'].upper()}")
    print(f"  Confidence: {summary['confidence']:.1%}")
    print(f"  Risk Level: {summary['risk_level']}")
    print(f"  Urgency: {summary['urgency']}")
    print(f"\n  Recommendations:")
    for i, rec in enumerate(result["recommendations"][:3], 1):
        print(f"    {i}. {rec}")
    print(f"\n  Rules Fired: {len(result['rules_fired'])}")
    for rule in result["rules_fired"][:2]:
        print(f"    - {rule['id']}: {rule['name']}")
    print(f"\n  Follow-up: {result['follow_up']['description']}")


def demo_fuzzy_system():
    """Demonstrate the Fuzzy Logic System."""
    print("\n" + "=" * 60)
    print("FUZZY LOGIC SYSTEM DEMO")
    print("=" * 60)
    
    fuzzy = FuzzyDiagnosisSystem()
    
    # Test Case 1: High confidence, high severity
    print("\n--- Test Case 1: High Risk Profile ---")
    result = fuzzy.analyze(
        confidence=0.90,
        severity_score=85,
        age=60,
        pain_level=7
    )
    print_fuzzy_result(result)
    
    # Test Case 2: Low confidence, moderate severity
    print("\n--- Test Case 2: Uncertain Case ---")
    result = fuzzy.analyze(
        confidence=0.55,
        severity_score=50,
        age=45
    )
    print_fuzzy_result(result)
    
    # Test Case 3: High confidence, low severity
    print("\n--- Test Case 3: Low Risk Profile ---")
    result = fuzzy.analyze(
        confidence=0.95,
        severity_score=15,
        age=38
    )
    print_fuzzy_result(result)


def print_fuzzy_result(result):
    """Pretty print fuzzy system results."""
    print(f"  Fuzzy Risk Score: {result['fuzzy_risk_score']:.1f}")
    print(f"  Risk Category: {result['risk_category']}")
    print(f"  Uncertainty Level: {result['uncertainty_level']}")
    print(f"\n  Interpretation: {result['interpretation']}")
    
    if result['active_rules']:
        print(f"\n  Active Rules ({len(result['active_rules'])}):")
        for rule in result['active_rules'][:2]:
            conditions = " AND ".join([f"{c[0]}={c[1]}" for c in rule['conditions']])
            print(f"    IF {conditions} THEN {rule['output'][0]}={rule['output'][1]}")
            print(f"       (Firing Strength: {rule['firing_strength']:.3f})")


def demo_cnn_classifier():
    """Demonstrate the CNN Classifier (without actual image)."""
    print("\n" + "=" * 60)
    print("CNN CLASSIFIER INFO")
    print("=" * 60)
    
    print("\nInitializing ResNet50-based classifier...")
    classifier = BreastTumorClassifier(model_type="resnet50")
    
    print(f"  Model Type: {classifier.model_type}")
    print(f"  Device: {classifier.device}")
    print(f"  Classes: {classifier.classes}")
    
    # Count parameters
    total_params = sum(p.numel() for p in classifier.model.parameters())
    trainable_params = sum(p.numel() for p in classifier.model.parameters() if p.requires_grad)
    
    print(f"  Total Parameters: {total_params:,}")
    print(f"  Trainable Parameters: {trainable_params:,}")
    
    print("\n  To make predictions, use:")
    print("    classifier.predict(image_bytes)")
    print("    classifier.generate_gradcam(image_bytes)")


def demo_integration():
    """Demonstrate the full integration pipeline."""
    print("\n" + "=" * 60)
    print("INTEGRATION PIPELINE DEMO")
    print("=" * 60)
    
    # Simulate ML prediction
    ml_prediction = {
        "predicted_class": "malignant",
        "confidence": 0.82,
        "severity_score": 82.0,
        "probabilities": {
            "benign": 0.18,
            "malignant": 0.82
        }
    }
    
    patient_data = {
        "age": 52,
        "pain_level": 4,
        "family_history": True,
        "lump_detected": True
    }
    
    print("\n--- Input Data ---")
    print(f"  ML Prediction: {ml_prediction['predicted_class']} ({ml_prediction['confidence']:.1%})")
    print(f"  Patient Age: {patient_data['age']}")
    print(f"  Family History: {patient_data['family_history']}")
    print(f"  Symptoms: Pain Level {patient_data['pain_level']}, Lump Detected: {patient_data['lump_detected']}")
    
    # Expert System Analysis
    expert = BreastTumorExpertSystem()
    expert_result = expert.analyze(ml_prediction, patient_data)
    
    # Fuzzy Logic Analysis
    fuzzy = FuzzyDiagnosisSystem()
    fuzzy_result = fuzzy.analyze(
        confidence=ml_prediction["confidence"],
        severity_score=ml_prediction["severity_score"],
        age=patient_data["age"],
        pain_level=patient_data["pain_level"]
    )
    
    print("\n--- Expert System Result ---")
    print(f"  Risk Level: {expert_result['diagnosis_summary']['risk_level']}")
    print(f"  Urgency: {expert_result['diagnosis_summary']['urgency']}")
    
    print("\n--- Fuzzy Logic Result ---")
    print(f"  Fuzzy Risk Score: {fuzzy_result['fuzzy_risk_score']:.1f}")
    print(f"  Uncertainty: {fuzzy_result['uncertainty_level']}")
    
    # Combined score
    expert_risk_map = {"very_low": 10, "low": 30, "moderate": 50, "high": 70, "very_high": 90}
    expert_risk_score = expert_risk_map.get(expert_result['diagnosis_summary']['risk_level'], 50)
    
    composite = (
        0.4 * ml_prediction["severity_score"] +
        0.35 * expert_risk_score +
        0.25 * fuzzy_result["fuzzy_risk_score"]
    )
    
    print("\n--- Combined Analysis ---")
    print(f"  ML Severity: {ml_prediction['severity_score']:.1f} (weight: 0.4)")
    print(f"  Expert Risk: {expert_risk_score:.1f} (weight: 0.35)")
    print(f"  Fuzzy Risk: {fuzzy_result['fuzzy_risk_score']:.1f} (weight: 0.25)")
    print(f"  Composite Risk Score: {composite:.1f}")
    
    if composite >= 70:
        print("\n  ⚠️  IMMEDIATE ATTENTION REQUIRED")
    elif composite >= 50:
        print("\n  ⚡ URGENT FOLLOW-UP RECOMMENDED")
    else:
        print("\n  ✓ ROUTINE MONITORING ADVISED")


if __name__ == "__main__":
    print("=" * 60)
    print("BREAST TUMOR DIAGNOSIS SYSTEM - DEMO")
    print("=" * 60)
    
    demo_cnn_classifier()
    demo_expert_system()
    demo_fuzzy_system()
    demo_integration()
    
    print("\n" + "=" * 60)
    print("Demo complete! Start the API with: python main.py")
    print("=" * 60)

