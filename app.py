import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime

DB_FILE = "brg_erp_db.json"
UPLOAD_DIR = "uploaded_permits"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# MSB İHRACAT İZNİ GERÇEK VERİLERİ
INITIAL_DATA = {
    "customers": [
        {
            "id": "CUST-IRAQ-01",
            "name": "IRAK İÇİŞLERİ BAKANLIĞI",
            "country": "Iraq / Irak",
            "contact_person": "T.C. MSB KOORDİNASYON",
            "phone": "-",
            "email": "info@moi.gov.iq",
            "address": "BAGHDAD / IRAQ",
            "import_permits": [],
            "export_permits": [
                {
                    "permit_no": "E-38100341-302.04-6134334",
                    "issue_date": "13.05.2026",
                    "valid_until": "30.12.2028",
                    "items": [
                        {"code": "BRG9-ELITE", "name": "BRG9 Elite 9x19mm", "total_qty": 3300, "used_qty": 0},
                        {"code": "BRG9-ELITE-G2", "name": "BRG9 Elite Gen 2 9x19mm", "total_qty": 5000, "used_qty": 0},
                        {"code": "BRG9-TACTICAL", "name": "BRG9 Tactical 9x19mm", "total_qty": 2750, "used_qty": 0},
                        {"code": "BRG9-FD", "name": "BRG9 FD 9x19mm", "total_qty": 5000, "used_qty": 0},
                        {"code": "BRG9-FDX", "name": "BRG9 FDX 9x19mm", "total_qty": 5000, "used_qty": 0},
                        {"code": "BRG55", "name": "BRG55 5.56x45mm Rifle", "total_qty": 5000, "used_qty": 0},
                        {"code": "BRG55-CH", "name": "Charging Handle for BRG55", "total_qty": 500, "used_qty": 0},
                        {"code": "BRG55-HG", "name": "Hand Guard for BRG55", "total_qty": 500, "used_qty": 0},
                        {"code": "BRG55-LPK", "name": "Lower Part Kit for BRG55", "total_qty": 500, "used_qty": 0},
                        {"code": "BRG55-BK", "name": "Buffer Kit for BRG55", "total_qty": 500, "used_qty": 0}
                    ]
                }
            ]
        }
    ]
}

def load_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(INITIAL_DATA, f, ensure_ascii=False, indent=2)
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

st.set_page_config(page_title="BRG DEFENCE — ERP Portal", page_icon="🛡️", layout="wide")
db = load_db()

# KOMPAKT CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #f8fafc; }
    
    .top-header {
        background: linear-gradient(90deg, #0f172a 0%, #1e293b 100%);
        color: white;
        padding: 10px 18px;
        border-radius: 8px;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .top-title { font-size: 18px; font-weight: 700; }
    .card-box {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
    }
    .status-ok {
        background-color: #dcfce7;
        color: #15803d;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 12px;
        display: inline-block;
        margin-top: 8px;
    }
    .status-err {
        background-color: #fee2e2;
        color: #b91c1c;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 12px;
        display: inline-block;
        margin-top: 8px;
    }
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("""
<div class="top-header">
    <div><span style="font-size: 20px;">🛡️</span> <span class="top-title">BRG DEF
