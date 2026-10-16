import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime

DB_FILE = "brg_erp_db.json"
UPLOAD_DIR = "uploaded_permits"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# GERÇEK MÜŞTERİ VE MSB İHRACAT İZNİ VERİ YAPISI
INITIAL_DATA = {
    "customers": [
        {
            "id": "CUST-IRAQ-01",
            "name": "IRAK İÇİŞLERİ BAKANLIĞI",
            "country": "Iraq / Irak",
            "contact_person": "T.C. MSB KOORDİNASYON",
            "phone": "+964 770 000 0000",
            "email": "info@moi.gov.iq",
            "address": "BAGHDAD / IRAQ",
            "import_permits": [
                {
                    "id": "EUC-001",
                    "euc_no": "EUC-2026-IRAQ-88",
                    "qty": 25000,
                    "date": "10.05.2026",
                    "file_name": "EUC_IRAK_2026.pdf",
                    "file_path": os.path.join(UPLOAD_DIR, "EUC_IRAK_2026.pdf")
                }
            ],
            "export_permits": [
                {
                    "id": "EXP-001",
                    "permit_no": "E-38100341-302.04-6134334",
                    "issue_date": "13.05.2026",
                    "valid_until": "30.12.2028",
                    "file_name": "20260513 Irak İhracat İzni- BURGU (6134334).pdf",
                    "file_path": os.path.join(UPLOAD_DIR, "20260513_Irak_Ihracat_Izni.pdf"),
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
            ],
            "orders": [
                {
                    "order_no": "ORD-2026-001",
                    "date": "15.05.2026",
                    "status": "Müşteri Onayladı",
                    "proforma_no": "PI-2026-8801",
                    "work_order_no": "WO-9901",
                    "items": [
                        {"code": "BRG9-ELITE", "name": "BRG9 Elite 9x19mm", "qty": 1000, "unit_price": 450.0},
                        {"code": "BRG9-ELITE-G2", "name": "BRG9 Elite Gen 2 9x19mm", "qty": 1000, "unit_price": 480.0}
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

def save_uploaded_file(uploaded_file, prefix):
    if uploaded_file is not None:
        file_ext = uploaded_file.name.split(".")[-1]
        filename = f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{file_ext}"
        filepath = os.path.join(UPLOAD_DIR, filename)
        with open(filepath, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return filename, filepath
    return None, None

st.set_page_config(page_title="BRG DEFENCE — ERP Portal", page_icon="🛡️", layout="wide")
db = load_db()

# KURUMSAL ŞIK STİL
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #f8fafc; }
    
    .top-header {
        background: linear-gradient(90deg, #0f172a 0%, #1e293b 100%);
        color: white;
        padding: 12px 20px;
        border-radius: 8px;
        margin-bottom: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .top-title { font-size: 20px; font-weight: 700; }
    .card-box {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 14px;
        margin-bottom: 12px;
    }
    .status-ok {
        background-color: #dcfce7;
        color: #15803d;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 12px;
        display: inline-block;
    }
    .status-err {
        background-color: #fee2e2;
        color: #b91c1c;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 12px;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("""
<div class="top-header">
    <div><span style="font-size: 22px;">🛡️</span> <span class="top-title">BRG DEFENCE ERP</span></div>
    <div style="font-size:11px; text-align:right; color:#94a3b8;">SATIŞ VE İHRACAT OPERASYONLARI</div>
</div>
""", unsafe_allow_html=True)

# NAVİGASYON
c_nav1, c_nav2, c_nav3, _ = st.columns([1, 1, 1.2, 5])
with c_nav1:
    st.button("← Back / Geri")
with c_nav2:
    st.button("Forward / İleri →")
with c_nav3:
    if st.button("🏠 Home / Ana Ekran"):
        st.session_state.current_tab = "customers"
        st.rerun()

st.markdown("---")

if "current_tab" not in st.session_state:
    st.session_state.current_tab = "customers"

if "order_items" not in st.session_state:
    st.session_state.order_items = []

col_m1, _ = st.columns([2, 6])
with col_m1:
    if st.button("👥 Customers / Müşterilerimiz", type="primary", use_container_width=True):
        st.session_state.current_tab = "customers"
        st.rerun()

# ==========================================
# MÜŞTERİLERİMİZ VE 8 ENTEGRE OPERASYONEL ADIM
# ==========================================
if st.session_state.current_tab == "customers":
    st.markdown("## 👥 Customers & Permits / Müşterilerimiz ve İzin Yönetimi")
    
    if not db.get("customers"):
        db["customers"] = INITIAL_DATA["customers"]
        save_db(db)
        
    cust_names = [c["name"] for c in db["customers"]]
    selected_cust_name = st.selectbox("🎯 İşlem Yapılacak Müşteriyi Seçin:", cust_names)
    selected_cust = next(c for c in db["customers"] if c["name"] == selected_cust_name)
    
    st.markdown(f"""
    <div class="card-box">
        <h3 style="margin:0; color:#0f172a;">{selected_cust['name']} <span style="font-size:13px; color:#64748b;">({selected_cust['country']})</span></h3>
        <p style="margin:4px 0; color:#475569; font-size:12px;">
            👤 <b>Yetkili:</b> {selected_cust.get('contact_person','-')} | 📞 <b>Tel:</b> {selected_cust.get('phone','-')} | ✉️ <b>E-posta:</b> {selected_cust.get('email','-')}
        </p>
        <p style="margin:0; color:#64748b; font-size:12px;">📍 <b>Adres:</b> {selected_cust.get('address','-')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 8 ADIM ENTEGRE SEKMELER
    t1, t2, t3, t4, t5, t6, t7, t8 = st.tabs([
        "1. 🏢 Firma Bilgileri",
        "2. 📄 EUC / İthalat İzni",
        "3. 🛡️ MSB İhracat İzni",
        "4. 📦 Sipariş Yönetimi",
        "5. ✍️ Müşteri Onayı",
        "6. 📑 Proforma Oluştur",
        "7. 🏭 İş Emri (WO)",
        "8. 🚚 Sevkiyat & Düşüm"
    ])
    
    # 1. FİRMA BİLGİLERİ (DÜZENLE / SİL / YENİ EKLE)
    with t1:
        st.markdown("### 🏢 Firma Bilgileri Düzenle / Sil")
        e_name = st.text_input("Firma Unvanı", value=selected_cust["name"], key="e_name")
        e_country = st.text_input("Ülke", value=selected_cust["country"], key="e_country")
        e_contact = st.text_input("Yetkili Kişi", value=selected_cust["contact_person"], key="e_contact")
        e_phone = st.text_input("Telefon", value=selected_cust["phone"], key="e_phone")
        e_email = st.text_input("E-posta", value=selected_cust["email"], key="e_email")
        e_address = st.text_area("Adres", value=selected_cust["address"], key="e_address")
        
        b_col1, b_col2 = st.columns(2)
        if b_col1.button("💾 Firma Bilgilerini Güncelle", type="primary"):
            selected_cust["name"] = e_name
            selected_cust["country"] = e_country
            selected_cust["contact_person"] = e_contact
            selected_cust["phone"] = e_phone
            selected_cust["email"] = e_email
            selected_cust["address"] = e_address
            save_db(db)
            st.success("✅ Firma bilgileri güncellendi!")
            st.rerun()
            
        if b_col2.button("🗑️ Firmayı Sil"):
            db["customers"] = [c for c in db["customers"] if c["id"] != selected_cust["id"]]
            save_db(db)
            st.warning("Firma silindi.")
            st.rerun()

    # 2. EUC / İTHALAT İZNİ VE PDF YÖNETİMİ
    with t2:
        st.markdown("### 📄 EUC / İthalat İzinleri & PDF Evrakları")
        euc_list = selected_cust.get("import_permits", [])
        for euc in euc_list:
            st.write(f"• **EUC No:** `{euc['euc_no']}` | **Miktar:** {euc['qty']:,} Adet | **Tarih:** {euc['date']}")
            if euc.get("file_path") and os.path.exists(euc["file_path"]):
                with open(euc["file_path"], "rb") as f:
                    st.download_button(
                        label=f"📥 Taranmış EUC Belgesini İndir ({euc.get('file_name','Belge.pdf')})",
                        data=f,
                        file_name=euc.get("file_name", "EUC.pdf"),
                        key=f"down_euc_{euc['id']}"
                    )
        
        st.markdown("---")
        st.caption("➕ Yeni EUC Belgesi ve Taranmış PDF/Görsel Yükle:")
        n_euc_no = st.text_input("EUC Belge No", key="n_euc_no")
        n_euc_qty = st.number_input("İzin Verilen Adet", min_value=1, value=5000, key="n_euc_qty")
        up_euc_file = st.file_uploader("Taranmış EUC Yükle (PDF/Görsel)", type=["pdf", "png", "jpg", "jpeg"], key="up_euc")
        
        if st.button("Save EUC / Kaydet", key="btn_save_euc"):
            fname, fpath = save_uploaded_file(up_euc_file, f"EUC_{selected_cust['id']}")
            selected_cust.setdefault("import_permits", []).append({
                "id": f"EUC-{len(selected_cust.get('import_permits', []))+1:03d}",
                "euc_no": n_euc_no,
                "qty": n_euc_qty,
                "date": datetime.now().strftime("%d.%m.%Y"),
                "file_name": fname,
                "file_path": fpath
            })
            save_db(db)
            st.success("✅ EUC İzin Belgesi Yüklendi!")
            st.rerun()

    # 3. MSB İHRACAT İZNİ VE PDF YÖNETİMİ
    with t3:
        st.markdown("### 🛡️ MSB İhracat İzin Belgeleri & PDF Evrakları")
        exp_permits = selected_cust.get("export_permits", [])
        for exp in exp_permits:
            st.markdown(f"📄 **MSB İzin No:** `{exp['permit_no']}` (Son Geçerlilik: {exp['valid_until']})")
            if exp.get("file_path") and os.path.exists(exp["file_path"]):
                with open(exp["file_path"], "rb") as f:
                    st.download_button(
                        label=f"📥 Taranmış MSB İznini İndir ({exp.get('file_name','Belge.pdf')})",
                        data=f,
                        file_name=exp.get("file_name", "MSB_Izin.pdf"),
                        key=f"down_exp_{exp['id']}"
                    )
            
            p_rows = []
            for item in exp.get("items", []):
                p_rows.append({
                    "Ürün Kodu": item["code"],
                    "Ürün Adı": item["name"],
                    "Belge İzinli": f"{item['total_qty']:,} Adet",
                    "Sevk Edilen": f"{item['used_qty']:,} Adet",
                    "
