import streamlit as st
from datetime import date
import csv
import io

st.set_page_config(page_title="Daily Planner", layout="centered")

# ======================
# INIT DATA
# ======================
if "tasks" not in st.session_state:
    st.session_state.tasks = []

st.title("📝 Daily Planner / To-Do List")

# ======================
# FORM INPUT
# ======================
st.subheader("➕ Tambah Tugas")

with st.form("form_tugas"):
    nama = st.text_input("Nama Tugas")
    kategori = st.selectbox(
        "Kategori",
        ["Kuliah", "Pekerjaan", "Pribadi", "Lainnya"]
    )
    tanggal = st.date_input("Tanggal", date.today())
    submit = st.form_submit_button("Tambah")

if submit:
    if nama:
        st.session_state.tasks.append({
            "nama": nama,
            "kategori": kategori,
            "tanggal": tanggal,
            "status": "Belum Selesai"
        })
        st.success("Tugas berhasil ditambahkan")
    else:
        st.error("Nama tugas wajib diisi")

st.divider()

# ======================
# DASHBOARD RINGKAS
# ======================
st.subheader("📊 Ringkasan")

total = len(st.session_state.tasks)
selesai = len([t for t in st.session_state.tasks if t["status"] == "Selesai"])
belum = total - selesai

col1, col2, col3 = st.columns(3)
col1.metric("Total Tugas", total)
col2.metric("Selesai", selesai)
col3.metric("Belum", belum)

st.divider()

# ======================
# FITUR BARU 1: SEARCH
# ======================
st.subheader("🔎 Cari Tugas")
keyword = st.text_input("Cari berdasarkan nama tugas")

# ======================
# FITUR BARU 2: FILTER
# ======================
st.subheader("🗂 Filter")
filter_kategori = st.selectbox(
    "Filter Kategori",
    ["Semua", "Kuliah", "Pekerjaan", "Pribadi", "Lainnya"]
)

filter_status = st.selectbox(
    "Filter Status",
    ["Semua", "Belum Selesai", "Selesai"]
)

# ======================
# PROSES FILTER & SEARCH
# ======================
filtered_tasks = st.session_state.tasks

if keyword:
    filtered_tasks = [t for t in filtered_tasks if keyword.lower() in t["nama"].lower()]

if filter_kategori != "Semua":
    filtered_tasks = [t for t in filtered_tasks if t["kategori"] == filter_kategori]

if filter_status != "Semua":
    filtered_tasks = [t for t in filtered_tasks if t["status"] == filter_status]

st.divider()

# ======================
# DAFTAR TUGAS
# ======================
st.subheader("📋 Daftar Tugas")

if not filtered_tasks:
    st.info("Tidak ada tugas yang ditampilkan")
else:
    for i, t in enumerate(filtered_tasks):
        col1, col2, col3, col4 = st.columns([4, 2, 2, 2])

        col1.write(f"**{t['nama']}**")
        col2.write(t["kategori"])
        col3.write(t["status"])

        if t["status"] == "Belum Selesai":
            if col4.button("✔ Selesai", key=f"done{i}"):
                t["status"] = "Selesai"
                st.experimental_rerun()

        if col4.button("🗑 Hapus", key=f"del{i}"):
            st.session_state.tasks.remove(t)
            st.experimental_rerun()

st.divider()

# ======================
# FITUR BARU 3: EXPORT CSV
# ======================
st.subheader("📥 Export Data")

if st.session_state.tasks:
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["nama", "kategori", "tanggal", "status"])
    writer.writeheader()
    for t in st.session_state.tasks:
        writer.writerow(t)

    st.download_button(
        label="Download To-Do List (CSV)",
        data=output.getvalue(),
        file_name="todo_list.csv",
        mime="text/csv"
    )
else:
    st.info("Tidak ada data untuk diexport")
