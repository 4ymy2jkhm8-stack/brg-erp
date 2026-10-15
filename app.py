import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime

DB_FILE = "brg_erp_db.json"

INITIAL_DATA = {
    "company": {
        "title": "BURGU SAVUNMA TEKNOLOJİLERİ VE HAVACILIK A.Ş.",
        "tax_office": "Pendik V.D.",
        "tax_no": "1910543210",
        "address": "Sanayi Mah. Teknopark Bulvarı No:1 Pendik / İstanbul",
        "iban": "TR12 0001 5001 5800 7300 1234 56",
        "swift": "VAKFTR2A"
    },
    "customers": [
        {
            "id": "CUST-001", 
            "name": "KAVIANI 2015", 
            "country": "Georgia / Gürcistan", 
            "contact_person": "ROMA", 
            "phone": "+995 599351351", 
            "email": "fatih@brgdefence.com", 
            "address": "BATUMI, BAGRATIONI 157A",
            "quotations_count": 0,
            "open_orders": 2,
            "in_production": 0
        }
    ],
    "products": [
        {"code": "BRG55", "name": "BRG55 Infantry Rifle / Piyade Tüfeği", "category": "Rifle / Tüfek", "unit_price": 1200.0, "stock": 150},
        {"code": "BRG9-ELITE-G2", "name": "BRG9 ELITE Gen2 Pistol / Tabanca", "category": "Pistol / Tabanca", "unit_price": 450.0, "stock": 320},
        {"code": "BRG9-FDX", "name": "BRG9 FDX Pistol / Tabanca", "category": "Pistol / Tabanca", "unit_price": 420.0, "stock": 85}
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

st.set_page_config(page_title="BRG Defence — Sales Operations / Satış Yönetimi", page_icon="🛡️", layout="wide")
db = load_db()

# MODERN VE ŞIK CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background-color: #f8fafc;
    }
    
    .main-header {
        background: linear-gradient(90deg, #0f172a 0%, #1e293b 100%);
        color: #ffffff;
        padding: 16px 28px;
        border-radius: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 16px;
    }
    .main-title {
        font-size: 22px;
        font-weight: 700;
        letter-spacing: 1px;
    }
    .main-sub {
        font-size: 11px;
        color: #94a3b8;
        text-align: right;
    }

    .alert-box {
        background-color: #fffbeb;
        border: 1px solid #fef3c7;
        border-left: 4px solid #f59e0b;
        border-radius: 8px;
        padding: 14px 20px;
        color: #b45309;
        font-weight: 600;
        font-size: 14px;
        margin-bottom: 20px;
    }

    .kpi-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .kpi-num {
        font-size: 32px;
        font-weight: 700;
        color: #0f172a;
    }
    .kpi-desc {
        font-size: 13px;
        color: #64748b;
        font-weight: 500;
    }

    .cust-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        margin-top: 15px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .avatar-box {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        color: #ffffff;
        width: 46px;
        height: 46px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 16px;
    }
</style>
""", unsafe_allow_html=True)

# Session State
if "current_view" not in st.session_state:
    st.session_state.current_view = "dashboard"

if "quote_data" not in st.session_state:
    st.session_state.quote_data = {"customer": {}, "dates": {}, "items": [], "payment": {}}

if "magazines" not in st.session_state:
    st.session_state.magazines = [{"capacity": "18 Round / 18'lik", "qty": 2}]

# HEADER
st.markdown("""
<div class="main-header">
    <div style="display: flex; align-items: center; gap: 14px;">
        <span style="font-size: 26px;">🛡️</span>
        <span class="main-title">BRG DEFENCE</span>
    </div>
    <div class="main-sub">
        SALES OPERATIONS<br><b>SATIŞ YÖNETİMİ</b>
    </div>
</div>
""", unsafe_allow_html=True)

# ÜST MENÜ BUTONLARI (TAM ÇALIŞIR ŞEKİLDE ENTEGRE EDİLDİ)
m1, m2, m3, m4, m5 = st.columns([2, 1.5, 2.5, 2, 1.5])
with m1:
    if st.button("👥 Customers / Müşterilerimiz", type="primary" if st.session_state.current_view == "dashboard" else "secondary", use_container_width=True):
        st.session_state.current_view = "dashboard"
        st.rerun()
with m2:
    if st.button("🔍 Search / Ara", type="primary" if st.session_state.current_view == "search" else "secondary", use_container_width=True):
        st.session_state.current_view = "search"
        st.rerun()
with m3:
    if st.button("🏢 Our Company / Firma Bilgilerimiz", type="primary" if st.session_state.current_view == "company" else "secondary", use_container_width=True):
        st.session_state.current_view = "company"
        st.rerun()
with m4:
    if st.button("📦 Products / Ürünler", type="primary" if st.session_state.current_view == "products" else "secondary", use_container_width=True):
        st.session_state.current_view = "products"
        st.rerun()
with m5:
    if st.button("▶ Tools / Araçlar", type="primary" if st.session_state.current_view == "tools" else "secondary", use_container_width=True):
        st.session_state.current_view = "tools"
        st.rerun()

st.markdown("<div style='margin-bottom: 8px;'></div>", unsafe_allow_html=True)

# SÜREÇ VE GEZİNTİ BAR
nav_1, nav_2, nav_3, nav_4, nav_right = st.columns([1, 1, 1.3, 1.8, 2.5])
with nav_1:
    st.button("← Back / Geri")
with nav_2:
    st.button("Forward / İleri →")
with nav_3:
    if st.button("🏠 Home / Ana Ekran"):
        st.session_state.current_view = "dashboard"
        st.rerun()
with nav_4:
    if st.button("Resume Form / Formuma Dön", type="primary" if st.session_state.current_view == "form" else "secondary"):
        st.session_state.current_view = "form"
        st.rerun()
with nav_right:
    st.markdown("<div style='text-align: right; color: #64748b; font-size: 13px; margin-top: 8px; font-weight: 500;'>Home / Ana Ekran</div>", unsafe_allow_html=True)

today_str = datetime.now().strftime("%d.%m.%Y")

# ==========================================
# EKRAN 1: ANA DASHBOARD
# ==========================================
if st.session_state.current_view == "dashboard":
    st.caption("Records are saved in this browser / Kayıtlar bu tarayıcıda saklanır.")

    c_alert_text, c_alert_btn = st.columns([4, 1])
    with c_alert_text:
        st.markdown('<div class="alert-box">⚠️ 1 checks need attention / 1 kontrol bekliyor</div>', unsafe_allow_html=True)
    with c_alert_btn:
        if st.button("Review / Kontrol Et →", type="primary", use_container_width=True):
            st.session_state.current_view = "search"
            st.rerun()

    st.caption(f"BRG DEFENCE - {today_str}")
    head_left, head_right = st.columns([4, 1])
    with head_left:
        st.markdown("## **Customers** <span style='font-size: 16px; color: #64748b; font-weight: 400;'>Müşterilerimiz</span>", unsafe_allow_html=True)
        st.caption("Select a company to continue. / İşlem yapmak için bir firma seçin.")
    with head_right:
        if st.button("+ Add Company / Firma Ekle", type="primary", use_container_width=True):
            st.session_state.current_view = "add_company"
            st.rerun()

    k1, k2, k3 = st.columns(3)
    with k1:
        st.markdown(f'<div class="kpi-card"><div class="kpi-num">{len(db["customers"])}</div><div class="kpi-desc">Companies / Müşteri Firması</div></div>', unsafe_allow_html=True)
    with k2:
        st.markdown('<div class="kpi-card"><div class="kpi-num">2</div><div class="kpi-desc">Open Orders / Açık Sipariş</div></div>', unsafe_allow_html=True)
    with k3:
        st.markdown('<div class="kpi-card"><div class="kpi-num">1</div><div class="kpi-desc">Needs Attention → / Kontrol Bekleyen</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.text_input("Search companies / Firma ara", placeholder="Company or country / Firma adı veya ülke", label_visibility="collapsed")

    for cust in db["customers"]:
        avatar_text = cust.get("name", "CU")[:2].upper()
        
        st.markdown(f"""
        <div class="cust-card">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div style="display: flex; align-items: center; gap: 16px;">
                    <div class="avatar-box">{avatar_text}</div>
                    <div>
                        <div style="font-size: 18px; font-weight: 700; color: #0f172a;">{cust.get('name', 'Customer')}</div>
                        <div style="font-size: 13px; color: #64748b; font-weight: 500;">{cust.get('country', '-')}</div>
                    </div>
                </div>
                <div style="font-size: 20px; color: #94a3b8;">→</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        c_q, c_o, c_p, c_action = st.columns([1, 1, 1, 1])
        c_q.caption(f"<b>{cust.get('quotations_count', 0)}</b> Quotations / Açık Teklif")
        c_o.caption(f"<b>{cust.get('open_orders', 0)}</b> Orders / Açık Sipariş")
        c_p.caption(f"<b>{cust.get('in_production', 0)}</b> Production / Üretimde")
        if c_action.button("Forma Geç / Sipariş Oluştur", key=f"open_form_{cust.get('id', '001')}"):
            st.session_state.current_view = "form"
            st.rerun()

# ==========================================
# EKRAN 2: FİRMA BİLGİLERİMİZ
# ==========================================
elif st.session_state.current_view == "company":
    st.markdown("## 🏢 Our Company Profile / Firma Bilgilerimiz")
    comp = db["company"]
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.text_input("Title / Ünvan", value=comp["title"], disabled=True)
        st.text_input("Tax Office / Vergi Dairesi", value=comp["tax_office"], disabled=True)
        st.text_input("Tax No / Vergi Numarası", value=comp["tax_no"], disabled=True)
    with col_b:
        st.text_area("Address / Adres", value=comp["address"], disabled=True)
        st.text_input("IBAN / Banka Hesabı", value=comp["iban"], disabled=True)
        st.text_input("SWIFT Code", value=comp["swift"], disabled=True)

# ==========================================
# EKRAN 3: ÜRÜN KATALOĞU
# ==========================================
elif st.session_state.current_view == "products":
    st.markdown("## 📦 Product Catalog & Stock / Ürün Kataloğu ve Stok")
    st.dataframe(pd.DataFrame(db["products"]), use_container_width=True)

# ==========================================
# EKRAN 4: ARAMA VE FİLTRELEME
# ==========================================
elif st.session_state.current_view == "search":
    st.markdown("## 🔍 Search & Filters / Arama ve Filtreleme")
    q = st.text_input("Search query / Arama terimi girin")
    st.info("Arama sonuçları burada listelenecektir.")

# ==========================================
# EKRAN 5: ARAÇLAR
# ==========================================
elif st.session_state.current_view == "tools":
    st.markdown("## ▶ Sales Tools / Satış Araçları")
    st.write("Döviz Kuru Dönüştürücü / Exchange Rate Calculator")
    val = st.number_input("Amount in USD ($) / Tutar", value=1000.0)
    st.success(f"Estimated TRY Equivalent / Tahmini TL Karşılığı: {val * 34.5:.2f} ₺")

# ==========================================
# EKRAN 6: YENİ FİRMA EKLE
# ==========================================
elif st.session_state.current_view == "add_company":
    st.markdown("## ➕ Add New Company / Yeni Firma Ekle")
    new_name = st.text_input("Company Name / Firma Adı *")
    new_country = st.text_input("Country / Ülke *")
    new_contact = st.text_input("Contact Person / Yetkili Kişi")
    new_phone = st.text_input("Phone / Telefon")
    new_email = st.text_input("Email / E-posta")
    new_address = st.text_area("Address / Adres")
    
    if st.button("Save Company / Firmayı Kaydet", type="primary"):
        new_cust = {
            "id": f"CUST-{len(db['customers'])+1:03d}",
            "name": new_name, "country": new_country, "contact_person": new_contact,
            "phone": new_phone, "email": new_email, "address": new_address,
            "quotations_count": 0, "open_orders": 0, "in_production": 0
        }
        db["customers"].append(new_cust)
        save_db(db)
        st.success("✅ Firma eklendi!")
        st.session_state.current_view = "dashboard"
        st.rerun()

# ==========================================
# EKRAN 7: SİPARİŞ & TEKLİF FORMU (RESUME FORM)
# ==========================================
elif st.session_state.current_view == "form":
    st.caption("🔴 Unsaved Changes / Kaydedilmemiş Değişiklikler")
    
    t1, t2, t3, t4 = st.tabs([
        "1️⃣ Customer / Müşteri", 
        "2️⃣ Dates / Tarihler", 
        "3️⃣ Products / Ürünler", 
        "4️⃣ Payment & Save / Ödeme ve Kayıt"
    ])

    with t1:
        st.markdown("### **01 Customer Details / Müşteri Bilgileri**")
        col_c1, col_c2 = st.columns(2)
        
        cust_options = {f"{c.get('name', 'Firma')} — {c.get('country', '')}": c for c in db["customers"]}
        selected_cust_label = col_c2.selectbox("Saved Customers / Kayıtlı Müşteriler", list(cust_options.keys()))
        selected_cust = cust_options[selected_cust_label]
        
        cust_selection = col_c1.selectbox("Customer Selection / Müşteri Seçimi", ["Saved Customer / Kayıtlı Müşteri", "New Customer / Yeni Müşteri"])
        
        col1, col2 = st.columns(2)
        company_name = col1.text_input("Company or Customer / Firma veya Müşteri Adı *", value=selected_cust.get("name", ""))
        contact_person = col2.text_input("Contact Person / Yetkili Kişi", value=selected_cust.get("contact_person", ""))
        
        country_options = ["Georgia / Gürcistan", "Iraq / Irak", "Azerbaijan / Azerbaycan", "Turkey / Türkiye"]
        country = col1.selectbox("Country / Ülke *", country_options, index=0)
        phone = col2.text_input("Phone / Telefon", value=selected_cust.get("phone", ""))
        email = col1.text_input("Email / E-posta", value=selected_cust.get("email", ""))
        address = st.text_area("Customer Address / Müşteri Adresi", value=selected_cust.get("address", ""), height=80)
        
        st.caption("New customers are saved with the order. Edit company profiles in Company folders. / Yeni müşteriler siparişle kaydedilir.")
        
        if st.button("Next / Devam →", key="s1_next", type="primary"):
            st.session_state.quote_data["customer"] = {
                "name": company_name, "contact_person": contact_person,
                "country": country, "phone": phone, "email": email, "address": address
            }
            st.success("Müşteri bilgileri kaydedildi. Tarihler adımına geçebilirsiniz.")

    with t2:
        st.markdown("### **Quotation Tracking / Teklif Takibi**")
        valid_until_date = st.date_input("Valid Until / Geçerlilik Tarihi *", format="DD.MM.YYYY")
        
        st.markdown("### **02 Quotation Details / Teklif Bilgileri**")
        col_d1, col_d2 = st.columns(2)
        quote_number = col_d1.text_input("Quotation Number — Automatic / Teklif Numarası — Otomatik", value="QUO-2026-C2C27E56", disabled=True)
        quote_date = col_d2.date_input("Quotation Date / Teklif Tarihi *", datetime.now(), format="DD.MM.YYYY")
        delivery_date = col_d1.date_input("Requested Delivery Date / İstenen Teslim Tarihi *", format="DD.MM.YYYY")
        currency = col_d2.selectbox("Currency / Para Birimi", ["USD", "EUR", "TRY"])

        if st.button("Next / Devam →", key="s2_next", type="primary"):
            st.session_state.quote_data["dates"] = {
                "quote_number": quote_number, 
                "quote_date": quote_date.strftime("%d.%m.%Y"),
                "delivery_date": delivery_date.strftime("%d.%m.%Y"),
                "currency": currency
            }
            st.success("Tarih bilgileri kaydedildi.")

    with t3:
        st.markdown("### **Item / Ürün Kalemi**")
        col_p1, col_p2, col_p3 = st.columns([3, 1, 1])
        prod_options = {f"{p['code']} - {p['name']}": p for p in db["products"]}
        selected_p_label = col_p1.selectbox("Product / Model / Ürün *", list(prod_options.keys()))
        selected_p = prod_options[selected_p_label]
        
        qty = col_p2.number_input("Quantity / Adet *", min_value=1, value=1)
        unit_price = col_p3.number_input("Unit Price / Birim Fiyat *", min_value=0.0, value=float(selected_p["unit_price"]))
        
        col_col1, col_col2 = st.columns(2)
        prod_color = col_col1.selectbox("Product Color / Ürün Rengi *", ["Siyah / Black", "FDE / Tan", "Çöl / Desert Sand"])
        cerakote_code = col_col2.text_input("Cerakote Code / Cerakote Kodu (Optional / İsteğe Bağlı)")
        
        st.markdown("#### **Magazine Capacity & Quantity / Şarjör Kapasitesi ve Adedi**")
        cap_options = ["15 Round / 15'lik", "18 Round / 18'lik", "20 Round / 20'lik", "30 Round / 30'luk"]

        to_remove = None
        for idx, mag in enumerate(st.session_state.magazines):
            col_m1, col_m2, col_m3 = st.columns([3, 2, 0.5])
            curr_cap_idx = cap_options.index(mag["capacity"]) if mag["capacity"] in cap_options else 0
            selected_cap = col_m1.selectbox(f"Capacity / Kapasite * #{idx+1}", cap_options, index=curr_cap_idx, key=f"mag_cap_{idx}")
            selected_qty = col_m2.number_input(f"Quantity per Product / Adet * #{idx+1}", min_value=1, value=mag["qty"], key=f"mag_qty_{idx}")
            
            st.session_state.magazines[idx] = {"capacity": selected_cap, "qty": selected_qty}
            if col_m3.button("✖", key=f"del_mag_{idx}"):
                to_remove = idx

        if to_remove is not None:
            st.session_state.magazines.pop(to_remove)
            st.rerun()

        if st.button("+ Add Magazine Type / Şarjör Tipi Ekle"):
            st.session_state.magazines.append({"capacity": "15 Round / 15'lik", "qty": 1})
            st.rerun()

        if st.button("+ Add Item / Ürün Ekle", type="primary"):
            mag_summary = " + ".join([f"{m['qty']} × {m['capacity']}" for m in st.session_state.magazines])
            item_entry = {
                "product": selected_p["name"], "code": selected_p["code"],
                "quantity": qty, "unit_price": unit_price, "total": qty * unit_price,
                "color": prod_color, "cerakote": cerakote_code, "magazines": mag_summary
            }
            st.session_state.quote_data["items"].append(item_entry)
            st.success(f"✅ {selected_p['name']} eklendi!")

        if st.session_state.quote_data["items"]:
            st.table(pd.DataFrame(st.session_state.quote_data["items"]))

    with t4:
        st.markdown("### **04 Payment and Notes / Ödeme ve Açıklamalar**")
        pay_terms = st.text_area("Payment Terms / Ödeme Koşulları *", placeholder="Örn. %30 avans, %70 yükleme öncesi TT")
        quote_notes = st.text_area("Quotation Notes / Teklif Notları")
        
        if st.button("Save Quotation / Teklifi Kaydet", type="primary"):
            final_record = st.session_state.quote_data
            final_record["created_at"] = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            db["quotations"].append(final_record)
            save_db(db)
            st.balloons()
            st.success("✅ Teklif başarıyla kaydedildi!")
