import streamlit as st
from datetime import date

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
# DAFTAR TUGAS
# ======================
st.subheader("📋 Daftar Tugas")

if not st.session_state.tasks:
    st.info("Belum ada tugas")
else:
    for i, t in enumerate(st.session_state.tasks):
        with st.container():
            col1, col2, col3 = st.columns([4, 2, 2])

            col1.write(f"**{t['nama']}**")
            col2.write(t["kategori"])
            col3.write(t["status"])

            col4, col5 = st.columns([2, 2])

            if t["status"] == "Belum Selesai":
                if col4.button("✔ Selesai", key=f"done{i}"):
                    st.session_state.tasks[i]["status"] = "Selesai"
                    st.experimental_rerun()

            if col5.button("🗑 Hapus", key=f"del{i}"):
                st.session_state.tasks.pop(i)
                st.experimental_rerun()

