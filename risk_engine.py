"""
PayShield AI - Pre-Payment Safeguard System
Team: Syntax Sorcerers
Module: risk_engine.py

Phase 3: Hybrid Risk Engine
Combines deterministic duress rule filters, scikit-learn anomaly classification,
and behavioral feature attribution into an explainable composite risk score.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from data_simulation import generate_ml_training_dataset, scan_text_for_threat_keywords

# ==============================================================================
# 1. MACHINE LEARNING ENGINE SINGLETON
# ==============================================================================

class MLFraudModel:
    """Trained machine learning models for anomaly & coercion scoring."""
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        # Generate training dataset and fit models
        self.df_train = generate_ml_training_dataset(n_samples=2000)
        
        self.feature_cols = [
            "amount", "is_known_payee", "has_active_call", "has_secrecy",
            "has_threat", "urgency_level", "emotional_pressure",
            "keyword_count", "hesitation_seconds", "category_code"
        ]

        X = self.df_train[self.feature_cols]
        y = self.df_train["label"]

        # Supervised Coercion Classifier
        self.clf = RandomForestClassifier(
            n_estimators=100,
            max_depth=6,
            random_state=42,
            class_weight="balanced"
        )
        self.clf.fit(X, y)

        # Unsupervised Isolation Forest for Spending Telemetry Outliers
        self.iso_forest = IsolationForest(
            n_estimators=75,
            contamination=0.15,
            random_state=42
        )
        self.iso_forest.fit(X[["amount", "hesitation_seconds", "urgency_level"]])

    def predict_coercion_proba(self, feature_dict: dict) -> float:
        """Returns ML model's predicted probability of coercion [0.0, 1.0]."""
        sample_df = pd.DataFrame([feature_dict])[self.feature_cols]
        proba = self.clf.predict_proba(sample_df)[0][1]
        return float(proba)

    def get_feature_importances(self) -> dict:
        """Returns model feature importance weights for technical transparency."""
        importances = self.clf.feature_importances_
        return dict(zip(self.feature_cols, [round(float(v), 3) for v in importances]))


# ==============================================================================
# 2. HYBRID RISK ASSESSMENT ENGINE
# ==============================================================================

class HybridRiskEngine:
    """
    Evaluates transaction telemetry using:
    1. Deterministic Hard-Rule Duress Interceptor
    2. ML Supervised Coercion Probability
    3. Historical Baseline Anomaly Ratio
    4. Explainable Factor Attribution (XAI)
    """

    @staticmethod
    def _map_category_to_code(category_str: str) -> int:
        cat = category_str.lower()
        if "grocery" in cat or "shopping" in cat:
            return 0
        if "rent" in cat or "utilit" in cat:
            return 1
        if "family" in cat or "friend" in cat:
            return 2
        if "invest" in cat or "crypto" in cat or "task" in cat:
            return 3
        if "fine" in cat or "bail" in cat or "legal" in cat or "verif" in cat:
            return 4
        return 0

    @classmethod
    def evaluate_transaction(cls, telemetry: dict, user_baseline: dict) -> dict:
        """
        Main evaluation entrypoint.
        Returns composite risk score (0-100), risk tier, explainable factors, and triggers.
        """
        ml_model = MLFraudModel.get_instance()

        # Extract features
        amount = float(telemetry.get("amount", 0.0))
        mean_amount = max(1.0, float(user_baseline.get("mean_amount", 400.0)))
        amount_ratio = amount / mean_amount
        is_known_payee = 1 if telemetry.get("is_known_payee", False) else 0

        has_active_call = 1 if "Yes" in telemetry.get("q_active_call", "") else 0
        has_secrecy = 1 if "Yes" in telemetry.get("q_secrecy_instructed", "") else 0
        has_threat = 1 if "Yes" in telemetry.get("q_threat_or_fine", "") else 0

        urgency_str = telemetry.get("q_time_urgency", "")
        urgency_level = 2 if "Extreme" in urgency_str else (1 if "Moderate" in urgency_str else 0)

        emotional_pressure = int(telemetry.get("q_emotional_pressure", 1))
        hesitation = max(0.5, float(telemetry.get("elapsed_intake_seconds", 8.0)))
        category_code = cls._map_category_to_code(telemetry.get("q_payment_category", ""))

        flagged_kw = scan_text_for_threat_keywords(
            f"{telemetry.get('payment_note', '')} {telemetry.get('recipient_name', '')}"
        )
        keyword_count = len(flagged_kw)

        # Assemble ML Feature Dict
        feature_dict = {
            "amount": amount,
            "is_known_payee": is_known_payee,
            "has_active_call": has_active_call,
            "has_secrecy": has_secrecy,
            "has_threat": has_threat,
            "urgency_level": urgency_level,
            "emotional_pressure": emotional_pressure,
            "keyword_count": keyword_count,
            "hesitation_seconds": hesitation,
            "category_code": category_code,
        }

        # 1. ML Coercion Model Inference
        ml_coercion_proba = ml_model.predict_coercion_proba(feature_dict)
        ml_score = ml_coercion_proba * 100.0

        # 2. Deterministic Rule Score & Explainability Attribution
        rule_score = 0.0
        explainable_factors = []

        # Hard Coercion Trigger Flags
        is_hard_coercion = False

        # Truecaller-Style Community Fraud Registry Factor
        if telemetry.get("community_scam_flagged"):
            rep_count = int(telemetry.get("community_report_count", 1))
            pts = min(40.0, 28.0 + (rep_count // 12))
            rule_score += pts
            explainable_factors.append({
                "factor": f"Truecaller Community Fraud Registry ({rep_count} reports)",
                "impact": f"+{pts:.0f} pts",
                "severity": "CRITICAL",
                "desc": f"Identifier is blacklisted in SQLite Community Database with {rep_count} reports ({telemetry.get('community_category', 'Fraud')})."
            })
            if rep_count >= 50:
                is_hard_coercion = True

        if has_active_call:
            rule_score += 32.0
            explainable_factors.append({
                "factor": "Active Call in Progress",
                "impact": "+32 pts",
                "severity": "HIGH",
                "desc": "Fraudsters maintain continuous live calls during digital arrest."
            })

        if has_secrecy:
            rule_score += 26.0
            explainable_factors.append({
                "factor": "Secrecy / Isolation Mandate",
                "impact": "+26 pts",
                "severity": "HIGH",
                "desc": "Victim was instructed not to inform family or bank officials."
            })

        if has_threat:
            rule_score += 35.0
            explainable_factors.append({
                "factor": "Police / Legal Threat Claim",
                "impact": "+35 pts",
                "severity": "CRITICAL",
                "desc": "Payment coerced under threat of arrest, FIR, or account freeze."
            })

        relation = telemetry.get("q_beneficiary_relation", "")
        if "Police" in relation or "CBI" in relation or "Govt" in relation:
            rule_score += 30.0
            explainable_factors.append({
                "factor": "Impersonation of Authority",
                "impact": "+30 pts",
                "severity": "CRITICAL",
                "desc": "Beneficiary claims to be law enforcement or regulatory officer."
            })

        if keyword_count > 0:
            impact_val = min(20.0, keyword_count * 10.0)
            rule_score += impact_val
            explainable_factors.append({
                "factor": f"High-Risk Coercion Terms ({', '.join(flagged_kw)})",
                "impact": f"+{impact_val:.0f} pts",
                "severity": "HIGH",
                "desc": "Payment narrative contains verified fraud/extortion vocabulary."
            })

        # Baseline Deviations
        if amount_ratio >= 15.0:
            rule_score += 22.0
            explainable_factors.append({
                "factor": f"Extreme Amount Spike ({amount_ratio:.1f}x baseline)",
                "impact": "+22 pts",
                "severity": "MEDIUM",
                "desc": f"Transfer is massively higher than 60-day historical mean (₹{mean_amount:.0f})."
            })
        elif amount_ratio >= 4.0:
            rule_score += 10.0
            explainable_factors.append({
                "factor": f"Elevated Amount ({amount_ratio:.1f}x baseline)",
                "impact": "+10 pts",
                "severity": "LOW",
                "desc": "Transfer exceeds standard spending threshold."
            })

        if is_known_payee == 1:
            rule_score -= 18.0
            explainable_factors.append({
                "factor": "Verified Whitelisted Payee",
                "impact": "-18 pts",
                "severity": "SAFE",
                "desc": "Recipient has extensive verified prior transaction history."
            })
        else:
            rule_score += 15.0
            explainable_factors.append({
                "factor": "Unseen / New Beneficiary",
                "impact": "+15 pts",
                "severity": "MEDIUM",
                "desc": "First time transacting with this VPA."
            })

        # Check for hard coercion combo
        if (has_active_call and has_secrecy) or (has_threat and has_active_call) or ("Police" in relation):
            is_hard_coercion = True

        # 3. Hybrid Blend: 50% Rule-Based Duress + 35% ML Supervised Model + 15% Anomaly
        raw_composite = (0.50 * rule_score) + (0.35 * ml_score) + (0.15 * min(100.0, amount_ratio * 4.0))

        # Enforce floors/ceilings
        raw_composite = min(100.0, max(0.0, raw_composite))
        if is_hard_coercion:
            final_score = max(94.0, raw_composite)
        else:
            final_score = raw_composite

        final_score = round(final_score, 1)

        # 4. Tier Determination
        if final_score < 35.0:
            risk_tier = "LOW"
            recommended_action = "PROCEED_SEAMLESS"
            tier_label = "🟢 Zero Friction Gateway"
            tier_color = "#10b981"
        elif final_score < 70.0:
            risk_tier = "MEDIUM"
            recommended_action = "DYNAMIC_CHALLENGE"
            tier_label = "🟡 Step-Up Dynamic Friction"
            tier_color = "#f59e0b"
        else:
            risk_tier = "CRITICAL"
            recommended_action = "COOLING_PAUSE_AND_ESCORT"
            tier_label = "🔴 15-Minute Duress Cooling Pause"
            tier_color = "#ef4444"

        return {
            "composite_score": final_score,
            "ml_coercion_proba": round(ml_coercion_proba, 3),
            "ml_model_score": round(ml_score, 1),
            "deterministic_rule_score": round(rule_score, 1),
            "risk_tier": risk_tier,
            "tier_label": tier_label,
            "tier_color": tier_color,
            "recommended_action": recommended_action,
            "is_hard_coercion": is_hard_coercion,
            "explainable_factors": explainable_factors,
            "feature_snapshot": feature_dict,
        }
