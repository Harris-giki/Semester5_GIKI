"""
Rule-Based Expert System for Breast Tumor Diagnosis
Implements IF-THEN rules based on oncology guidelines
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Callable
from enum import Enum


class RiskLevel(Enum):
    """Risk level classifications."""
    VERY_LOW = "very_low"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    VERY_HIGH = "very_high"


class UrgencyLevel(Enum):
    """Urgency level for recommendations."""
    ROUTINE = "routine"
    SOON = "soon"
    URGENT = "urgent"
    IMMEDIATE = "immediate"


@dataclass
class Rule:
    """
    Represents a single IF-THEN rule in the expert system.
    """
    id: str
    name: str
    description: str
    conditions: Callable[[Dict], bool]
    conclusions: Dict
    priority: int = 1
    
    def evaluate(self, facts: Dict) -> Optional[Dict]:
        """
        Evaluate the rule against given facts.
        
        Args:
            facts: Dictionary of current facts
        
        Returns:
            Conclusions if rule fires, None otherwise
        """
        try:
            if self.conditions(facts):
                return self.conclusions
        except (KeyError, TypeError):
            pass
        return None


class RuleBase:
    """
    Collection of rules for the expert system.
    Implements forward chaining inference.
    """
    
    def __init__(self):
        self.rules: List[Rule] = []
        self._setup_default_rules()
    
    def _setup_default_rules(self):
        """Initialize default oncology-based rules."""
        
        # Rule 1: High confidence malignant - Very High Risk
        self.add_rule(Rule(
            id="R001",
            name="High Confidence Malignant",
            description="Malignant tumor with high confidence requires immediate biopsy",
            conditions=lambda f: (
                f.get("predicted_class") == "malignant" and 
                f.get("confidence", 0) > 0.85
            ),
            conclusions={
                "risk_level": RiskLevel.VERY_HIGH,
                "urgency": UrgencyLevel.IMMEDIATE,
                "recommendations": [
                    "Immediate biopsy recommended",
                    "Oncology referral required",
                    "Additional imaging (MRI/Ultrasound) suggested",
                    "Discuss treatment options with oncology team"
                ],
                "explanation": "High confidence malignant classification indicates high probability of cancer. Immediate specialist consultation is critical.",
                "follow_up_days": 3
            },
            priority=10
        ))
        
        # Rule 2: Moderate confidence malignant
        self.add_rule(Rule(
            id="R002",
            name="Moderate Confidence Malignant",
            description="Malignant with moderate confidence needs additional imaging",
            conditions=lambda f: (
                f.get("predicted_class") == "malignant" and 
                0.70 <= f.get("confidence", 0) <= 0.85
            ),
            conclusions={
                "risk_level": RiskLevel.HIGH,
                "urgency": UrgencyLevel.URGENT,
                "recommendations": [
                    "Additional diagnostic imaging recommended (MRI/Ultrasound)",
                    "Core needle biopsy should be scheduled",
                    "Oncology consultation within 1 week",
                    "Consider second radiologist opinion"
                ],
                "explanation": "Moderate confidence malignant finding requires confirmation through additional imaging and biopsy.",
                "follow_up_days": 7
            },
            priority=9
        ))
        
        # Rule 3: Low confidence malignant (borderline)
        self.add_rule(Rule(
            id="R003",
            name="Borderline Malignant",
            description="Low confidence malignant - uncertainty requires careful evaluation",
            conditions=lambda f: (
                f.get("predicted_class") == "malignant" and 
                0.55 <= f.get("confidence", 0) < 0.70
            ),
            conclusions={
                "risk_level": RiskLevel.MODERATE,
                "urgency": UrgencyLevel.SOON,
                "recommendations": [
                    "Supplemental imaging required (breast ultrasound)",
                    "Short-term follow-up mammogram in 3-6 months",
                    "Consider MRI for dense breast tissue",
                    "Second radiologist review recommended"
                ],
                "explanation": "Borderline classification with uncertainty. Additional evaluation needed to rule out malignancy.",
                "follow_up_days": 14
            },
            priority=8
        ))
        
        # Rule 4: High confidence benign
        self.add_rule(Rule(
            id="R004",
            name="High Confidence Benign",
            description="Benign tumor with high confidence - routine follow-up",
            conditions=lambda f: (
                f.get("predicted_class") == "benign" and 
                f.get("confidence", 0) > 0.90
            ),
            conclusions={
                "risk_level": RiskLevel.VERY_LOW,
                "urgency": UrgencyLevel.ROUTINE,
                "recommendations": [
                    "Continue routine annual mammography screening",
                    "Breast self-examination monthly",
                    "No immediate intervention required",
                    "Healthy lifestyle maintenance recommended"
                ],
                "explanation": "High confidence benign finding. Continue regular screening schedule.",
                "follow_up_days": 365
            },
            priority=5
        ))
        
        # Rule 5: Moderate confidence benign
        self.add_rule(Rule(
            id="R005",
            name="Moderate Confidence Benign",
            description="Benign with moderate confidence - enhanced monitoring",
            conditions=lambda f: (
                f.get("predicted_class") == "benign" and 
                0.75 <= f.get("confidence", 0) <= 0.90
            ),
            conclusions={
                "risk_level": RiskLevel.LOW,
                "urgency": UrgencyLevel.ROUTINE,
                "recommendations": [
                    "Follow-up mammogram in 6 months",
                    "Supplemental ultrasound if breast density is high",
                    "Continue breast self-examination",
                    "Monitor for any changes"
                ],
                "explanation": "Moderate confidence benign finding. Short-term follow-up recommended for confirmation.",
                "follow_up_days": 180
            },
            priority=6
        ))
        
        # Rule 6: Low confidence benign (uncertain)
        self.add_rule(Rule(
            id="R006",
            name="Uncertain Benign",
            description="Low confidence benign - additional evaluation needed",
            conditions=lambda f: (
                f.get("predicted_class") == "benign" and 
                0.55 <= f.get("confidence", 0) < 0.75
            ),
            conclusions={
                "risk_level": RiskLevel.MODERATE,
                "urgency": UrgencyLevel.SOON,
                "recommendations": [
                    "Diagnostic mammogram views recommended",
                    "Breast ultrasound for characterization",
                    "Follow-up in 3 months",
                    "Consider second opinion"
                ],
                "explanation": "Low confidence classification warrants additional imaging for accurate assessment.",
                "follow_up_days": 90
            },
            priority=7
        ))
        
        # Rule 7: Age-based risk modification (older patients)
        self.add_rule(Rule(
            id="R007",
            name="Elderly Patient Consideration",
            description="Adjust recommendations for older patients",
            conditions=lambda f: (
                f.get("age", 0) >= 65 and
                f.get("predicted_class") == "malignant"
            ),
            conclusions={
                "age_consideration": True,
                "additional_recommendations": [
                    "Consider overall health status and life expectancy",
                    "Discuss treatment preferences and quality of life goals",
                    "Evaluate for comorbidities before aggressive treatment"
                ]
            },
            priority=3
        ))
        
        # Rule 8: Young patient high risk
        self.add_rule(Rule(
            id="R008",
            name="Young Patient Malignant",
            description="Young patients with malignant findings need aggressive follow-up",
            conditions=lambda f: (
                f.get("age", 50) < 40 and
                f.get("predicted_class") == "malignant" and
                f.get("confidence", 0) > 0.60
            ),
            conclusions={
                "age_consideration": True,
                "additional_recommendations": [
                    "Genetic counseling and BRCA testing recommended",
                    "Consider family history of breast/ovarian cancer",
                    "Discuss fertility preservation options before treatment",
                    "Aggressive treatment approach typically recommended"
                ]
            },
            priority=4
        ))
        
        # Rule 9: Family history consideration
        self.add_rule(Rule(
            id="R009",
            name="Family History Risk Factor",
            description="Family history increases risk assessment",
            conditions=lambda f: (
                f.get("family_history", False) and
                f.get("confidence", 0) > 0.50
            ),
            conclusions={
                "family_history_flag": True,
                "risk_modifier": "elevated",
                "additional_recommendations": [
                    "Genetic counseling strongly recommended",
                    "Consider more frequent screening intervals",
                    "Discuss prophylactic options if appropriate"
                ]
            },
            priority=2
        ))
        
        # Rule 10: Symptoms present
        self.add_rule(Rule(
            id="R010",
            name="Symptomatic Patient",
            description="Symptoms increase clinical concern",
            conditions=lambda f: (
                (f.get("pain_level", 0) > 5 or 
                 f.get("lump_detected", False) or
                 f.get("nipple_discharge", False)) and
                f.get("predicted_class") == "malignant"
            ),
            conclusions={
                "symptom_flag": True,
                "urgency_modifier": "increased",
                "additional_recommendations": [
                    "Clinical examination required immediately",
                    "Correlate imaging findings with physical exam",
                    "Document all symptoms for oncology referral"
                ]
            },
            priority=3
        ))
    
    def add_rule(self, rule: Rule):
        """Add a rule to the knowledge base."""
        self.rules.append(rule)
        # Sort by priority (higher priority first)
        self.rules.sort(key=lambda r: r.priority, reverse=True)
    
    def infer(self, facts: Dict) -> List[Dict]:
        """
        Forward chaining inference.
        
        Args:
            facts: Dictionary of current facts
        
        Returns:
            List of conclusions from fired rules
        """
        fired_rules = []
        
        for rule in self.rules:
            conclusion = rule.evaluate(facts)
            if conclusion:
                fired_rules.append({
                    "rule_id": rule.id,
                    "rule_name": rule.name,
                    "description": rule.description,
                    "conclusions": conclusion
                })
        
        return fired_rules


class BreastTumorExpertSystem:
    """
    Main Expert System class that integrates ML predictions with rule-based reasoning.
    """
    
    def __init__(self):
        self.rule_base = RuleBase()
        self.working_memory: Dict = {}
    
    def analyze(
        self,
        ml_prediction: Dict,
        patient_data: Optional[Dict] = None
    ) -> Dict:
        """
        Analyze ML predictions using rule-based expert reasoning.
        
        Args:
            ml_prediction: Dictionary with CNN prediction results
            patient_data: Optional patient metadata (age, symptoms, etc.)
        
        Returns:
            Comprehensive diagnosis report
        """
        # Build facts from ML prediction and patient data
        facts = {
            "predicted_class": ml_prediction.get("predicted_class"),
            "confidence": ml_prediction.get("confidence", 0),
            "severity_score": ml_prediction.get("severity_score", 0),
            "probabilities": ml_prediction.get("probabilities", {})
        }
        
        # Add patient data if available
        if patient_data:
            facts.update(patient_data)
        
        # Store in working memory
        self.working_memory = facts.copy()
        
        # Run inference
        fired_rules = self.rule_base.infer(facts)
        
        # Compile results
        result = self._compile_diagnosis(facts, fired_rules)
        
        return result
    
    def _compile_diagnosis(self, facts: Dict, fired_rules: List[Dict]) -> Dict:
        """Compile all fired rules into a unified diagnosis report."""
        
        # Find primary diagnosis (highest priority rule with main classification)
        primary_diagnosis = None
        risk_level = RiskLevel.MODERATE
        urgency = UrgencyLevel.ROUTINE
        
        all_recommendations = []
        all_explanations = []
        additional_considerations = []
        
        for fr in fired_rules:
            conclusions = fr["conclusions"]
            
            # Get primary diagnosis from classification rules
            if "risk_level" in conclusions and primary_diagnosis is None:
                primary_diagnosis = fr
                risk_level = conclusions["risk_level"]
                urgency = conclusions.get("urgency", UrgencyLevel.ROUTINE)
            
            # Collect all recommendations
            if "recommendations" in conclusions:
                all_recommendations.extend(conclusions["recommendations"])
            if "additional_recommendations" in conclusions:
                additional_considerations.extend(conclusions["additional_recommendations"])
            
            # Collect explanations
            if "explanation" in conclusions:
                all_explanations.append(conclusions["explanation"])
        
        # Remove duplicates while preserving order
        all_recommendations = list(dict.fromkeys(all_recommendations))
        additional_considerations = list(dict.fromkeys(additional_considerations))
        
        # Calculate follow-up days
        follow_up_days = 365
        for fr in fired_rules:
            if "follow_up_days" in fr["conclusions"]:
                follow_up_days = min(follow_up_days, fr["conclusions"]["follow_up_days"])
        
        return {
            "diagnosis_summary": {
                "predicted_class": facts.get("predicted_class"),
                "confidence": facts.get("confidence"),
                "severity_score": facts.get("severity_score"),
                "risk_level": risk_level.value if isinstance(risk_level, RiskLevel) else risk_level,
                "urgency": urgency.value if isinstance(urgency, UrgencyLevel) else urgency
            },
            "recommendations": all_recommendations[:8],  # Top 8 recommendations
            "additional_considerations": additional_considerations,
            "explanations": all_explanations,
            "follow_up": {
                "recommended_days": follow_up_days,
                "description": self._get_follow_up_description(follow_up_days)
            },
            "rules_fired": [
                {
                    "id": fr["rule_id"],
                    "name": fr["rule_name"],
                    "description": fr["description"]
                }
                for fr in fired_rules
            ],
            "confidence_assessment": self._assess_confidence(facts.get("confidence", 0)),
            "patient_data_used": {k: v for k, v in facts.items() if k not in ["predicted_class", "confidence", "severity_score", "probabilities"]}
        }
    
    def _get_follow_up_description(self, days: int) -> str:
        """Get human-readable follow-up description."""
        if days <= 7:
            return "Immediate follow-up required within 1 week"
        elif days <= 14:
            return "Urgent follow-up within 2 weeks"
        elif days <= 30:
            return "Follow-up within 1 month"
        elif days <= 90:
            return "Follow-up in 3 months"
        elif days <= 180:
            return "Follow-up in 6 months"
        else:
            return "Annual routine screening"
    
    def _assess_confidence(self, confidence: float) -> Dict:
        """Assess the model's confidence level."""
        if confidence >= 0.90:
            return {
                "level": "very_high",
                "description": "Very high confidence in prediction",
                "reliability": "Results are highly reliable"
            }
        elif confidence >= 0.80:
            return {
                "level": "high",
                "description": "High confidence in prediction",
                "reliability": "Results are reliable with minor uncertainty"
            }
        elif confidence >= 0.70:
            return {
                "level": "moderate",
                "description": "Moderate confidence in prediction",
                "reliability": "Additional confirmation recommended"
            }
        elif confidence >= 0.60:
            return {
                "level": "low",
                "description": "Low confidence in prediction",
                "reliability": "Further evaluation strongly recommended"
            }
        else:
            return {
                "level": "very_low",
                "description": "Very low confidence - borderline case",
                "reliability": "Results require additional diagnostic workup"
            }

