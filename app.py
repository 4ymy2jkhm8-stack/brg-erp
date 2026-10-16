import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime

DB_FILE = "brg_erp_db.json"
UPLOAD_DIR = "uploaded_permits"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# TAM ENTEGRE GERÇEK VERİ YAPISI
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
                {"id": "EUC-001", "euc_no": "EUC-2026-IRAQ-88", "qty": 25000, "date": "10.05.2026"}
            ],
            "export_permits": [
                {
                    "id": "EXP-001",
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
            ],
            "orders": [
                {
                    "order_no": "ORD-2026-001",
                    "date": "15.05.2026",
                    "status": "Müşteri Onayladı",
                    "approval_doc": "APPROVED_MOI_SIGNED.pdf",
                    "proforma_no": "PI-2026-8801",
                    "work_order_no": "WO-9901",
                    "items": [
                        {"code": "BRG9-ELITE", "name": "BRG9 Elite 9x19mm", "qty": 1000, "unit_price": 450.0},
                        {"code": "BRG9-ELITE-G2", "name": "BRG9 Elite Gen 2 9x19mm", "qty": 1000, "unit_price": 480.0}
                    ],
                    "shipments": [
                        {"shipment_no": "SHP-001", "date": "01.06.2026", "item_code": "BRG9-ELITE", "qty": 500}
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

# KURUMSAL SIKI CSS
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
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 12px;
    }
</style>
""", unsafe_allow_html=True)

# EN ÜST HEADER
st.markdown("""
<div class="top-header">
    <div><span style="font-size: 20px;">🛡️</span> <span class="top-title">BRG DEFENCE ERP</span></div>
    <div style="font-size:11px; text-align:right; color:#94a3b8;">DEFENCE EXPORT OPERATIONS</div>
</div>
""", unsafe_allow_html=True)

# GEZİNTİ
c1, c2, c3, _ = st.columns([1, 1, 1.2, 5])
with c1: st.button("← Back / Geri")
with c2: st.button("Forward / İleri →")
with c3:
    if st.button("🏠 Home / Ana Ekran"):
        st.session_state.current_tab = "customers"
        st.rerun()

st.markdown("---")

if "current_tab" not in st.session_state:
    st.session_state.current_tab = "customers"

# MÜŞTERİLERİMİZ ANA MODÜLÜ
if st.session_state.current_tab == "customers":
    st.markdown("## 👥 Customers & Integrated Operations / Müşteri ve Entegre Operasyonlar")
    
    # 1. MÜŞTERİ SEÇİMİ VEYA YENİ MÜŞTERİ EKLEME
    cust_names = [c["name"] for c in db["customers"]]
    selected_cust_name = st.selectbox("🎯 İşlem Yapılacak Müşteriyi Seçin:", cust_names)
    
    selected_cust = next(c for c in db["customers"] if c["name"] == selected_cust_name)
    
    # 8 ENTEGRE ADIMIN SEKMELERİ (TABS)
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
    
    # --- 1. FİRMA BİLGİLERİ (DÜZENLE / SİL) ---
    with t1:
        st.markdown("### 🏢 Firma Bilgileri Düzenle / Sil")
        edit_name = st.text_input("Firma Unvanı", value=selected_cust["name"])
        edit_country = st.text_input("Ülke", value=selected_cust["country"])
        edit_contact = st.text_input("Yetkili Kişi", value=selected_cust["contact_person"])
        edit_email = st.text_input("E-posta", value=selected_cust["email"])
        edit_address = st.text_area("Adres", value=selected_cust["address"])
        
        c_btn1, c_btn2 = st.columns(2)
        if c_btn1.button("💾 Firma Bilgilerini Güncelle", type="primary"):
            selected_cust["name"] = edit_name
            selected_cust["country"] = edit_country
            selected_cust["contact_person"] = edit_contact
            selected_cust["email"] = edit_email
            selected_cust["address"] = edit_address
            save_db(db)
            st.success("✅ Firma bilgileri başarıyla güncellendi!")
            st.rerun()
            
        if c_btn2.button("🗑️ Firmayı Sil", help="Müşteriyi tamamen siler"):
            db["customers"] = [c for c in db["customers"] if c["id"] != selected_cust["id"]]
            save_db(db)
            st.warning("Firmayı sildiniz.")
            st.rerun()

    # --- 2. EUC / İTHALAT İZNİ ---
    with t2:
        st.markdown("### 📄 EUC / İthalat İzinleri (Ekle / Düzenle / Sil)")
        for euc in selected_cust.get("import_permits", []):
            st.write(f"• **EUC No:** `{euc['euc_no']}` | **Adet:** {euc['qty']:,} Adet | **Tarih:** {euc['date']}")
        
        st.markdown("---")
        st.caption("➕ Yeni EUC / İthalat İzni Ekle:")
        new_euc_no = st.text_input("EUC Belge No")
        new_euc_qty = st.number_input("İzin Verilen Miktar", min_value=1, value=1000)
        if st.button("Save EUC / İzni Kaydet"):
            selected_cust["import_permits"].append({
                "id": f"EUC-{len(selected_cust['import_permits'])+1:03d}",
                "euc_no": new_euc_no,
                "qty": new_euc_qty,
                "date": datetime.now().strftime("%d.%m.%Y")
            })
            save_db(db)
            st.success("EUC Belgesi Eklendi!")
            st.rerun()

    # --- 3. İHRACAT İZNİ (MSB) ---
    with t3:
        st.markdown("### 🛡️ MSB İhracat İzin Belgesi Kotaları (Ekle / Düzenle / Sil)")
        exp_permits = selected_cust.get("export_permits", [])
        if exp_permits:
            exp_p = exp_permits[0]
            st.info(f"📄 **Aktif MSB İzin No:** {exp_p['permit_no']} (Geçerlilik: {exp_p['valid_until']})")
            
            p_rows = []
            for item in exp_p["items"]:
                p_rows.append({
                    "Ürün Kodu": item["code"],
                    "Ürün Adı": item["name"],
                    "Belge İzinli": f"{item['total_qty']:,} Adet",
                    "Sevk Edilen": f"{item['used_qty']:,} Adet",
                    "Kalan Kota": f"{item['total_qty'] - item['used_qty']:,} Adet"
                })
            st.table(pd.DataFrame(p_rows))

    # --- 4. SİPARİŞ YÖNETİMİ ---
    with t4:
        st.markdown("### 📦 Sipariş Oluştur / Düzenle (Canlı MSB Kota Doğrulaması)")
        if st.button("⚡ MSB İznindeki Ürünlerle Otomatik Sipariş Taslağı Aç", type="primary"):
            exp_p = selected_cust["export_permits"][0]
            new_ord = {
                "order_no": f"ORD-2026-{len(selected_cust.get('orders', []))+1:03d}",
                "date": datetime.now().strftime("%d.%m.%Y"),
                "status": "Müşteri Onayı Bekliyor",
                "items": [{"code": it["code"], "name": it["name"], "qty": it["total_qty"] - it["used_qty"], "unit_price": 450.0} for it in exp_p["items"][:2]]
            }
            selected_cust.setdefault("orders", []).append(new_ord)
            save_db(db)
            st.success("Sipariş oluşturuldu!")
            st.rerun()

        for ord_item in selected_cust.get("orders", []):
            st.write(f"📦 **Sipariş No:** `{ord_item['order_no']}` | **Durum:** {ord_item['status']} | **Tarih:** {ord_item['date']}")

    # --- 5. MÜŞTERİ ONAYI ---
    with t5:
        st.markdown("### ✍️ Müşteri Onayı Yönetimi")
        for ord_item in selected_cust.get("orders", []):
            st.write(f"Sipariş: **{ord_item['order_no']}** — Mevcut Durum: `{ord_item['status']}`")
            if st.button(f"✅ Müşteri Onayını Kaydet ({ord_item['order_no']})"):
                ord_item["status"] = "Müşteri Onayladı"
                save_db(db)
                st.success("Müşteri onayı sisteme işlendi!")
                st.rerun()

    # --- 6. PROFORMA OLUŞTUR ---
    with t6:
        st.markdown("### 📑 Proforma Fatura (PI) Oluştur / Düzenle")
        for ord_item in selected_cust.get("orders", []):
            st.write(f"📄 **Proforma No:** {ord_item.get('proforma_no', 'PI-2026-TEMP')} | Sipariş: {ord_item['order_no']}")
            st.caption("Müşteri Unvanı: " + selected_cust["name"])
            st.caption("Adres: " + selected_cust["address"])

    # --- 7. İŞ EMRİ (WORK ORDER) ---
    with t7:
        st.markdown("### 🏭 Üretim & Hazırlık İş Emri (Work Order)")
        for ord_item in selected_cust.get("orders", []):
            st.write(f"🏭 **İş Emri Kodu:** `{ord_item.get('work_order_no', 'WO-9000')}`")
            st.caption("Üretim / Montaj Hazırlık Durumu: AKTİF")

    # --- 8. SEVKİYAT & MSB KOTA DÜŞÜMİ ---
    with t8:
        st.markdown("### 🚚 Sevkiyat Çıkışı Ekle & MSB Kotasından Otomatik Düşüm")
        exp_p = selected_cust["export_permits"][0]
        
        c_s1, c_s2, c_s3 = st.columns([2, 1, 1])
        item_opts = {f"{it['name']} (Kalan: {it['total_qty'] - it['used_qty']})": it for it in exp_p["items"]}
        sel_item_label = c_s1.selectbox("Sevk Edilecek Ürün", list(item_opts.keys()))
        ship_qty = c_s2.number_input("Sevk Miktarı", min_value=1, value=100)
        
        if c_s3.button("🚚 Sevkiyatı Düş / Eksilt", type="primary"):
            target_it = item_opts[sel_item_label]
            if target_it["used_qty"] + ship_qty <= target_it["total_qty"]:
                target_it["used_qty"] += ship_qty
                save_db(db)
                st.success(f"✅ {ship_qty} Adet sevk edildi. Kalan Kota: {target_it['total_qty'] - target_it['used_qty']}")
                st.rerun()
            else:
                st.error("❌ HATA: İzin kotası aşılamaz!")
