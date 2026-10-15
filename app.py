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
        },
        {
            "id": "CUST-002",
            "name": "AL-TAJ COMPANY",
            "country": "Iraq / Irak",
            "contact_person": "AHMED",
            "phone": "+964 7701234567",
            "email": "info@altaj.iq",
            "address": "Baghdad, Karrada District"
        }
    ],
    "products": [
        {"code": "BRG55", "name": "BRG55 Piyade Tüfeği (5.56x45mm)", "category": "Tüfek", "unit_price": 1200.0},
        {"code": "BRG9-ELITE-G2", "name": "BRG9 ELITE Gen2 Tabanca (9x19mm)", "category": "Tabanca", "unit_price": 450.0},
        {"code": "BRG9-FDX", "name": "BRG9 FDX Tabanca (9x19mm)", "category": "Tabanca", "unit_price": 420.0}
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

st.set_page_config(page_title="BRG DEFENCE | ERP Portal", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")
db = load_db()

# ==========================================
# GÜÇLÜ & FÜTÜRİSTİK ÖZEL CSS TASARIMI (DARK / GLASS)
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Arka Plan ve Genel Tema */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }

    /* Glassmorphism Kartlar */
    div[data-testid="stVerticalBlock"] > div[style*="background-color"] {
        background: rgba(30, 41, 59, 0.7) !important;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }

    /* Üst İlerleme Çubuğu (Stepper) */
    .stepper-wrapper {
        display: flex;
        justify-content: space-between;
        margin-bottom: 28px;
        background: rgba(15, 23, 42, 0.6);
        padding: 16px 28px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .step-item {
        display: flex;
        align-items: center;
        gap: 12px;
        color: #64748b;
        font-weight: 600;
        font-size: 14px;
    }
    .step-item.active {
        color: #38bdf8;
    }
    .step-number {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: #334155;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
    }
    .step-item.active .step-number {
        background: linear-gradient(135deg, #0284c7 0%, #38bdf8 100%);
        color: #ffffff;
        box-shadow: 0 0 12px rgba(56, 189, 248, 0.5);
    }

    /* Özel Buton Stilleri */
    .stButton > button {
        border-radius: 10px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease-in-out !important;
        border: none !important;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        color: white !important;
        box-shadow: 0 4px 14px 0 rgba(2, 132, 199, 0.39) !important;
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px 0 rgba(2, 132, 199, 0.55) !important;
    }

    /* Rozet (Badge) Etiketleri */
    .mag-badge {
        display: inline-block;
        background: rgba(56, 189, 248, 0.15);
        color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.3);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        margin-right: 6px;
    }

    /* Başlık Efekti */
    .brand-header {
        font-size: 28px;
        font-weight: 800;
        background: linear-gradient(to right, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Session State İlklendirme
if "step" not in st.session_state:
    st.session_state.step = 1

if "quote_data" not in st.session_state:
    st.session_state.quote_data = {
        "customer": {},
        "dates": {},
        "items": [],
        "payment": {}
    }

if "mag_list" not in st.session_state:
    st.session_state.mag_list = [
        {"capacity": "18 Round / 18'lik", "qty": 2},
        {"capacity": "15 Round / 15'lik", "qty": 1}
    ]

# ==========================================
# ÜST BİLGİ VE MOD ERKAN
# ==========================================
col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.markdown("<h1 style='text-align: center;'>🛡️</h1>", unsafe_allow_html=True)
with col_title:
    st.markdown("<div class='brand-header'>BRG DEFENCE — QUOTATION & ORDER ENGINE</div>", unsafe_allow_html=True)
    st.caption("Burgu Savunma Teknolojileri A.Ş. — Yüksek Hassasiyetli Sipariş Yönetim Portalı")

st.markdown("---")

# Interaktif Stepper Bar
steps_html = f"""
<div class="stepper-wrapper">
    <div class="step-item {'active' if st.session_state.step >= 1 else ''}">
        <div class="step-number">1</div> 👤 Customer / Müşteri
    </div>
    <div class="step-item {'active' if st.session_state.step >= 2 else ''}">
        <div class="step-number">2</div> 📅 Dates / Tarihler
    </div>
    <div class="step-item {'active' if st.session_state.step >= 3 else ''}">
        <div class="step-number">3</div> 🎯 Products & Mag Config
    </div>
    <div class="step-item {'active' if st.session_state.step >= 4 else ''}">
        <div class="step-number">4</div> 💳 Payment & Confirm
    </div>
</div>
"""
st.markdown(steps_html, unsafe_allow_html=True)

# ==========================================
# ADIM 1: MÜŞTERİ SEÇİMİ VE DETAYLARI
# ==========================================
if st.session_state.step == 1:
    st.subheader("01 / Customer Details — Müşteri Bilgileri")
    
    with st.container():
        c_mode, c_list = st.columns(2)
        cust_selection = c_mode.radio("Customer selection / Müşteri seçimi", ["Saved customer / Kayıtlı Müşteri", "New customer / Yeni Kayıt"], horizontal=True)
        
        cust_options = {f"{c['name']} ({c['country']})": c for c in db["customers"]}
        selected_cust_label = c_list.selectbox("Saved customers / Kayıtlı müşteriler", list(cust_options.keys()))
        selected_cust = cust_options[selected_cust_label]
        
        col1, col2 = st.columns(2)
        company_name = col1.text_input("Company or customer / Firma veya Müşteri adı *", value=selected_cust["name"])
        contact_person = col2.text_input("Contact person / Yetkili kişi", value=selected_cust.get("contact_person", ""))
        
        country = col1.selectbox("Country / Ülke *", ["Georgia / Gürcistan", "Iraq / Irak", "Azerbaijan / Azerbaycan", "Turkey / Türkiye", "USA / ABD"])
        phone = col2.text_input("Phone / Telefon", value=selected_cust.get("phone", ""))
        
        email = col1.text_input("Email / E-posta", value=selected_cust.get("email", ""))
        address = st.text_area("Customer address / Müşteri adresi", value=selected_cust.get("address", ""), height=70)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Next: Dates & Numbers / Devam Et →", type="primary", use_container_width=True):
            st.session_state.quote_data["customer"] = {
                "name": company_name, "contact_person": contact_person,
                "country": country, "phone": phone, "email": email, "address": address
            }
            st.session_state.step = 2
            st.rerun()

# ==========================================
# ADIM 2: TARİHLER VE TEKLİF NUMARASI
# ==========================================
elif st.session_state.step == 2:
    st.subheader("02 / Quotation Dates & Tracking — Tarih ve Kod Bilgileri")
    
    with st.container():
        col_d1, col_d2 = st.columns(2)
        quote_number = col_d1.text_input("Quotation Reference — Automatic", value="QUO-2026-C2C27E56", disabled=True)
        quote_date = col_d2.date_input("Quotation Date / Teklif Tarihi *", datetime.now())
        
        valid_until = col_d1.date_input("Valid Until / Geçerlilik Tarihi *")
        delivery_date = col_d2.date_input("Requested Delivery Date / İstenen Teslim Tarihi *")
        
        currency = col_d1.selectbox("Currency / Para Birimi", ["USD (\$)", "EUR (€)", "TRY (₺)"])
        
        b_back, b_next = st.columns([1, 2])
        if b_back.button("← Previous / Geri"):
            st.session_state.step = 1
            st.rerun()
            
        if b_next.button("Next: Product Config / Ürün Seçimine Geç →", type="primary", use_container_width=True):
            st.session_state.quote_data["dates"] = {
                "quote_number": quote_number, "valid_until": str(valid_until),
                "quote_date": str(quote_date), "delivery_date": str(delivery_date), "currency": currency
            }
            st.session_state.step = 3
            st.rerun()

# ==========================================
# ADIM 3: ÜRÜN SEÇİMİ VE ÇOKLU DİNAMİK ŞARJÖR MODÜLÜ
# ==========================================
elif st.session_state.step == 3:
    st.subheader("03 / Product & Magazine Configuration — Ürün ve Konfigürasyon")
    
    col_main, col_summary = st.columns([2, 1])
    
    with col_main:
        with st.container():
            col_p1, col_p2, col_p3 = st.columns([2, 1, 1])
            prod_options = {f"{p['code']} — {p['name']}": p for p in db["products"]}
            selected_p_label = col_p1.selectbox("Product / Model Seçin *", list(prod_options.keys()))
            selected_p = prod_options[selected_p_label]
            
            qty = col_p2.number_input("Adet (Qty) *", min_value=1, value=5)
            unit_price = col_p3.number_input("Birim Fiyat *", min_value=0.0, value=float(selected_p["unit_price"]))
            
            st.markdown("---")
            st.markdown("##### 🎨 Color & Coating / Renk ve Kaplama")
            col_c1, col_c2 = st.columns(2)
            prod_color = col_c1.selectbox("Product Color / Renk *", ["Siyah / Black", "FDE / Tan", "Çöl Sand / Desert", "OD Green"])
            cerakote_code = col_c2.text_input("Cerakote Code (Optional / İsteğe Bağlı)")
            
            st.markdown("---")
            st.markdown("##### 🔫 Magazine Capacity & Mix / Şarjör Kombinasyonu (Çoklu Ekleme)")
            st.caption("Her ürünle teslim edilecek şarjör tiplerini ve adetlerini özgürce tanımlayın:")

            cap_options = ["15 Round / 15'lik", "18 Round / 18'lik", "20 Round / 20'lik", "30 Round / 30'luk"]

            # Dinamik Şarjör Listesi Yönetimi
            to_remove = None
            for idx, mag in enumerate(st.session_state.mag_list):
                m1, m2, m3 = st.columns([2, 2, 1])
                
                curr_cap = cap_options.index(mag["capacity"]) if mag["capacity"] in cap_options else 0
                new_cap = m1.selectbox(f"Kapasite #{idx+1}", cap_options, index=curr_cap, key=f"c_sel_{idx}")
                new_qty = m2.number_input(f"Şarjör Adet / Ürün #{idx+1}", min_value=1, value=mag["qty"], key=f"q_sel_{idx}")
                
                st.session_state.mag_list[idx] = {"capacity": new_cap, "qty": new_qty}
                
                if m3.button("🗑️ Sil", key=f"del_m_{idx}"):
                    to_remove = idx

            if to_remove is not None:
                st.session_state.mag_list.pop(to_remove)
                st.rerun()

            if st.button("➕ Add Magazine Type / Yeni Şarjör Tipi Ekle"):
                st.session_state.mag_list.append({"capacity": "18 Round / 18'lik", "qty": 1})
                st.rerun()

            st.markdown("---")
            if st.button("🚀 Add Item to Quotation / Kalemi Teklife Ekle", type="primary", use_container_width=True):
                mag_summary = " + ".join([f"{m['qty']}x {m['capacity']}" for m in st.session_state.mag_list])
                
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
                st.toast(f"✅ {selected_p['code']} teklife başarıyla eklendi!", icon="🎉")

    # CANLI ÖZET PANELİ (Sağ Taraf)
    with col_summary:
        st.markdown("### 📋 Quotation Summary")
        if not st.session_state.quote_data["items"]:
            st.info("Henüz ürün eklenmedi. Sol panelden ürün seçip ekleyin.")
        else:
            grand_total = 0
            for i, item in enumerate(st.session_state.quote_data["items"]):
                st.markdown(f"**{i+1}. {item['code']}** × {item['quantity']} Adet")
                st.caption(f"🎨 {item['color']} | 🔫 {item['magazines']}")
                st.markdown(f"**Tutar:** `${item['total']:,.2f}`")
                grand_total += item['total']
                st.markdown("---")
            
            st.markdown(f"### **Total Amount:** `${grand_total:,.2f}`")

    st.markdown("<br>", unsafe_allow_html=True)
    b_back, b_next = st.columns([1, 2])
    if b_back.button("← Previous / Tarihlere Dön"):
        st.session_state.step = 2
        st.rerun()
        
    if b_next.button("Next: Payment & Save / Ödeme Adımına Geç →", type="primary", use_container_width=True):
        if not st.session_state.quote_data["items"]:
            st.error("Lütfen ilerlemeden önce en az 1 ürün kalemi ekleyin!")
        else:
            st.session_state.step = 4
            st.rerun()

# ==========================================
# ADIM 4: ÖDEME ŞARTLARI VE SİPARİŞ KAYIT
# ==========================================
elif st.session_state.step == 4:
    st.subheader("04 / Payment Terms & Final Approval — Ödeme ve Kayıt")
    
    with st.container():
        st.markdown("### **Review Quotation Details / Teklif Özeti**")
        
        c_info, p_info = st.columns(2)
        with c_info:
            st.markdown("**Müşteri:** " + st.session_state.quote_data["customer"].get("name", "-"))
            st.markdown("**Ülke:** " + st.session_state.quote_data["customer"].get("country", "-"))
        with p_info:
            st.markdown("**Teklif Ref:** " + st.session_state.quote_data["dates"].get("quote_number", "-"))
            st.markdown("**Para Birimi:** " + st.session_state.quote_data["dates"].get("currency", "-"))
        
        st.markdown("---")
        st.markdown("#### **Ürün Kalemleri**")
        st.table(pd.DataFrame(st.session_state.quote_data["items"]))
        
        st.markdown("---")
        pay_terms = st.text_area("Payment Terms / Ödeme Koşulları *", value="%30 Avans (TT), %70 Yükleme Öncesi Ödeme")
        quote_notes = st.text_area("Notes & Exclusions / Teklif Notları", value="Fiyatlara KDV ve Nakliye dahil değildir. Teslimat Fabrika çıkışlıdır.")
        
        b_back, b_save = st.columns([1, 2])
        if b_back.button("← Previous / Ürün Düzenle"):
            st.session_state.step = 3
            st.rerun()
            
        if b_save.button("🔥 Complete & Issue Quotation / Teklifi Onayla ve Kaydet", type="primary", use_container_width=True):
            final_record = st.session_state.quote_data
            final_record["payment"] = {"terms": pay_terms, "notes": quote_notes}
            final_record["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            db["quotations"].append(final_record)
            save_db(db)
            
            st.balloons()
            st.success("🎉 Teklif başarıyla ERP veritabanına kaydedildi ve referans numarası oluşturuldu!")
            st.json(final_record)
