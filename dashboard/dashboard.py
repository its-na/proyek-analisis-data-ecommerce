import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Mengatur tema visualisasi dasar
sns.set_theme(style="whitegrid")

# ==========================================
# 1. LOAD DATA & CACHING
# ==========================================
@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/main_data.csv")
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    return df

main_data_all = load_data()

# ==========================================
# 2. SIDEBAR FILTER WAKTU
# ==========================================
st.sidebar.image("https://raw.githubusercontent.com/streamlit/executable-tutorials/master/images/logo.png", width=100)
st.sidebar.header("Filter Analisis")

min_date = main_data_all["order_purchase_timestamp"].min().date()
max_date = main_data_all["order_purchase_timestamp"].max().date()

if min_date == max_date:
    start_date = min_date
    end_date = max_date
    st.sidebar.write(f"Rentang Tanggal Data: {min_date}")
else:
    start_date, end_date = st.sidebar.date_input(
        label="Pilih Rentang Waktu Transaksi:",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Menyaring data berdasarkan input tanggal
main_data = main_data_all[
    (main_data_all["order_purchase_timestamp"].dt.date >= start_date) & 
    (main_data_all["order_purchase_timestamp"].dt.date <= end_date)
].copy()

# ==========================================
# 3. HEADER DASHBOARD
# ==========================================
st.title("🛒 E-Commerce Performance & Customer Dashboard")
st.markdown("Dashboard interaktif untuk memonitor performa penjualan produk dan segmentasi loyalitas pelanggan.")

# Menampilkan Ringkasan Metrik Utama (KPIs)
col1, col2, col3 = st.columns(3)
with col1:
    total_orders = main_data.shape[0]
    st.metric("Total Pesanan Sukses", value=f"{total_orders:,}")
with col2:
    total_revenue = main_data["price"].sum()
    st.metric("Total Pendapatan (BRL)", value=f"R$ {total_revenue:,.2f}")
with col3:
    cust_col = "customer_unique_id" if "customer_unique_id" in main_data.columns else "order_id"
    total_customers = main_data[cust_col].nunique()
    st.metric("Pelanggan Unik Aktif", value=f"{total_customers:,}")

st.write("---")

# ==========================================
# 4. VISUALISASI 1: PERFORMA KATEGORI PRODUK
# ==========================================
st.subheader("📦 Performa Kategori Produk Teratas & Terbawah")

cat_col = "product_category_name_english" if "product_category_name_english" in main_data.columns else "product_category_name"

if cat_col in main_data.columns:
    category_revenue = main_data.groupby(cat_col)["price"].sum().reset_index()
    top_categories = category_revenue.sort_values(by="price", ascending=False).head(5)
    bottom_categories = category_revenue.sort_values(by="price", ascending=True).head(5)

    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(16, 6))

    # Grafik Top 5
    sns.barplot(x="price", y=cat_col, data=top_categories, palette=["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"], ax=ax[0])
    ax[0].set_title("5 Kategori Produk dengan Revenue Tertinggi", fontsize=12)
    ax[0].set_xlabel("Revenue (BRL)")
    ax[0].set_ylabel(None)

    # Grafik Bottom 5
    sns.barplot(x="price", y=cat_col, data=bottom_categories, palette=["#D14D4D", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"], ax=ax[1])
    ax[1].set_title("5 Kategori Produk dengan Revenue Terendah", fontsize=12)
    ax[1].set_xlabel("Revenue (BRL)")
    ax[1].set_ylabel(None)
    ax[1].invert_xaxis()
    ax[1].yaxis.set_label_position("right")
    ax[1].yaxis.tick_right()

    plt.tight_layout()
    st.pyplot(fig)
else:
    st.warning("Kolom kategori produk tidak ditemukan.")

# ==========================================
# 5. VISUALISASI 2: ANALISIS LANJUTAN RFM
# ==========================================
st.subheader("👥 Segmentasi Pelanggan Berdasarkan Analisis Lanjutan (RFM)")

recent_date = main_data["order_purchase_timestamp"].max() + pd.Timedelta(days=1)
cust_id_col = "customer_unique_id" if "customer_unique_id" in main_data.columns else "order_id"

rfm_df = main_data.groupby(cust_id_col).agg(
    Recency=("order_purchase_timestamp", lambda x: (recent_date - x.max()).days),
    Frequency=("order_id", "count"),
    Monetary=("price", "sum")
).reset_index()

col_r, col_f, col_m = st.columns(3)

with col_r:
    st.write("**Top Pelanggan - Recency**")
    top_r = rfm_df.sort_values(by="Recency", ascending=True).head(5)
    fig_r, ax_r = plt.subplots(figsize=(6, 4))
    sns.barplot(y="Recency", x=cust_id_col, data=top_r, palette="Blues_r", ax=ax_r)
    ax_r.set_xticklabels([])
    ax_r.set_xlabel("Pelanggan Unik")
    st.pyplot(fig_r)

with col_f:
    st.write("**Top Pelanggan - Frequency**")
    top_f = rfm_df.sort_values(by="Frequency", ascending=False).head(5)
    fig_f, ax_f = plt.subplots(figsize=(6, 4))
    sns.barplot(y="Frequency", x=cust_id_col, data=top_f, palette="Greens_r", ax=fig_f.gca())
    ax_f = fig_f.gca()
    ax_f.set_xticklabels([])
    ax_f.set_xlabel("Pelanggan Unik")
    st.pyplot(fig_f)

with col_m:
    st.write("**Top Pelanggan - Monetary**")
    top_m = rfm_df.sort_values(by="Monetary", ascending=False).head(5)
    fig_m, ax_m = plt.subplots(figsize=(6, 4))
    sns.barplot(y="Monetary", x=cust_id_col, data=top_m, palette="Oranges_r", ax=ax_m)
    ax_m.set_xticklabels([])
    ax_m.set_xlabel("Pelanggan Unik")
    st.pyplot(fig_m)

st.caption("Copyright © 2026 | Proyek Analisis Data E-Commerce")
