import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime

DB_FILE = "brg_erp_db.json"

INITIAL_DATA = {
    "customers": [
        {
            "id": "CUST-001", 
            "name": "KAVIANI 2015", 
            "country": "Georgia / Gürcistan", 
            "contact_person": "ROMA", 
            "phone": "+995 599351351", 
            "email": "fatih@brgdefence.com", 
            "address": "BATUMI, BAGRATIONI 157A"
        }
    ],
    "products": [
        {"code": "BRG55", "name": "BRG55 Piyade Tüfeği", "category": "Tüfek", "unit_price": 1200.0},
        {"code": "BRG9-ELITE-G2", "name": "BRG9 ELITE Gen2 Tabanca", "category": "Tabanca", "unit_price": 450.0},
        {"code": "BRG9-FDX", "name": "BRG9 FDX Tabanca", "category": "Tabanca", "unit_price": 420.0}
    ],
    "quotations": []
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

st.set_page_config(page_title="BRG Defence — Sipariş Alma", page_icon="🛡️", layout="wide")
db = load_db()

# Custom CSS — Eski Sistem Arayüzüne Benzeyen Gri/Beyaz Kutu Stili
st.markdown("""
<style>
    .stApp {
        background-color: #f8f9fa;
    }
    .box-container {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .top-nav {
        display: flex;
        gap: 10px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Üst Navigasyon
c_nav1, c_nav2, c_nav3, _ = st.columns([1, 1, 1.5, 5])
with c_nav1:
    st.button("← Back / Geri")
with c_nav2:
    st.button("Forward / İleri →")
with c_nav3:
    st.button("🏠 Home / Ana ekran")

st.caption("🔴 Unsaved changes / Kaydedilmemiş değişiklikler")

# Session State Yönetimi
if "quote_data" not in st.session_state:
    st.session_state.quote_data = {
        "customer": {},
        "dates": {},
        "items": [],
        "payment": {}
    }

if "magazines" not in st.session_state:
    st.session_state.magazines = [
        {"capacity": "Select capacity / Kapasite seçin", "qty": 1}
    ]

# 4 Adımlı Sekmeler
t1, t2, t3, t4 = st.tabs([
    "1️⃣ Customer / Müşteri", 
    "2️⃣ Dates / Tarihler", 
    "3️⃣ Products / Ürünler", 
    "4️⃣ Payment & save / Ödeme ve kayıt"
])

# ==========================================
# ADIM 1: MÜŞTERİ BİLGİLERİ
# ==========================================
with t1:
    st.markdown("### **01 Customer details / Müşteri bilgileri**")
    
    col_c1, col_c2 = st.columns(2)
    cust_options = {f"{c['name']} — {c['country']}": c for c in db["customers"]}
    selected_cust_label = col_c2.selectbox("Saved customers / Kayıtlı müşteriler", list(cust_options.keys()))
    selected_cust = cust_options[selected_cust_label]
    
    cust_selection = col_c1.selectbox("Customer selection / Müşteri seçimi", ["Saved customer / Kayıtlı müşteri", "New customer / Yeni müşteri"])
    
    col1, col2 = st.columns(2)
    company_name = col1.text_input("Company or customer / Firma veya müşteri adı *", value=selected_cust["name"])
    contact_person = col2.text_input("Contact person / Yetkili kişi", value=selected_cust.get("contact_person", ""))
    
    country = col1.selectbox("Country / Ülke *", ["Georgia / Gürcistan", "Iraq / Irak", "Azerbaijan / Azerbaycan", "Turkey / Türkiye"])
    phone = col2.text_input("Phone / Telefon", value=selected_cust.get("phone", ""))
    
    email = col1.text_input("Email / E-posta", value=selected_cust.get("email", ""))
    address = st.text_area("Customer address / Müşteri adresi", value=selected_cust.get("address", ""), height=80)
    
    st.caption("New customers are saved with the order. Edit company profiles in Company folders. / Yeni müşteriler siparişle kaydedilir.")
    
    col_b1, col_b2 = st.columns([4, 1])
    if col_b2.button("Next / Devam →", key="s1_next", type="primary"):
        st.session_state.quote_data["customer"] = {
            "name": company_name, "contact_person": contact_person,
            "country": country, "phone": phone, "email": email, "address": address
        }
        st.success("Müşteri bilgileri kaydedildi.")

# ==========================================
# ADIM 2: TARİHLER VE TEKLİF DETAYLARI
# ==========================================
with t2:
    st.markdown("### **Quotation tracking / Teklif takibi**")
    valid_until = st.date_input("Valid until / Geçerlilik tarihi *")
    st.caption("Saving as sent records the status; it does not email the customer.")
    
    st.markdown("### **02 Quotation details / Teklif bilgileri**")
    col_d1, col_d2 = st.columns(2)
    quote_number = col_d1.text_input("Quotation number — automatic / Teklif numarası — otomatik", value="QUO-2026-C2C27E56", disabled=True
