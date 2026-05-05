import streamlit as st
from datetime import datetime
import json
import os
import base64
from pathlib import Path

st.set_page_config(
    page_title="Undangan Wisuda - Muhammad Hamdan Fadhlani",
    page_icon="🎓",
    layout="centered"
)

params = st.query_params
nama_tamu_url = params.get("tamu", "")

if "page" not in st.session_state:
    st.session_state.page = "splash"
if "owner_unlocked" not in st.session_state:
    st.session_state.owner_unlocked = False

OWNER_URL_KEY = "hamdan2026"
OWNER_PASSWORD = "hamdan123"

# Cek URL parameter owner
if params.get("owner", "") == OWNER_URL_KEY:
    st.session_state.owner_url_valid = True
else:
    if "owner_url_valid" not in st.session_state:
        st.session_state.owner_url_valid = False

UCAPAN_FILE = "ucapan.json"
MUSIC_FILE  = "music.mp3"   # Letakkan file MP3 kamu dengan nama ini di root repo

def autoplay_audio(filepath: str):
    """Encode MP3 ke base64 lalu inject sebagai hidden audio autoplay."""
    import base64
    if not os.path.exists(filepath):
        return
    with open(filepath, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    st.markdown(
        f'''
        <audio id="bg-audio" autoplay loop style="display:none;">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        <script>
        // Browser butuh interaksi user sebelum autoplay — coba play saat ada klik pertama
        (function() {{
            var audio = document.getElementById("bg-audio");
            if (!audio) return;
            var played = false;
            function tryPlay() {{
                if (!played) {{ audio.play().catch(function(){{}}); played = true; }}
            }}
            audio.play().catch(function() {{
                document.addEventListener("click", tryPlay, {{once: true}});
                document.addEventListener("touchstart", tryPlay, {{once: true}});
            }});
        }})();
        </script>
        ''',
        unsafe_allow_html=True
    )
PHOTOS_FILE = "photos.json"
PHOTOS_DIR  = "foto_wisuda"
Path(PHOTOS_DIR).mkdir(exist_ok=True)

def muat_ucapan():
    if os.path.exists(UCAPAN_FILE):
        with open(UCAPAN_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def simpan_ucapan(data):
    with open(UCAPAN_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def muat_photos():
    """Load list of saved photo filenames."""
    if os.path.exists(PHOTOS_FILE):
        with open(PHOTOS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def simpan_photos(data):
    with open(PHOTOS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def upload_foto(uploaded_files, pengunggah="Tamu"):
    """Save uploaded files to disk and record metadata."""
    photos = muat_photos()
    saved = 0
    for uf in uploaded_files:
        ext      = uf.name.rsplit(".", 1)[-1].lower()
        ts       = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"{ts}.{ext}"
        filepath = os.path.join(PHOTOS_DIR, filename)
        with open(filepath, "wb") as f:
            f.write(uf.read())
        photos.insert(0, {
            "filename"   : filename,
            "pengunggah" : pengunggah.strip() or "Anonim",
            "waktu"      : datetime.now().strftime("%d %b %Y, %H:%M"),
        })
        saved += 1
    simpan_photos(photos)
    return saved

# ── GLOBAL CSS (Night Sky theme) ─────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Lato:wght@300;400;700&display=swap');

html, body, [class*="css"] { font-family: 'Lato', sans-serif; }

.stApp {
    background-color: #050B1F;
    background-image:
        radial-gradient(ellipse at 15% 20%, rgba(72,52,140,0.55) 0px, transparent 40%),
        radial-gradient(ellipse at 80% 10%, rgba(30,60,120,0.45) 0px, transparent 35%),
        radial-gradient(ellipse at 50% 80%, rgba(20,40,100,0.5) 0px, transparent 45%),
        radial-gradient(ellipse at 90% 70%, rgba(60,20,100,0.35) 0px, transparent 30%);
    min-height: 100vh;
}

/* Bintang-bintang latar */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image:
        radial-gradient(1px 1px at 10% 8%,  #fff 100%, transparent),
        radial-gradient(1px 1px at 25% 20%, #fff 100%, transparent),
        radial-gradient(1px 1px at 40% 5%,  #fff 100%, transparent),
        radial-gradient(1px 1px at 55% 15%, #fff 100%, transparent),
        radial-gradient(1px 1px at 70% 3%,  #fff 100%, transparent),
        radial-gradient(1px 1px at 85% 22%, #fff 100%, transparent),
        radial-gradient(1.5px 1.5px at 18% 35%, rgba(255,255,180,0.9) 100%, transparent),
        radial-gradient(1px 1px at 33% 50%, #fff 100%, transparent),
        radial-gradient(1px 1px at 60% 42%, #fff 100%, transparent),
        radial-gradient(1.5px 1.5px at 78% 55%, rgba(180,200,255,0.9) 100%, transparent),
        radial-gradient(1px 1px at 92% 38%, #fff 100%, transparent),
        radial-gradient(1px 1px at 5%  65%, #fff 100%, transparent),
        radial-gradient(1px 1px at 48% 72%, #fff 100%, transparent),
        radial-gradient(1.5px 1.5px at 65% 68%, rgba(255,255,200,0.8) 100%, transparent),
        radial-gradient(1px 1px at 88% 80%, #fff 100%, transparent),
        radial-gradient(1px 1px at 12% 88%, #fff 100%, transparent),
        radial-gradient(1px 1px at 37% 92%, #fff 100%, transparent),
        radial-gradient(1px 1px at 72% 90%, #fff 100%, transparent),
        radial-gradient(1px 1px at 95% 95%, #fff 100%, transparent),
        radial-gradient(1px 1px at 22% 55%, rgba(200,220,255,0.7) 100%, transparent),
        radial-gradient(1px 1px at 82% 45%, rgba(255,230,200,0.7) 100%, transparent);
    opacity: 0.7;
    pointer-events: none;
    z-index: 0;
}

label, .stTextInput label, .stTextArea label, .stFileUploader label {
    color: #C8D8F8 !important;
    font-weight: 600 !important;
}

.stButton > button {
    background: linear-gradient(135deg, #2A4A8A, #3D2A80);
    color: #E8F0FF !important;
    border: 1px solid rgba(150,180,255,0.4);
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
    background: linear-gradient(135deg, #3D5FAA, #4F3A9A);
    color: #FFFFFF !important;
    border-color: rgba(180,210,255,0.6);
}

.card {
    background: rgba(10,20,55,0.75);
    border-radius: 24px;
    padding: 1.5rem 1.8rem;
    margin: 1rem 0;
    border: 1px solid rgba(100,140,220,0.3);
    box-shadow: 0 4px 32px rgba(0,0,80,0.4), inset 0 1px 0 rgba(255,255,255,0.05);
}

.info-label {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    color: #7EB8E8;
    text-transform: uppercase;
    margin-bottom: 2px;
}

.info-value {
    font-family: 'Playfair Display', serif;
    font-size: 1.05rem;
    color: #E8F0FF;
    margin-bottom: 0.9rem;
    line-height: 1.5;
}

.countdown-box {
    background: linear-gradient(135deg, #0D1B4B, #1A0E4A);
    border: 1px solid rgba(100,140,220,0.35);
    border-radius: 20px;
    padding: 1.5rem 1rem;
    text-align: center;
    margin: 1rem 0;
    box-shadow: 0 0 40px rgba(60,40,160,0.3);
}

.countdown-title {
    font-size: 0.78rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #A8C8F0;
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
    color: #F0E080;
}

.count-label {
    font-size: 0.62rem;
    letter-spacing: 0.1em;
    opacity: 0.8;
    text-transform: uppercase;
    color: #A8C8F0;
}

.count-sep {
    font-size: 2rem;
    color: #F0E080;
    opacity: 0.5;
    padding-bottom: 12px;
}

.divider {
    text-align: center;
    font-size: 1.2rem;
    margin: 0.4rem 0;
    opacity: 0.7;
}

.quote-text {
    font-family: 'Playfair Display', serif;
    font-style: italic;
    font-size: 1rem;
    color: #C8D8F8;
    text-align: center;
    line-height: 1.8;
}

.section-heading {
    font-family: 'Playfair Display', serif;
    font-size: 1.2rem;
    color: #A8C8F8;
    margin: 1.2rem 0 0.6rem;
}

.splash-card {
    background: rgba(8,15,45,0.85);
    border-radius: 28px;
    padding: 2.5rem 1.8rem;
    border: 1px solid rgba(100,140,220,0.35);
    box-shadow: 0 8px 60px rgba(0,0,80,0.5), inset 0 1px 0 rgba(255,255,255,0.05);
    text-align: center;
}

.footer-stars {
    text-align: center;
    font-size: 1.3rem;
    padding: 1rem;
    letter-spacing: 0.3rem;
    opacity: 0.7;
}

.ucapan-item {
    background: rgba(15,25,65,0.7);
    border-left: 3px solid #4A7AC8;
    border-radius: 12px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.75rem;
    border-top: 1px solid rgba(100,140,220,0.15);
    border-right: 1px solid rgba(100,140,220,0.15);
    border-bottom: 1px solid rgba(100,140,220,0.15);
}
.ucapan-nama {
    font-weight: 700;
    color: #7EB8E8;
    font-size: 0.9rem;
    margin-bottom: 0.25rem;
}
.ucapan-teks {
    color: #C8D8F8;
    font-size: 0.93rem;
    line-height: 1.6;
    font-style: italic;
}
.ucapan-waktu {
    font-size: 0.75rem;
    color: #6888B0;
    margin-top: 0.3rem;
}

.moon {
    display: inline-block;
    width: 60px; height: 60px;
    border-radius: 50%;
    background: radial-gradient(circle at 35% 35%, #FFF8D0, #F0E080 40%, #C8A800 80%);
    box-shadow: 0 0 20px rgba(240,220,80,0.6), 0 0 60px rgba(240,220,80,0.2);
    position: relative;
    margin: 0 auto 0.8rem;
}

.photo-credit {
    font-size: 0.75rem;
    color: #6888B0;
    margin-top: 0.25rem;
}
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════
# SPLASH PAGE
# ════════════════════════════════════════════════════════
if st.session_state.page == "splash":

    # Autoplay musik saat splash dibuka
    autoplay_audio(MUSIC_FILE)

    st.markdown(
        '<div style="text-align:center; font-size:1.8rem; letter-spacing:0.4rem; margin-bottom:1rem; opacity:0.85;">'
        '🌙 ✨ ⭐ ✨ 🌙'
        '</div>',
        unsafe_allow_html=True
    )

    if nama_tamu_url:
        sapaan = (
            '<div style="font-size:0.85rem; color:#7EB8E8; margin-bottom:0.4rem; font-style:italic;">Kepada Yth,</div>'
            + f'<div style="font-family:\'Playfair Display\',serif; font-size:1.5rem; color:#F0E080; font-weight:700; margin-bottom:1.2rem;">{nama_tamu_url} ✨</div>'
        )
    else:
        sapaan = ""

    isi_splash = (
        '<div class="splash-card">'
        + '<div class="moon"></div>'
        + sapaan
        + '<div style="font-size:0.78rem; font-weight:700; color:#7EB8E8; letter-spacing:0.2em; text-transform:uppercase; margin-bottom:0.8rem;">🎓 Undangan Wisuda</div>'
        + '<div style="font-family:\'Playfair Display\',serif; font-size:1.9rem; color:#E8F0FF; font-weight:700; line-height:1.3; margin-bottom:0.4rem;">Muhammad Hamdan<br>Fadhlani, S.T.</div>'
        + '<div style="font-family:\'Playfair Display\',serif; font-style:italic; font-size:0.95rem; color:#A8C8F0; margin-bottom:1.3rem;">Sarjana Teknik &#8212; Teknik Industri</div>'
        + '<div style="font-size:0.88rem; color:#F0E080; margin-bottom:0.3rem; font-weight:600;">📅 Minggu, 10 Mei 2026</div>'
        + '<div style="font-size:0.88rem; color:#A8C8F0; margin-bottom:1.4rem; font-weight:600;">📍 Gedung Teknik Industri, Unand</div>'
        + '<div style="font-size:0.82rem; color:#8898C0; font-style:italic; margin-bottom:1.8rem; line-height:1.6;">"Seperti bintang yang menerangi langit malam,<br>perjalananmu kini sampai di puncaknya ✨"</div>'
        + '</div>'
    )
    st.markdown(isi_splash, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🌙 Buka Undangan", key="btn_buka", use_container_width=True):
            st.session_state.page = "main"
            st.rerun()

    st.markdown("""
    <div style="text-align:center; margin-top:0.5rem; margin-bottom:0.2rem;">
        <button onclick="
            var a=document.getElementById('bg-audio');
            if(a){
                if(a.muted){a.muted=false;this.textContent='🔊 Musik Menyala';}
                else{a.muted=true;this.textContent='🔇 Musik Mati';}
            }
        " style="background:rgba(10,20,60,0.7); color:#A8C8F0; border:1px solid rgba(100,140,220,0.35); border-radius:20px; padding:4px 16px; font-size:0.78rem; cursor:pointer; letter-spacing:0.05em;">
            🔊 Musik Menyala
        </button>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="footer-stars">🌟 ✨ ⭐ 🌙 ⭐ ✨ 🌟</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════
# MAIN INVITATION PAGE
# ════════════════════════════════════════════════════════
elif st.session_state.page == "main":

    # ── HEADER ──────────────────────────────────────────
    st.markdown(
        '<div style="text-align:center; font-size:1.5rem; padding:1.2rem 0 0.3rem; letter-spacing:0.4rem; opacity:0.8;">'
        '🌙 ✨ ⭐ ✨ 🌙'
        '</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<h1 style="font-family:Playfair Display,serif; font-size:2.2rem; color:#E8F0FF; text-align:center; line-height:1.2; margin:0.3rem 0; text-shadow:0 0 30px rgba(100,140,255,0.4);">Undangan Wisuda</h1>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<p style="font-family:Playfair Display,serif; font-style:italic; font-size:0.9rem; color:#7EB8E8; text-align:center; margin-bottom:1rem;">Di bawah langit malam yang penuh bintang, merayakan pencapaianmu ✨</p>',
        unsafe_allow_html=True
    )

    if nama_tamu_url:
        st.markdown(
            '<div style="text-align:center; background:rgba(10,20,60,0.6); border-radius:16px; padding:0.8rem 1rem; margin-bottom:0.5rem; border:1px solid rgba(100,140,220,0.25);">'
            + '<span style="font-size:0.78rem; color:#7EB8E8; text-transform:uppercase; letter-spacing:0.1em;">Kepada Yth,</span><br>'
            + f'<span style="font-family:\'Playfair Display\',serif; font-size:1.3rem; color:#F0E080; font-weight:700;">{nama_tamu_url} ✨</span>'
            + '</div>',
            unsafe_allow_html=True
        )

    # ── INFO WISUDAWAN ───────────────────────────────────
    st.markdown("""
    <div class="card" style="text-align:center;">
        <div style="font-size:0.78rem; color:#7EB8E8; letter-spacing:0.12em; text-transform:uppercase; margin-bottom:0.5rem; font-weight:700;">🌙 Wisudawan 🌙</div>
        <div style="font-family:'Playfair Display',serif; font-size:1.8rem; color:#E8F0FF; font-weight:700; line-height:1.3; text-shadow:0 0 20px rgba(120,160,255,0.3);">Muhammad Hamdan<br>Fadhlani, S.T.</div>
        <div style="margin-top:0.8rem; display:inline-block; background:rgba(30,50,120,0.7); color:#F0E080; padding:5px 16px; border-radius:20px; font-size:0.85rem; font-weight:700; border:1px solid rgba(240,224,128,0.3);">
            🎓 S1 Teknik Industri
        </div>
        <div style="font-size:0.88rem; color:#A8C8F0; margin-top:0.4rem; font-weight:600;">Universitas Andalas</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="divider">⭐ · · · ⭐</div>', unsafe_allow_html=True)

    # ── FOTO WISUDA ──────────────────────────────────────
    st.markdown('<p class="section-heading">📸 Foto Wisuda</p>', unsafe_allow_html=True)

    # Panel upload — hanya muncul jika URL valid DAN password benar
    is_owner = st.session_state.owner_url_valid and st.session_state.owner_unlocked

    if st.session_state.owner_url_valid:
        if not st.session_state.owner_unlocked:
            with st.expander("🔐 Panel Pemilik"):
                pw_input = st.text_input("Masukkan password", type="password", key="pw_input")
                if st.button("🔑 Masuk", key="btn_login"):
                    if pw_input == OWNER_PASSWORD:
                        st.session_state.owner_unlocked = True
                        st.rerun()
                    else:
                        st.error("❌ Password salah.")
        else:
            with st.expander("📤 Upload Foto Wisuda (Owner)", expanded=True):
                with st.form("upload_foto_form", clear_on_submit=True):
                    uploaded_files = st.file_uploader(
                        "Pilih foto-foto wisudamu",
                        type=["jpg", "jpeg", "png"],
                        accept_multiple_files=True,
                        key="foto_upload"
                    )
                    submit_foto = st.form_submit_button("📤 Upload Foto", use_container_width=True)
                if submit_foto:
                    if uploaded_files:
                        jumlah = upload_foto(uploaded_files, pengunggah="Hamdan")
                        st.success(f"✅ {jumlah} foto berhasil diupload!")
                        st.rerun()
                    else:
                        st.warning("⚠️ Pilih foto terlebih dahulu.")
                if st.button("🚪 Keluar dari panel owner", key="btn_logout"):
                    st.session_state.owner_unlocked = False
                    st.rerun()

    # Tampilkan foto dari disk
    photos_meta = muat_photos()
    if photos_meta:
        cols = st.columns(3)
        for i, meta in enumerate(photos_meta[:12]):
            filepath = os.path.join(PHOTOS_DIR, meta["filename"])
            if os.path.exists(filepath):
                with cols[i % 3]:
                    st.image(filepath, use_container_width=True)
        if len(photos_meta) > 12:
            st.markdown(
                f'<div style="text-align:center; color:#7EB8E8; font-size:0.82rem; margin-top:0.3rem;">+ {len(photos_meta)-12} foto lainnya</div>',
                unsafe_allow_html=True
            )
    else:
        st.markdown("""
        <div style="background:rgba(10,20,60,0.5); border-radius:16px; padding:2rem 1rem; text-align:center; border:1.5px dashed rgba(80,120,200,0.4); margin:0.5rem 0;">
            🌌<br>
            <span style="font-size:0.95rem; font-weight:700; color:#A8C8F0;">Belum ada foto</span><br>
            <span style="font-size:0.82rem; color:#6888B0;">Upload fotomu dan abadikan momen ini ✨</span>
        </div>
        """, unsafe_allow_html=True)

    # Credit fotografer
    st.markdown("""
    <div style="text-align:center; margin-top:0.8rem; margin-bottom:0.2rem;">
        <span style="font-size:0.82rem; color:#6888B0;">Photo by&nbsp;</span><svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#A8C8F0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle; margin-right:3px;"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1.5" fill="#A8C8F0" stroke="none"/></svg><a href="https://www.instagram.com/nine.moment" target="_blank" style="color:#A8C8F0; font-size:0.82rem; font-weight:700; text-decoration:none; letter-spacing:0.02em;">@nine.moment</a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="divider">🌙 · · · 🌙</div>', unsafe_allow_html=True)

    # ── INFO ACARA ───────────────────────────────────────
    st.markdown("""
    <div class="card">
        <div style="text-align:center; font-size:0.78rem; color:#7EB8E8; font-weight:700; letter-spacing:0.12em; text-transform:uppercase; margin-bottom:1rem;">✨ Detail Acara ✨</div>
        <div class="info-label">📅 Hari &amp; Tanggal</div>
        <div class="info-value">Minggu, 10 Mei 2026</div>
        <div class="info-label">🕐 Waktu</div>
        <div class="info-value">Pukul 14.00 WIB — Selesai</div>
        <div class="info-label">📍 Lokasi</div>
        <div class="info-value">Gedung Teknik Industri<br>
        <span style="font-size:0.88rem; color:#7EB8E8;">Universitas Andalas, Padang, Sumatera Barat</span></div>
    </div>
    """, unsafe_allow_html=True)

    # ── COUNTDOWN ────────────────────────────────────────
    wisuda_dt = datetime(2026, 5, 10, 14, 0, 0)

    @st.fragment(run_every=1)
    def tampilkan_countdown():
        now        = datetime.now()
        total_secs = int((wisuda_dt - now).total_seconds())
        if total_secs <= 0:
            st.markdown("""
            <div class="countdown-box">
                <div style="font-family:'Playfair Display',serif; font-size:1.6rem; color:#F0E080;">
                    🎉 Hari ini hari wisudanya! Selamat! 🎓
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
                <div class="countdown-title">🌙 Hitung Mundur Menuju Hari Wisuda 🌙</div>
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

    st.markdown('<div class="divider">⭐ · · · ⭐</div>', unsafe_allow_html=True)

    # ── PETA LOKASI ──────────────────────────────────────
    st.markdown('<p class="section-heading">📍 Lokasi Acara</p>', unsafe_allow_html=True)
    st.markdown("""
    <div style="border-radius:16px; overflow:hidden; border:1px solid rgba(100,140,220,0.3); margin-bottom:0.5rem;">
    <iframe
        src="https://maps.google.com/maps?q=Gedung+Teknik+Industri+Universitas+Andalas+Padang&output=embed"
        width="100%" height="280" style="border:0; display:block;"
        allowfullscreen="" loading="lazy">
    </iframe>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="divider">🌙 · · · 🌙</div>', unsafe_allow_html=True)

    # ── KUTIPAN ──────────────────────────────────────────
    st.markdown("""
    <div class="card">
        <div style="font-size:2rem; text-align:center; margin-bottom:0.8rem; opacity:0.6;">🌙</div>
        <div class="quote-text">
            "Setiap perjuangan panjang selalu berujung pada kebahagiaan.<br>
            Terima kasih telah menjadi bagian dari perjalanan ini. ✨"
        </div>
        <div style="text-align:center; margin-top:1rem; font-size:0.82rem; color:#6888B0;">&#8212; Muhammad Hamdan Fadhlani, S.T.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="divider">⭐ · · · ⭐</div>', unsafe_allow_html=True)

    # ── FORM UCAPAN & DOA ────────────────────────────────
    st.markdown('<p class="section-heading">💬 Kirim Ucapan &amp; Doa</p>', unsafe_allow_html=True)

    with st.form("ucapan_form", clear_on_submit=True):
        nama_pengirim = st.text_input("Nama Kamu", placeholder="Masukkan namamu")
        ucapan = st.text_area(
            "Ucapan & Doa untuk Hamdan",
            placeholder="Tuliskan ucapan dan doamu di sini... ✨",
            height=120
        )
        submitted = st.form_submit_button("🌟 Kirim Ucapan", use_container_width=True)

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
            st.success(f"✨ Terima kasih, **{nama_pengirim}**! Ucapanmu sudah terkirim.")
        else:
            st.warning("⚠️ Mohon isi nama dan ucapanmu terlebih dahulu.")

    daftar_ucapan = muat_ucapan()
    if daftar_ucapan:
        st.markdown(
            f'<div style="font-size:0.85rem; color:#7EB8E8; margin:0.8rem 0 0.4rem;">'
            f'🌟 {len(daftar_ucapan)} ucapan telah dikirimkan</div>',
            unsafe_allow_html=True
        )
        for u in daftar_ucapan[:20]:
            st.markdown(
                f'<div class="ucapan-item">'
                f'<div class="ucapan-nama">⭐ {u["nama"]}</div>'
                f'<div class="ucapan-teks">"{u["ucapan"]}"</div>'
                f'<div class="ucapan-waktu">🕐 {u.get("waktu", "")}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    # ── BACK & FOOTER ────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🌙 Kembali ke Halaman Awal"):
            st.session_state.page = "splash"
            st.rerun()

    st.markdown("""
    <div style="text-align:center; margin-top:1.5rem; padding:1rem; color:#6888B0; font-size:0.82rem;">
        Dibuat dengan ✨ untuk Muhammad Hamdan Fadhlani, S.T.<br>
        <span style="opacity:0.7;">Undangan digital — tidak ada kertas yang digunakan 🌿</span>
    </div>
    <div class="footer-stars">🌟 ✨ 🌙 ⭐ 🌙 ✨ 🌟</div>
    """, unsafe_allow_html=True)