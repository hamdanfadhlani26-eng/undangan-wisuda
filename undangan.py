import streamlit as st
from datetime import datetime
import time
import json
import os

st.set_page_config(
    page_title="Undangan Wisuda - Muhammad Hamdan Fadhlani",
    page_icon="🎓",
    layout="centered"
)

# ── AMBIL NAMA TAMU DARI URL PARAMETER ──────────────────
params = st.query_params
nama_tamu_url = params.get("tamu", "")

# ── SESSION STATE ────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "splash"
if "photos" not in st.session_state:
    st.session_state.photos = []

# ── FILE UCAPAN ──────────────────────────────────────────
UCAPAN_FILE = "ucapan.json"

def muat_ucapan():
    if os.path.exists(UCAPAN_FILE):
        with open(UCAPAN_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def simpan_ucapan(data):
    with open(UCAPAN_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ── GLOBAL CSS ───────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Lato:wght@300;400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Lato', sans-serif;
}

.stApp {
    background-color: #FFF0F5;
    background-image:
        radial-gradient(circle at 10% 10%, #FFB7C5 0px, transparent 220px),
        radial-gradient(circle at 90% 15%, #B5EAD7 0px, transparent 200px),
        radial-gradient(circle at 50% 88%, #FFDAC1 0px, transparent 220px),
        radial-gradient(circle at 80% 75%, #C7CEEA 0px, transparent 180px);
    min-height: 100vh;
}

label, .stTextInput label, .stTextArea label,
.stFileUploader label {
    color: #5A1A3A !important;
    font-weight: 600 !important;
}

.stButton > button {
    background: linear-gradient(135deg, #C2185B, #AD1457);
    color: white !important;
    border: none;
    border-radius: 50px;
    padding: 0.7rem 2rem;
    font-size: 1rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    cursor: pointer;
    width: 100%;
    transition: all 0.2s;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #AD1457, #880E4F);
    color: white !important;
}

.card {
    background: rgba(255,255,255,0.88);
    border-radius: 24px;
    padding: 1.5rem 1.8rem;
    margin: 1rem 0;
    border: 1.5px solid rgba(255,105,150,0.3);
    box-shadow: 0 4px 24px rgba(180,80,120,0.08);
}

.info-label {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    color: #C2185B;
    text-transform: uppercase;
    margin-bottom: 2px;
}

.info-value {
    font-family: 'Playfair Display', serif;
    font-size: 1.05rem;
    color: #2D0A1F;
    margin-bottom: 0.9rem;
    line-height: 1.5;
}

.countdown-box {
    background: linear-gradient(135deg, #880E4F, #C2185B);
    border-radius: 20px;
    padding: 1.5rem 1rem;
    text-align: center;
    margin: 1rem 0;
}

.countdown-title {
    font-size: 0.78rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: white;
    opacity: 0.9;
    margin-bottom: 1rem;
}

.countdown-numbers {
    display: flex;
    justify-content: center;
    gap: 0.5rem;
    flex-wrap: nowrap;
    align-items: center;
}

.count-item { text-align: center; min-width: 55px; }

.count-num {
    font-family: 'Playfair Display', serif;
    font-size: 2.4rem;
    font-weight: 700;
    line-height: 1;
    display: block;
    color: white;
}

.count-label {
    font-size: 0.62rem;
    letter-spacing: 0.1em;
    opacity: 0.85;
    text-transform: uppercase;
    color: white;
}

.count-sep {
    font-size: 2rem;
    color: white;
    opacity: 0.5;
    padding-bottom: 12px;
}

.divider {
    text-align: center;
    font-size: 1.3rem;
    margin: 0.4rem 0;
}

.quote-text {
    font-family: 'Playfair Display', serif;
    font-style: italic;
    font-size: 1rem;
    color: #5A1A3A;
    text-align: center;
    line-height: 1.8;
}

.section-heading {
    font-family: 'Playfair Display', serif;
    font-size: 1.2rem;
    color: #5A1A3A;
    margin: 1.2rem 0 0.6rem;
}

.splash-card {
    background: rgba(255,255,255,0.92);
    border-radius: 28px;
    padding: 2.5rem 1.8rem;
    border: 1.5px solid rgba(255,105,150,0.35);
    box-shadow: 0 8px 40px rgba(180,80,120,0.12);
    text-align: center;
}

.footer-flowers {
    text-align: center;
    font-size: 1.5rem;
    padding: 1rem;
    letter-spacing: 0.2rem;
}

.ucapan-item {
    background: linear-gradient(90deg, rgba(255,182,193,0.2), rgba(255,240,245,0.4));
    border-left: 4px solid #F48FB1;
    border-radius: 12px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.75rem;
}
.ucapan-nama {
    font-weight: 700;
    color: #880E4F;
    font-size: 0.9rem;
    margin-bottom: 0.25rem;
}
.ucapan-teks {
    color: #2D0A1F;
    font-size: 0.93rem;
    line-height: 1.6;
    font-style: italic;
}
.ucapan-waktu {
    font-size: 0.75rem;
    color: #AD1457;
    opacity: 0.7;
    margin-top: 0.3rem;
}
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════
# SPLASH PAGE
# ════════════════════════════════════════════════════════
if st.session_state.page == "splash":

    st.markdown('<div style="text-align:center; font-size:2.2rem; letter-spacing:0.3rem; margin-bottom:1.2rem;">&#127800; &#127826; &#127804; &#127799; &#127803;</div>', unsafe_allow_html=True)

    if nama_tamu_url:
        sapaan = (
            '<div style="font-size:0.85rem; color:#AD1457; margin-bottom:0.4rem; font-style:italic;">Kepada Yth,</div>'
            + f'<div style="font-family:\'Playfair Display\',serif; font-size:1.5rem; color:#880E4F; font-weight:700; margin-bottom:1.2rem;">{nama_tamu_url} &#127800;</div>'
        )
    else:
        sapaan = ""

    isi_splash = (
        '<div class="splash-card">'
        + sapaan
        + '<div style="font-size:0.78rem; font-weight:700; color:#C2185B; letter-spacing:0.2em; text-transform:uppercase; margin-bottom:0.8rem;">&#127891; Undangan Wisuda</div>'
        + '<div style="font-family:\'Playfair Display\',serif; font-size:1.9rem; color:#5A1A3A; font-weight:700; line-height:1.3; margin-bottom:0.4rem;">Muhammad Hamdan<br>Fadhlani, S.T.</div>'
        + '<div style="font-family:\'Playfair Display\',serif; font-style:italic; font-size:0.95rem; color:#AD1457; margin-bottom:1.3rem;">Sarjana Teknik &#8212; Teknik Industri</div>'
        + '<div style="font-size:0.88rem; color:#C2185B; margin-bottom:0.3rem; font-weight:600;">&#128197; Minggu, 10 Mei 2026</div>'
        + '<div style="font-size:0.88rem; color:#C2185B; margin-bottom:1.4rem; font-weight:600;">&#128205; Gedung Teknik Industri, Unand</div>'
        + '<div style="font-size:0.82rem; color:#888; font-style:italic; margin-bottom:1.8rem; line-height:1.6;">&#8220;Dengan penuh syukur dan kebahagiaan,<br>kami mengundang kehadiranmu &#127800;&#8221;</div>'
        + '</div>'
    )
    st.markdown(isi_splash, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("💌 Buka Undangan"):
            st.session_state.page = "main"
            st.rerun()

    st.markdown('<div class="footer-flowers">&#127800; &#127826; &#127804; &#127799; &#127803; &#127799; &#127804; &#127826; &#127800;</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════
# MAIN INVITATION PAGE
# ════════════════════════════════════════════════════════
elif st.session_state.page == "main":

    # ── HEADER ──────────────────────────────────────────
    st.markdown('<div style="text-align:center; font-size:1.8rem; padding:1.2rem 0 0.3rem; letter-spacing:0.3rem;">&#127800; &#127826; &#127804; &#127799; &#127803;</div>', unsafe_allow_html=True)
    st.markdown('<h1 style="font-family:Playfair Display,serif; font-size:2.2rem; color:#5A1A3A; text-align:center; line-height:1.2; margin:0.3rem 0;">Undangan Wisuda</h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-family:Playfair Display,serif; font-style:italic; font-size:0.9rem; color:#AD1457; text-align:center; margin-bottom:1rem;">Dengan penuh syukur dan kebahagiaan, kami mengundang kehadiranmu</p>', unsafe_allow_html=True)

    # Sapaan di halaman utama
    if nama_tamu_url:
        st.markdown(
            '<div style="text-align:center; background:rgba(255,255,255,0.7); border-radius:16px; padding:0.8rem 1rem; margin-bottom:0.5rem; border:1px solid rgba(255,105,150,0.25);">'
            + '<span style="font-size:0.78rem; color:#AD1457; text-transform:uppercase; letter-spacing:0.1em;">Kepada Yth,</span><br>'
            + f'<span style="font-family:\'Playfair Display\',serif; font-size:1.3rem; color:#880E4F; font-weight:700;">{nama_tamu_url} &#127800;</span>'
            + '</div>',
            unsafe_allow_html=True
        )

    # ── INFO WISUDAWAN ───────────────────────────────────
    st.markdown("""
    <div class="card" style="text-align:center;">
        <div style="font-size:0.78rem; color:#C2185B; letter-spacing:0.12em; text-transform:uppercase; margin-bottom:0.5rem; font-weight:700;">&#127800; Wisudawan &#127800;</div>
        <div style="font-family:'Playfair Display',serif; font-size:1.8rem; color:#5A1A3A; font-weight:700; line-height:1.3;">Muhammad Hamdan<br>Fadhlani, S.T.</div>
        <div style="margin-top:0.8rem; display:inline-block; background:#FCE4EC; color:#880E4F; padding:5px 16px; border-radius:20px; font-size:0.85rem; font-weight:700;">
            &#127891; S1 Teknik Industri
        </div>
        <div style="font-size:0.88rem; color:#AD1457; margin-top:0.4rem; font-weight:600;">Universitas Andalas</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="divider">&#127804; &#10022; &#127804;</div>', unsafe_allow_html=True)

    # ── FOTO WISUDA ──────────────────────────────────────
    st.markdown('<p class="section-heading">&#128247; Foto Wisuda</p>', unsafe_allow_html=True)

    with st.expander("🔐 Panel Pemilik — Upload Foto (khusus Hamdan)"):
        uploaded = st.file_uploader(
            "Upload foto-foto wisudamu",
            type=["jpg", "jpeg", "png"],
            accept_multiple_files=True,
            key="owner_upload"
        )
        if uploaded:
            st.session_state.photos = uploaded
            st.success(f"✅ {len(uploaded)} foto berhasil diupload!")

    if st.session_state.photos:
        cols = st.columns(min(len(st.session_state.photos), 3))
        for i, f in enumerate(st.session_state.photos):
            with cols[i % 3]:
                st.image(f, use_container_width=True, caption=f"Foto {i+1}")
    else:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#FCE4EC,#FFF0F5); border-radius:16px; padding:2rem 1rem; text-align:center; border:2px dashed #F48FB1; margin:0.5rem 0;">
            &#127800;<br>
            <span style="font-size:0.95rem; font-weight:700; color:#880E4F;">Foto akan tampil di sini</span><br>
            <span style="font-size:0.82rem; color:#AD1457;">Belum ada foto yang diupload</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="divider">&#127826; &#10022; &#127826;</div>', unsafe_allow_html=True)

    # ── INFO ACARA ───────────────────────────────────────
    st.markdown("""
    <div class="card">
        <div style="text-align:center; font-size:0.78rem; color:#C2185B; font-weight:700; letter-spacing:0.12em; text-transform:uppercase; margin-bottom:1rem;">&#127799; Detail Acara &#127799;</div>
        <div class="info-label">&#128197; Hari &amp; Tanggal</div>
        <div class="info-value">Minggu, 10 Mei 2026</div>
        <div class="info-label">&#128336; Waktu</div>
        <div class="info-value">Pukul 14.00 WIB &#8212; Selesai</div>
        <div class="info-label">&#128205; Lokasi</div>
        <div class="info-value">Gedung Teknik Industri<br>
        <span style="font-size:0.88rem; color:#AD1457;">Universitas Andalas, Padang, Sumatera Barat</span></div>
        <div class="info-label">&#128087; Dresscode</div>
        <div class="info-value">Formal / Batik</div>
    </div>
    """, unsafe_allow_html=True)

    # ── COUNTDOWN REAL-TIME (st.fragment) ────────────────
    wisuda_dt = datetime(2026, 5, 10, 14, 0, 0)

    @st.fragment(run_every=1)
    def tampilkan_countdown():
        now          = datetime.now()
        total_secs   = int((wisuda_dt - now).total_seconds())

        if total_secs <= 0:
            st.markdown("""
            <div class="countdown-box">
                <div style="font-family:'Playfair Display',serif; font-size:1.6rem; color:white;">
                    &#127881; Hari ini hari wisudanya! Selamat! &#127881;
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            days    = total_secs // 86400
            hours   = (total_secs % 86400) // 3600
            minutes = (total_secs % 3600) // 60
            seconds = total_secs % 60

            st.markdown(f"""
            <div class="countdown-box">
                <div class="countdown-title">&#127800; Hitung Mundur Menuju Hari Wisuda &#127800;</div>
                <div class="countdown-numbers">
                    <div class="count-item">
                        <span class="count-num">{days:02d}</span>
                        <span class="count-label">Hari</span>
                    </div>
                    <div class="count-sep">:</div>
                    <div class="count-item">
                        <span class="count-num">{hours:02d}</span>
                        <span class="count-label">Jam</span>
                    </div>
                    <div class="count-sep">:</div>
                    <div class="count-item">
                        <span class="count-num">{minutes:02d}</span>
                        <span class="count-label">Menit</span>
                    </div>
                    <div class="count-sep">:</div>
                    <div class="count-item">
                        <span class="count-num">{seconds:02d}</span>
                        <span class="count-label">Detik</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    tampilkan_countdown()

    st.markdown('<div class="divider">&#127803; &#10022; &#127803;</div>', unsafe_allow_html=True)

    # ── PETA LOKASI ──────────────────────────────────────
    st.markdown('<p class="section-heading">&#128205; Lokasi Acara</p>', unsafe_allow_html=True)
    st.markdown("""
    <div style="border-radius:16px; overflow:hidden; border:1.5px solid rgba(255,105,150,0.35); margin-bottom:0.5rem;">
    <iframe
        src="https://maps.google.com/maps?q=Gedung+Teknik+Industri+Universitas+Andalas+Padang&output=embed"
        width="100%" height="280" style="border:0; display:block;"
        allowfullscreen="" loading="lazy">
    </iframe>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="divider">&#127800; &#10022; &#127800;</div>', unsafe_allow_html=True)

    # ── KUTIPAN ──────────────────────────────────────────
    st.markdown("""
    <div class="card">
        <div class="quote-text">
            &#8220;Setiap perjuangan panjang selalu berujung pada kebahagiaan.<br>
            Terima kasih telah menjadi bagian dari perjalanan ini. &#127800;&#8221;
        </div>
        <div style="text-align:center; margin-top:1rem; font-size:0.82rem; color:#AD1457;">&#8212; Muhammad Hamdan Fadhlani, S.T.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="divider">&#127799; &#10022; &#127799;</div>', unsafe_allow_html=True)

    # ── FORM UCAPAN & DOA ────────────────────────────────
    st.markdown('<p class="section-heading">&#128172; Kirim Ucapan &amp; Doa</p>', unsafe_allow_html=True)

    with st.form("ucapan_form", clear_on_submit=True):
        nama_pengirim = st.text_input("Nama Kamu", placeholder="Masukkan namamu")
        ucapan        = st.text_area(
            "Ucapan & Doa untuk Hamdan",
            placeholder="Tuliskan ucapan dan doamu di sini... 🌸",
            height=120
        )
        submitted = st.form_submit_button("💌 Kirim Ucapan", use_container_width=True)

    if submitted:
        if nama_pengirim.strip() and ucapan.strip():
            daftar = muat_ucapan()
            daftar.insert(0, {
                "nama"  : nama_pengirim.strip(),
                "ucapan": ucapan.strip(),
                "waktu" : datetime.now().strftime("%d %b %Y, %H:%M"),
            })
            simpan_ucapan(daftar)
            st.balloons()
            st.success(f"🌸 Terima kasih, **{nama_pengirim}**! Ucapanmu sudah terkirim.")
        else:
            st.warning("⚠️ Mohon isi nama dan ucapanmu terlebih dahulu.")

    # Tampilkan ucapan yang sudah masuk
    daftar_ucapan = muat_ucapan()
    if daftar_ucapan:
        st.markdown(
            f'<div style="font-size:0.85rem; color:#AD1457; margin:0.8rem 0 0.4rem;">'
            f'&#128149; {len(daftar_ucapan)} ucapan telah dikirimkan</div>',
            unsafe_allow_html=True
        )
        for u in daftar_ucapan[:20]:
            st.markdown(
                f'<div class="ucapan-item">'
                f'<div class="ucapan-nama">&#127800; {u["nama"]}</div>'
                f'<div class="ucapan-teks">&#8220;{u["ucapan"]}&#8221;</div>'
                f'<div class="ucapan-waktu">&#128337; {u.get("waktu", "")}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    # ── BACK & FOOTER ────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🌸 Kembali ke Halaman Awal"):
            st.session_state.page = "splash"
            st.rerun()

    st.markdown("""
    <div style="text-align:center; margin-top:1.5rem; padding:1rem; color:#AD1457; font-size:0.82rem;">
        Dibuat dengan &#128149; untuk Muhammad Hamdan Fadhlani, S.T.<br>
        <span style="opacity:0.7;">Undangan digital &#8212; tidak ada kertas yang digunakan &#127807;</span>
    </div>
    <div class="footer-flowers">&#127800; &#127826; &#127804; &#127799; &#127803; &#127799; &#127804; &#127826; &#127800;</div>
    """, unsafe_allow_html=True)