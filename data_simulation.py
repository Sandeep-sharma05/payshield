"""
PayShield AI - Pre-Payment Safeguard System
Team: Syntax Sorcerers
Module: data_simulation.py

Handles user historical baseline profiling, synthetic ledger generation,
ML training dataset synthesis (normal vs coerced transactions),
threat vocabulary extraction, and curated hackathon demo presets.
"""

import time
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# ==============================================================================
# 1. USER PROFILE & HISTORICAL BASELINE
# ==============================================================================

class UserProfile:
    """Simulates a realistic digital banking consumer with 60-day transaction history."""
    def __init__(self, user_id="USR-88219", name="Rahul Sharma", upi_id="rahul@okhdfcbank"):
        self.user_id = user_id
        self.name = name
        self.upi_id = upi_id
        self.account_created_days = 428
        self.emergency_contact = {
            "name": "Priya Sharma (Sister)",
            "phone": "+91 98765 43210",
            "relationship": "Immediate Family",
            "notify_enabled": True
        }

        # Whitelisted / verified recurring payees
        self.whitelisted_payees = {
            "freshmart@okhdfcbank": {"name": "Fresh Mart Daily", "category": "Groceries", "tx_count": 46},
            "landlord.ramesh@okaxis": {"name": "Ramesh Kumar (Landlord)", "category": "Rent", "tx_count": 14},
            "bescom.utility@karnataka": {"name": "BESCOM Electricity Board", "category": "Utilities", "tx_count": 12},
            "airtel.broadband@paytm": {"name": "Airtel Fiber Broadband", "category": "Utilities", "tx_count": 14},
            "priya.sharma@oksbi": {"name": "Priya Sharma (Sister)", "category": "Family", "tx_count": 28},
            "swiggy.food@icici": {"name": "Swiggy Food Delivery", "category": "Dining", "tx_count": 68},
            "metro.smartcard@dmrc": {"name": "Namma Metro Transit", "category": "Transit", "tx_count": 34},
            "rohit.gupta@okaxis": {"name": "Rohit Gupta (Colleague)", "category": "Friend", "tx_count": 19},
        }

        self.history_df = self._generate_synthetic_history(n_records=95)
        self.baseline_stats = self._calculate_baseline_stats()

    def _generate_synthetic_history(self, n_records=95) -> pd.DataFrame:
        np.random.seed(42)
        random.seed(42)

        records = []
        now = datetime.now()
        payee_keys = list(self.whitelisted_payees.keys())

        for i in range(n_records):
            is_rent = (i % 30 == 0)
            if is_rent:
                amount = round(float(np.random.normal(18000, 400)), 2)
                payee_upi = "landlord.ramesh@okaxis"
                category = "Rent"
            else:
                amount = round(float(np.random.lognormal(mean=5.8, sigma=0.72)), 2)
                amount = max(40.0, min(amount, 3800.0))
                payee_upi = random.choice(payee_keys)
                category = self.whitelisted_payees[payee_upi]["category"]

            payee_name = self.whitelisted_payees[payee_upi]["name"]
            days_ago = random.randint(1, 60)
            hour = int(np.random.choice(range(7, 23)))
            minute = random.randint(0, 59)
            tx_time = now - timedelta(days=days_ago, hours=now.hour - hour, minutes=now.minute - minute)

            records.append({
                "tx_id": f"TXN-{100000 + i}",
                "timestamp": tx_time,
                "hour": hour,
                "amount": amount,
                "recipient_name": payee_name,
                "recipient_upi": payee_upi,
                "category": category,
                "status": "COMPLETED",
                "risk_tier": "LOW",
            })

        df = pd.DataFrame(records).sort_values(by="timestamp", ascending=False).reset_index(drop=True)
        return df

    def _calculate_baseline_stats(self) -> dict:
        routine_amounts = self.history_df[self.history_df["category"] != "Rent"]["amount"]
        return {
            "mean_amount": float(routine_amounts.mean()),
            "median_amount": float(routine_amounts.median()),
            "std_amount": float(routine_amounts.std()),
            "p95_amount": float(routine_amounts.quantile(0.95)),
            "max_routine_amount": float(routine_amounts.max()),
            "total_transactions": len(self.history_df),
            "whitelisted_count": len(self.whitelisted_payees),
        }

    def evaluate_payee(self, recipient_upi: str) -> dict:
        clean_upi = recipient_upi.strip().lower()
        if clean_upi in self.whitelisted_payees:
            item = self.whitelisted_payees[clean_upi]
            return {
                "is_known": True,
                "status_label": "Verified Payee",
                "category": item["category"],
                "historical_tx_count": item["tx_count"],
                "risk_offset": -15.0,
            }
        return {
            "is_known": False,
            "status_label": "Unseen / New Payee",
            "category": "Unknown",
            "historical_tx_count": 0,
            "risk_offset": 25.0,
        }


# ==============================================================================
# 2. NLP SUSPICIOUS VOCABULARY SCANNER
# ==============================================================================

THREAT_KEYWORDS = [
    "cbi", "police", "arrest", "fir", "customs", "narcotics", "court",
    "bail", "seizure", "clearing fee", "crypto", "unlock profit",
    "telegram task", "penalty", "parcel fee", "fedex parcel", "cybercrime",
    "interrogation", "digital arrest", "asset verification", "fine deposit"
]

def scan_text_for_threat_keywords(text: str) -> list:
    """Returns all coercion/extortion keywords found in notes or payee names."""
    if not text:
        return []
    clean = text.lower()
    return [w for w in THREAT_KEYWORDS if w in clean]


# ==============================================================================
# 3. SYNTHETIC ML TRAINING DATASET GENERATOR
# ==============================================================================

def generate_ml_training_dataset(n_samples=1800) -> pd.DataFrame:
    """
    Generates a realistic synthetic training corpus of digital transactions:
    - Normal transactions (75%): low amounts, known payees, no calls, no duress
    - Coerced / Scam transactions (25%): high amounts, active call, secrecy, duress, threats
    """
    np.random.seed(1337)
    random.seed(1337)

    records = []
    for _ in range(n_samples):
        is_coerced = np.random.random() < 0.25

        if not is_coerced:
            # Normal distribution
            amount = float(np.random.lognormal(mean=5.9, sigma=0.8))
            amount = max(20.0, min(amount, 8500.0))
            is_known_payee = 1 if np.random.random() < 0.85 else 0
            has_active_call = 1 if np.random.random() < 0.03 else 0
            has_secrecy = 1 if np.random.random() < 0.02 else 0
            has_threat = 1 if np.random.random() < 0.01 else 0
            urgency_level = int(np.random.choice([0, 1, 2], p=[0.85, 0.12, 0.03]))
            emotional_pressure = int(np.random.choice([1, 2, 3], p=[0.80, 0.16, 0.04]))
            keyword_count = 0 if np.random.random() < 0.98 else 1
            hesitation_seconds = float(np.random.normal(8.0, 3.0))
            hesitation_seconds = max(1.5, hesitation_seconds)
            category_code = int(np.random.choice([0, 1, 2])) # Groceries, Rent, Family
            label = 0 # Safe
        else:
            # Coerced / Scam distribution
            amount = float(np.random.normal(65000, 22000))
            amount = max(4500.0, min(amount, 250000.0))
            is_known_payee = 1 if np.random.random() < 0.06 else 0
            has_active_call = 1 if np.random.random() < 0.88 else 0
            has_secrecy = 1 if np.random.random() < 0.82 else 0
            has_threat = 1 if np.random.random() < 0.74 else 0
            urgency_level = int(np.random.choice([1, 2], p=[0.25, 0.75]))
            emotional_pressure = int(np.random.choice([3, 4, 5], p=[0.15, 0.40, 0.45]))
            keyword_count = int(np.random.choice([1, 2, 3], p=[0.35, 0.45, 0.20]))
            hesitation_seconds = float(np.random.normal(24.0, 10.0))
            hesitation_seconds = max(3.0, hesitation_seconds)
            category_code = int(np.random.choice([3, 4])) # Investment task, Legal Fine
            label = 1 # Coerced / Scam

        records.append({
            "amount": amount,
            "is_known_payee": is_known_payee,
            "has_active_call": has_active_call,
            "has_secrecy": has_secrecy,
            "has_threat": has_threat,
            "urgency_level": urgency_level,
            "emotional_pressure": emotional_pressure,
            "keyword_count": keyword_count,
            "hesitation_seconds": hesitation_seconds,
            "category_code": category_code,
            "label": label,
        })

    return pd.DataFrame(records)


# ==============================================================================
# 4. CURATED HACKATHON DEMO SCENARIOS
# ==============================================================================

SCENARIOS = {
    "SCENARIO_1": {
        "title": "🟢 Routine Grocery Checkout",
        "badge": "LOW RISK (SAFE)",
        "subtitle": "Standard ₹450 daily purchase to verified vendor. No friction triggered.",
        "payload": {
            "recipient_name": "Fresh Mart Daily",
            "recipient_upi": "freshmart@okhdfcbank",
            "amount": 450.0,
            "payment_note": "Weekly vegetables & bread",
            "q_active_call": "No, making payment independently",
            "q_secrecy_instructed": "No secrecy requested",
            "q_threat_or_fine": "No threat involved",
            "q_time_urgency": "Standard / No rush",
            "q_beneficiary_relation": "Known vendor / Regular merchant",
            "q_payment_category": "Groceries / Retail Shopping",
            "q_emotional_pressure": 1,
        }
    },
    "SCENARIO_2": {
        "title": "🔴 'Digital Arrest' Fake Police Coercion",
        "badge": "CRITICAL RISK (DURESS LOCK)",
        "subtitle": "Extortion call claiming arrest warrant for customs contraband. Total secrecy demanded.",
        "payload": {
            "recipient_name": "CBI Clearance Escrow Desk",
            "recipient_upi": "cbi.investigation.desk99@fakebank",
            "amount": 85000.0,
            "payment_note": "Bail clearance fine FIR-2024-91",
            "q_active_call": "Yes, currently on active voice/video call",
            "q_secrecy_instructed": "Yes, strictly told not to discuss with anyone",
            "q_threat_or_fine": "Yes, threatened with immediate arrest or account seizure",
            "q_time_urgency": "Extreme (< 15 mins or immediate arrest)",
            "q_beneficiary_relation": "Claiming to be Police / CBI / Court / Govt Authority",
            "q_payment_category": "Legal Fine / Penalty / Bail / Asset Verification",
            "q_emotional_pressure": 5,
        }
    },
    "SCENARIO_3": {
        "title": "🟠 Telegram VIP Task Investment Fraud",
        "badge": "HIGH RISK (PAUSE & CHALLENGE)",
        "subtitle": "Unregistered crypto wallet claiming 300% profit unlock upon ₹35,000 transfer.",
        "payload": {
            "recipient_name": "Apex Crypto Treasury Node",
            "recipient_upi": "apex.liquidity.pool77@okaxis",
            "amount": 35000.0,
            "payment_note": "VIP Level 3 profit unlock fee",
            "q_active_call": "No, making payment independently",
            "q_secrecy_instructed": "Yes, strictly told not to discuss with anyone",
            "q_threat_or_fine": "No threat involved",
            "q_time_urgency": "Moderate urgency (within a few hours)",
            "q_beneficiary_relation": "Met recently online (job offer, investment, Telegram group)",
            "q_payment_category": "Investment / Crypto / High-Return Task",
            "q_emotional_pressure": 3,
        }
    },
    "SCENARIO_4": {
        "title": "🟡 Family Medical Urgent Transfer",
        "badge": "MEDIUM RISK (GENUINE EMERGENCY)",
        "subtitle": "High value ₹15,000 transfer to verified sister for emergency hospital admission.",
        "payload": {
            "recipient_name": "Priya Sharma (Sister)",
            "recipient_upi": "priya.sharma@oksbi",
            "amount": 15000.0,
            "payment_note": "Emergency hospital admission advance",
            "q_active_call": "No, making payment independently",
            "q_secrecy_instructed": "No secrecy requested",
            "q_threat_or_fine": "No threat involved",
            "q_time_urgency": "Extreme (< 15 mins or immediate arrest)",
            "q_beneficiary_relation": "Family member or close personal friend",
            "q_payment_category": "Family & Emergency Assistance",
            "q_emotional_pressure": 4,
        }
    }
}
