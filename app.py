import streamlit as st
import json
import os
from datetime import datetime

DB_FILE = "brg_erp_db.json"

INITIAL_DATA = {
    "company": {
        "title": "BURGU SAVUNMA TEKNOLOJİLERİ VE HAVACILIK A.Ş.",
        "short_name": "BRG DEFENCE",
        "address": "Pendik / İstanbul",
        "bank_name": "Vakıfbank",
        "iban": "TR123456789012345678901234",
        "swift": "VAKFTR2A"
    },
    "products": [
        {"code": "BRG55", "name": "BRG55 Piyade Tüfeği", "category": "Tüfek", "caliber": "5.56x45mm", "unit_price": 1200.0, "stock": 50},
        {"code": "BRG9-ELITE-G2", "name": "BRG9 ELITE Gen2 Tabanca", "category": "Tabanca", "caliber": "9x19mm", "unit_price": 450.0, "stock": 100},
        {"code": "BRG9-FDX", "name": "BRG9 FDX Tabanca", "category": "Tabanca", "caliber": "9x19mm", "unit_price": 420.0, "stock": 10}
    ],
    "inventory_packaging": [
        {"code": "BOX-TABANCA", "description": "Tabanca Taşıma Çantası", "stock": 150, "unit": "Adet"},
        {"code": "BOX-TUFEK", "description": "Tüfek Kolisi", "stock": 30, "unit": "Adet"},
        {"code": "CLEAN-KIT", "description": "Temizlik Kiti", "stock": 200, "unit": "Adet"}
    ],
    "customers": [
        {"id": "CUST-001", "name": "KAVIANI 2015", "country": "Gürcistan", "tax_id": "GEO-998811"},
        {"id": "CUST-002", "name": "AL-TAJ COMPANY FOR IMPORT AND EXPORT", "country": "Irak", "tax_id": "IRQ-554422"}
    ],
    "export_permits": [
        {
            "permit_no": "E-38100341-302.04-6134334",
            "euc_no": "B2101",
            "customer_id": "CUST-002",
            "product_code": "BRG9-ELITE-G2",
            "valid_until": "2026-12-31",
            "max_quantity": 500
        }
    ],
    "orders": []
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

st.set_page_config(page_title="BRG DEFENCE ERP", page_icon="🛡️", layout="wide")

db = load_db()

st.title("🛡️ BRG DEFENCE ERP Portalı")
st.sidebar.header("Menü")
menu = st.sidebar.radio("Sayfa Seçin", ["Gösterge Paneli", "Yeni Sipariş Oluştur", "Mevcut Siparişler", "Stok & Envanter", "İhracat İzinleri"])

if menu == "Gösterge Paneli":
    st.header("📊 Genel Durum")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Toplam Ürün Tipi", len(db["products"]))
    col2.metric("Müşteri Sayısı", len(db["customers"]))
    col3.metric("Aktif Siparişler", len(db["orders"]))
    col4.metric("İhracat İzin İzinleri", len(db["export_permits"]))

    st.subheader("Şirket Bilgileri")
    st.json(db["company"])

elif menu == "Yeni Sipariş Oluştur":
    st.header("📝 Yeni Deneme Siparişi Girişi")
    
    with st.form("order_form"):
        customer_names = {c["name"]: c["id"] for c in db["customers"]}
        selected_cust_name = st.selectbox("Müşteri Seçin", list(customer_names.keys()))
        
        product_names = {p["name"]: p["code"] for p in db["products"]}
        selected_prod_name = st.selectbox("Ürün Seçin", list(product_names.keys()))
        
        quantity = st.number_input("Miktar (Adet)", min_value=1, value=5)
        price_override = st.number_input("Birim Fiyat (USD)", min_value=0.0, value=450.0)
        
        serials_input = st.text_area("Seri Numaraları (Her satıra bir tane yazın)", "BRG9-2026-001\nBRG9-2026-002")
        
        submitted = st.form_submit_button("Siparişi Kaydet ve Denetle")
        
        if submitted:
            cust_id = customer_names[selected_cust_name]
            prod_code = product_names[selected_prod_name]
            serials = [s.strip() for s in serials_input.split("\n") if s.strip()]
            
            warnings = []
            permit = next((p for p in db["export_permits"] if p["customer_id"] == cust_id and p["product_code"] == prod_code), None)
            if not permit:
                warnings.append("⚠️ İhracat İzni / EUC Belgesi eksik!")
            if len(serials) != quantity:
                warnings.append(f"⚠️ Seri numarası sayısı ({len(serials)}) sipariş miktarı ({quantity}) ile eşleşmiyor!")
            
            new_order = {
                "order_id": f"SO-2026-{len(db['orders'])+1:04d}",
                "customer": selected_cust_name,
                "product": selected_prod_name,
                "quantity": quantity,
                "unit_price": price_override,
                "total_amount": quantity * price_override,
                "serials": serials,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "warnings": warnings
            }
            
            db["orders"].append(new_order)
            save_db(db)
            st.success(f"Sipariş başarıyla oluşturuldu! ID: {new_order['order_id']}")
            if warnings:
                for w in warnings:
                    st.warning(w)

elif menu == "Mevcut Siparişler":
    st.header("📋 Sipariş Listesi")
    st.table(db["orders"])

elif menu == "Stok & Envanter":
    st.header("📦 Stok Durumu")
    st.subheader("Ürünler")
    st.table(db["products"])
    st.subheader("Ambalaj ve Sarf Malzemeleri")
    st.table(db["inventory_packaging"])

elif menu == "İhracat İzinleri":
    st.header("📜 İhracat ve EUC İzin Belgeleri")
    st.table(db["export_permits"])
