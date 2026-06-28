import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Mengatur tema visualisasi dasar
sns.set_theme(style="whitegrid")

# ==========================================
# 1. LOAD DATA & CACHING (Jauh lebih cepat & ringkas)
# ==========================================
@st.cache_data
def load_data():
    # Memuat data yang sudah bersih dan digabung dari notebook
    df = pd.read_csv("dashboard/main_data.csv")
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    return df

main_data_all = load_data()

# ==========================================
# 2. SIDEBAR FILTER WAKTU (Interaktivitas)
# ==========================================
st.sidebar.image("https://raw.githubusercontent.com/streamlit/executable-tutorials/master/images/logo.png", width=100)
st.sidebar.header("Filter Analisis")

# Menentukan rentang tanggal minimum & maksimum dari data
min_date = main_data_all["order_purchase_timestamp"].min().date()
max_date = main_data_all["order_purchase_timestamp"].max().date()

start_date, end_date = st.sidebar.date_input(
    label="Pilih Rentang Waktu Transaksi:",
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

# Menyaring data utama berdasarkan input tanggal pembeli di sidebar
main_data = main_data_all[
    (main_data_all["order_purchase_timestamp"].dt.date >= start_date) & 
    (main_data_all["order_purchase_timestamp"].dt.date <= end_date)
]

# ==========================================
# 3. HEADER DASHBOARD
# ==========================================
st.title("🛒 E-Commerce Performance & Customer Dashboard")
st.markdown("Dashboard interaktif untuk memonitor performa penjualan produk dan segmentasi loyalitas pelanggan.")

# Menampilkan Ringkasan Metrik Utama (KPIs)
col1, col2, col3 = st.columns(3)
with col1:
    total_orders = filtered_orders.shape[0]
    st.metric("Total Pesanan Sukses", value=f"{total_orders:,}")
with col2:
    total_revenue = main_data["price"].sum()
    st.metric("Total Pendapatan (BRL)", value=f"R$ {total_revenue:,.2f}")
with col3:
    total_customers = main_data["customer_unique_id"].nunique()
    st.metric("Pelanggan Unik Aktif", value=f"{total_customers:,}")

st.write("---")

# ==========================================
# 4. VISUALISASI 1: PERFORMA KATEGORI PRODUK
# ==========================================
st.subheader("📦 Performa Kategori Produk Teratas & Terbawah")

category_revenue = main_data.groupby("product_category_name_english")["price"].sum().reset_index()
top_categories = category_revenue.sort_values(by="price", ascending=False).head(5)
bottom_categories = category_revenue.sort_values(by="price", ascending=True).head(5)

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(16, 6))

# Grafik Top 5
sns.barplot(x="price", y="product_category_name_english", data=top_categories, palette=["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"], ax=ax[0])
ax[0].set_title("5 Kategori Produk dengan Revenue Tertinggi", fontsize=12)
ax[0].set_xlabel("Revenue (BRL)")
ax[0].set_ylabel(None)

# Grafik Bottom 5
sns.barplot(x="price", y="product_category_name_english", data=bottom_categories, palette=["#D14D4D", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"], ax=ax[1])
ax[1].set_title("5 Kategori Produk dengan Revenue Terendah", fontsize=12)
ax[1].set_xlabel("Revenue (BRL)")
ax[1].set_ylabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()

plt.tight_layout()
st.pyplot(fig)

# ==========================================
# 5. VISUALISASI 2: ANALISIS LANJUTAN RFM
# ==========================================
st.subheader("👥 Segmentasi Pelanggan Berdasarkan Analisis Lanjutan (RFM)")

# Kalkulasi RFM berdasarkan tanggal acuan filter
recent_date = main_data["order_purchase_timestamp"].max() + pd.Timedelta(days=1)
rfm_df = main_data.groupby("customer_unique_id").agg(
    Recency=("order_purchase_timestamp", lambda x: (recent_date - x.max()).days),
    Frequency=("order_id", "nunique"),
    Monetary=("price", "sum")
).reset_index()

col_r, col_f, col_m = st.columns(3)

with col_r:
    st.write("**Top Pelanggan - Paling Baru Belanja (Recency)**")
    top_r = rfm_df.sort_values(by="Recency", ascending=True).head(5)
    fig_r, ax_r = plt.subplots(figsize=(6, 4))
    sns.barplot(y="Recency", x="customer_unique_id", data=top_r, palette="Blues_r", ax=ax_r)
    ax_r.set_xticklabels([])
    ax_r.set_xlabel("Pelanggan Unik")
    st.pyplot(fig_r)

with col_f:
    st.write("**Top Pelanggan - Paling Sering Belanja (Frequency)**")
    top_f = rfm_df.sort_values(by="Frequency", ascending=False).head(5)
    fig_f, ax_f = plt.subplots(figsize=(6, 4))
    sns.barplot(y="Frequency", x="customer_unique_id", data=top_f, palette="Greens_r", ax=ax_f)
    ax_f.set_xticklabels([])
    ax_f.set_xlabel("Pelanggan Unik")
    st.pyplot(fig_f)

with col_m:
    st.write("**Top Pelanggan - Nilai Belanja Tertinggi (Monetary)**")
    top_m = rfm_df.sort_values(by="Monetary", ascending=False).head(5)
    fig_m, ax_m = plt.subplots(figsize=(6, 4))
    sns.barplot(y="Monetary", x="customer_unique_id", data=top_m, palette="Oranges_r", ax=ax_m)
    ax_m.set_xticklabels([])
    ax_m.set_xlabel("Pelanggan Unik")
    st.pyplot(fig_m)

st.caption("Copyright © 2026 | Proyek Analisis Data E-Commerce")