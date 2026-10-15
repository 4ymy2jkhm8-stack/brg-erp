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
        {"code": "BRG9-ELITE-G2", "name": "BRG9 ELITE Gen2 Tabanca", "category": "Tabanca", "unit_price": 450.0},
        {"code": "BRG55", "name": "BRG55 Piyade Tüfeği", "category": "Tüfek", "unit_price": 1200.0},
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

st.set_page_config(page_title="BRG Defence - Sipariş Alma", page_icon="🛡️", layout="wide")
db = load_db()

# Navigation Bar
col_nav1, col_nav2, col_nav3 = st.columns([1, 1, 4])
with col_nav1:
    st.button("← Back / Geri")
with col_nav2:
    st.button("Forward / İleri →")
with col_nav3:
    st.button("🏠 Home / Ana ekran")

st.title("🛡️ BRG Defence — Sipariş Alma & Teklif Modülü")

# Session State Yönetimi
if "quote_data" not in st.session_state:
    st.session_state.quote_data = {
        "customer": {},
        "dates": {},
        "items": [],
        "payment": {}
    }

if "mag_list" not in st.session_state:
    st.session_state.mag_list = [
        {"capacity": "18 Round / 18'lik", "qty": 2}
    ]

# Step Tabs
t1, t2, t3, t4 = st.tabs([
    "1️⃣ Customer / Müşteri", 
    "2️⃣ Dates / Tarihler", 
    "3️⃣ Products / Ürünler", 
    "4️⃣ Payment & save / Ödeme ve kayıt"
])

# --- ADIM 1: MÜŞTERİ BİLGİLERİ ---
with t1:
    st.subheader("01 Customer details / Müşteri bilgileri")
    col_c1, col_c2 = st.columns(2)
    
    cust_options = {f"{c['name']} — {c['country']}": c for c in db["customers"]}
    selected_cust_label = col_c2.selectbox("Saved customers / Kayıtlı müşteriler", list(cust_options.keys()))
    selected_cust = cust_options[selected_cust_label]
    
    cust_selection = col_c1.selectbox("Customer selection / Müşteri seçimi", ["Saved customer / Kayıtlı müşteri", "Yeni Müşteri Ekle"])
    
    col1, col2 = st.columns(2)
    company_name = col1.text_input("Company or customer / Firma veya müşteri adı *", value=selected_cust["name"])
    contact_person = col2.text_input("Contact person / Yetkili kişi", value=selected_cust.get("contact_person", ""))
    country = col1.selectbox("Country / Ülke *", ["Georgia / Gürcistan", "Iraq / Irak", "Azerbaijan / Azerbaycan", "Turkey / Türkiye"])
    phone = col2.text_input("Phone / Telefon", value=selected_cust.get("phone", ""))
    email = col1.text_input("Email / E-posta", value=selected_cust.get("email", ""))
    address = st.text_area("Customer address / Müşteri adresi", value=selected_cust.get("address", ""), height=80)
    
    if st.button("Next / Devam →", key="step1_next", type="primary"):
        st.session_state.quote_data["customer"] = {
            "name": company_name, "contact_person": contact_person, "country": country,
            "phone": phone, "email": email, "address": address
        }
        st.success("Müşteri bilgileri kaydedildi.")

# --- ADIM 2: TARİHLER ---
with t2:
    st.subheader("Quotation tracking / Teklif takibi")
    valid_until = st.date_input("Valid until / Geçerlilik tarihi *")
    
    st.subheader("02 Quotation details / Teklif bilgileri")
    col_d1, col_d2 = st.columns(2)
    quote_number = col_d1.text_input("Quotation number — automatic / Teklif numarası — otomatik", value="QUO-2026-C2C27E56", disabled=True)
    quote_date = col_d2.date_input("Quotation date / Teklif tarihi *", datetime.now())
    delivery_date = col_d1.date_input("Requested delivery date / İstenen teslim tarihi *")
    currency = col_d2.selectbox("Currency / Para birimi", ["USD", "EUR", "TRY"])

    if st.button("Next / Devam →", key="step2_next", type="primary"):
        st.session_state.quote_data["dates"] = {
            "quote_number": quote_number, "valid_until": str(valid_until),
            "quote_date": str(quote_date), "delivery_date": str(delivery_date), "currency": currency
        }
        st.success("Tarih detayları kaydedildi.")

# --- ADIM 3: ÜRÜNLER VE ÇOKLU ŞARJÖR SEÇİMİ ---
with t3:
    st.subheader("Item / Ürün Kalemi")
    
    col_p1, col_p2, col_p3 = st.columns([2, 1, 1])
    prod_options = {f"{p['code']} - {p['name']}": p for p in db["products"]}
    selected_p_label = col_p1.selectbox("Product / Model / Ürün *", list(prod_options.keys()))
    selected_p = prod_options[selected_p_label]
    
    qty = col_p2.number_input("Quantity / Adet *", min_value=1, value=1)
    unit_price = col_p3.number_input("Unit price / Birim fiyat *", min_value=0.0, value=float(selected_p["unit_price"]))
    
    st.markdown("#### Color / Renk")
    prod_color = st.selectbox("Product color / Ürün rengi *", ["Siyah / Black", "FDE / Tan", "Çöl / Desert Sand"])
    cerakote_code = st.text_input("Cerakote code / Cerakote kodu (optional / isteğe bağlı)")
    
    st.markdown("#### Magazine capacity & quantity / Şarjör kapasitesi ve adedi")
    
    cap_options = ["15 Round / 15'lik", "18 Round / 18'lik", "20 Round / 20'lik", "30 Round / 30'luk"]

    # Dinamik Şarjör Satırları
    to_remove = None
    for i, mag in enumerate(st.session_state.mag_list):
        m_col1, m_col2, m_col3 = st.columns([2, 2, 1])
        
        # Kapasite Seçimi
        current_cap_idx = cap_options.index(mag["capacity"]) if mag["capacity"] in cap_options else 0
        new_cap = m_col1.selectbox(f"Capacity / Kapasite * #{i+1}", cap_options, index=current_cap_idx, key=f"cap_select_{i}")
        
        # Adet Seçimi
        new_qty = m_col2.number_input(f"Quantity per product · Adet / ürün * #{i+1}", min_value=1, value=mag["qty"], key=f"qty_select_{i}")
        
        # Güncelleme
        st.session_state.mag_list[i] = {"capacity": new_cap, "qty": new_qty}
        
        # Sil Butonu
        if m_col3.button("🗑️ Sil", key=f"del_mag_btn_{i}"):
            to_remove = i

    if to_remove is not None:
        st.session_state.mag_list.pop(to_remove)
        st.rerun()

    # Yeni Şarjör Satırı Ekleme Butonu
    if st.button("+ Add magazine type / Şarjör tipi ekle"):
        st.session_state.mag_list.append({"capacity": "15 Round / 15'lik", "qty": 1})
        st.rerun()

    st.caption("Örnek: 2 × 18-round + 1 × 15-round. Her satırdaki adet, bir ürünle verilecek miktardır.")

    st.markdown("---")
    if st.button("+ Add item / Ürün ekle", type="primary"):
        mag_summary = " + ".join([f"{m['qty']} x {m['capacity']}" for m in st.session_state.mag_list])
        
        item_entry = {
            "product": selected_p["name"],
            "code": selected_p["code"],
            "quantity": qty,
            "unit_price": unit_price,
            "total": qty * unit_price,
            "color": prod_color,
            "cerakote": cerakote_code,
            "magazines": mag_summary
        }
        st.session_state.quote_data["items"].append(item_entry)
        st.success(f"✅ {selected_p['name']} eklendi! (Şarjörler: {mag_summary})")

    if st.session_state.quote_data["items"]:
        st.markdown("---")
        st.write("### Eklenen Ürünler")
        st.table(pd.DataFrame(st.session_state.quote_data["items"]))

# --- ADIM 4: ÖDEME VE KAYIT ---
with t4:
    st.subheader("Draft quotation / Taslak teklif")
    pay_terms = st.text_area("Payment terms / Ödeme koşulları *", placeholder="Örn. %30 avans, %70 yükleme öncesi TT")
    quote_notes = st.text_area("Quotation notes / Teklif notları", height=100)
    
    if st.button("Save quotation / Teklifi kaydet", type="primary"):
        final_record = st.session_state.quote_data
        final_record["payment"] = {"terms": pay_terms, "notes": quote_notes}
        final_record["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        db["quotations"].append(final_record)
        save_db(db)
        
        st.balloons()
        st.success("✅ Teklif başarıyla kaydedildi!")
        st.json(final_record)
