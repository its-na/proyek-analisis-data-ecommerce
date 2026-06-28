# Proyek Analisis Data: E-Commerce Dataset

## Deskripsi Proyek
Proyek ini merupakan submission akhir untuk kelas "Belajar Analisis Data dengan Python" di Dicoding. Proyek ini berfokus pada analisis data transaksi e-commerce untuk menemukan pola penjualan produk, performa kategori, serta melakukan segmentasi pelanggan menggunakan analisis RFM (Recency, Frequency, Monetary).

## Struktur Direktori
- `/dashboard`: Berisi file kode aplikasi dashboard Streamlit (`dashboard.py`) dan dataset yang telah diproses (`main_data.csv`).
- `/data`: Berisi dataset mentah (opsional untuk lokal).
- `notebook.ipynb`: Berkas Jupyter Notebook tempat eksplorasi data (EDA), pembersihan data, dan analisis dilakukan.
- `requirements.txt`: Daftar pustaka (dependencies) Python yang dibutuhkan untuk menjalankan aplikasi.
- `url.txt`: Berisi tautan/URL aplikasi dashboard yang telah dideploy secara online.

## Tautan Dashboard Streamlit Cloud
Anda dapat mengakses dashboard interaktif yang telah dideploy secara online melalui tautan berikut:
👉 [Dashboard E-Commerce Anda](https://sxeivtpycoxccsz9y7kfjv.streamlit.app/)

## Cara Menjalankan Aplikasi Secara Lokal

### 1. Kloning atau Unduh Proyek
Pastikan Anda sudah mengunduh seluruh file proyek ini ke komputer Anda.

### 2. Instalasi Dependensi
Buka terminal atau command prompt pada direktori proyek, lalu jalankan perintah berikut untuk menginstal pustaka yang diperlukan:
```bash
pip install -r requirements.txt
```

### 3. Menjalankan Dashboard Streamlit
Untuk menjalankan aplikasi dashboard secara lokal, jalankan perintah berikut di terminal Anda:
```bash
streamlit run dashboard/dashboard.py
```
