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
        {"code": "BRG55-556", "name": "BRG55 Piyade Tüfeği 5.56x45mm", "category": "Tüfek", "unit_price": 1200.0},
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

# CSS İle Özel Stepper / Buton Stilleri
st.markdown("""
<style>
    .stButton>button {
        border-radius: 6px;
    }
    .wizard-header {
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #e9ecef;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Navigation Bar
col_nav1, col_nav2, col_nav3 = st.columns([1, 1, 4])
with col_nav1:
    if st.button("← Back / Geri"):
        pass
with col_nav2:
    if st.button("Forward / İleri →"):
        pass
with col_nav3:
    if st.button("🏠 Home / Ana ekran"):
        pass

st.title("🛡️ BRG Defence — Sipariş Alma & Teklif Modülü")

# Session State Hazırlıkları
if "step" not in st.session_state:
    st.session_state.step = 1

if "quote_data" not in st.session_state:
    st.session_state.quote_data = {
        "customer": {},
        "dates": {},
        "items": [],
        "payment": {}
    }

# Step Navigation Tabs
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
    
    st.caption("New customers are saved with the order. Edit company profiles in Company folders. / Yeni müşteriler siparişle kaydedilir.")
    
    if st.button("Next / Devam →", key="step1_next", type="primary"):
        st.session_state.quote_data["customer"] = {
            "name": company_name,
            "contact_person": contact_person,
            "country": country,
            "phone": phone,
            "email": email,
            "address": address
        }
        st.success("Müşteri bilgileri kaydedildi. Lütfen üstteki '2️⃣ Dates / Tarihler' sekmesine geçiniz.")

# --- ADIM 2: TARİHLER VE KODLAR ---
with t2:
    st.subheader("Quotation tracking / Teklif takibi")
    valid_until = st.date_input("Valid until / Geçerlilik tarihi *")
    st.caption("Saving as sent records the status; it does not email the customer. / Gönderildi olarak kaydetmek durum kaydıdır; müşteriye e-posta göndermez.")
    
    st.subheader("02 Quotation details / Teklif bilgileri")
    col_d1, col_d2 = st.columns(2)
    
    auto_quote_num = f"QUO-2026-C2C27E56"
    quote_number = col_d1.text_input("Quotation number — automatic / Teklif numarası — otomatik", value=auto_quote_num, disabled=True)
    quote_date = col_d2.date_input("Quotation date / Teklif tarihi *", datetime.now())
    
    delivery_date = col_d1.date_input("Requested delivery date / İstenen teslim tarihi *")
    currency = col_d2.selectbox("Currency / Para birimi", ["USD", "EUR", "TRY"])

    if st.button("Next / Devam →", key="step2_next", type="primary"):
        st.session_state.quote_data["dates"] = {
            "quote_number": quote_number,
            "valid_until": str(valid_until),
            "quote_date": str(quote_date),
            "delivery_date": str(delivery_date),
            "currency": currency
        }
        st.success("Tarih ve teklif detayları kaydedildi. Lütfen '3️⃣ Products / Ürünler' sekmesine geçiniz.")

# --- ADIM 3: ÜRÜNLER VE ŞARJÖR DETAYLARI ---
with t3:
    st.subheader("Item / Ürün Kalemi")
    
    col_p1, col_p2, col_p3 = st.columns([2, 1, 1])
    prod_options = {f"{p['code']} - {p['name']}": p for p in db["products"]}
    selected_p_label = col_p1.selectbox("Product / Model / Ürün *", list(prod_options.keys()))
    selected_p = prod_options[selected_p_label]
    
    qty = col_p2.number_input("Quantity / Adet *", min_value=1, value=1)
    unit_price = col_p3.number_input("Unit price / Birim fiyat *", min_value=0.0, value=float(selected_p["unit_price"]))
    
    st.markdown("#### Color / Renk")
    col_mode = st.radio("Color Mode", ["Single color / Tek renk", "Different colors / Farklı renkler"], horizontal=True)
    prod_color = st.selectbox("Product color / Ürün rengi *", ["Select color / Renk seçin", "Siyah / Black", "FDE / Tan", "Çöl / Desert Sand"])
    cerakote_code = st.text_input("Cerakote code / Cerakote kodu (optional / isteğe bağlı)")
    
    st.markdown("#### Magazine capacity & quantity / Şarjör kapasitesi ve adedi")
    col_m1, col_m2 = st.columns(2)
    mag_cap = col_m1.selectbox("Capacity / Kapasite *", ["Select capacity / Kapasite seçin", "15 Round / 15'lik", "18 Round / 18'lik", "20 Round / 20'lik"])
    mag_qty = col_m2.number_input("Quantity per product · Adet / ürün *", min_value=1, value=2)
    
    if st.button("+ Add item / Ürün ekle"):
        item_entry = {
            "product": selected_p["name"],
            "code": selected_p["code"],
            "quantity": qty,
            "unit_price": unit_price,
            "total": qty * unit_price,
            "color": prod_color,
            "cerakote": cerakote_code,
            "magazine": f"{mag_qty}x {mag_cap}"
        }
        st.session_state.quote_data["items"].append(item_entry)
        st.success(f"{selected_p['name']} teklife eklendi!")

    if st.session_state.quote_data["items"]:
        st.markdown("---")
        st.write("### Eklenen Ürünler")
        st.table(pd.DataFrame(st.session_state.quote_data["items"]))

    if st.button("Next / Devam →", key="step3_next", type="primary"):
        st.success("Ürünler kaydedildi. Lütfen '4️⃣ Payment & save / Ödeme ve kayıt' sekmesine geçiniz.")

# --- ADIM 4: ÖDEME VE TEKLİF KAYIT ---
with t4:
    st.subheader("QUO-2026-C2C27E56 - NEW / YENİ")
    st.markdown("### **Draft quotation / Taslak teklif**")
    st.caption("Complete the fields before issuing. / Göndermeden önce bilgileri tamamlayın.")
    
    st.subheader("04 Payment and notes / Ödeme ve açıklamalar")
    
    pay_terms = st.text_area(
        "Payment terms / Ödeme koşulları *", 
        placeholder="Advance payment and balance payment terms / Örn. avans oranı ve kalan ödemenin zamanı"
    )
    
    quote_notes = st.text_area("Quotation notes / Teklif notları", height=100)
    
    col_b1, col_b2, col_b3 = st.columns([1, 1, 2])
    
    with col_b2:
        if st.button("Save draft / Taslak kaydet"):
            st.info("Taslak olarak kaydedildi.")
            
    with col_b3:
        if st.button("Save quotation / Teklifi kaydet", type="primary"):
            final_record = st.session_state.quote_data
            final_record["payment"] = {
                "terms": pay_terms,
                "notes": quote_notes
            }
            final_record["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            db["quotations"].append(final_record)
            save_db(db)
            
            st.balloons()
            st.success("✅ Teklif başarıyla kaydedildi!")
            st.json(final_record)
