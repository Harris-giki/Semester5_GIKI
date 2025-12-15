"""
Fuzzy Logic System for Breast Tumor Diagnosis
Handles uncertainty in ML predictions and patient symptoms
"""

import numpy as np
from typing import Dict, Tuple, Optional


class FuzzyMembershipFunctions:
    """
    Defines fuzzy membership functions for different variables.
    """
    
    @staticmethod
    def triangular(x: float, a: float, b: float, c: float) -> float:
        """
        Triangular membership function.
        
        Args:
            x: Input value
            a: Left foot
            b: Peak
            c: Right foot
        
        Returns:
            Membership degree [0, 1]
        """
        if x <= a or x >= c:
            return 0.0
        elif a < x <= b:
            return (x - a) / (b - a)
        else:
            return (c - x) / (c - b)
    
    @staticmethod
    def trapezoidal(x: float, a: float, b: float, c: float, d: float) -> float:
        """
        Trapezoidal membership function.
        
        Args:
            x: Input value
            a: Left foot
            b: Left shoulder
            c: Right shoulder
            d: Right foot
        
        Returns:
            Membership degree [0, 1]
        """
        if x <= a or x >= d:
            return 0.0
        elif a < x < b:
            return (x - a) / (b - a)
        elif b <= x <= c:
            return 1.0
        else:
            return (d - x) / (d - c)
    
    @staticmethod
    def gaussian(x: float, mean: float, sigma: float) -> float:
        """
        Gaussian membership function.
        
        Args:
            x: Input value
            mean: Center of the gaussian
            sigma: Standard deviation
        
        Returns:
            Membership degree [0, 1]
        """
        return np.exp(-0.5 * ((x - mean) / sigma) ** 2)


class FuzzyDiagnosisSystem:
    """
    Fuzzy Logic System for handling uncertainty in breast tumor diagnosis.
    Uses Mamdani inference system.
    """
    
    def __init__(self):
        self.mf = FuzzyMembershipFunctions()
        
        # Define fuzzy sets for confidence
        self.confidence_sets = {
            "very_low": lambda x: self.mf.trapezoidal(x, 0, 0, 0.3, 0.45),
            "low": lambda x: self.mf.triangular(x, 0.35, 0.5, 0.65),
            "medium": lambda x: self.mf.triangular(x, 0.55, 0.7, 0.85),
            "high": lambda x: self.mf.trapezoidal(x, 0.75, 0.9, 1.0, 1.0)
        }
        
        # Define fuzzy sets for severity score (0-100)
        self.severity_sets = {
            "minimal": lambda x: self.mf.trapezoidal(x, 0, 0, 15, 30),
            "low": lambda x: self.mf.triangular(x, 20, 35, 50),
            "moderate": lambda x: self.mf.triangular(x, 40, 55, 70),
            "high": lambda x: self.mf.triangular(x, 60, 75, 90),
            "critical": lambda x: self.mf.trapezoidal(x, 80, 90, 100, 100)
        }
        
        # Define fuzzy sets for age
        self.age_sets = {
            "young": lambda x: self.mf.trapezoidal(x, 18, 18, 35, 45),
            "middle": lambda x: self.mf.triangular(x, 40, 50, 65),
            "senior": lambda x: self.mf.trapezoidal(x, 55, 70, 100, 100)
        }
        
        # Define fuzzy sets for pain level (0-10)
        self.pain_sets = {
            "none": lambda x: self.mf.trapezoidal(x, 0, 0, 1, 2),
            "mild": lambda x: self.mf.triangular(x, 1, 3, 5),
            "moderate": lambda x: self.mf.triangular(x, 4, 6, 8),
            "severe": lambda x: self.mf.trapezoidal(x, 7, 8, 10, 10)
        }
        
        # Define fuzzy sets for risk output (0-100)
        self.risk_sets = {
            "very_low": lambda x: self.mf.trapezoidal(x, 0, 0, 10, 25),
            "low": lambda x: self.mf.triangular(x, 15, 30, 45),
            "moderate": lambda x: self.mf.triangular(x, 35, 50, 65),
            "high": lambda x: self.mf.triangular(x, 55, 70, 85),
            "very_high": lambda x: self.mf.trapezoidal(x, 75, 90, 100, 100)
        }
        
        # Define fuzzy rules
        self.rules = self._define_rules()
    
    def _define_rules(self) -> list:
        """Define fuzzy IF-THEN rules."""
        return [
            # High confidence + High severity = Very High Risk
            {
                "conditions": [("confidence", "high"), ("severity", "critical")],
                "output": ("risk", "very_high"),
                "weight": 1.0
            },
            {
                "conditions": [("confidence", "high"), ("severity", "high")],
                "output": ("risk", "very_high"),
                "weight": 0.95
            },
            # Medium confidence + High severity = High Risk
            {
                "conditions": [("confidence", "medium"), ("severity", "high")],
                "output": ("risk", "high"),
                "weight": 0.9
            },
            {
                "conditions": [("confidence", "medium"), ("severity", "critical")],
                "output": ("risk", "very_high"),
                "weight": 0.85
            },
            # Low confidence + High severity = Moderate-High Risk
            {
                "conditions": [("confidence", "low"), ("severity", "high")],
                "output": ("risk", "moderate"),
                "weight": 0.8
            },
            {
                "conditions": [("confidence", "low"), ("severity", "critical")],
                "output": ("risk", "high"),
                "weight": 0.85
            },
            # High confidence + Low severity = Low Risk
            {
                "conditions": [("confidence", "high"), ("severity", "low")],
                "output": ("risk", "low"),
                "weight": 0.95
            },
            {
                "conditions": [("confidence", "high"), ("severity", "minimal")],
                "output": ("risk", "very_low"),
                "weight": 1.0
            },
            # Medium confidence + Moderate severity = Moderate Risk
            {
                "conditions": [("confidence", "medium"), ("severity", "moderate")],
                "output": ("risk", "moderate"),
                "weight": 0.85
            },
            # Very low confidence = Uncertain, default moderate
            {
                "conditions": [("confidence", "very_low")],
                "output": ("risk", "moderate"),
                "weight": 0.7
            },
            # Age considerations
            {
                "conditions": [("age", "young"), ("severity", "high")],
                "output": ("risk", "high"),
                "weight": 0.8
            },
            {
                "conditions": [("age", "senior"), ("severity", "moderate")],
                "output": ("risk", "moderate"),
                "weight": 0.7
            },
            # Pain considerations
            {
                "conditions": [("pain", "severe"), ("severity", "high")],
                "output": ("risk", "very_high"),
                "weight": 0.9
            },
            {
                "conditions": [("pain", "moderate"), ("severity", "moderate")],
                "output": ("risk", "moderate"),
                "weight": 0.75
            }
        ]
    
    def fuzzify(self, input_values: Dict) -> Dict:
        """
        Fuzzify input values into fuzzy sets.
        
        Args:
            input_values: Dictionary with confidence, severity, age, pain
        
        Returns:
            Dictionary of fuzzy memberships
        """
        memberships = {}
        
        # Fuzzify confidence
        if "confidence" in input_values:
            conf = input_values["confidence"]
            memberships["confidence"] = {
                name: func(conf) 
                for name, func in self.confidence_sets.items()
            }
        
        # Fuzzify severity
        if "severity_score" in input_values:
            sev = input_values["severity_score"]
            memberships["severity"] = {
                name: func(sev)
                for name, func in self.severity_sets.items()
            }
        
        # Fuzzify age
        if "age" in input_values:
            age = input_values["age"]
            memberships["age"] = {
                name: func(age)
                for name, func in self.age_sets.items()
            }
        
        # Fuzzify pain
        if "pain_level" in input_values:
            pain = input_values["pain_level"]
            memberships["pain"] = {
                name: func(pain)
                for name, func in self.pain_sets.items()
            }
        
        return memberships
    
    def evaluate_rules(self, memberships: Dict) -> Dict:
        """
        Evaluate fuzzy rules using Mamdani inference.
        
        Args:
            memberships: Fuzzified input values
        
        Returns:
            Aggregated output fuzzy set
        """
        output_activations = {}
        rule_details = []
        
        for rule in self.rules:
            # Calculate firing strength (AND = min)
            firing_strength = 1.0
            applicable = True
            
            for var, fuzzy_set in rule["conditions"]:
                if var in memberships:
                    membership_val = memberships[var].get(fuzzy_set, 0)
                    firing_strength = min(firing_strength, membership_val)
                else:
                    applicable = False
                    break
            
            if not applicable or firing_strength <= 0:
                continue
            
            # Apply rule weight
            firing_strength *= rule["weight"]
            
            # Get output fuzzy set
            output_var, output_set = rule["output"]
            
            # Aggregate using MAX
            if output_set not in output_activations:
                output_activations[output_set] = firing_strength
            else:
                output_activations[output_set] = max(
                    output_activations[output_set], 
                    firing_strength
                )
            
            if firing_strength > 0.1:
                rule_details.append({
                    "conditions": rule["conditions"],
                    "output": rule["output"],
                    "firing_strength": firing_strength
                })
        
        return output_activations, rule_details
    
    def defuzzify(self, output_activations: Dict) -> float:
        """
        Defuzzify using centroid method.
        
        Args:
            output_activations: Activated output fuzzy sets
        
        Returns:
            Crisp output value (risk score 0-100)
        """
        if not output_activations:
            return 50.0  # Default moderate risk
        
        # Create universe of discourse
        x = np.linspace(0, 100, 200)
        
        # Build aggregated output
        aggregated = np.zeros_like(x)
        
        for fuzzy_set, activation in output_activations.items():
            if fuzzy_set in self.risk_sets:
                membership_func = self.risk_sets[fuzzy_set]
                # Apply activation level (truncate)
                for i, val in enumerate(x):
                    aggregated[i] = max(
                        aggregated[i], 
                        min(activation, membership_func(val))
                    )
        
        # Centroid defuzzification
        if np.sum(aggregated) == 0:
            return 50.0
        
        centroid = np.sum(x * aggregated) / np.sum(aggregated)
        return float(centroid)
    
    def analyze(
        self,
        confidence: float,
        severity_score: float,
        age: Optional[int] = None,
        pain_level: Optional[int] = None
    ) -> Dict:
        """
        Perform complete fuzzy analysis.
        
        Args:
            confidence: ML model confidence (0-1)
            severity_score: Tumor severity score (0-100)
            age: Patient age (optional)
            pain_level: Pain level 0-10 (optional)
        
        Returns:
            Fuzzy analysis results
        """
        # Prepare input
        input_values = {
            "confidence": confidence,
            "severity_score": severity_score
        }
        if age is not None:
            input_values["age"] = age
        if pain_level is not None:
            input_values["pain_level"] = pain_level
        
        # Fuzzification
        memberships = self.fuzzify(input_values)
        
        # Rule evaluation
        output_activations, rule_details = self.evaluate_rules(memberships)
        
        # Defuzzification
        risk_score = self.defuzzify(output_activations)
        
        # Determine risk category
        risk_category = self._categorize_risk(risk_score)
        
        # Get uncertainty level
        uncertainty = self._calculate_uncertainty(memberships, output_activations)
        
        return {
            "fuzzy_risk_score": risk_score,
            "risk_category": risk_category,
            "uncertainty_level": uncertainty,
            "input_memberships": memberships,
            "output_activations": output_activations,
            "active_rules": rule_details[:5],  # Top 5 active rules
            "interpretation": self._interpret_results(risk_score, uncertainty)
        }
    
    def _categorize_risk(self, risk_score: float) -> str:
        """Categorize risk score into levels."""
        if risk_score < 20:
            return "very_low"
        elif risk_score < 40:
            return "low"
        elif risk_score < 60:
            return "moderate"
        elif risk_score < 80:
            return "high"
        else:
            return "very_high"
    
    def _calculate_uncertainty(
        self, 
        memberships: Dict, 
        activations: Dict
    ) -> str:
        """Calculate overall uncertainty level."""
        # Check confidence memberships
        if "confidence" in memberships:
            conf_mem = memberships["confidence"]
            
            # High uncertainty if multiple confidence sets have significant membership
            significant_memberships = sum(
                1 for v in conf_mem.values() if v > 0.3
            )
            
            if significant_memberships >= 3:
                return "high"
            elif significant_memberships >= 2:
                return "moderate"
            elif conf_mem.get("very_low", 0) > 0.5:
                return "high"
        
        # Check output activations
        if len(activations) >= 3:
            return "moderate"
        
        return "low"
    
    def _interpret_results(self, risk_score: float, uncertainty: str) -> str:
        """Generate human-readable interpretation."""
        if risk_score >= 80:
            base = "Very high risk detected. Immediate medical attention strongly recommended."
        elif risk_score >= 60:
            base = "High risk level. Prompt medical evaluation is advised."
        elif risk_score >= 40:
            base = "Moderate risk. Follow-up evaluation recommended."
        elif risk_score >= 20:
            base = "Low risk. Continue routine monitoring."
        else:
            base = "Very low risk. Standard screening schedule is appropriate."
        
        if uncertainty == "high":
            base += " Note: High uncertainty in assessment. Additional testing recommended."
        elif uncertainty == "moderate":
            base += " Note: Some uncertainty in assessment. Consider confirmatory tests."
        
        return base

