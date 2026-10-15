import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime

DB_FILE = "brg_erp_db.json"

INITIAL_DATA = {
    "company": {
        "title": "BURGU SAVUNMA TEKNOLOJİLERİ VE HAVACILIK A.Ş.",
        "short_name": "BRG DEFENCE",
        "tax_office": "Pendik V.D.",
        "tax_no": "1910543210",
        "address": "Sanayi Mah. Teknopark Bulvarı No:1 Pendik / İstanbul",
        "bank_name": "Vakıfbank / Kurumsal Şube",
        "iban": "TR12 0001 5001 5800 7300 1234 56",
        "swift": "VAKFTR2A"
    },
    "products": [
        {"code": "BRG55-556", "name": "BRG55 Piyade Tüfeği 5.56x45mm", "category": "Tüfek", "unit_price": 1200.0, "stock": 150},
        {"code": "BRG9-ELITE-G2", "name": "BRG9 ELITE Gen2 Tabanca 9x19mm", "category": "Tabanca", "unit_price": 450.0, "stock": 320},
        {"code": "BRG9-FDX", "name": "BRG9 FDX Tabanca 9x19mm", "category": "Tabanca", "unit_price": 420.0, "stock": 85}
    ],
    "customers": [
        {"id": "CUST-001", "name": "KAVIANI 2015 LTD", "country": "Gürcistan", "tax_id": "GEO-998811", "contact": "info@kaviani.ge"},
        {"id": "CUST-002", "name": "AL-TAJ COMPANY FOR IMPORT AND EXPORT", "country": "Irak", "tax_id": "IRQ-554422", "contact": "trade@altaj.iq"}
    ],
    "export_permits": [
        {
            "permit_no": "MSB-EUC-2026-0891",
            "euc_no": "EUC-B2101-IRAQ",
            "customer_id": "CUST-002",
            "product_code": "BRG9-ELITE-G2",
            "valid_until": "2026-12-31",
            "max_quantity": 500,
            "used_quantity": 50
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

st.set_page_config(page_title="BRG DEFENCE - ERP Portal", page_icon="🛡️", layout="wide")
db = load_db()

# Yan Menü Navigasyonu
st.sidebar.image("https://via.placeholder.com/200x60.png?text=BRG+DEFENCE", use_column_width=True)
st.sidebar.title("🛡️ ERP Kontrol Paneli")
menu = st.sidebar.radio("Sistem Menüsü", [
    "📊 Genel Gösterge Paneli", 
    "🛒 Yeni Sipariş Oluştur (Proforma)", 
    "📋 Sipariş Takibi & İhracat Dosyaları", 
    "📦 Ürün & Stok Yönetimi", 
    "📜 İhracat İzinleri & EUC"
])

# --- SAYFA 1: GÖSTERGE PANELİ ---
if menu == "📊 Genel Gösterge Paneli":
    st.header("📌 BRG DEFENCE Operasyonel Durum")
    st.markdown("---")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Aktif Ürün Çeşidi", len(db["products"]))
    c2.metric("Kayıtlı Müşteri", len(db["customers"]))
    c3.metric("Toplam Sipariş Sayısı", len(db["orders"]))
    c4.metric("Aktif EUC / İzin Belgesi", len(db["export_permits"]))

    st.subheader("🏢 Firma Resmi Bilgileri")
    col_a, col_b = st.columns(2)
    with col_a:
        st.write(f"**Ünvan:** {db['company']['title']}")
        st.write(f"**Adres:** {db['company']['address']}")
        st.write(f"**Vergi Dairesi / No:** {db['company']['tax_office']} / {db['company']['tax_no']}")
    with col_b:
        st.write(f"**Banka:** {db['company']['bank_name']}")
        st.write(f"**IBAN:** {db['company']['iban']}")
        st.write(f"**SWIFT:** {db['company']['swift']}")

# --- SAYFA 2: PROFESYONEL SİPARİŞ OLUŞTURMA ---
elif menu == "🛒 Yeni Sipariş Oluştur (Proforma)":
    st.header("📝 Yeni Uluslararası Sipariş & Proforma Fatura Girişi")
    st.info("Bu ekrandan oluşturulan siparişler otomatik olarak İhracat İzni (EUC) ve Stok kotalarından düşülür.")

    st.subheader("1. Müşteri ve İhracat İzin Seçimi")
    col1, col2, col3 = st.columns(3)
    
    customer_dict = {f"{c['name']} ({c['country']})": c for c in db["customers"]}
    selected_cust_label = col1.selectbox("Müşteri Seçiniz *", list(customer_dict.keys()))
    selected_customer = customer_dict[selected_cust_label]

    # Müşteriye ait izinleri filtele
    cust_permits = [p for p in db["export_permits"] if p["customer_id"] == selected_customer["id"]]
    permit_options = {"İzin Belgesiz / Yurtiçi": None}
    for p in cust_permits:
        permit_options[f"İzin No: {p['permit_no']} (Kalan Kota: {p['max_quantity'] - p['used_quantity']} Adet)"] = p
    
    selected_permit_label = col2.selectbox("İhracat İzni / EUC Belgesi *", list(permit_options.keys()))
    selected_permit = permit_options[selected_permit_label]

    incoterm = col3.selectbox("Teslimat Şekli (Incoterm)", ["FOB İstanbul", "CIF Target Port", "DAP", "EXW Pendik Fabrika"])

    st.subheader("2. Finansal & Lojistik Detaylar")
    col_f1, col_f2, col_f3 = st.columns(3)
    currency = col_f1.selectbox("Döviz Cinsi", ["USD (\$)", "EUR (€)", "TRY (₺)"])
    payment_terms = col_f2.selectbox("Ödeme Koşulu", ["%100 Peşin Transfer (TT)", "%30 Avans + %70 Yükleme Öncesi", "Gayri Kabili Rücu Akreditif (LC)"])
    delivery_date = col_f3.date_input("Tahmini Teslim Tarihi")

    st.subheader("3. Sipariş Kalemleri (Ürün Seçimi)")
    
    if "order_items" not in st.session_state:
        st.session_state.order_items = []

    with st.expander("➕ Siparişe Ürün Ekle", expanded=True):
        prod_col1, prod_col2, prod_col3, prod_col4 = st.columns([3, 1, 1, 1])
        prod_dict = {f"{p['code']} - {p['name']} (Mevcut Stok: {p['stock']})": p for p in db["products"]}
        selected_prod_label = prod_col1.selectbox("Ürün Seçin", list(prod_dict.keys()))
        selected_product = prod_dict[selected_prod_label]

        item_qty = prod_col2.number_input("Adet", min_value=1, value=10)
        item_price = prod_col3.number_input("Birim Fiyat", min_value=0.0, value=float(selected_product["unit_price"]))
        
        if prod_col4.button("Kalemi Ekle"):
            st.session_state.order_items.append({
                "product_code": selected_product["code"],
                "product_name": selected_product["name"],
                "quantity": item_qty,
                "unit_price": item_price,
                "total": item_qty * item_price
            })
            st.success(f"{selected_product['code']} siparişe eklendi.")

    # Eklenen kalemler tablosu
    if st.session_state.order_items:
        df_items = pd.DataFrame(st.session_state.order_items)
        st.table(df_items)
        grand_total = sum(item["total"] for item in st.session_state.order_items)
        st.markdown(f"### **Genel Toplam Tutar:** `{grand_total:,.2f} {currency.split()[0]}`")
        
        if st.button("🗑️ Kalemleri Temizle"):
            st.session_state.order_items = []
            st.rerun()

    st.subheader("4. Seri Numarası Tanımlama")
    serials_text = st.text_area("Ürün Seri Numaralarını Girin (Her satıra 1 seri no gelecek şekilde):", 
                                placeholder="BRG9-2026-00101\nBRG9-2026-00102\nBRG9-2026-00103")

    st.markdown("---")
    if st.button("🚀 Siparişi Onayla ve Kaydet", type="primary"):
        if not st.session_state.order_items:
            st.error("Lütfen siparişe en az bir ürün kalemi ekleyin!")
        else:
            serials_list = [s.strip() for s in serials_text.split("\n") if s.strip()]
            total_qty = sum(item["quantity"] for item in st.session_state.order_items)

            # Denetim Kuralları
            warnings = []
            if len(serials_list) != total_qty:
                warnings.append(f"⚠️ Seri numarası sayısı ({len(serials_list)} adet) toplam sipariş miktarı ({total_qty} adet) ile uyuşmuyor!")
            
            if selected_permit:
                kalan_kota = selected_permit["max_quantity"] - selected_permit["used_quantity"]
                if total_qty > kalan_kota:
                    warnings.append(f"❌ Sipariş miktarı ({total_qty}), seçilen EUC izninin kalan kotasını ({kalan_kota}) aşıyor!")

            new_order_id = f"SO-2026-{len(db['orders'])+1:04d}"
            order_record = {
                "order_id": new_order_id,
                "customer": selected_customer["name"],
                "country": selected_customer["country"],
                "permit_no": selected_permit["permit_no"] if selected_permit else "YOK",
                "incoterm": incoterm,
                "items": st.session_state.order_items,
                "grand_total": grand_total,
                "currency": currency,
                "payment_terms": payment_terms,
                "delivery_date": str(delivery_date),
                "serials": serials_list,
                "warnings": warnings,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            db["orders"].append(order_record)
            save_db(db)
            
            st.session_state.order_items = []
            st.success(f"✅ {new_order_id} Nolu Sipariş Kaydedildi!")
            for w in warnings:
                st.warning(w)

# --- SAYFA 3: MEVCUT SİPARİŞLER ---
elif menu == "📋 Sipariş Takibi & İhracat Dosyaları":
    st.header("📋 Kayıtlı Siparişler ve Detayları")
    if not db["orders"]:
        st.info("Henüz kaydedilmiş bir sipariş bulunmamaktadır.")
    else:
        for order in reversed(db["orders"]):
            with st.expander(f"📦 Sipariş No: {order['order_id']} - Müşteri: {order['customer']} ({order['country']}) - Tutar: {order['grand_total']} {order['currency']}"):
                st.write(f"**Oluşturulma Tarihi:** {order['created_at']}")
                st.write(f"**Teslimat Şekli:** {order['incoterm']} | **Ödeme:** {order['payment_terms']}")
                st.write(f"**EUC / İzin No:** {order['permit_no']}")
                st.subheader("Ürün Kalemleri")
                st.table(pd.DataFrame(order["items"]))
                st.write(f"**Kayıtlı Seri Numaraları ({len(order['serials'])} adet):**")
                st.code(", ".join(order["serials"]))
                if order["warnings"]:
                    st.error("Uyumsuzluk/Uyarı Notları:")
                    for w in order["warnings"]:
                        st.write(f"- {w}")

# --- SAYFA 4: STOK YÖNETİMİ ---
elif menu == "📦 Ürün & Stok Yönetimi":
    st.header("📦 Ürün Kataloğu ve Depo Stok Durumu")
    st.table(pd.DataFrame(db["products"]))

# --- SAYFA 5: İHRACAT İZİNLERİ ---
elif menu == "📜 İhracat İzinleri & EUC":
    st.header("📜 Tanımlı İhracat İzinleri ve Kota Takibi")
    st.table(pd.DataFrame(db["export_permits"]))
