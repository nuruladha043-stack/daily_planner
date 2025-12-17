import streamlit as st
from datetime import date

# ===========================
# KONFIGURASI HALAMAN
# ===========================
st.set_page_config(page_title="To-Do List & Daily Planner", layout="wide")

# ===========================
# INISIALISASI DATA
# ===========================
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# ===========================
# SIDEBAR NAVIGASI
# ===========================
st.sidebar.title("📝 Daily Planner")
menu = st.sidebar.radio(
    "Menu",
    ["Dashboard", "Tambah Tugas", "Daftar Tugas", "Filter Tugas", "Tentang Aplikasi"]
)

# ===========================
# DASHBOARD
# ===========================
if menu == "Dashboard":
    st.title("📊 Dashboard To-Do List")

    total = len(st.session_state.tasks)
    selesai = len([t for t in st.session_state.tasks if t["status"] == "Selesai"])
    belum = total - selesai

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Tugas", total)
    col2.metric("Selesai", selesai)
    col3.metric("Belum Selesai", belum)

    st.subheader("📊 Statistik Prioritas")
    if total > 0:
        prioritas_count = {}
        for t in st.session_state.tasks:
            prioritas_count[t["prioritas"]] = prioritas_count.get(t["prioritas"], 0) + 1
        st.bar_chart(prioritas_count)

    st.subheader("📅 Tugas Hari Ini")
    today_tasks = [t for t in st.session_state.tasks if t["tanggal"] == date.today()]

    if today_tasks:
        for t in today_tasks:
            st.write(f"- {t['nama']} ({t['status']})")
    else:
        st.info("Tidak ada tugas hari ini")
    st.title("📊 Dashboard To-Do List")

    total = len(st.session_state.tasks)
    selesai = len([t for t in st.session_state.tasks if t["status"] == "Selesai"])
    belum = total - selesai

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Tugas", total)
    col2.metric("Selesai", selesai)
    col3.metric("Belum Selesai", belum)

    st.subheader("📅 Tugas Hari Ini")
    today_tasks = [t for t in st.session_state.tasks if t["tanggal"] == date.today()]

    if today_tasks:
        for t in today_tasks:
            st.write(f"- {t['nama']} ({t['status']})")
    else:
        st.info("Tidak ada tugas hari ini")

# ===========================
# TAMBAH TUGAS
# ===========================
elif menu == "Tambah Tugas":
    st.title("➕ Tambah Tugas Baru")

    with st.form("form_tugas"):
        nama = st.text_input("Nama Tugas")
        kategori = st.selectbox("Kategori", ["Kuliah", "Pekerjaan", "Pribadi", "Lainnya"])
        tanggal = st.date_input("Tanggal", date.today())
        prioritas = st.selectbox("Prioritas", ["Rendah", "Sedang", "Tinggi"])
        submit = st.form_submit_button("Simpan")

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

# ===========================
# DAFTAR TUGAS
# ===========================
elif menu == "Daftar Tugas":
    st.title("📋 Daftar Tugas")

    if not st.session_state.tasks:
        st.warning("Belum ada tugas")
    else:
        for i, t in enumerate(st.session_state.tasks):
            with st.expander(f"{t['nama']} ({t['status']})"):
                st.write(f"Kategori: {t['kategori']}")
                st.write(f"Tanggal: {t['tanggal']}")
                st.write(f"Prioritas: {t['prioritas']}")

                col1, col2 = st.columns(2)
                if t["status"] == "Belum Selesai":
                    if col1.button("✔ Tandai Selesai", key=f"done_{i}"):
                        st.session_state.tasks[i]["status"] = "Selesai"
                        st.experimental_rerun()

                if col2.button("🗑 Hapus Tugas", key=f"del_{i}"):
                    st.session_state.tasks.pop(i)
                    st.experimental_rerun()
    st.title("📋 Daftar Tugas")

    if not st.session_state.tasks:
        st.warning("Belum ada tugas")
    else:
        for i, t in enumerate(st.session_state.tasks):
            with st.expander(f"{t['nama']} ({t['status']})"):
                st.write(f"Kategori: {t['kategori']}")
                st.write(f"Tanggal: {t['tanggal']}")
                st.write(f"Prioritas: {t['prioritas']}")

                if t["status"] == "Belum Selesai":
                    if st.button("Tandai Selesai", key=f"done_{i}"):
                        st.session_state.tasks[i]["status"] = "Selesai"
                        st.experimental_rerun()

# ===========================
# TENTANG
# ===========================
elif menu == "Filter Tugas":
    st.title("🔍 Filter Tugas")

    kategori_filter = st.selectbox(
        "Filter berdasarkan Kategori",
        ["Semua", "Kuliah", "Pekerjaan", "Pribadi", "Lainnya"]
    )

    status_filter = st.selectbox(
        "Filter berdasarkan Status",
        ["Semua", "Belum Selesai", "Selesai"]
    )

    filtered_tasks = st.session_state.tasks

    if kategori_filter != "Semua":
        filtered_tasks = [t for t in filtered_tasks if t["kategori"] == kategori_filter]

    if status_filter != "Semua":
        filtered_tasks = [t for t in filtered_tasks if t["status"] == status_filter]

    if not filtered_tasks:
        st.info("Tidak ada tugas sesuai filter")
    else:
        for t in filtered_tasks:
            st.write(f"- {t['nama']} | {t['kategori']} | {t['status']}")

else:
    st.title("ℹ️ Tentang Aplikasi")
    st.write(""
    Aplikasi To-Do List & Daily Planner ini digunakan untuk membantu
    mengatur tugas harian seperti kuliah, pekerjaan, dan kegiatan pribadi.

    Fitur utama:
    - Tambah dan kelola tugas
    - Dashboard ringkasan tugas
    - Penandaan tugas selesai
    ""
    )
