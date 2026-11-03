"""
PayShield AI - Pre-Payment Safeguard System
Team: Syntax Sorcerers
Module: interventions.py

Phase 4: Dynamic Interventions & Adaptive Friction Protocols (Light Theme / White Background)
Implements:
1. Zero-Friction Instant Execution (Low Risk)
2. Step-Up Mindful Friction & OTP Challenge (Medium Risk)
3. Dynamic Ticking Timer Engine (15:00 -> 14:59 -> 14:58) with Pulse Animations
4. Anti-Coercion Reality Check & Emergency SOS Escalation
"""

import time
import random
import streamlit as st
import streamlit.components.v1 as components

# ==============================================================================
# 1. TIER 1: ZERO FRICTION SUCCESS GATEWAY
# ==============================================================================

def render_tier_1_success(telemetry: dict, risk_result: dict):
    """Seamless zero-friction execution for safe, routine transactions."""
    st.markdown(
        """
        <div style="background: #f0fdf4; border: 1.5px solid #86efac; border-radius: 16px; padding: 22px; text-align: center; margin-bottom: 20px; box-shadow: 0 4px 16px rgba(16, 185, 129, 0.08);">
            <div style="font-size: 48px; margin-bottom: 6px;">✅</div>
            <h2 style="color: #15803d; margin: 0; font-size: 24px; font-weight: 800;">Payment Successful</h2>
            <p style="color: #4b5563; font-size: 14px; margin-top: 4px;">Zero friction applied — verified against baseline behavioral profile.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    utr_number = f"UTR-{random.randint(20261000, 20269999)}-{random.randint(100000, 999999)}"
    st.markdown(
        f"""
        <div class="tx-card">
            <span style="color: #64748b; font-size: 12px; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px;">Transaction Receipt</span>
            <div class="amount-display">₹{telemetry.get('amount', 0):,.2f}</div>
            <div style="font-size: 14px; color: #1e293b; line-height: 1.8;">
                <b>Beneficiary:</b> {telemetry.get('recipient_name')} (<code style="background:#f1f5f9; color:#0f172a; padding:2px 6px; border-radius:4px; font-weight:600;">{telemetry.get('recipient_upi')}</code>)<br>
                <b>NPCI Reference (UTR):</b> <code style="background:#f1f5f9; color:#0f172a; padding:2px 6px; border-radius:4px; font-weight:600;">{utr_number}</code><br>
                <b>Timestamp:</b> {time.strftime('%d-%b-%Y %I:%M:%S %p')}<br>
                <b>PayShield Score:</b> <span style="color: #16a34a; font-weight: 800;">{risk_result.get('composite_score')}/100 (Safe)</span><br>
                <b>Security Status:</b> Verified Zero Duress & 0 Community Scam Flags
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📄 Download PDF Receipt", use_container_width=True):
            st.toast("Receipt saved to local downloads.", icon="💾")
    with col2:
        if st.button("🔄 Make Another Transfer", type="primary", use_container_width=True):
            st.session_state.current_screen = "PAYMENT_INITIATION"
            st.rerun()


# ==============================================================================
# 2. TIER 2: STEP-UP DYNAMIC FRICTION & MINDFUL COOLDOWN
# ==============================================================================

def render_tier_2_step_up(telemetry: dict, risk_result: dict):
    """Step-up friction for medium risk (elevated amount or unfamiliar contact)."""
    st.markdown(
        """
        <div style="background: #fffbeb; border: 1.5px solid #fcd34d; border-radius: 16px; padding: 20px; margin-bottom: 20px; box-shadow: 0 4px 16px rgba(245, 158, 11, 0.08);">
            <div style="display: flex; align-items: center; gap: 14px;">
                <span style="font-size: 36px;">⚠️</span>
                <div>
                    <h3 style="color: #92400e; margin: 0; font-size: 19px; font-weight: 800;">Step-Up Security Verification Required</h3>
                    <p style="color: #78350f; font-size: 14px; margin: 2px 0 0 0;">Anomalous transfer pattern detected. Dynamic safety friction engaged.</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="tx-card">
            <span style="color: #64748b; font-size: 12px; text-transform: uppercase; font-weight: 700;">Pending Transfer</span>
            <div class="amount-display">₹{telemetry.get('amount', 0):,.2f}</div>
            <div style="font-size: 14px; color: #1e293b; line-height: 1.6;">
                <b>Beneficiary:</b> {telemetry.get('recipient_name')} (<code style="background:#f1f5f9; color:#0f172a; padding:2px 6px; border-radius:4px; font-weight:600;">{telemetry.get('recipient_upi')}</code>)<br>
                <b>Risk Score:</b> <span style="color: #d97706; font-weight: 800;">{risk_result.get('composite_score')}/100 (Medium Risk)</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("🛡️ Mindful Verification Checks")
    st.caption("Please confirm these safety checkpoints before entering your UPI PIN:")

    chk1 = st.checkbox(
        "I have independently spoken with this recipient or personally verified their identity.",
        value=st.session_state.get("chk_verified_identity", False),
        key="chk_verified_identity"
    )
    chk2 = st.checkbox(
        "I am not paying to unlock investment returns, trading tasks, or online lottery prizes.",
        value=st.session_state.get("chk_no_task_fraud", False),
        key="chk_no_task_fraud"
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.write("📱 **Step-Up SMS OTP Authentication**")
    st.caption("A 4-digit safety code has been sent to your registered mobile (+91 98765 •••••).")
    
    otp_input = st.text_input("Enter 4-Digit Security Code (Demo PIN: 4096)", max_chars=4, placeholder="4096")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚫 Abort & Return to Safety", use_container_width=True):
            st.session_state.current_screen = "PAYMENT_INITIATION"
            st.rerun()
    with col2:
        confirm_btn = st.button("Authorize & Release Payment ➔", type="primary", use_container_width=True)

    if confirm_btn:
        if not chk1 or not chk2:
            st.error("⚠️ You must review and acknowledge both safety confirmations.")
        elif otp_input.strip() != "4096":
            st.error("⚠️ Invalid OTP code. For this simulation, use demo code: 4096")
        else:
            st.success("✅ Verification successful! Releasing transfer...")
            st.session_state.risk_level = "RESOLVED_SAFE"
            render_tier_1_success(telemetry, risk_result)


# ==============================================================================
# 3. DYNAMIC TICKING TIMER ENGINE COMPONENT (WHITE THEME COMPLIANT)
# ==============================================================================

def render_dynamic_countdown_timer(start_seconds=900):
    """
    Renders an authentic, client-side, dynamic second-by-second countdown clock
    with pulsating radar animations, live progress bar, and fast-forward testing (Light Theme).
    """
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            * {{
                box-sizing: border-box;
                margin: 0;
                padding: 0;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace;
            }}
            body {{
                background: transparent;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
            }}
            .timer-container {{
                width: 100%;
                background: radial-gradient(circle at center, #ffffff 0%, #fff5f5 100%);
                border: 2px solid #ef4444;
                border-radius: 20px;
                padding: 24px 20px;
                text-align: center;
                position: relative;
                box-shadow: 0 8px 30px rgba(239, 68, 68, 0.14);
                overflow: hidden;
            }}
            .pulse-ring {{
                display: inline-block;
                width: 14px;
                height: 14px;
                background-color: #ef4444;
                border-radius: 50%;
                margin-right: 8px;
                box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7);
                animation: pulseAnimation 1.6s infinite cubic-bezier(0.66, 0, 0, 1);
                vertical-align: middle;
            }}
            @keyframes pulseAnimation {{
                0% {{
                    transform: scale(0.95);
                    box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7);
                }}
                70% {{
                    transform: scale(1.1);
                    box-shadow: 0 0 0 16px rgba(239, 68, 68, 0);
                }}
                100% {{
                    transform: scale(0.95);
                    box-shadow: 0 0 0 0 rgba(239, 68, 68, 0);
                }}
            }}
            .timer-badge {{
                display: inline-flex;
                align-items: center;
                font-size: 12px;
                font-weight: 800;
                letter-spacing: 1px;
                color: #b91c1c;
                text-transform: uppercase;
                background: #fee2e2;
                border: 1px solid #fca5a5;
                padding: 5px 14px;
                border-radius: 100px;
                margin-bottom: 12px;
            }}
            .clock-display {{
                font-size: 56px;
                font-weight: 900;
                color: #dc2626;
                letter-spacing: 2px;
                margin: 4px 0 10px 0;
                text-shadow: 0 0 14px rgba(239, 68, 68, 0.2);
                font-variant-numeric: tabular-nums;
            }}
            .progress-bar-bg {{
                width: 85%;
                height: 9px;
                background: #e2e8f0;
                border-radius: 6px;
                margin: 0 auto 14px auto;
                overflow: hidden;
            }}
            .progress-bar-fill {{
                height: 100%;
                width: 100%;
                background: linear-gradient(90deg, #ef4444, #f59e0b);
                border-radius: 6px;
                transition: width 1s linear;
            }}
            .timer-subtext {{
                color: #475569;
                font-size: 13.5px;
                font-weight: 500;
                max-width: 460px;
                margin: 0 auto;
                line-height: 1.5;
            }}
            .controls-row {{
                margin-top: 14px;
                display: flex;
                gap: 10px;
                justify-content: center;
            }}
            .demo-btn {{
                background: #ffffff;
                border: 1.5px solid #cbd5e1;
                color: #1e293b;
                font-size: 12px;
                font-weight: 700;
                padding: 7px 14px;
                border-radius: 8px;
                cursor: pointer;
                transition: all 0.2s ease;
                box-shadow: 0 2px 6px rgba(0,0,0,0.04);
            }}
            .demo-btn:hover {{
                background: #f0f9ff;
                color: #0284c7;
                border-color: #0284c7;
            }}
        </style>
    </head>
    <body>
        <div class="timer-container">
            <div class="timer-badge">
                <span class="pulse-ring"></span>
                Active Cooling Pause • Anti-Coercion Protocol
            </div>
            <div class="clock-display" id="timeRemaining">15:00</div>
            <div class="progress-bar-bg">
                <div class="progress-bar-fill" id="progressFill"></div>
            </div>
            <p class="timer-subtext">
                Psychological manipulation relies on constant panic. Breaking the time window allows independent second-opinion verification.
            </p>
            <div class="controls-row">
                <button class="demo-btn" onclick="fastForward()">⚡ Judge Fast-Forward Demo (-14 Mins)</button>
                <button class="demo-btn" onclick="resetTimer()">🔄 Reset Clock (15:00)</button>
            </div>
        </div>

        <script>
            let totalSeconds = {start_seconds};
            let remainingSeconds = totalSeconds;
            const displayEl = document.getElementById('timeRemaining');
            const progressEl = document.getElementById('progressFill');

            function updateClock() {{
                if (remainingSeconds < 0) remainingSeconds = 0;
                const minutes = Math.floor(remainingSeconds / 60);
                const seconds = remainingSeconds % 60;
                const minStr = String(minutes).padStart(2, '0');
                const secStr = String(seconds).padStart(2, '0');
                displayEl.textContent = `${{minStr}}:${{secStr}}`;

                const pct = (remainingSeconds / totalSeconds) * 100;
                progressEl.style.width = pct + '%';

                if (remainingSeconds === 0) {{
                    displayEl.style.color = '#16a34a';
                    displayEl.textContent = "00:00 - UNLOCKED";
                    displayEl.style.textShadow = "0 0 14px rgba(22, 163, 74, 0.3)";
                }}
            }}

            setInterval(() => {{
                if (remainingSeconds > 0) {{
                    remainingSeconds--;
                    updateClock();
                }}
            }}, 1000);

            function fastForward() {{
                remainingSeconds = 15;
                updateClock();
            }}

            function resetTimer() {{
                remainingSeconds = totalSeconds;
                updateClock();
            }}

            updateClock();
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=245)


# ==============================================================================
# 4. TIER 3: CRITICAL DURESS LOCK INTERVENTION
# ==============================================================================

def render_tier_3_duress_pause(telemetry: dict, risk_result: dict, user_profile):
    """
    Mandatory dynamic cooling pause and anti-coercion reality escort for
    severe risk scenarios (Digital Arrest, extortions, forced transfers).
    """
    st.markdown(
        """
        <div style="background: #fef2f2; border: 2px solid #ef4444; border-radius: 18px; padding: 22px; margin-bottom: 20px; box-shadow: 0 4px 20px rgba(239, 68, 68, 0.12);">
            <div style="display: flex; align-items: center; gap: 14px;">
                <span style="font-size: 42px;">🚨</span>
                <div>
                    <h3 style="color: #b91c1c; margin: 0; font-size: 21px; font-weight: 800;">PAYMENT FROZEN: 15-MINUTE COOLING PAUSE</h3>
                    <p style="color: #991b1b; font-size: 14px; margin: 4px 0 0 0; font-weight: 500;">
                        Severe duress / coercion indicators intercepted. PayShield AI has temporarily locked this transaction.
                    </p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 1. Dynamic Ticking Timer Component
    render_dynamic_countdown_timer(start_seconds=900)

    # 2. Anti-Coercion Cognitive Reality-Check
    st.subheader("⚖️ Anti-Coercion Legal Reality Check")
    st.info(
        "**Official Advisory from Ministry of Home Affairs & Cyber Crime Portal (1930):**\n\n"
        "• Indian Law Enforcement (Police, CBI, ED, Courts) **NEVER** issues arrest warrants or conducts judicial proceedings over Skype/WhatsApp video calls.\n"
        "• Govt agencies **NEVER** demand money transfers to UPI accounts or personal bank accounts for 'bail deposits' or 'asset clearing'."
    )

    st.write("##### Mandatory Cognitive Question:")
    reality_answer = st.radio(
        "Does any Indian law enforcement officer or court collect penalties or bail via UPI?",
        options=[
            "Please select an option...",
            "Yes, in urgent cybercrime investigations",
            "NO, NEVER. Demands for UPI payments to avoid arrest are ALWAYS criminal fraud."
        ],
        index=0
    )

    st.write("---")

    # 3. Trusted Emergency Contact Alert Dispatch
    emergency = user_profile.emergency_contact
    st.subheader("🚨 Trusted Contact Escalation Alert")
    st.caption(f"Configured Emergency Contact: **{emergency['name']}** ({emergency['phone']})")

    st.markdown(
        f"""
        <div class="telemetry-card" style="border-left: 4px solid #f59e0b; margin-bottom: 15px; background: #fffbeb; border: 1.5px solid #fde68a;">
            <b style="color: #92400e;">Automated Emergency SMS Dispatch:</b><br>
            <i style="color: #78350f; font-size: 14px;">"🚨 [PayShield Alert] Your family member Rahul Sharma is attempting an unusual ₹{telemetry.get('amount', 0):,.2f} transfer while under suspected phone duress. Please call him immediately on normal phone line to verify his safety."</i>
        </div>
        """,
        unsafe_allow_html=True,
    )

    sos_col1, sos_col2 = st.columns(2)
    with sos_col1:
        if st.button("📤 Send Emergency SMS to Sister Now", use_container_width=True, type="secondary"):
            st.success(f"✅ Alert dispatched to {emergency['name']} at {emergency['phone']}!")
    with sos_col2:
        if st.button("📞 Dial 1930 (National Cyber Crime Helpline)", use_container_width=True):
            st.info("Simulating direct call connection to National Cyber Crime Reporting Helpline (1930)...")

    st.write("---")

    # 4. Action Pathways
    c_abort, c_override = st.columns([2, 1])
    with c_abort:
        if st.button("🛡️ Cancel Payment & Block Beneficiary (Recommended)", type="primary", use_container_width=True):
            st.balloons()
            st.success("✅ **Payment Safely Cancelled.** Your account balance is safe. Fraudulent VPA has been flagged to the security ledger.")
            st.session_state.current_screen = "PAYMENT_INITIATION"
            time.sleep(2)
            st.rerun()

    with c_override:
        override_clicked = st.button("⚠️ Request Bypass (Cooldown Locked)", use_container_width=True)
        if override_clicked:
            if "NEVER" not in reality_answer:
                st.error("❌ Bypass blocked: You must correctly answer the Anti-Coercion Legal Reality Check.")
            else:
                st.warning("⚠️ Cooldown lock active: Manual unfreeze requires 15-minute wait or two-party authorization from your emergency contact.")
