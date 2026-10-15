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
        {
            "id": "PROD-001",
            "code": "BRG9-ELITE",
            "name": "BRG9 ELITE",
            "category": "Pistol / Tabanca",
            "supply_method": "Own production / Kendi üretimimiz",
            "manufacturer": "BRG Defence",
            "supplier": "BRG Defence",
            "caliber": "9x19mm",
            "weight": "810",
            "length": "187",
            "width": "32",
            "height": "142",
            "unit_price": 450.0
        },
        {
            "id": "PROD-002",
            "code": "BRG9-ELITE-G2",
            "name": "BRG9 ELITE Gen2",
            "category": "Pistol / Tabanca",
            "supply_method": "Own production / Kendi üretimimiz",
            "manufacturer": "BRG Defence",
            "supplier": "BRG Defence",
            "caliber": "9x19mm",
            "weight": "820",
            "length": "189",
            "width": "32",
            "height": "142",
            "unit_price": 480.0
        },
        {
            "id": "PROD-003",
            "code": "BRG9-TACTICAL",
            "name": "BRG9 TACTICAL",
            "category": "Pistol / Tabanca",
            "supply_method": "Own production / Kendi üretimimiz",
            "manufacturer": "BRG Defence",
            "supplier": "BRG Defence",
            "caliber": "9x19mm",
            "weight": "850",
            "length": "205",
            "width": "34",
            "height": "148",
            "unit_price": 520.0
        },
        {
            "id": "PROD-004",
            "code": "BRG9-FD",
            "name": "BRG9 FD",
            "category": "Pistol / Tabanca",
            "supply_method": "Own production / Kendi üretimimiz",
            "manufacturer": "BRG Defence",
            "supplier": "BRG Defence",
            "caliber": "9x19mm",
            "weight": "800",
            "length": "185",
            "width": "32",
            "height": "140",
            "unit_price": 430.0
        },
        {
            "id": "PROD-005",
            "code": "BRG55",
            "name": "BRG55 Piyade Tüfeği",
            "category": "Rifle / Tüfek",
            "supply_method": "Own production / Kendi üretimimiz",
            "manufacturer": "BRG Defence",
            "supplier": "BRG Defence",
            "caliber": "5.56x45mm",
            "weight": "3200",
            "length": "840",
            "width": "65",
            "height": "205",
            "unit_price": 1200.0
        }
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

# BİREBİR FOTOĞRAFTAKİ ÖZEL CSS
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

    /* Ürün Kartı Stili */
    .product-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }
    .product-title {
        font-size: 20px;
        font-weight: 800;
        color: #0f172a;
        margin-top: 6px;
        margin-bottom: 8px;
    }
    .badge-cat {
        font-size: 11px;
        color: #0284c7;
        background-color: #e0f2fe;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: 600;
    }
    .badge-supply {
        font-size: 11px;
        color: #16a34a;
        background-color: #dcfce7;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: 600;
        float: right;
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

if "selected_prod_cat" not in st.session_state:
    st.session_state.selected_prod_cat = "All products / Tüm ürünler"

if "show_add_product_modal" not in st.session_state:
    st.session_state.show_add_product_modal = False

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

# ÜST MENÜ
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

# GEZİNTİ BAR
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
    st.markdown("<div style='text-align: right; color: #64748b; font-size: 13px; margin-top: 8px; font-weight: 500;'>Products / Ürünler</div>", unsafe_allow_html=True)

today_str = datetime.now().strftime("%d.%m.%Y")

# ==========================================
# EKRAN: ÜRÜN YÖNETİMİ VE KATALOĞU (FOTOĞRAFTAKİ BİREBİR SAYFA)
# ==========================================
if st.session_state.current_view == "products":
    st.caption("BRG DEFENCE - CATALOGUE / ÜRÜN KATALOĞU")
    
    col_p_title, col_p_btn = st.columns([4, 1])
    with col_p_title:
        st.markdown("## **Products / Ürünler**")
        st.caption("Select a category to find products and compatible spare parts. / Ürünleri ve uyumlu yedek parçaları bulmak için kategori seçin.")
    with col_p_btn:
        if st.button("+ Add Product / Ürün Ekle", type="primary", use_container_width=True):
            st.session_state.show_add_product_modal = not st.session_state.show_add_product_modal

    # Kategori Sayıları
    prods = db["products"]
    cnt_pistol = sum(1 for p in prods if "Pistol" in p["category"])
    cnt_rifle = sum(1 for p in prods if "Rifle" in p["category"] and "Spare" not in p["category"])
    cnt_p_spare = sum(1 for p in prods if "Pistol Spare" in p["category"])
    cnt_r_spare = sum(1 for p in prods if "Rifle Spare" in p["category"])
    cnt_ammo = sum(1 for p in prods if "Ammunition" in p["category"])

    # 5 Kategori Kutusu
    c1, c2, c3, c4, c5 = st.columns(5)
    if c1.button(f"Pistols / Tabancalar ({cnt_pistol})", use_container_width=True):
        st.session_state.selected_prod_cat = "Pistol / Tabanca"
    if c2.button(f"Rifles / Tüfekler ({cnt_rifle})", use_container_width=True):
        st.session_state.selected_prod_cat = "Rifle / Tüfek"
    if c3.button(f"Pistol Spare Parts ({cnt_p_spare})", use_container_width=True):
        st.session_state.selected_prod_cat = "Pistol Spare Parts / Tabanca Yedek Parçaları"
    if c4.button(f"Rifle Spare Parts ({cnt_r_spare})", use_container_width=True):
        st.session_state.selected_prod_cat = "Rifle Spare Parts / Tüfek Yedek Parçaları"
    if c5.button(f"Ammunition / Mühimmat ({cnt_ammo})", use_container_width=True):
        st.session_state.selected_prod_cat = "Ammunition / Mühimmat"

    col_filter_all, col_search_p = st.columns([1, 3])
    with col_filter_all:
        if st.button("All Products / Tüm Ürünler", type="primary" if st.session_state.selected_prod_cat == "All products / Tüm ürünler" else "secondary", use_container_width=True):
            st.session_state.selected_prod_cat = "All products / Tüm ürünler"
    with col_search_p:
        search_kw = st.text_input("Search product, code / Ürün, kod ara", placeholder="Product, code, manufacturer or compatible model / Ürün, kod...", label_visibility="collapsed")

    # ÜRÜN EKLEME FORMU (PENCERE / EXPANDER)
    if st.session_state.show_add_product_modal:
        with st.expander("➕ Add Product / Ürün Ekle Formu", expanded=True):
            st.markdown("### **Add Product / Ürün Ekle**")
            p_name = st.text_input("Product / model name / Ürün veya model adı *")
            
            f_col1, f_col2 = st.columns(2)
            p_type = f_col1.selectbox("Product type / Ürün türü *", ["Pistol / Tabanca", "Rifle / Tüfek", "Pistol Spare Parts / Tabanca Yedek Parçaları", "Rifle Spare Parts / Tüfek Yedek Parçaları", "Ammunition / Mühimmat"])
            p_supply = f_col2.selectbox("Supply method / Tedarik şekli", ["Own production / Kendi üretimimiz", "Supplier / Tedarik"])
            
            p_code = f_col1.text_input("Product code / Ürün kodu", value=f"BRG9-NEW-{len(prods)+1:02d}")
            p_mfg = f_col2.text_input("Manufacturer / Üretici", value="BRG Defence")
            p_sup = f_col1.text_input("Supplier / Tedarikçi", value="BRG Defence")
            p_price = f_col2.number_input("Unit Price ($) / Birim Fiyat", value=450.0)

            st.markdown("##### **▼ Specifications / Ürün özellikleri (optional / isteğe bağlı)**")
            s1, s2 = st.columns(2)
            p_caliber = s1.text_input("Caliber / Kalibre", value="9x19mm")
            p_weight = s2.text_input("Weight (g) / Ağırlık (g)", value="820")
            p_length = s1.text_input("Overall length (mm) / Toplam uzunluk (mm)", value="187")
            p_width = s2.text_input("Width (mm) / Genişlik (mm)", value="32")
            p_height = s1.text_input("Height (mm) / Yükseklik (mm)", value="142")

            if st.button("Save Product / Ürünü Kaydet", type="primary"):
                new_prod_item = {
                    "id": f"PROD-{len(prods)+1:03d}",
                    "code": p_code,
                    "name": p_name if p_name else "Yeni Model",
                    "category": p_type,
                    "supply_method": p_supply,
                    "manufacturer": p_mfg,
                    "supplier": p_sup,
                    "caliber": p_caliber,
                    "weight": p_weight,
                    "length": p_length,
                    "width": p_width,
                    "height": p_height,
                    "unit_price": p_price
                }
                db["products"].append(new_prod_item)
                save_db(db)
                st.success("✅ Ürün başarıyla eklendi!")
                st.session_state.show_add_product_modal = False
                st.rerun()

    st.markdown("---")

    # Ürünleri Filtrele
    filtered_prods = db["products"]
    if st.session_state.selected_prod_cat != "All products / Tüm ürünler":
        filtered_prods = [p for p in filtered_prods if st.session_state.selected_prod_cat.split(" / ")[0] in p["category"]]
    
    if search_kw:
        filtered_prods = [p for p in filtered_prods if search_kw.lower() in p["name"].lower() or search_kw.lower() in p["code"].lower()]

    st.caption(f"{len(filtered_prods)} products / Ürün gösteriliyor")

    # GRID KART DİZİLİMİ (4'lü Sütunlar)
    cols = st.columns(4)
    for idx, p in enumerate(filtered_prods):
        with cols[idx % 4]:
            st.markdown(f"""
            <div class="product-card">
                <span class="badge-cat">{p.get('category', 'Pistol')}</span>
                <span class="badge-supply">{p.get('supply_method', 'Kendi Üretimimiz').split(' / ')[0]}</span>
                <div class="product-title">{p.get('name', 'Ürün')}</div>
                <div style="font-size: 12px; color: #64748b; margin-bottom: 8px;">Kod: {p.get('code', '-')} | Fiyat: <b>${p.get('unit_price', 0)}</b></div>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("▶ Details / Özellikler"):
                st.write(f"**Kalibre:** {p.get('caliber', '-')}")
                st.write(f"**Ağırlık:** {p.get('weight', '-')} g")
                st.write(f"**Boyutlar (L/W/H):** {p.get('length', '-')} x {p.get('width', '-')} x {p.get('height', '-')} mm")
                st.write(f"**Üretici:** {p.get('manufacturer', 'BRG Defence')}")

            btn_e, btn_r = st.columns(2)
            btn_e.button("Edit / Düzenle", key=f"edit_p_{p['id']}")
            if btn_r.button("Remove / Çıkar", key=f"del_p_{p['id']}"):
                db["products"] = [item for item in db["products"] if item["id"] != p["id"]]
                save_db(db)
                st.success(f"{p['name']} silindi.")
                st.rerun()

# ==========================================
# EKRAN 1: ANA DASHBOARD
# ==========================================
elif st.session_state.current_view == "dashboard":
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
# DİĞER EKRANLAR (COMPANY, SEARCH, TOOLS, ADD_COMPANY, FORM)
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

elif st.session_state.current_view == "search":
    st.markdown("## 🔍 Search & Filters / Arama ve Filtreleme")
    st.text_input("Search query / Arama terimi girin")

elif st.session_state.current_view == "tools":
    st.markdown("## ▶ Sales Tools / Satış Araçları")
    val = st.number_input("Amount in USD ($) / Tutar", value=1000.0)
    st.success(f"TRY Equivalent / TL Karşılığı: {val * 34.5:.2f} ₺")

elif st.session_state.current_view == "add_company":
    st.markdown("## ➕ Add New Company / Yeni Firma Ekle")
    new_name = st.text_input("Company Name / Firma Adı *")
    new_country = st.text_input("Country / Ülke *")
    if st.button("Save Company / Firmayı Kaydet", type="primary"):
        db["customers"].append({
            "id": f"CUST-{len(db['customers'])+1:03d}",
            "name": new_name, "country": new_country, "quotations_count": 0, "open_orders": 0, "in_production": 0
        })
        save_db(db)
        st.success("✅ Firma eklendi!")
        st.session_state.current_view = "dashboard"
        st.rerun()

elif st.session_state.current_view == "form":
    st.caption("🔴 Unsaved Changes / Kaydedilmemiş Değişiklikler")
    t1, t2, t3, t4 = st.tabs(["1️⃣ Customer / Müşteri", "2️⃣ Dates / Tarihler", "3️⃣ Products / Ürünler", "4️⃣ Payment & Save / Ödeme ve Kayıt"])

    with t1:
        st.markdown("### **01 Customer Details / Müşteri Bilgileri**")
        cust_options = {f"{c.get('name', 'Firma')} — {c.get('country', '')}": c for c in db["customers"]}
        selected_cust_label = st.selectbox("Saved Customers / Kayıtlı Müşteriler", list(cust_options.keys()))
        selected_cust = cust_options[selected_cust_label]
        
        company_name = st.text_input("Company or Customer / Firma veya Müşteri Adı *", value=selected_cust.get("name", ""))
        contact_person = st.text_input("Contact Person / Yetkili Kişi", value=selected_cust.get("contact_person", ""))
        country = st.selectbox("Country / Ülke *", ["Georgia / Gürcistan", "Iraq / Irak", "Azerbaijan / Azerbaycan", "Turkey / Türkiye"], index=0)
        phone = st.text_input("Phone / Telefon", value=selected_cust.get("phone", ""))
        email = st.text_input("Email / E-posta", value=selected_cust.get("email", ""))
        address = st.text_area("Customer Address / Müşteri Adresi", value=selected_cust.get("address", ""), height=80)
        
        if st.button("Next / Devam →", key="s1_next", type="primary"):
            st.session_state.quote_data["customer"] = {"name": company_name, "country": country, "phone": phone}
            st.success("Müşteri kaydedildi.")

    with t2:
        st.markdown("### **02 Quotation Details / Teklif Bilgileri**")
        quote_number = st.text_input("Quotation Number", value="QUO-2026-C2C27E56", disabled=True)
        quote_date = st.date_input("Quotation Date *", datetime.now(), format="DD.MM.YYYY")
        delivery_date = st.date_input("Requested Delivery Date *", format="DD.MM.YYYY")
        currency = st.selectbox("Currency / Para Birimi", ["USD", "EUR", "TRY"])
        if st.button("Next / Devam →", key="s2_next", type="primary"):
            st.session_state.quote_data["dates"] = {"quote_number": quote_number, "currency": currency}
            st.success("Tarihler kaydedildi.")

    with t3:
        st.markdown("### **Item / Ürün Kalemi & Çoklu Şarjör Seçimi**")
        prod_options = {f"{p['code']} - {p['name']}": p for p in db["products"]}
        selected_p_label = st.selectbox("Product / Model / Ürün *", list(prod_options.keys()))
        selected_p = prod_options[selected_p_label]
        
        qty = st.number_input("Quantity / Adet *", min_value=1, value=1)
        unit_price = st.number_input("Unit Price / Birim Fiyat *", min_value=0.0, value=float(selected_p["unit_price"]))
        prod_color = st.selectbox("Product Color / Ürün Rengi *", ["Siyah / Black", "FDE / Tan", "Çöl / Desert Sand"])
        
        st.markdown("#### **Magazine capacity & quantity / Şarjör kapasitesi ve adedi**")
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
                "color": prod_color, "magazines": mag_summary
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
            st.success("✅ Teklif kaydedildi!")
