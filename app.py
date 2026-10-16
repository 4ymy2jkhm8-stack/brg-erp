import streamlit as st
import json
import os
import base64
from datetime import datetime

DB_FILE = "brg_erp_db.json"
UPLOAD_DIR = "uploaded_permits"

# Dosya Yükleme Klasörü Kontrolü
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

INITIAL_DATA = {
    "customers": [
        {
            "id": "CUST-001",
            "name": "KAVIANI 2015",
            "country": "Georgia / Gürcistan",
            "contact_person": "ROMA",
            "phone": "+995 599351351",
            "email": "fatih@brgdefence.com",
            "address": "BATUMI, BAGRATIONI 157A",
            "import_permits": [],
            "export_permits": []
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

# 1. EN ÜST KURUMSAL HEADER
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

# 2. STANDART GEZİNTİ BUTONLARI (BACK / FORWARD / HOME)
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

# 3. İLK MODÜLÜMÜZ: MÜŞTERİLERİMİZ (CUSTOMERS)
if "current_tab" not in st.session_state:
    st.session_state.current_tab = "customers"

col_m1, _ = st.columns([2, 6])
with col_m1:
    if st.button("👥 Customers / Müşterilerimiz", type="primary", use_container_width=True):
        st.session_state.current_tab = "customers"
        st.rerun()

# ==========================================
# MODÜL 1: MÜŞTERİ BİLGİLERİ & BELGE YÜKLEME
# ==========================================
if st.session_state.current_tab == "customers":
    st.markdown("## 👥 Customers & Licenses / Müşteri Bilgileri ve İzinler")
    
    tab_list, tab_add = st.tabs(["📋 Customer List / Müşteri Listesi", "➕ Add Customer / Yeni Müşteri Ekle"])
    
    # MÜŞTERİ LİSTESİ VE TARANMIŞ İZİN BELGELERİ
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
                
                exp1, exp2 = st.columns(2)
                
                # EUC / İTHALAT İZNİ EKLE VE TARANMIŞ DOSYA YÜKLE
                with exp1.expander("📄 EUC / Import Permits / İthalat İzinleri"):
                    euc_list = cust.get("import_permits", [])
                    if euc_list:
                        for e in euc_list:
                            st.write(f"• **{e['euc_no']}** — {e['qty']} Adet / Pcs ({e['date']})")
                            if e.get("file_path") and os.path.exists(e["file_path"]):
                                with open(e["file_path"], "rb") as f:
                                    st.download_button(
                                        label=f"📥 Taranmış Evrak İndir ({e['file_name']})",
                                        data=f,
                                        file_name=e["file_name"],
                                        key=f"down_euc_{e['euc_no']}"
                                    )
                    else:
                        st.info("Kayıtlı ithalat izni bulunmuyor.")
                    
                    st.markdown("---")
                    st.caption("➕ Add EUC & Upload Scan / İthalat İzni ve Taranmış Evrak Ekle")
                    new_euc_no = st.text_input("EUC / Permit No", key=f"euc_no_{cust['id']}")
                    new_euc_qty = st.number_input("Allowed Qty / Miktar (Adet)", min_value=1, value=500, key=f"euc_qty_{cust['id']}")
                    euc_file = st.file_uploader("Upload Scanned EUC (PDF/Image) / Taranmış İzin Belgesi Yükle", type=["pdf", "png", "jpg", "jpeg", "webp"], key=f"euc_file_{cust['id']}")
                    
                    if st.button("Save EUC / İzni Kaydet", key=f"btn_euc_{cust['id']}"):
                        fname, fpath = save_uploaded_file(euc_file, f"EUC_{cust['id']}")
                        if "import_permits" not in cust:
                            cust["import_permits"] = []
                        cust["import_permits"].append({
                            "euc_no": new_euc_no,
                            "qty": new_euc_qty,
                            "date": datetime.now().strftime("%d.%m.%Y"),
                            "file_name": fname,
                            "file_path": fpath
                        })
                        save_db(db)
                        st.success("EUC Belgesi ve Taranmış Evrak Kaydedildi!")
                        st.rerun()

                # İHRACAT İZNİ (MSB) EKLE VE TARANMIŞ DOSYA YÜKLE
                with exp2.expander("🛡️ Export Permits / İhracat İzinleri (MSB)"):
                    exp_list = cust.get("export_permits", [])
                    if exp_list:
                        for ex in exp_list:
                            st.write(f"• **{ex['permit_no']}** — {ex['qty']} Adet / Pcs (Son Tarih: {ex['valid_until']})")
                            if ex.get("file_path") and os.path.exists(ex["file_path"]):
                                with open(ex["file_path"], "rb") as f:
                                    st.download_button(
                                        label=f"📥 Taranmış Evrak İndir ({ex['file_name']})",
                                        data=f,
                                        file_name=ex["file_name"],
                                        key=f"down_exp_{ex['permit_no']}"
                                    )
                    else:
                        st.info("Kayıtlı ihracat izni bulunmuyor.")
                    
                    st.markdown("---")
                    st.caption("➕ Add Export Permit & Upload Scan / İhracat İzni ve Taranmış Evrak Ekle")
                    new_exp_no = st.text_input("MSB License No / İzin No", key=f"exp_no_{cust['id']}")
                    new_exp_qty = st.number_input("Approved Qty / Onaylanan Miktar", min_value=1, value=500, key=f"exp_qty_{cust['id']}")
                    new_exp_date = st.date_input("Valid Until / Geçerlilik Tarihi", format="DD.MM.YYYY", key=f"exp_date_{cust['id']}")
                    exp_file = st.file_uploader("Upload Scanned Permit (PDF/Image) / Taranmış İzin Belgesi Yükle", type=["pdf", "png", "jpg", "jpeg", "webp"], key=f"exp_file_{cust['id']}")
                    
                    if st.button("Save Export Permit / İhracat İznini Kaydet", key=f"btn_exp_{cust['id']}"):
                        fname, fpath = save_uploaded_file(exp_file, f"MSB_{cust['id']}")
                        if "export_permits" not in cust:
                            cust["export_permits"] = []
                        cust["export_permits"].append({
                            "permit_no": new_exp_no,
                            "qty": new_exp_qty,
                            "valid_until": new_exp_date.strftime("%d.%m.%Y"),
                            "file_name": fname,
                            "file_path": fpath
                        })
                        save_db(db)
                        st.success("İhracat İzni ve Taranmış Evrak Kaydedildi!")
                        st.rerun()

    # YENİ MÜŞTERİ EKLEME FORMU
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
