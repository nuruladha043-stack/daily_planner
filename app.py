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
    kategori = st.selectbox("Kategori", ["Kuliah", "Pekerjaan", "Pribadi", "Lainnya"])
    tanggal = st.date_input("Deadline", date.today())
    prioritas = st.selectbox("Prioritas", ["Rendah", "Sedang", "Tinggi"])
    submit = st.form_submit_button("Tambah")

if submit:
    if nama:
        st.session_state.tasks.append({
            "nama": nama,
            "kategori": kategori,
            "tanggal": tanggal,
            "prioritas": prioritas,
            "status": "Belum Selesai"
        })
        st.success("Tugas berhasil ditambahkan")
    else:
        st.error("Nama tugas wajib diisi")

st.divider()

# ======================
# DASHBOARD
# ======================
st.subheader("📊 Ringkasan")

total = len(st.session_state.tasks)
selesai = len([t for t in st.session_state.tasks if t["status"] == "Selesai"])
belum = total - selesai
overdue = len([
    t for t in st.session_state.tasks
    if t["status"] == "Belum Selesai" and t["tanggal"] < date.today()
])

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total", total)
c2.metric("Selesai", selesai)
c3.metric("Belum", belum)
c4.metric("Overdue", overdue)

st.divider()

# ======================
# SEARCH & SORT
# ======================
st.subheader("🔍 Cari & Urutkan")
keyword = st.text_input("Cari tugas")
sort_by = st.selectbox("Urutkan berdasarkan", ["Deadline", "Prioritas"])

# ======================
# FILTER
# ======================
filter_kategori = st.selectbox("Filter Kategori", ["Semua", "Kuliah", "Pekerjaan", "Pribadi", "Lainnya"])
filter_status = st.selectbox("Filter Status", ["Semua", "Belum Selesai", "Selesai"])

# ======================
# PROSES DATA
# ======================
data = st.session_state.tasks

if keyword:
    data = [t for t in data if keyword.lower() in t["nama"].lower()]

if filter_kategori != "Semua":
    data = [t for t in data if t["kategori"] == filter_kategori]

if filter_status != "Semua":
    data = [t for t in data if t["status"] == filter_status]

if sort_by == "Deadline":
    data = sorted(data, key=lambda x: x["tanggal"])
else:
    priority_order = {"Tinggi": 1, "Sedang": 2, "Rendah": 3}
    data = sorted(data, key=lambda x: priority_order[x["prioritas"]])

st.divider()

# ======================
# DAFTAR TUGAS
# ======================
st.subheader("📋 Daftar Tugas")

if not data:
    st.info("Tidak ada tugas")
else:
    for t in data:
        col1, col2, col3, col4, col5 = st.columns([4, 2, 2, 2, 2])
        col1.write(f"**{t['nama']}**")
        col2.write(t["kategori"])
        col3.write(t["prioritas"])

        if t["status"] == "Belum Selesai" and t["tanggal"] < date.today():
            col4.error("Overdue")
        else:
            col4.write(t["status"])

        if t["status"] == "Belum Selesai":
            if col5.button("✔", key=f"done{t['nama']}"):
                t["status"] = "Selesai"
                st.experimental_rerun()

st.divider()

# ======================
# EXPORT & RESET
# ======================
st.subheader("📥 Data")

if st.session_state.tasks:
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["nama", "kategori", "tanggal", "prioritas", "status"])
    writer.writeheader()
    for t in st.session_state.tasks:
        writer.writerow(t)

    st.download_button("Download CSV", output.getvalue(), "todo_list.csv", "text/csv")

    if st.button("🗑 Hapus Semua Tugas"):
        st.session_state.tasks = []
        st.experimental_rerun()
else:
    st.info("Belum ada data")
