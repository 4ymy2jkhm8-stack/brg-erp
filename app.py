import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime

DB_FILE = "brg_erp_db.json"
UPLOAD_DIR = "uploaded_permits"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# GERÇEK BELGENİZDEKİ HER ÜRÜN VE APAYRI ADETLERİ
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
                        {"code": "BRG9-ELITE", "name": "BRG9 Elite 9x19mm Semi Automatic Pistol", "total_qty": 3300, "used_qty": 0},
                        {"code": "BRG9-ELITE-G2", "name": "BRG9 Elite Gen 2 9x19mm Semi Automatic Pistol", "total_qty": 5000, "used_qty": 0},
                        {"code": "BRG9-TACTICAL", "name": "BRG9 Tactical 9x19mm Semi Automatic Pistol", "total_qty": 2750, "used_qty": 0},
                        {"code": "BRG9-FD", "name": "BRG9 FD 9x19mm Semi Automatic Pistol", "total_qty": 5000, "used_qty": 0},
                        {"code": "BRG9-FDX", "name": "BRG9 FDX 9x19mm Semi Automatic Pistol", "total_qty": 5000, "used_qty": 0},
                        {"code": "BRG55", "name": "BRG55 5.56x45mm Full Automatic Rifle", "total_qty": 5000, "used_qty": 0},
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

# KURUMSAL TASARIM
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #f8fafc; }
    
    .top-header {
        background: linear-gradient(90deg, #0f172a 0%, #1e293b 100%);
        color: white;
        padding: 16px 24px;
        border-radius: 8px;
        margin-bottom: 16px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .top-title { font-size: 22px; font-weight: 700; letter-spacing: 1px; }
    .top-sub { font-size: 11px; color: #94a3b8; text-align: right; }
    
    .card-box {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
</style>
""", unsafe_allow_html=True)

# 1. EN ÜST HEADER
st.markdown("""
<div class="top-header">
    <div>
        <span style="font-size: 24px;">🛡️</span>
        <span class="top-title">BRG DEFENCE</span>
    </div>
    <div class="top-sub">
        SALES OPERATIONS & ERP<br><b>SATIŞ VE OPERASYON YÖNETİMİ</b>
    </div>
</div>
""", unsafe_allow_html=True)

# 2. NAVİGASYON BUTONLARI
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

col_m1, _ = st.columns([2, 6])
with col_m1:
    if st.button("👥 Customers / Müşterilerimiz", type="primary", use_container_width=True):
        st.session_state.current_tab = "customers"
        st.rerun()

# ==========================================
# MÜŞTERİLER VE HER BİRİ AYRI ADETLİ İZİNLER
# ==========================================
if st.session_state.current_tab == "customers":
    st.markdown("## 👥 Customers & MSB Export Permits / Müşteri Bilgileri ve İhracat İzinleri")
    
    tab_list, tab_add = st.tabs(["📋 Customer List & Permits / Müşteri Listesi ve İzinler", "➕ Add Customer / Yeni Müşteri Ekle"])
    
    with tab_list:
        for cust in db["customers"]:
            with st.container():
                st.markdown(f"""
                <div class="card-box">
                    <h3 style="margin:0; color:#0f172a;">{cust['name']} <span style="font-size:14px; color:#64748b;">({cust['country']})</span></h3>
                    <p style="margin:4px 0; color:#475569; font-size:13px;">
                        👤 <b>Yetkili:</b> {cust.get('contact_person','-')} | 📞 <b>Tel:</b> {cust.get('phone','-')} | ✉️ <b>E-posta:</b> {cust.get('email','-')}
                    </p>
                    <p style="margin:0; color:#64748b; font-size:12px;">📍 <b>Adres:</b> {cust.get('address','-')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                exp_permits = cust.get("export_permits", [])
                st.markdown(f"#### 🛡️ Registered MSB Permits / Kayıtlı MSB İhracat İzinleri ({len(exp_permits)} Adet Belge)")
                
                for p_idx, permit in enumerate(exp_permits):
                    exp_title = f"📄 MSB İzin No: {permit['permit_no']} — (Son Geçerlilik: {permit['valid_until']})"
                    with st.expander(exp_title, expanded=True):
                        st.caption(f"İzin Tarihi: {permit.get('issue_date', '-')} | Son Geçerlilik Tarihi: {permit['valid_until']}")
                        
                        # HER ÜRÜNÜN ADEDİ VE KALAN KOTASI
                        item_rows = []
                        for it in permit.get("items", []):
                            rem = it['total_qty'] - it['used_qty']
                            item_rows.append({
                                "Ürün / Model Adı": it['name'],
                                "Ürün Kodu": it['code'],
                                "İzin Verilen Miktar": f"{it['total_qty']:,} Adet",
                                "Sevk Edilen Miktar": f"{it['used_qty']:,} Adet",
                                "Kalan İzin Kotası": f"{rem:,} Adet"
                            })
                        st.table(pd.DataFrame(item_rows))
                        
                        # SEVKİYAT EKSİLTME İŞLEMİ
                        st.markdown("##### 🚚 Sevkiyat Çıkışı / Kota Eksiltme")
                        sim_c1, sim_c2, sim_c3 = st.columns([2.5, 1, 1])
                        
                        item_options = {f"{it['name']} (Kalan Kota: {it['total_qty'] - it['used_qty']:,} Adet)": it for it in permit.get("items", [])}
                        selected_item_label = sim_c1.selectbox("Sevk Edilecek Ürünü Seçin", list(item_options.keys()), key=f"sel_it_{p_idx}")
                        selected_item = item_options[selected_item_label]
                        
                        ship_qty = sim_c2.number_input("Sevk Adedi", min_value=1, value=100, key=f"ship_qty_{p_idx}")
                        
                        if sim_c3.button("Sevkiyatı Düş / Eksilt", type="primary", key=f"btn_ship_{p_idx}"):
                            if selected_item["used_qty"] + ship_qty <= selected_item["total_qty"]:
                                selected_item["used_qty"] += ship_qty
                                save_db(db)
                                st.success(f"✅ {ship_qty} adet '{selected_item['name']}' sevk edildi. Kalan Kota: {selected_item['total_qty'] - selected_item['used_qty']:,} adet.")
                                st.rerun()
                            else:
                                st.error(f"❌ İzin kotası aşılamaz! Bu ürün için kalan maksimum miktar: {selected_item['total_qty'] - selected_item['used_qty']:,} adet.")

                # YENİ İZİN BELGESİ EKLEME
                with st.expander("➕ Add New MSB Export Permit / Yeni MSB İhracat İzni Ekle"):
                    new_exp_no = st.text_input("MSB License / Decision No (Sayı) *", placeholder="E-38100341-302.04-...", key=f"new_p_no_{cust['id']}")
                    new_exp_date = st.date_input("Valid Until / Son Geçerlilik Tarihi *", format="DD.MM.YYYY", key=f"new_p_date_{cust['id']}")
                    exp_file = st.file_uploader("Upload Scanned MSB Document (PDF/Image)", type=["pdf", "png", "jpg", "jpeg"], key=f"new_p_file_{cust['id']}")
                    
                    st.caption("İzin Belgesindeki Kalem ve Adet Bilgisi:")
                    p_item_code = st.text_input("Product Code / Ürün Kodu (Örn: BRG9-ELITE)", key=f"p_ic_{cust['id']}")
                    p_item_name = st.text_input("Product Name / Ürün Adı (Örn: BRG9 Elite 9x19mm)", key=f"p_in_{cust['id']}")
                    p_item_qty = st.number_input("Allowed Total Quantity / İzin Verilen Miktar (Adet)", min_value=1, value=1000, key=f"p_iq_{cust['id']}")
                    
                    if st.button("Save New Permit / Yeni İzni Kaydet", key=f"btn_save_p_{cust['id']}"):
                        fname, fpath = save_uploaded_file(exp_file, f"MSB_{cust['id']}")
                        new_permit_data = {
                            "permit_no": new_exp_no,
                            "issue_date": datetime.now().strftime("%d.%m.%Y"),
                            "valid_until": new_exp_date.strftime("%d.%m.%Y"),
                            "file_name": fname,
                            "file_path": fpath,
                            "items": [
                                {"code": p_item_code, "name": p_item_name, "total_qty": p_item_qty, "used_qty": 0}
                            ]
                        }
                        cust["export_permits"].append(new_permit_data)
                        save_db(db)
                        st.success("✅ Yeni MSB İzin Belgesi sisteme eklendi!")
                        st.rerun()

    with tab_add:
        st.markdown("### ➕ New Customer Registration / Yeni Müşteri Kaydı")
        c_col1, c_col2 = st.columns(2)
        c_name = c_col1.text_input("Company or Customer / Firma veya Müşteri Adı *")
        c_country = c_col2.text_input("Country / Ülke *", value="Georgia / Gürcistan")
        c_contact = c_col1.text_input("Contact Person / Yetkili Kişi")
        c_phone = c_col2.text_input("Phone / Telefon")
        c_email = c_col1.text_input("Email / E-posta")
        c_address = st.text_area("Customer Address / Müşteri Adresi")
        
        if st.button("Save Customer / Müşteriyi Kaydet", type="primary"):
            new_cust_data = {
                "id": f"CUST-{len(db['customers'])+1:03d}",
                "name": c_name,
                "country": c_country,
                "contact_person": c_contact,
                "phone": c_phone,
                "email": c_email,
                "address": c_address,
                "import_permits": [],
                "export_permits": []
            }
            db["customers"].append(new_cust_data)
            save_db(db)
            st.success("✅ Müşteri başarıyla kaydedildi!")
            st.rerun()
