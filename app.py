import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime

DB_FILE = "brg_erp_db.json"
UPLOAD_DIR = "uploaded_permits"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# MSB İHRACAT İZNİ GERÇEK VERİLERİ
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

st.set_page_config(page_title="BRG DEFENCE — ERP Portal", page_icon="🛡️", layout="wide")
db = load_db()

# KOMPAKT VE ŞIK TASARIM CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #f8fafc; }
    
    .top-header {
        background: linear-gradient(90deg, #0f172a 0%, #1e293b 100%);
        color: white;
        padding: 10px 18px;
        border-radius: 8px;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .top-title { font-size: 18px; font-weight: 700; }
    .card-box {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
    }
    .status-ok {
        background-color: #dcfce7;
        color: #15803d;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 12px;
        display: inline-block;
        margin-top: 8px;
    }
    .status-err {
        background-color: #fee2e2;
        color: #b91c1c;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 12px;
        display: inline-block;
        margin-top: 8px;
    }
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("""
<div class="top-header">
    <div><span style="font-size: 20px;">🛡️</span> <span class="top-title">BRG DEFENCE</span></div>
    <div style="font-size:11px; text-align:right; color:#94a3b8;">SALES OPERATIONS & ERP</div>
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
# MÜŞTERİ DÜĞMESİNE BASILDIĞINDA ÇALIŞAN EKRAN
# ==========================================
if st.session_state.current_tab == "customers":
    st.markdown("## 👥 Customers & Permits / Müşterilerimiz ve İzin Yönetimi")
    
    if not db.get("customers"):
        db["customers"] = INITIAL_DATA["customers"]
        save_db(db)
        
    for cust in db["customers"]:
        st.markdown(f"""
        <div class="card-box">
            <h3 style="margin:0; color:#0f172a;">{cust['name']} <span style="font-size:13px; color:#64748b;">({cust['country']})</span></h3>
            <p style="margin:4px 0; color:#475569; font-size:12px;">
                👤 <b>Yetkili:</b> {cust.get('contact_person','-')} | ✉️ <b>E-posta:</b> {cust.get('email','-')}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        exp_permits = cust.get("export_permits", [])
        if exp_permits:
            exp_permit = exp_permits[0]
            
            c_p1, c_p2 = st.columns([3, 2])
            with c_p1:
                st.markdown(f"📄 **Aktif MSB İzin No:** `{exp_permit['permit_no']}` (Son Tarih: {exp_permit['valid_until']})")
            with c_p2:
                if st.button("⚡ Bu İznin Tüm Ürünlerini ve Adetlerini Otomatik Yükle", type="primary", key=f"auto_load_{cust['id']}"):
                    st.session_state.order_items = []
                    for item in exp_permit.get("items", []):
                        st.session_state.order_items.append({
                            "code": item["code"],
                            "name": item["name"],
                            "qty": item["total_qty"] - item["used_qty"]
                        })
                    st.success("✅ İzin belgesindeki tüm kalemler ve onaylı adetler tabloya eklendi!")
                    st.rerun()

            st.markdown("---")
            st.markdown("#### **Sipariş & Sevkiyat Kalem Girişi (Otomatik & Canlı Doğrulama)**")
            
            permit_items_dict = {it["code"]: it for it in exp_permit.get("items", [])}
            
            if not st.session_state.order_items:
                st.info("💡 Yukarıdaki **'⚡ Bu İznin Tüm Ürünlerini ve Adetlerini Otomatik Yükle'** butonuna basarak veya aşağıdaki **'+ Satır / Ürün Ekle'** butonundan ürün ekleyebilirsiniz.")
            
            to_delete = None
            for idx, item in enumerate(st.session_state.order_items):
                r1, r2, r3, r4 = st.columns([3, 1.2, 3.3, 0.5])
                
                prod_keys = list(permit_items_dict.keys())
                curr_idx = prod_keys.index(item["code"]) if item["code"] in prod_keys else 0
                
                sel_code = r1.selectbox(f"Ürün Adı #{idx+1}", prod_keys, format_func=lambda x: permit_items_dict[x]["name"], index=curr_idx, key=f"p_code_{idx}")
                sel_qty = r2.number_input(f"Adet (Ad) #{idx+1}", min_value=1, value=item["qty"], key=f"p_qty_{idx}")
                
                st.session_state.order_items[idx]["code"] = sel_code
                st.session_state.order_items[idx]["name"] = permit_items_dict[sel_code]["name"]
                st.session_state.order_items[idx]["qty"] = sel_qty

                # CANLI KARŞILAŞTIRMA KONTROLÜ
                target_permit_item = permit_items_dict.get(sel_code)
                if target_permit_item:
                    rem_quota = target_permit_item["total_qty"] - target_permit_item["used_qty"]
                    if sel_qty <= rem_quota:
                        r3.markdown(f'<div class="status-ok">✅ Doğru (İzin Kotası İçi: Kalan {rem_quota:,} Adet)</div>', unsafe_allow_html=True)
                    else:
                        r3.markdown(f'<div class="status-err">⚠️ HATA: Miktar İzin Kotasını Aşıyor! (Maks: {rem_quota:,} Ad)</div>', unsafe_allow_html=True)
                else:
                    r3.markdown('<div class="status-err">❌ HATA: Ürün İzin Belgesinde Yer Almıyor!</div>', unsafe_allow_html=True)

                if r4.button("✖", key=f"del_row_{idx}"):
                    to_delete = idx

            if to_delete is not None:
                st.session_state.order_items.pop(to_delete)
                st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("➕ Satır / Ürün Ekle"):
                first_code = list(permit_items_dict.keys())[0]
                st.session_state.order_items.append({"code": first_code, "name": permit_items_dict[first_code]["name"], "qty": 100})
                st.rerun()

            st.markdown("---")
            st.markdown("#### 🛡️ Taranan MSB İhracat İzin Belgesi Orijinal Kotası")
            item_rows = []
            for it in exp_permit.get("items", []):
                rem = it['total_qty'] - it['used_qty']
                item_rows.append({
                    "Ürün / Model Adı": it['name'],
                    "Ürün Kodu": it['code'],
                    "Belge Onaylı Adet": f"{it['total_qty']:,} Adet",
                    "Kalan Kota": f"{rem:,} Adet"
                })
            st.table(pd.DataFrame(item_rows))
