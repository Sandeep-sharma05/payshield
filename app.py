"""
PayShield AI - Pre-Payment Safeguard System
Team: Syntax Sorcerers
Production Release: Pure White Fintech Theme (Light Mode)
Full 5-Phase Architecture + 3 Core Specifications:
1. Truecaller-Style Pre-Payment Scam Alert (Real-time SQLite lookup)
2. Community Reporting Module (SQLite scam_reports registry & live blacklist)
3. Dynamic Ticking Timer Engine (15:00 -> 14:59 -> 14:58 with pulsating radar)
"""

import time
import streamlit as st
import pandas as pd
from data_simulation import (
    UserProfile,
    SCENARIOS,
    scan_text_for_threat_keywords
)
from risk_engine import HybridRiskEngine, MLFraudModel
from database import (
    lookup_scam_database,
    submit_scam_report,
    get_all_scam_reports
)
from interventions import (
    render_tier_1_success,
    render_tier_2_step_up,
    render_tier_3_duress_pause
)

# ==============================================================================
# PAGE CONFIGURATION & LIGHT FINTECH THEME STYLING
# ==============================================================================

st.set_page_config(
    page_title="PayShield AI - Pre-Payment Safeguard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    /* Global Background & Light Fintech Theme */
    .stApp {
        background-color: #ffffff !important;
        color: #0f172a !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }

    body, p, span, div {
        color: #1e293b;
    }

    /* ALL STREAMLIT WIDGET LABELS (High-Contrast Bold Slate) */
    label[data-testid="stWidgetLabel"],
    div[data-testid="stWidgetLabel"],
    div[data-testid="stWidgetLabel"] p,
    div[data-testid="stWidgetLabel"] label,
    div[data-testid="stWidgetLabel"] span,
    .stWidgetLabel p,
    .stWidgetLabel span,
    label p {
        color: #0f172a !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        letter-spacing: 0.1px !important;
        line-height: 1.4 !important;
    }

    /* RADIO BUTTON LABELS & OPTIONS */
    div[data-testid="stRadio"] label,
    div[data-testid="stRadio"] label p,
    div[data-testid="stRadio"] label span,
    div[data-testid="stRadio"] div[role="radiogroup"] label {
        color: #1e293b !important;
        font-size: 15px !important;
        font-weight: 500 !important;
        transition: color 0.15s ease-in-out;
    }

    div[data-testid="stRadio"] label:hover p,
    div[data-testid="stRadio"] label:hover span {
        color: #0284c7 !important;
    }

    /* CHECKBOX OPTIONS */
    div[data-testid="stCheckbox"] label,
    div[data-testid="stCheckbox"] label p,
    div[data-testid="stCheckbox"] label span {
        color: #1e293b !important;
        font-size: 15px !important;
        font-weight: 500 !important;
    }

    /* SELECTBOX & DROPDOWNS */
    div[data-baseweb="select"] {
        background-color: #ffffff !important;
        border: 1.5px solid #cbd5e1 !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="select"] div,
    div[data-baseweb="select"] span {
        color: #0f172a !important;
        font-weight: 500 !important;
    }
    ul[data-baseweb="menu"] {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        box-shadow: 0 4px 16px rgba(0,0,0,0.08) !important;
    }
    li[data-baseweb="menu-item"] {
        color: #1e293b !important;
        background-color: #ffffff !important;
    }
    li[data-baseweb="menu-item"]:hover {
        background-color: #f0f9ff !important;
        color: #0284c7 !important;
    }

    /* TEXT INPUTS & NUMBER INPUTS */
    div[data-baseweb="input"] {
        background-color: #ffffff !important;
        border: 1.5px solid #cbd5e1 !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="input"] input {
        color: #0f172a !important;
        background-color: transparent !important;
        font-size: 15px !important;
        font-weight: 500 !important;
    }
    div[data-baseweb="input"] input::placeholder {
        color: #94a3b8 !important;
    }

    /* CAPTIONS & SUBTITLES */
    div[data-testid="stCaptionContainer"],
    div[data-testid="stCaptionContainer"] p,
    .stCaption,
    small {
        color: #64748b !important;
        font-size: 13.5px !important;
    }

    /* SLIDERS */
    div[data-testid="stSlider"] div,
    div[data-testid="stSlider"] label,
    div[data-testid="stSlider"] label p,
    div[data-testid="stSlider"] span {
        color: #0f172a !important;
    }

    /* HEADINGS */
    h1, h2, h3, h4, h5, h6 {
        color: #0f172a !important;
        font-weight: 800 !important;
    }

    .stMarkdown, .stMarkdown p {
        color: #334155 !important;
    }

    /* SIDEBAR STYLING */
    section[data-testid="stSidebar"] {
        background-color: #f8fafc !important;
        border-right: 1px solid #e2e8f0 !important;
    }
    section[data-testid="stSidebar"] * {
        color: #0f172a !important;
    }
    section[data-testid="stSidebar"] .stCaption {
        color: #64748b !important;
    }

    /* FORM CARD */
    div[data-testid="stForm"] {
        background: #ffffff;
        border: 1.5px solid #e2e8f0;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
    }

    /* TRUECALLER ALERT CARD WITH PULSE ANIMATION (LIGHT THEME) */
    .truecaller-alert-box {
        background: #fef2f2;
        border: 2px solid #ef4444;
        border-radius: 14px;
        padding: 16px 18px;
        margin: 12px 0 16px 0;
        box-shadow: 0 4px 20px rgba(239, 68, 68, 0.12);
        animation: truecallerPulse 2.2s infinite ease-in-out;
    }

    @keyframes truecallerPulse {
        0%, 100% {
            border-color: #ef4444;
            box-shadow: 0 4px 16px rgba(239, 68, 68, 0.12);
        }
        50% {
            border-color: #f87171;
            box-shadow: 0 4px 25px rgba(239, 68, 68, 0.25);
        }
    }

    .truecaller-tag {
        display: inline-flex;
        align-items: center;
        background: #ef4444;
        color: #ffffff;
        font-weight: 800;
        font-size: 11px;
        letter-spacing: 0.8px;
        text-transform: uppercase;
        padding: 4px 10px;
        border-radius: 6px;
    }
    
    /* Headers & Badges */
    .team-badge {
        display: inline-block;
        padding: 4px 12px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.2px;
        color: #0284c7;
        background: #e0f2fe;
        border: 1px solid #bae6fd;
        border-radius: 100px;
        text-transform: uppercase;
        margin-bottom: 6px;
    }
    
    .brand-title {
        font-size: 27px;
        font-weight: 800;
        color: #0f172a;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .brand-sub {
        font-size: 14px;
        color: #64748b;
        margin-bottom: 16px;
    }
    
    .tx-card {
        background: #ffffff;
        border: 1.5px solid #e2e8f0;
        border-radius: 14px;
        padding: 18px;
        margin-bottom: 18px;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
    }
    
    .amount-display {
        font-size: 34px;
        font-weight: 800;
        color: #0284c7;
        margin: 2px 0 10px 0;
    }
    
    .pill-known {
        background: #ecfdf5;
        color: #047857;
        border: 1px solid #a7f3d0;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 11.5px;
        font-weight: 600;
        display: inline-block;
    }
    
    .pill-unknown {
        background: #fffbeb;
        color: #b45309;
        border: 1px solid #fde68a;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 11.5px;
        font-weight: 600;
        display: inline-block;
    }

    .pill-danger {
        background: #fef2f2;
        color: #b91c1c;
        border: 1px solid #fecaca;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 11.5px;
        font-weight: 600;
        display: inline-block;
    }
    
    .step-pill {
        font-size: 12.5px;
        padding: 8px 14px;
        border-radius: 10px;
        font-weight: 600;
        text-align: center;
        display: block;
    }
    
    .step-active {
        background: #0284c7;
        color: #ffffff;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.25);
    }
    
    .step-inactive {
        background: #f1f5f9;
        color: #64748b;
        border: 1px solid #e2e8f0;
    }
    
    .telemetry-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 14px;
        font-family: monospace;
        font-size: 12.5px;
        color: #334155;
    }

    .xai-factor-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 12px 16px;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==============================================================================
# SESSION STATE INITIALIZATION
# ==============================================================================

def init_session_state():
    if "user_profile" not in st.session_state:
        st.session_state.user_profile = UserProfile()

    if "current_screen" not in st.session_state:
        st.session_state.current_screen = "PAYMENT_INITIATION"

    # Transaction fields
    if "amount" not in st.session_state:
        st.session_state.amount = 450.0
    if "recipient_upi" not in st.session_state:
        st.session_state.recipient_upi = "freshmart@okhdfcbank"
    if "recipient_name" not in st.session_state:
        st.session_state.recipient_name = "Fresh Mart Daily"
    if "payment_note" not in st.session_state:
        st.session_state.payment_note = "Weekly groceries"

    # Context Intake Question Responses
    if "q_active_call" not in st.session_state:
        st.session_state.q_active_call = "No, making payment independently"
    if "q_secrecy_instructed" not in st.session_state:
        st.session_state.q_secrecy_instructed = "No secrecy requested"
    if "q_threat_or_fine" not in st.session_state:
        st.session_state.q_threat_or_fine = "No threat involved"
    if "q_time_urgency" not in st.session_state:
        st.session_state.q_time_urgency = "Standard / No rush"
    if "q_beneficiary_relation" not in st.session_state:
        st.session_state.q_beneficiary_relation = "Known vendor / Regular merchant"
    if "q_payment_category" not in st.session_state:
        st.session_state.q_payment_category = "Groceries / Retail Shopping"
    if "q_emotional_pressure" not in st.session_state:
        st.session_state.q_emotional_pressure = 1

    # Telemetry and engine output
    if "intake_start_time" not in st.session_state:
        st.session_state.intake_start_time = time.time()
    if "elapsed_intake_seconds" not in st.session_state:
        st.session_state.elapsed_intake_seconds = 0.0
    if "context_telemetry" not in st.session_state:
        st.session_state.context_telemetry = {}
    if "risk_result" not in st.session_state:
        st.session_state.risk_result = {}

    # Audit Trail / Incident Log
    if "audit_log" not in st.session_state:
        st.session_state.audit_log = []


def load_preset_scenario(scenario_key: str):
    sc = SCENARIOS[scenario_key]["payload"]
    st.session_state.recipient_name = sc["recipient_name"]
    st.session_state.recipient_upi = sc["recipient_upi"]
    st.session_state.amount = float(sc["amount"])
    st.session_state.payment_note = sc["payment_note"]

    st.session_state.q_active_call = sc["q_active_call"]
    st.session_state.q_secrecy_instructed = sc["q_secrecy_instructed"]
    st.session_state.q_threat_or_fine = sc["q_threat_or_fine"]
    st.session_state.q_time_urgency = sc["q_time_urgency"]
    st.session_state.q_beneficiary_relation = sc["q_beneficiary_relation"]
    st.session_state.q_payment_category = sc["q_payment_category"]
    st.session_state.q_emotional_pressure = sc["q_emotional_pressure"]


def nav_to(screen_name: str):
    if screen_name == "SECURITY_CHECK":
        st.session_state.intake_start_time = time.time()
    st.session_state.current_screen = screen_name
    st.rerun()


# ==============================================================================
# SIDEBAR: JUDGE DEMO CONTROLS & BASELINE TELEMETRY
# ==============================================================================

def render_sidebar():
    profile: UserProfile = st.session_state.user_profile
    stats = profile.baseline_stats

    with st.sidebar:
        st.markdown('<div class="team-badge">SYNTAX SORCERERS</div>', unsafe_allow_html=True)
        st.title("🛡️ PayShield AI")
        st.caption("Pre-Payment Safeguard against Coerced & Anomalous Digital Transfers")
        st.write("---")

        # Hackathon Judge Scenario Selector
        st.subheader("⚡ Judge Evaluation Scenarios")
        st.caption("Select a scenario to auto-populate telemetry & test adaptive friction:")
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🟢 Routine Tx", use_container_width=True, help="₹450 Grocery payment (Zero risk)"):
                load_preset_scenario("SCENARIO_1")
                st.session_state.current_screen = "PAYMENT_INITIATION"
                st.rerun()
            if st.button("🟠 Task Scam", use_container_width=True, help="₹35,000 Telegram VIP task scam"):
                load_preset_scenario("SCENARIO_3")
                st.session_state.current_screen = "PAYMENT_INITIATION"
                st.rerun()
        with c2:
            if st.button("🔴 Digital Arrest", use_container_width=True, help="₹85,000 Fake CBI Coercion call"):
                load_preset_scenario("SCENARIO_2")
                st.session_state.current_screen = "PAYMENT_INITIATION"
                st.rerun()
            if st.button("🟡 Family Hosp", use_container_width=True, help="₹15,000 Hospital bill to sister"):
                load_preset_scenario("SCENARIO_4")
                st.session_state.current_screen = "PAYMENT_INITIATION"
                st.rerun()

        st.write("---")

        # Baseline Profile Stats
        st.subheader("👤 User Baseline Ledger")
        st.markdown(f"**Account Holder:** {profile.name} (`{profile.upi_id}`)")
        m1, m2 = st.columns(2)
        m1.metric("Daily Avg Tx", f"₹{stats['mean_amount']:.0f}")
        m2.metric("95th %ile Tx", f"₹{stats['p95_amount']:.0f}")

        with st.expander("📊 View Historical 90-Tx Ledger"):
            st.dataframe(
                profile.history_df[["timestamp", "amount", "recipient_name", "category"]].head(15),
                use_container_width=True,
                height=200,
            )

        with st.expander("🤖 ML Model Feature Weights"):
            ml_model = MLFraudModel.get_instance()
            weights = ml_model.get_feature_importances()
            st.json(weights)

        # Audit Log
        if st.session_state.audit_log:
            with st.expander("📜 Live Security Incident Ledger"):
                st.dataframe(pd.DataFrame(st.session_state.audit_log), use_container_width=True)


# ==============================================================================
# HEADER PROGRESS INDICATOR
# ==============================================================================

def render_header():
    screen = st.session_state.current_screen
    c1, c2, c3 = st.columns(3)
    with c1:
        cls = "step-active" if screen == "PAYMENT_INITIATION" else "step-inactive"
        st.markdown(f'<div class="step-pill {cls}">1. Payment Setup & Scam Alert</div>', unsafe_allow_html=True)
    with c2:
        cls = "step-active" if screen == "SECURITY_CHECK" else "step-inactive"
        st.markdown(f'<div class="step-pill {cls}">2. Context Safeguard Check</div>', unsafe_allow_html=True)
    with c3:
        cls = "step-active" if screen == "FINAL_OUTCOME" else "step-inactive"
        st.markdown(f'<div class="step-pill {cls}">3. Adaptive Outcome & 15-Min Timer</div>', unsafe_allow_html=True)
    st.write("")


# ==============================================================================
# SCREEN 1: PAYMENT INITIATION WITH TRUECALLER-STYLE SCAM ALERT
# ==============================================================================

def render_payment_initiation():
    st.markdown('<div class="brand-title">💳 UPI Payment Terminal</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-sub">Simulate an outgoing payment transfer. PayShield AI protects in real-time.</div>', unsafe_allow_html=True)

    col_main, _ = st.columns([2, 1])
    with col_main:
        with st.form("payment_form", clear_on_submit=False):
            recipient_name = st.text_input(
                "Beneficiary / Payee Name",
                value=st.session_state.recipient_name,
                placeholder="e.g. Ramesh Supermarket or Official CBI Desk",
            )

            recipient_upi = st.text_input(
                "Payee UPI ID (VPA) or Phone Number",
                value=st.session_state.recipient_upi,
                placeholder="e.g. user@okhdfcbank or 9876543210@paytm",
            )

            # -------------------------------------------------------------
            # FEATURE 1: TRUECALLER-STYLE PRE-PAYMENT SCAM ALERT (LIGHT THEME)
            # -------------------------------------------------------------
            scam_info = lookup_scam_database(recipient_upi)
            profile: UserProfile = st.session_state.user_profile
            payee_eval = profile.evaluate_payee(recipient_upi)
            stats = profile.baseline_stats

            if scam_info["is_flagged"]:
                st.markdown(
                    f"""
                    <div class="truecaller-alert-box">
                        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
                            <span class="truecaller-tag">🚨 TRUECALLER-STYLE FRAUD ALERT</span>
                            <span style="color: #b91c1c; font-size: 12.5px; font-weight: 800;">⚠️ {scam_info['report_count']} CITIZEN REPORTS</span>
                        </div>
                        <div style="font-size: 16.5px; font-weight: 800; color: #991b1b; margin-bottom: 4px;">
                            Critical Scam Entity ({scam_info['scam_confidence']}% Confidence)
                        </div>
                        <div style="font-size: 13.5px; color: #7f1d1d; line-height: 1.5; margin-bottom: 6px;">
                            <b>Category:</b> {scam_info['category']}<br>
                            <b>Reported MO:</b> {scam_info['sample_note']}
                        </div>
                        <div style="font-size: 12px; color: #475569; border-top: 1px solid rgba(239, 68, 68, 0.25); padding-top: 6px;">
                            Source: <b>National Cyber Crime Portal & SQLite Community Blacklist</b>. If ordered to transfer money to avoid arrest, disconnect immediately!
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            elif payee_eval["is_known"]:
                st.markdown(
                    f'<span class="pill-known">✅ Verified Known Merchant/Contact • 0 Community Complaints ({payee_eval["historical_tx_count"]} past transfers)</span>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    '<span class="pill-unknown">⚠️ New Beneficiary • 0 Community Fraud Reports in Vault (First-time transfer)</span>',
                    unsafe_allow_html=True
                )

            amount = st.number_input(
                "Transfer Amount (₹)",
                min_value=1.0,
                max_value=1000000.0,
                value=float(st.session_state.amount),
                step=100.0,
                format="%.2f",
            )

            note = st.text_input(
                "Payment Purpose / Note (Optional)",
                value=st.session_state.payment_note,
                placeholder="e.g. Groceries, Rent, Bail fine deposit, Task unlock",
            )

            if amount > (stats["mean_amount"] * 5):
                st.markdown(f'<div style="margin-top: 6px;"><span class="pill-danger">⚠️ Amount is {amount/stats["mean_amount"]:.1f}x higher than daily average (₹{stats["mean_amount"]:.0f})</span></div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button(
                f"Proceed to Pay ₹{amount:,.2f} ➔",
                use_container_width=True,
                type="primary"
            )

            if submitted:
                if not recipient_upi or ("@" not in recipient_upi and len(recipient_upi) < 10):
                    st.error("⚠️ Please enter a valid UPI ID (e.g. name@bank) or Phone Number.")
                elif amount <= 0:
                    st.error("⚠️ Transfer amount must be greater than zero.")
                else:
                    st.session_state.amount = amount
                    st.session_state.recipient_upi = recipient_upi.strip()
                    st.session_state.recipient_name = recipient_name.strip() if recipient_name else recipient_upi
                    st.session_state.payment_note = note.strip()
                    nav_to("SECURITY_CHECK")


# ==============================================================================
# SCREEN 2: CONTEXT INTAKE & MICRO-QUESTIONNAIRE
# ==============================================================================

def render_security_check():
    st.markdown('<div class="brand-title">🛡️ PayShield Context Intake</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-sub">Our safety protocol intercepts high-impact digital transfers to prevent coerced payments.</div>', unsafe_allow_html=True)

    profile: UserProfile = st.session_state.user_profile
    payee_eval = profile.evaluate_payee(st.session_state.recipient_upi)
    stats = profile.baseline_stats
    amount_ratio = st.session_state.amount / max(1.0, stats["mean_amount"])

    scam_info = lookup_scam_database(st.session_state.recipient_upi)
    flagged_keywords = scan_text_for_threat_keywords(
        f"{st.session_state.payment_note} {st.session_state.recipient_name}"
    )

    c_card1, c_card2 = st.columns([3, 2])
    with c_card1:
        st.markdown(
            f"""
            <div class="tx-card">
                <span style="color: #64748b; font-size: 12px; text-transform: uppercase; font-weight: 700;">Pending Transfer:</span>
                <div class="amount-display">₹{st.session_state.amount:,.2f}</div>
                <div style="font-size: 14px; color: #1e293b; line-height: 1.6;">
                    <b>Beneficiary:</b> {st.session_state.recipient_name} (<code style="background:#f1f5f9; color:#0f172a; padding:2px 6px; border-radius:4px; font-weight:600;">{st.session_state.recipient_upi}</code>)<br>
                    <b>Payment Note:</b> {st.session_state.payment_note if st.session_state.payment_note else '<i>None provided</i>'}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c_card2:
        st.markdown(
            f"""
            <div class="tx-card" style="border-left: 4px solid {'#ef4444' if scam_info['is_flagged'] or amount_ratio > 10 else '#10b981'};">
                <span style="color: #64748b; font-size: 12px; font-weight: 700; text-transform: uppercase;">TELEMETRY ANOMALIES:</span>
                <div style="font-size: 13.5px; margin-top: 6px; color: #1e293b; line-height: 1.6;">
                    • <b>Amount vs Baseline:</b> {amount_ratio:.1f}x of daily avg (₹{stats['mean_amount']:.0f})<br>
                    • <b>Truecaller Database:</b> {'<span style=\"color:#dc2626; font-weight:700;\">🚨 FLAGGED (' + str(scam_info['report_count']) + ' reports)</span>' if scam_info['is_flagged'] else '<span style=\"color:#16a34a; font-weight:700;\">Clean (0 Reports)</span>'}<br>
                    • <b>Threat Flags:</b> {f'<span style=\"color:#dc2626; font-weight:700;\">{flagged_keywords}</span>' if flagged_keywords else '<span style=\"color:#16a34a;\">None</span>'}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("---")
    st.subheader("📋 Pre-Payment Context Questionnaire")
    st.caption("Please respond candidly to ensure your account security.")

    with st.form("context_intake_form"):
        q_active_call = st.radio(
            "1. 📞 Are you currently on an active voice/video call or screen-share while making this payment?",
            options=[
                "No, making payment independently",
                "Yes, currently on active voice/video call",
                "Yes, sharing my screen or following audio instructions"
            ],
            index=0 if "No" in st.session_state.q_active_call else 1,
            help="Common hallmark of 'Digital Arrest' scams where fraudsters keep victims on continuous calls."
        )

        q_secrecy = st.radio(
            "2. 🤫 Were you instructed NOT to discuss or disclose this transfer to family, friends, or bank staff?",
            options=[
                "No secrecy requested",
                "Yes, strictly told not to discuss with anyone",
                "Yes, warned that confidentiality is required by law"
            ],
            index=0 if "No" in st.session_state.q_secrecy_instructed else 1,
            help="Coercive actors isolate victims to prevent second-opinion interventions."
        )

        q_threat = st.radio(
            "3. ⚖️ Is this payment being made to resolve an alleged parcel seizure, police investigation, FIR, or arrest warrant?",
            options=[
                "No threat involved",
                "Yes, threatened with immediate arrest or account seizure",
                "Yes, informed of an illegal package / tax audit penalty"
            ],
            index=0 if "No" in st.session_state.q_threat_or_fine else 1,
            help="Law enforcement agencies in India never demand money via UPI to settle cases."
        )

        q_urgency = st.selectbox(
            "4. ⏱️ How urgent is this payment demand?",
            options=[
                "Standard / No rush",
                "Moderate urgency (within a few hours)",
                "Extreme (< 15 mins or immediate arrest)"
            ],
            index=2 if "Extreme" in st.session_state.q_time_urgency else (1 if "Moderate" in st.session_state.q_time_urgency else 0)
        )

        q_relation = st.selectbox(
            "5. 🤝 How do you know this beneficiary?",
            options=[
                "Known vendor / Regular merchant",
                "Family member or close personal friend",
                "Met recently online (job offer, investment, Telegram group)",
                "Claiming to be Police / CBI / Court / Govt Authority",
                "Unknown third party"
            ],
            index=3 if "CBI" in st.session_state.q_beneficiary_relation else (2 if "online" in st.session_state.q_beneficiary_relation else (1 if "Family" in st.session_state.q_beneficiary_relation else 0))
        )

        q_category = st.selectbox(
            "6. 🏷️ What is the primary purpose of this transfer?",
            options=[
                "Groceries / Retail Shopping",
                "Rent / Recurring Utilities",
                "Family & Emergency Assistance",
                "Investment / Crypto / High-Return Task",
                "Legal Fine / Penalty / Bail / Asset Verification"
            ],
            index=4 if "Legal" in st.session_state.q_payment_category else (3 if "Investment" in st.session_state.q_payment_category else (2 if "Family" in st.session_state.q_payment_category else 0))
        )

        q_pressure = st.slider(
            "7. 💔 Are you feeling anxious, pressured, or threatened while executing this payment?",
            min_value=1,
            max_value=5,
            value=int(st.session_state.q_emotional_pressure),
            help="1 = Completely relaxed | 5 = Extremely panicked / Coerced"
        )

        st.markdown("<br>", unsafe_allow_html=True)
        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            back_clicked = st.form_submit_button("⬅️ Modify Payment Details", use_container_width=True)
        with col_btn2:
            submit_context = st.form_submit_button("Evaluate Risk & Run Safeguard ➔", type="primary", use_container_width=True)

        if back_clicked:
            nav_to("PAYMENT_INITIATION")

        if submit_context:
            elapsed = time.time() - st.session_state.intake_start_time
            st.session_state.elapsed_intake_seconds = round(elapsed, 2)

            st.session_state.q_active_call = q_active_call
            st.session_state.q_secrecy_instructed = q_secrecy
            st.session_state.q_threat_or_fine = q_threat
            st.session_state.q_time_urgency = q_urgency
            st.session_state.q_beneficiary_relation = q_relation
            st.session_state.q_payment_category = q_category
            st.session_state.q_emotional_pressure = q_pressure

            st.session_state.context_telemetry = {
                "amount": float(st.session_state.amount),
                "recipient_name": st.session_state.recipient_name,
                "recipient_upi": st.session_state.recipient_upi,
                "payment_note": st.session_state.payment_note,
                "is_known_payee": bool(payee_eval["is_known"]),
                "amount_ratio_to_mean": float(amount_ratio),
                "flagged_keywords": flagged_keywords,
                "community_scam_flagged": scam_info["is_flagged"],
                "community_report_count": scam_info.get("report_count", 0),
                "community_category": scam_info.get("category", ""),
                "q_active_call": q_active_call,
                "q_secrecy_instructed": q_secrecy,
                "q_threat_or_fine": q_threat,
                "q_time_urgency": q_urgency,
                "q_beneficiary_relation": q_relation,
                "q_payment_category": q_category,
                "q_emotional_pressure": int(q_pressure),
                "elapsed_intake_seconds": float(elapsed),
                "timestamp": time.time(),
            }

            eval_res = HybridRiskEngine.evaluate_transaction(
                st.session_state.context_telemetry,
                profile.baseline_stats
            )
            st.session_state.risk_result = eval_res

            st.session_state.audit_log.insert(0, {
                "Timestamp": time.strftime("%H:%M:%S"),
                "Amount": f"₹{st.session_state.amount:,.2f}",
                "Payee": st.session_state.recipient_name,
                "Score": f"{eval_res['composite_score']}/100",
                "Tier": eval_res["risk_tier"],
                "Action": eval_res["recommended_action"],
            })

            nav_to("FINAL_OUTCOME")


# ==============================================================================
# SCREEN 3: ADAPTIVE GATEWAY & DYNAMIC TICKING TIMER
# ==============================================================================

def render_final_outcome():
    telemetry = st.session_state.context_telemetry
    risk_result = st.session_state.risk_result

    if not telemetry or not risk_result:
        st.warning("No transaction telemetry evaluated. Please initiate a payment first.")
        if st.button("Start Payment ➔"):
            nav_to("PAYMENT_INITIATION")
        return

    score = risk_result.get("composite_score", 0.0)
    tier = risk_result.get("risk_tier", "LOW")
    tier_label = risk_result.get("tier_label", "Safe")
    tier_color = risk_result.get("tier_color", "#10b981")

    # 1. RISK SCORE METRICS DASHBOARD
    st.markdown('<div class="brand-title">🛡️ PayShield Risk Assessment</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="brand-sub">Real-Time Hybrid Engine Result: <b style="color: {tier_color};">{tier_label}</b></div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Composite Risk Score", f"{score:.1f} / 100")
    c2.metric("ML Coercion Model", f"{risk_result.get('ml_coercion_proba', 0)*100:.1f}%")
    c3.metric("Rule Duress Pts", f"{risk_result.get('deterministic_rule_score', 0):.0f} pts")
    c4.metric("Spending Anomaly", f"{telemetry.get('amount_ratio_to_mean', 1.0):.1f}x avg")

    st.write("---")

    # 2. EXPLAINABLE AI (XAI) ATTRIBUTION BREAKDOWN
    with st.expander("🔍 Explainable Risk Attribution (Why this decision was made)", expanded=(tier != "LOW")):
        st.caption("PayShield AI combines deterministic duress indicators with behavioral anomaly detection:")
        for factor in risk_result.get("explainable_factors", []):
            impact = factor["impact"]
            color = "#dc2626" if "+" in impact else "#16a34a"
            st.markdown(
                f"""
                <div class="xai-factor-card">
                    <div>
                        <span style="font-weight: 700; color: #0f172a; font-size: 14px;">{factor['factor']}</span><br>
                        <span style="color: #475569; font-size: 13px;">{factor['desc']}</span>
                    </div>
                    <div>
                        <span style="color: {color}; font-weight: 800; font-size: 14px; background: #f1f5f9; padding: 4px 10px; border-radius: 6px;">
                            {impact}
                        </span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.write("")

    # 3. DYNAMIC INTERVENTION (ZERO FRICTION / STEP UP / 15-MIN TICKING TIMER)
    if tier == "LOW":
        render_tier_1_success(telemetry, risk_result)
    elif tier == "MEDIUM":
        render_tier_2_step_up(telemetry, risk_result)
    else:
        render_tier_3_duress_pause(telemetry, risk_result, st.session_state.user_profile)

    st.write("---")
    if st.button("🔄 Test Another Transaction Scenario", use_container_width=True):
        nav_to("PAYMENT_INITIATION")


# ==============================================================================
# FEATURE 2: COMMUNITY REPORTING MODULE & BLACKLIST DESK
# ==============================================================================

def render_community_reporting_hub():
    """Citizen fraud reporting module and live SQLite scam registry."""
    st.markdown('<div class="brand-title">📢 Community Scam Registry & Reporter</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-sub">Crowdsourced Cyber Intelligence powered by SQLite — protecting digital citizens from coercive extortion rings.</div>', unsafe_allow_html=True)

    col_form, col_table = st.columns([1, 1], gap="large")

    with col_form:
        st.subheader("📝 Report a Fraudulent UPI ID or Phone")
        st.caption("Citizen reports directly update the local SQLite database and power real-time Truecaller-style alerts.")

        with st.form("community_report_form", clear_on_submit=True):
            target_id = st.text_input("Flagged UPI ID or Phone Number", placeholder="e.g. fake.cbi@bank or +91 98200 11930")
            id_type = st.selectbox("Identifier Type", ["UPI_VPA", "PHONE"])
            cat = st.selectbox(
                "Scam Type / Modus Operandi",
                [
                    "Digital Arrest / Fake Police Extortion",
                    "Telegram VIP Task / Crypto Investment Fraud",
                    "Customs / Courier Narcotics Parcel Scam",
                    "Electricity / Utility Disconnection Threat",
                    "Fake Job Offer / Work-From-Home Scam",
                    "Lottery Prize / Unsolicited Loan Fee",
                    "Other Coercive Fraud"
                ]
            )
            desc = st.text_area("Incident Details & Demands Made", placeholder="Describe how the caller coerced you, threats made, or fake warrants shown...")
            reporter = st.text_input("Your Name / Handle (Optional)", placeholder="Anonymous Citizen")

            submitted_report = st.form_submit_button("Submit Scam Report to Database ➔", type="primary", use_container_width=True)

            if submitted_report:
                if not target_id:
                    st.error("⚠️ Please specify the flagged UPI ID or Phone Number.")
                elif not desc:
                    st.error("⚠️ Please provide a brief description of the incident.")
                else:
                    res = submit_scam_report(target_id, id_type, cat, desc, reporter or "Anonymous Citizen")
                    if res["success"]:
                        st.balloons()
                        st.success(f"✅ {res['message']}")
                        st.rerun()
                    else:
                        st.error(f"❌ Error: {res.get('message', 'Failed to save')}")

    with col_table:
        st.subheader("🛡️ Live Community Blacklist Ledger")
        st.caption("Real-time table queried directly from SQLite `scam_reports` table:")

        search_query = st.text_input("🔍 Live Database Search", placeholder="Filter by VPA, phone, or scam type...")
        df_scams = get_all_scam_reports(limit=50)

        if search_query:
            clean_q = search_query.lower()
            df_scams = df_scams[
                df_scams["Flagged Identifier"].str.lower().str.contains(clean_q) |
                df_scams["Scam Category"].str.lower().str.contains(clean_q)
            ]

        st.dataframe(df_scams, use_container_width=True, height=430)


# ==============================================================================
# MAIN ROUTER WITH INTEGRATED TAB NAVIGATION
# ==============================================================================

def main():
    init_session_state()
    render_sidebar()

    tab_terminal, tab_community, tab_audit = st.tabs([
        "🛡️ PayShield Payment Safeguard",
        "📢 Community Scam Registry & Reporter (SQLite)",
        "🔬 Threat Intelligence & Audit Vault"
    ])

    with tab_terminal:
        render_header()
        if st.session_state.current_screen == "PAYMENT_INITIATION":
            render_payment_initiation()
        elif st.session_state.current_screen == "SECURITY_CHECK":
            render_security_check()
        elif st.session_state.current_screen == "FINAL_OUTCOME":
            render_final_outcome()
        else:
            st.session_state.current_screen = "PAYMENT_INITIATION"
            st.rerun()

    with tab_community:
        render_community_reporting_hub()

    with tab_audit:
        st.subheader("🔬 Enterprise Telemetry & Incident Audit Vault")
        st.caption("Complete operational intelligence for fraud monitoring and compliance officers.")
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.write("##### 🤖 Machine Learning Model Feature Importances")
            ml_model = MLFraudModel.get_instance()
            weights = ml_model.get_feature_importances()
            st.json(weights)
        with col_m2:
            st.write("##### 👤 User 60-Day Spending Profile Baseline")
            profile: UserProfile = st.session_state.user_profile
            st.json(profile.baseline_stats)

        st.write("---")
        st.write("##### 📜 Live Incident Audit Ledger")
        if st.session_state.audit_log:
            st.dataframe(pd.DataFrame(st.session_state.audit_log), use_container_width=True)
        else:
            st.info("No transaction events recorded yet in this session.")


if __name__ == "__main__":
    main()
