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
            "country": "Georgia", 
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

st.set_page_config(page_title="BRG Defence — Sales Operations", page_icon="🛡️", layout="wide")
db = load_db()

# BİREBİR FOTOĞRAFTAKİ ÖZEL CSS
st.markdown("""
<style>
    /* Genel Arka Plan ve Yazı Tipi */
    .stApp {
        background-color: #eef2f6;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* En Üst Lacivert Header */
    .main-header {
        background-color: #0d2847;
        color: #ffffff;
        padding: 18px 30px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-radius: 2px;
    }
    .main-title {
        font-size: 24px;
        font-weight: 800;
        letter-spacing: 1.5px;
    }
    .main-sub {
        font-size: 10px;
        color: #a0aec0;
        text-align: right;
        line-height: 1.3;
    }

    /* Üst Menü Çubuğu */
    .top-menu-bar {
        background-color: #e2e8f0;
        padding: 8px 16px;
        border-radius: 8px;
        margin-top: 12px;
        margin-bottom: 12px;
    }

    /* Sarı Uyarı Kutusu */
    .alert-box {
        background-color: #fef3c7;
        border: 1px solid #fde68a;
        border-radius: 6px;
        padding: 12px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 15px;
        margin-bottom: 20px;
    }
    .alert-text {
        color: #92400e;
        font-weight: 600;
        font-size: 14px;
    }

    /* KPI Sayaç Kutuları */
    .kpi-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 16px 20px;
        display: flex;
        align-items: center;
        gap: 15px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }
    .kpi-num {
        font-size: 32px;
        font-weight: 700;
        color: #1e293b;
    }
    .kpi-desc {
        font-size: 13px;
        color: #64748b;
    }

    /* Müşteri Kartı */
    .cust-card {
        background-color: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        padding: 18px 24px;
        margin-top: 15px;
    }
    .avatar-box {
        background-color: #0f172a;
        color: #ffffff;
        width: 44px;
        height: 44px;
        border-radius: 6px;
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

# 1. EN ÜST HEADER
st.markdown("""
<div class="main-header">
    <div style="display: flex; align-items: center; gap: 12px;">
        <span style="font-size: 28px;">🛡️</span>
        <span class="main-title">BRG DEFENCE</span>
    </div>
    <div class="main-sub">
        SALES OPERATIONS<br><b>SATIŞ YÖNETİMİ</b>
    </div>
</div>
""", unsafe_allow_html=True)

# 2. ÜST MENÜ BUTONLARI (Fotoğraftaki Birebir Dizilim)
m1, m2, m3, m4, m5 = st.columns([2, 1.5, 2.5, 2, 1.5])
with m1:
    if st.button("👥 Customers / Müşterilerimiz", type="primary", use_container_width=True):
        st.session_state.current_view = "dashboard"
        st.rerun()
with m2:
    st.button("🔍 Search / Ara", use_container_width=True)
with m3:
    st.button("🏢 Our company / Firma bilgilerimiz", use_container_width=True)
with m4:
    st.button("📦 Products / Ürünler", use_container_width=True)
with m5:
    st.button("▶ Tools / Araçlar", use_container_width=True)

# 3. ALT GEZİNTİ VE RESUME FORM BAR
nav_1, nav_2, nav_3, nav_4, nav_right = st.columns([1, 1, 1.3, 1.8, 2.5])
with nav_1:
    st.button("← Back / Geri")
with nav_2:
    st.button("Forward / İleri →")
with nav_3:
    if st.button("🏠 Home / Ana ekran"):
        st.session_state.current_view = "dashboard"
        st.rerun()
with nav_4:
    if st.button("Resume form / Formuma dön", type="primary"):
        st.session_state.current_view = "form"
        st.rerun()
with nav_right:
    st.markdown("<div style='text-align: right; color: #64748b; font-size: 13px; margin-top: 8px;'>Home / Ana ekran</div>", unsafe_allow_html=True)

# ==========================================
# EKRAN 1: ANA PORTAL (FOTOĞRAFINIZIN BİREBİR KOPYASI)
# ==========================================
if st.session_state.current_view == "dashboard":
    st.caption("Records are saved in this browser / Kayıtlar bu tarayıcıda saklanır.")

    # Sarı Uyarı Kutusu
    c_alert_text, c_alert_btn = st.columns([4, 1])
    with c_alert_text:
        st.markdown("""
        <div class="alert-box">
            <span class="alert-text">1 checks need attention / 1 kontrol bekliyor</span>
        </div>
        """, unsafe_allow_html=True)
    with c_alert_btn:
        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
        st.button("Review / Kontrol et →", type="primary", use_container_width=True)

    # Başlık Alanı
    st.caption("BRG DEFENCE - 15.10.2026")
    head_left, head_right = st.columns([4, 1])
    with head_left:
        st.markdown("## **Customers** <span style='font-size: 16px; color: #64748b; font-weight: normal;'>Müşterilerimiz</span>", unsafe_allow_html=True)
        st.caption("Select a company to continue. / İşlem yapmak için bir firma seçin.")
    with head_right:
        st.button("+ Add company / Firma ekle", type="primary", use_container_width=True)

    # 3'lü İstatistik Sayaç Kutuları
    k1, k2, k3 = st.columns(3)
    with k1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-num">{len(db['customers'])}</div>
            <div class="kpi-desc">Companies / Müşteri firması</div>
        </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-num">2</div>
            <div class="kpi-desc">Open orders / Açık sipariş</div>
        </div>
        """, unsafe_allow_html=True)
    with k3:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-num">1</div>
            <div class="kpi-desc">Needs attention → / Kontrol bekleyen</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("Search companies / Firma ara")
    st.text_input("Search companies input", placeholder="Company or country / Firma adı veya ülke", label_visibility="collapsed")

    # Müşteri Kartı Listeleme (KA | KAVIANI 2015)
    for cust in db["customers"]:
        avatar_text = cust["name"][:2].upper()
        
        st.markdown(f"""
        <div class="cust-card">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div style="display: flex; align-items: center; gap: 15px;">
                    <div class="avatar-box">{avatar_text}</div>
                    <div>
                        <div style="font-size: 18px; font-weight: 700; color: #0f172a;">{cust['name']}</div>
                        <div style="font-size: 13px; color: #64748b;">{cust['country']}</div>
                    </div>
                </div>
                <div style="font-size: 20px; color: #64748b;">→</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        c_q, c_o, c_p, c_action = st.columns([1, 1, 1, 1])
        c_q.caption(f"<b>{cust['quotations_count']}</b> Quotations / Açık teklif")
        c_o.caption(f"<b>{cust['open_orders']}</b> Orders / Açık sipariş")
        c_p.caption(f"<b>{cust['in_production']}</b> Production / Üretimde")
        if c_action.button("Forma Geç / Sipariş Oluştur", key=f"open_form_{cust['id']}"):
            st.session_state.current_view = "form"
            st.rerun()

# ==========================================
# EKRAN 2: SİPARİŞ / TEKLİF FORMU (RESUME FORM)
# ==========================================
elif st.session_state.current_view == "form":
    st.caption("🔴 Unsaved changes / Kaydedilmemiş değişiklikler")
    
    t1, t2, t3, t4 = st.tabs([
        "1️⃣ Customer / Müşteri", 
        "2️⃣ Dates / Tarihler", 
        "3️⃣ Products / Ürünler", 
        "4️⃣ Payment & save / Ödeme ve kayıt"
    ])

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
        
        country_options = ["Georgia / Gürcistan", "Iraq / Irak", "Azerbaijan / Azerbaycan", "Turkey / Türkiye"]
        country = col1.selectbox("Country / Ülke *", country_options, index=0)
        phone = col2.text_input("Phone / Telefon", value=selected_cust.get("phone", ""))
        email = col1.text_input("Email / E-posta", value=selected_cust.get("email", ""))
        address = st.text_area("Customer address / Müşteri adresi", value=selected_cust.get("address", ""), height=80)
        
        st.caption("New customers are saved with the order. Edit company profiles in Company folders.")
        
        if st.button("Next / Devam →", key="s1_next", type="primary"):
            st.session_state.quote_data["customer"] = {
                "name": company_name, "contact_person": contact_person,
                "country": country, "phone": phone, "email": email, "address": address
            }
            st.success("Müşteri bilgileri kaydedildi.")

    with t2:
        st.markdown("### **Quotation tracking / Teklif takibi**")
        valid_until = st.date_input("Valid until / Geçerlilik tarihi *")
        
        st.markdown("### **02 Quotation details / Teklif bilgileri**")
        col_d1, col_d2 = st.columns(2)
        quote_number = col_d1.text_input("Quotation number — automatic", value="QUO-2026-C2C27E56", disabled=True)
        quote_date = col_d2.date_input("Quotation date *", datetime.now())
        delivery_date = col_d1.date_input("Requested delivery date *")
        currency = col_d2.selectbox("Currency", ["USD", "EUR", "TRY"])

        if st.button("Next / Devam →", key="s2_next", type="primary"):
            st.session_state.quote_data["dates"] = {"quote_number": quote_number, "currency": currency}
            st.success("Tarihler kaydedildi.")

    with t3:
        st.markdown("### **Item / Ürün Kalemi**")
        col_p1, col_p2, col_p3 = st.columns([3, 1, 1])
        prod_options = {f"{p['code']} - {p['name']}": p for p in db["products"]}
        selected_p_label = col_p1.selectbox("Product / Model / Ürün *", list(prod_options.keys()))
        selected_p = prod_options[selected_p_label]
        
        qty = col_p2.number_input("Quantity / Adet *", min_value=1, value=1)
        unit_price = col_p3.number_input("Unit price / Birim fiyat *", min_value=0.0, value=float(selected_p["unit_price"]))
        
        col_col1, col_col2 = st.columns(2)
        prod_color = col_col1.selectbox("Product color / Ürün rengi *", ["Siyah / Black", "FDE / Tan", "Çöl / Desert Sand"])
        cerakote_code = col_col2.text_input("Cerakote code / Cerakote kodu (optional / isteğe bağlı)")
        
        st.markdown("#### **Magazine capacity & quantity / Şarjör kapasitesi ve adedi**")
        cap_options = ["15 Round / 15'lik", "18 Round / 18'lik", "20 Round / 20'lik", "30 Round / 30'luk"]

        to_remove = None
        for idx, mag in enumerate(st.session_state.magazines):
            col_m1, col_m2, col_m3 = st.columns([3, 2, 0.5])
            curr_cap_idx = cap_options.index(mag["capacity"]) if mag["capacity"] in cap_options else 0
            selected_cap = col_m1.selectbox(f"Capacity * #{idx+1}", cap_options, index=curr_cap_idx, key=f"mag_cap_{idx}")
            selected_qty = col_m2.number_input(f"Quantity per product * #{idx+1}", min_value=1, value=mag["qty"], key=f"mag_qty_{idx}")
            
            st.session_state.magazines[idx] = {"capacity": selected_cap, "qty": selected_qty}
            if col_m3.button("✖", key=f"del_mag_{idx}"):
                to_remove = idx

        if to_remove is not None:
            st.session_state.magazines.pop(to_remove)
            st.rerun()

        if st.button("+ Add magazine type / Şarjör tipi ekle"):
            st.session_state.magazines.append({"capacity": "15 Round / 15'lik", "qty": 1})
            st.rerun()

        if st.button("+ Add item / Ürün ekle", type="primary"):
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
        st.markdown("### **04 Payment and notes / Ödeme ve açıklamalar**")
        pay_terms = st.text_area("Payment terms / Ödeme koşulları *")
        quote_notes = st.text_area("Quotation notes / Teklif notları")
        
        if st.button("Save quotation / Teklifi kaydet", type="primary"):
            final_record = st.session_state.quote_data
            final_record["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            db["quotations"].append(final_record)
            save_db(db)
            st.balloons()
            st.success("✅ Teklif başarıyla kaydedildi!")
