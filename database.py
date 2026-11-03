"""
PayShield AI - Pre-Payment Safeguard System
Team: Syntax Sorcerers
Module: database.py

Implements:
1. SQLite Scam Reports Database (Community Fraud Registry)
2. Truecaller-Style Pre-Payment Scam Lookup Engine
3. In-App Community Reporting System & Audit Ledger
"""

import sqlite3
import os
from datetime import datetime
import pandas as pd

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "payshield_vault.db")

def get_db_connection():
    """Returns a connection to the SQLite database with row factory enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initializes SQLite tables and seeds known community fraud registries."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Community Scam Reports Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scam_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            identifier TEXT UNIQUE NOT NULL,
            identifier_type TEXT NOT NULL,
            category TEXT NOT NULL,
            threat_level TEXT NOT NULL,
            report_count INTEGER DEFAULT 1,
            sample_note TEXT,
            source TEXT DEFAULT 'COMMUNITY',
            first_reported TEXT,
            last_reported TEXT
        )
    """)

    # 2. Transaction Audit Ledger Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transaction_audit (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            user_id TEXT NOT NULL,
            amount REAL NOT NULL,
            recipient_upi TEXT NOT NULL,
            recipient_name TEXT,
            risk_score REAL NOT NULL,
            risk_tier TEXT NOT NULL,
            action_taken TEXT NOT NULL,
            telemetry_snapshot TEXT
        )
    """)

    conn.commit()

    # Seed known high-profile scam cases if empty
    cursor.execute("SELECT COUNT(*) FROM scam_reports")
    count = cursor.fetchone()[0]

    if count == 0:
        seed_data = [
            (
                "cbi.investigation.desk99@fakebank",
                "UPI_VPA",
                "Digital Arrest / Fake CBI Impersonation",
                "CRITICAL",
                342,
                "Victims coerced on Skype calls alleging narcotics parcel seizures under threat of arrest.",
                "NATIONAL_CYBER_CRIME_PORTAL",
                "2026-09-12 10:15:00",
                "2026-11-03 18:30:00"
            ),
            (
                "apex.liquidity.pool77@okaxis",
                "UPI_VPA",
                "Telegram VIP Task / Crypto Investment Fraud",
                "HIGH",
                187,
                "Promised 300% profit returns upon completing prepaid deposit tasks in private Telegram channels.",
                "COMMUNITY",
                "2026-10-01 14:22:00",
                "2026-11-02 21:45:00"
            ),
            (
                "+91 98200 11930",
                "PHONE",
                "Fake Mumbai Cyber Cell Police Officer",
                "CRITICAL",
                256,
                "Caller poses as DCP Crime Branch demanding immediate bail transfer to avoid detention.",
                "COMMUNITY",
                "2026-08-20 09:00:00",
                "2026-11-03 14:10:00"
            ),
            (
                "customs.clearance.delhi@icici",
                "UPI_VPA",
                "FedEx / Customs Illegal Contraband Extortion",
                "CRITICAL",
                98,
                "SMS/IVR claiming a FedEx parcel containing passports and illegal drugs is held at airport.",
                "COMMUNITY",
                "2026-10-15 16:40:00",
                "2026-11-01 11:20:00"
            ),
            (
                "+91 88765 22341",
                "PHONE",
                "Electricity Bill Power Cut Threat Scam",
                "SUSPICIOUS",
                64,
                "Fake power department message claiming electricity will be disconnected tonight unless paid.",
                "COMMUNITY",
                "2026-10-25 19:12:00",
                "2026-11-02 17:05:00"
            ),
            (
                "vip.payout.node8@paytm",
                "UPI_VPA",
                "Work-From-Home Rating Task Fraud",
                "HIGH",
                142,
                "Victim given small initial ₹500 payout, then coerced into depositing ₹50,000 to unlock capital.",
                "COMMUNITY",
                "2026-09-30 11:11:00",
                "2026-11-03 12:00:00"
            )
        ]

        cursor.executemany("""
            INSERT INTO scam_reports (
                identifier, identifier_type, category, threat_level, report_count,
                sample_note, source, first_reported, last_reported
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, seed_data)
        conn.commit()

    conn.close()

# ==============================================================================
# TRUECALLER-STYLE REAL-TIME LOOKUP
# ==============================================================================

def lookup_scam_database(identifier: str) -> dict:
    """
    Real-time database lookup across UPI IDs and phone numbers.
    Returns community report details if flagged, or safe clean status.
    """
    if not identifier:
        return {"is_flagged": False, "report_count": 0}

    clean_id = identifier.strip().lower()
    conn = get_db_connection()
    cursor = conn.cursor()

    # Exact match on UPI VPA or phone
    cursor.execute("""
        SELECT * FROM scam_reports 
        WHERE LOWER(identifier) = ? OR LOWER(identifier) LIKE ?
    """, (clean_id, f"%{clean_id}%"))
    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "is_flagged": True,
            "identifier": row["identifier"],
            "identifier_type": row["identifier_type"],
            "category": row["category"],
            "threat_level": row["threat_level"],
            "report_count": row["report_count"],
            "sample_note": row["sample_note"],
            "source": row["source"],
            "last_reported": row["last_reported"],
            "scam_confidence": min(99, 70 + (row["report_count"] // 5))
        }

    return {"is_flagged": False, "report_count": 0}

# ==============================================================================
# COMMUNITY REPORTING MODULE
# ==============================================================================

def submit_scam_report(identifier: str, id_type: str, category: str, description: str, reporter_name="Anonymous Citizen") -> dict:
    """
    Submits a new citizen fraud report to the SQLite database.
    Increments report_count if already exists, or inserts new registry entry.
    """
    if not identifier:
        return {"success": False, "message": "Identifier cannot be empty."}

    clean_id = identifier.strip().lower()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM scam_reports WHERE LOWER(identifier) = ?", (clean_id,))
    existing = cursor.fetchone()

    if existing:
        new_count = existing["report_count"] + 1
        new_level = "CRITICAL" if new_count >= 100 else ("HIGH" if new_count >= 20 else "SUSPICIOUS")
        cursor.execute("""
            UPDATE scam_reports 
            SET report_count = ?, threat_level = ?, last_reported = ?, sample_note = ?
            WHERE id = ?
        """, (new_count, new_level, now_str, description, existing["id"]))
        conn.commit()
        conn.close()
        return {
            "success": True,
            "status": "INCREMENTED",
            "identifier": clean_id,
            "new_count": new_count,
            "threat_level": new_level,
            "message": f"Report added! This identifier now has {new_count} community fraud reports."
        }
    else:
        cursor.execute("""
            INSERT INTO scam_reports (
                identifier, identifier_type, category, threat_level, report_count,
                sample_note, source, first_reported, last_reported
            ) VALUES (?, ?, ?, ?, 1, ?, 'COMMUNITY', ?, ?)
        """, (clean_id, id_type, category, "SUSPICIOUS", description, now_str, now_str))
        conn.commit()
        conn.close()
        return {
            "success": True,
            "status": "CREATED",
            "identifier": clean_id,
            "new_count": 1,
            "threat_level": "SUSPICIOUS",
            "message": "New scam registry created! Thank you for protecting the digital payment community."
        }

def get_all_scam_reports(limit=50) -> pd.DataFrame:
    """Returns top reported scam entities as a Pandas DataFrame for the Community Hub."""
    conn = get_db_connection()
    query = """
        SELECT identifier as "Flagged Identifier",
               identifier_type as "Type",
               category as "Scam Category",
               threat_level as "Threat Severity",
               report_count as "Community Flags",
               last_reported as "Last Active"
        FROM scam_reports 
        ORDER BY report_count DESC LIMIT ?
    """
    df = pd.read_sql_query(query, conn, params=(limit,))
    conn.close()
    return df

# Initialize database on module import
init_database()
