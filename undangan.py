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

# ── Query params ──────────────────────────────────────
params = st.query_params
nama_tamu_url = params.get("tamu", "")

# ── Session state init ────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "splash"
if "owner_unlocked" not in st.session_state:
    st.session_state.owner_unlocked = False
if "musik_mulai" not in st.session_state:
    st.session_state.musik_mulai = False

# ── Owner auth ────────────────────────────────────────
OWNER_URL_KEY  = "hamdan2026"
OWNER_PASSWORD = "hamdan123"

if params.get("owner", "") == OWNER_URL_KEY:
    st.session_state.owner_url_valid = True
else:
    if "owner_url_valid" not in st.session_state:
        st.session_state.owner_url_valid = False

is_owner = st.session_state.owner_url_valid and st.session_state.owner_unlocked

# ── File & dir paths ──────────────────────────────────
UCAPAN_FILE = "ucapan.json"
MUSIC_FILE  = "music.mp3"
PHOTOS_FILE = "photos.json"
PHOTOS_DIR  = "foto_wisuda"
Path(PHOTOS_DIR).mkdir(exist_ok=True)

# ═════════════════════════════════════════════════════
# HELPERS
# ═════════════════════════════════════════════════════

def autoplay_audio(filepath: str):
    if not os.path.exists(filepath):
        return
    file_size = os.path.getsize(filepath)
    MAX_EMBED_SIZE = int(2.5 * 1024 * 1024)
    if file_size > MAX_EMBED_SIZE:
        st.caption("⚠️ File musik terlalu besar. Kompress MP3 ke < 2MB.")
        return
    with open(filepath, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    st.markdown(
        f'<audio id="bg-audio" autoplay loop preload="none" style="display:none;">'
        f'<source src="data:audio/mp3;base64,{b64}" type="audio/mp3">'
        f'</audio>',
        unsafe_allow_html=True
    )

def mute_button_html():
    return """
    <div style="position:fixed; bottom:18px; right:18px; z-index:9999;">
        <button id="mute-btn" onclick="
            var a=document.getElementById('bg-audio');
            if(a){ a.muted=!a.muted; this.textContent=a.muted ? '🔇' : '🔊'; }
        " style="background:rgba(99,102,241,0.85); color:#fff; border:1px solid rgba(167,139,250,0.5);
            border-radius:50%; width:44px; height:44px; font-size:1.1rem; cursor:pointer;
            box-shadow:0 2px 12px rgba(99,102,241,0.5); touch-action:manipulation;">
            🔊
        </button>
    </div>
    """

def muat_ucapan():
    if os.path.exists(UCAPAN_FILE):
        with open(UCAPAN_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def simpan_ucapan(data):
    with open(UCAPAN_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def muat_photos():
    if os.path.exists(PHOTOS_FILE):
        with open(PHOTOS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def simpan_photos(data):
    with open(PHOTOS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def upload_foto(uploaded_files, pengunggah="Hamdan"):
    photos = muat_photos()
    saved  = 0
    for uf in uploaded_files:
        ext      = uf.name.rsplit(".", 1)[-1].lower()
        ts       = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"{ts}.{ext}"
        filepath = os.path.join(PHOTOS_DIR, filename)
        with open(filepath, "wb") as f:
            f.write(uf.read())
        photos.insert(0, {
            "filename"  : filename,
            "pengunggah": pengunggah.strip() or "Hamdan",
            "waktu"     : datetime.now().strftime("%d %b %Y, %H:%M"),
        })
        saved += 1
    simpan_photos(photos)
    return saved

# ═════════════════════════════════════════════════════
# GLOBAL CSS — NIGHT SKY THEME
# ═════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Lato:wght@300;400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Lato', sans-serif;
    -webkit-text-size-adjust: 100%;
    text-size-adjust: 100%;
}

/* ── Night Sky Background ── */
.stApp {
    background: radial-gradient(ellipse at top, #0f0c29 0%, #1a1a2e 40%, #16213e 70%, #0f0c29 100%);
    min-height: 100vh;
}

/* Bintang-bintang statis */
.stApp::before { display: none; }

/* ── Animasi ── */
@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes twinkle {
    0%, 100% { opacity: 0.2; }
    50%       { opacity: 1; }
}
@keyframes shimmer {
    0%   { background-position: -200% center; }
    100% { background-position:  200% center; }
}

.anim-fade-up   { animation: fadeSlideUp .5s ease both; }
.anim-fade-up-2 { animation: fadeSlideUp .5s ease .1s both; }
.anim-fade-up-3 { animation: fadeSlideUp .5s ease .2s both; }
.anim-fade-up-4 { animation: fadeSlideUp .5s ease .3s both; }
.anim-fade-up-5 { animation: fadeSlideUp .5s ease .4s both; }
.anim-fade-in   { animation: fadeIn .8s ease both; }
.photo-s1 { animation: fadeSlideUp .5s ease both; }
.photo-s2 { animation: fadeSlideUp .5s ease .08s both; }
.photo-s3 { animation: fadeSlideUp .5s ease .16s both; }

/* ── Cards ── */
.card {
    background: rgba(255,255,255,0.05);
    border-radius: 20px;
    padding: 1.3rem 1.5rem;
    margin: .9rem 0;
    border: 1px solid rgba(167,139,250,0.25);
    box-shadow: 0 3px 30px rgba(99,102,241,0.15), inset 0 1px 0 rgba(255,255,255,0.05);
}

/* ── Form inputs ── */
label, .stTextInput label, .stTextArea label, .stFileUploader label {
    color: #A78BFA !important;
    font-weight: 600 !important;
}
.stTextInput input, .stTextArea textarea {
    background: rgba(255,255,255,0.07) !important;
    color: #E2E8F0 !important;
    border: 1.5px solid rgba(167,139,250,0.35) !important;
    border-radius: 12px !important;
    font-size: 16px !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    color: #F8FAFC !important;
    background: rgba(255,255,255,0.10) !important;
    border-color: rgba(167,139,250,0.7) !important;
}
.stTextInput input::placeholder, .stTextArea textarea::placeholder {
    color: #64748B !important;
    opacity: 1 !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #6366F1, #8B5CF6, #A78BFA);
    color: #FFFFFF !important;
    border: none;
    border-radius: 50px;
    padding: .75rem 2rem;
    font-size: 1rem;
    font-weight: 700;
    letter-spacing: .04em;
    cursor: pointer;
    width: 100%;
    transition: opacity .2s;
    box-shadow: 0 3px 20px rgba(99,102,241,0.45);
    -webkit-tap-highlight-color: transparent;
    touch-action: manipulation;
}
.stButton > button:hover  { opacity: .88; color: #FFFFFF !important; }
.stButton > button:active { opacity: .75; transform: scale(0.98); }

/* ── Info labels ── */
.info-label {
    font-size: .7rem;
    font-weight: 700;
    letter-spacing: .12em;
    color: #A78BFA;
    text-transform: uppercase;
    margin-bottom: 2px;
}
.info-value {
    font-family: 'Playfair Display', serif;
    font-size: 1rem;
    color: #E2E8F0;
    margin-bottom: .85rem;
    line-height: 1.5;
}

/* ── Countdown ── */
.countdown-box {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(167,139,250,0.30);
    border-radius: 18px;
    padding: 1.3rem .8rem;
    text-align: center;
    margin: .9rem 0;
    box-shadow: 0 3px 24px rgba(99,102,241,0.20);
}
.countdown-title {
    font-size: .75rem;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: #A78BFA;
    margin-bottom: .9rem;
    font-weight: 700;
}
.countdown-numbers {
    display: flex;
    justify-content: center;
    gap: .4rem;
    flex-wrap: nowrap;
    align-items: center;
}
.count-item { text-align: center; min-width: 52px; }
.count-num {
    font-family: 'Playfair Display', serif;
    font-size: 2.2rem;
    font-weight: 700;
    line-height: 1;
    display: block;
    background: linear-gradient(135deg, #A78BFA, #F9A8D4, #FBBF24);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 3s linear infinite;
}
.count-label {
    font-size: .58rem;
    letter-spacing: .08em;
    opacity: .85;
    text-transform: uppercase;
    color: #A78BFA;
    font-weight: 600;
}
.count-sep {
    font-size: 1.8rem;
    color: #7C3AED;
    opacity: .6;
    padding-bottom: 10px;
}

/* ── Misc ── */
.divider { text-align: center; font-size: 1.1rem; margin: .4rem 0; opacity: .6; }
.quote-text {
    font-family: 'Playfair Display', serif;
    font-style: italic;
    font-size: .95rem;
    color: #CBD5E1;
    text-align: center;
    line-height: 1.8;
}
.section-heading {
    font-family: 'Playfair Display', serif;
    font-size: 1.15rem;
    background: linear-gradient(90deg, #A78BFA, #F9A8D4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 1rem 0 .5rem;
}

/* ── Night sky title gradient ── */
.night-title {
    background: linear-gradient(135deg, #A78BFA 0%, #F9A8D4 45%, #FBBF24 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* ── Moon ── */
.moon {
    display: inline-block;
    width: 62px; height: 62px;
    border-radius: 50%;
    background: radial-gradient(circle at 35% 35%, #FFF9C4, #FCD34D 45%, #F59E0B 80%);
    box-shadow: 0 0 18px rgba(251,191,36,.8), 0 0 50px rgba(251,191,36,.3), 0 0 80px rgba(251,191,36,.1);
    margin: 0 auto .9rem;
}

/* ── Stars decorative ── */
.stars-deco {
    position: fixed; top: 0; left: 0; right: 0; bottom: 0;
    pointer-events: none; z-index: 0;
    background-image:
        radial-gradient(1.5px 1.5px at  5%  8%, rgba(255,255,255,.9) 100%, transparent),
        radial-gradient(1px   1px   at 12% 15%, rgba(255,255,255,.7) 100%, transparent),
        radial-gradient(2px   2px   at 20%  5%, rgba(255,255,255,.8) 100%, transparent),
        radial-gradient(1px   1px   at 30% 20%, rgba(255,255,255,.6) 100%, transparent),
        radial-gradient(1.5px 1.5px at 40%  3%, rgba(255,255,255,.9) 100%, transparent),
        radial-gradient(1px   1px   at 50% 12%, rgba(255,255,255,.7) 100%, transparent),
        radial-gradient(2px   2px   at 58%  7%, rgba(255,255,255,.8) 100%, transparent),
        radial-gradient(1px   1px   at 65% 18%, rgba(255,255,255,.6) 100%, transparent),
        radial-gradient(1.5px 1.5px at 72%  2%, rgba(255,255,255,.9) 100%, transparent),
        radial-gradient(1px   1px   at 80% 14%, rgba(255,255,255,.7) 100%, transparent),
        radial-gradient(2px   2px   at 88%  9%, rgba(255,255,255,.8) 100%, transparent),
        radial-gradient(1px   1px   at 95% 22%, rgba(255,255,255,.6) 100%, transparent),
        radial-gradient(1.5px 1.5px at 15% 35%, rgba(255,255,255,.5) 100%, transparent),
        radial-gradient(1px   1px   at 25% 42%, rgba(255,255,255,.4) 100%, transparent),
        radial-gradient(2px   2px   at 35% 30%, rgba(255,255,255,.6) 100%, transparent),
        radial-gradient(1px   1px   at 45% 48%, rgba(255,255,255,.5) 100%, transparent),
        radial-gradient(1.5px 1.5px at 55% 38%, rgba(255,255,255,.7) 100%, transparent),
        radial-gradient(1px   1px   at 75% 45%, rgba(255,255,255,.4) 100%, transparent),
        radial-gradient(2px   2px   at 85% 32%, rgba(255,255,255,.6) 100%, transparent),
        radial-gradient(1px   1px   at 92% 50%, rgba(255,255,255,.5) 100%, transparent),
        /* Bintang warna ungu/pink */
        radial-gradient(2px 2px at 18% 25%, rgba(167,139,250,.9) 100%, transparent),
        radial-gradient(2px 2px at 62% 10%, rgba(249,168,212,.9) 100%, transparent),
        radial-gradient(2px 2px at 78% 28%, rgba(251,191,36,.8)  100%, transparent);
}

/* ── Splash card ── */
.splash-card {
    background: rgba(255,255,255,0.05);
    border-radius: 24px;
    padding: 2.2rem 1.5rem;
    border: 1px solid rgba(167,139,250,.25);
    text-align: center;
    box-shadow: 0 8px 40px rgba(99,102,241,.20), inset 0 1px 0 rgba(255,255,255,.07);
}

/* ── Footer ── */
.footer-stars {
    text-align: center;
    font-size: 1.2rem;
    padding: 1rem;
    letter-spacing: .25rem;
    opacity: .7;
}

/* ── Ucapan items ── */
.ucapan-item {
    background: rgba(255,255,255,0.04);
    border-left: 3px solid #7C3AED;
    border-radius: 12px;
    padding: .85rem 1rem;
    margin-bottom: .65rem;
    border-top: 1px solid rgba(167,139,250,.15);
    border-right: 1px solid rgba(167,139,250,.15);
    border-bottom: 1px solid rgba(167,139,250,.15);
    animation: fadeSlideUp .5s ease both;
    box-shadow: 0 2px 10px rgba(99,102,241,.10);
}
.ucapan-nama  { font-weight: 700; color: #A78BFA; font-size: .88rem; margin-bottom: .2rem; }
.ucapan-teks  { color: #CBD5E1; font-size: .9rem; line-height: 1.6; font-style: italic; }
.ucapan-waktu { font-size: .72rem; color: #6D28D9; margin-top: .25rem; }

.ucapan-locked {
    background: rgba(255,255,255,0.04);
    border: 1.5px dashed rgba(167,139,250,.30);
    border-radius: 14px;
    padding: 1.3rem 1rem;
    text-align: center;
    margin: .5rem 0;
}

/* ── Mobile fixes ── */
@media (max-width: 480px) {
    .stImage img { border-radius: 10px; }
    h1 { font-size: 1.6rem !important; }
    .count-num { font-size: 1.8rem; }
    .count-item { min-width: 42px; }
    .count-sep { font-size: 1.4rem; }
    .stButton > button { padding: .85rem 1.5rem; min-height: 48px; }
}
</style>
""", unsafe_allow_html=True)

# Bintang-bintang dekoratif
st.markdown('<div class="stars-deco"></div>', unsafe_allow_html=True)


# ═════════════════════════════════════════════════════
# SPLASH PAGE
# ═════════════════════════════════════════════════════
if st.session_state.page == "splash":

    st.markdown(
        '<div class="anim-fade-in" style="text-align:center;font-size:1.6rem;letter-spacing:.3rem;margin-bottom:.8rem;opacity:.85;">'
        '⭐ 🌙 ✨ 🌙 ⭐</div>',
        unsafe_allow_html=True
    )

    sapaan = ""
    if nama_tamu_url:
        sapaan = (
            '<div style="font-size:.82rem;color:#A78BFA;margin-bottom:.35rem;font-style:italic;">Kepada Yth,</div>'
            f'<div style="font-family:\'Playfair Display\',serif;font-size:1.4rem;'
            f'background:linear-gradient(90deg,#A78BFA,#F9A8D4);'
            f'-webkit-background-clip:text;-webkit-text-fill-color:transparent;'
            f'background-clip:text;font-weight:700;margin-bottom:1.1rem;">{nama_tamu_url} ✨</div>'
        )

    isi_splash = (
        '<div class="splash-card anim-fade-up">'
        + '<div class="moon"></div>'
        + sapaan
        + '<div style="font-size:.75rem;font-weight:700;color:#A78BFA;letter-spacing:.18em;text-transform:uppercase;margin-bottom:.7rem;">&#127891; Undangan Wisuda</div>'
        + '<div class="night-title" style="font-family:\'Playfair Display\',serif;font-size:1.75rem;font-weight:700;line-height:1.3;margin-bottom:.35rem;">Muhammad Hamdan<br>Fadhlani, S.T.</div>'
        + '<div style="font-family:\'Playfair Display\',serif;font-style:italic;font-size:.9rem;color:#A78BFA;margin-bottom:1.1rem;">Sarjana Teknik &#8212; Teknik Industri</div>'
        + '<div style="font-size:.85rem;background:linear-gradient(90deg,#A78BFA,#F9A8D4);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin-bottom:.25rem;font-weight:700;">&#128197; Minggu, 10 Mei 2026</div>'
        + '<div style="font-size:.85rem;color:#7C3AED;margin-bottom:1.2rem;font-weight:600;">&#128205; Gedung Teknik Industri, Unand</div>'
        + '<div style="font-size:.8rem;color:#94A3B8;font-style:italic;margin-bottom:1.5rem;line-height:1.6;">&#8220;Di bawah langit malam yang penuh bintang,<br>perjalananmu kini sampai di puncaknya &#11088;&#8221;</div>'
        + '</div>'
    )
    st.markdown(isi_splash, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🌙 Buka Undangan", key="btn_buka", use_container_width=True):
            st.session_state.page = "main"
            st.session_state.musik_mulai = True
            st.rerun()

    st.markdown('<div class="footer-stars anim-fade-in">⭐ 🌙 ✨ 🌌 ✨ 🌙 ⭐</div>', unsafe_allow_html=True)


# ═════════════════════════════════════════════════════
# MAIN PAGE
# ═════════════════════════════════════════════════════
elif st.session_state.page == "main":

    if st.session_state.musik_mulai:
        autoplay_audio(MUSIC_FILE)
        st.markdown(mute_button_html(), unsafe_allow_html=True)

    # ── HEADER ──────────────────────────────────────
    st.markdown(
        '<div class="anim-fade-in" style="text-align:center;font-size:1.3rem;padding:1rem 0 .2rem;letter-spacing:.3rem;opacity:.8;">'
        '⭐ 🌙 ✨ 🌙 ⭐</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<h1 class="night-title anim-fade-up" style="font-family:Playfair Display,serif;font-size:2rem;text-align:center;line-height:1.2;margin:.3rem 0;">Undangan Wisuda</h1>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<p class="anim-fade-up-2" style="font-family:Playfair Display,serif;font-style:italic;font-size:.88rem;color:#A78BFA;text-align:center;margin-bottom:.8rem;">Di bawah langit malam yang penuh bintang, merayakan pencapaianmu &#11088;</p>',
        unsafe_allow_html=True
    )

    if nama_tamu_url:
        st.markdown(
            '<div class="anim-fade-up-3" style="text-align:center;background:rgba(255,255,255,0.04);border-radius:14px;padding:.7rem 1rem;margin-bottom:.5rem;border:1px solid rgba(167,139,250,.25);">'
            '<span style="font-size:.75rem;color:#A78BFA;text-transform:uppercase;letter-spacing:.08em;">Kepada Yth,</span><br>'
            f'<span style="font-family:\'Playfair Display\',serif;font-size:1.2rem;background:linear-gradient(90deg,#A78BFA,#F9A8D4);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;font-weight:700;">{nama_tamu_url} ✨</span>'
            '</div>',
            unsafe_allow_html=True
        )

    # ── INFO WISUDAWAN ───────────────────────────────
    st.markdown("""
    <div class="card anim-fade-up-2" style="text-align:center;">
        <div style="font-size:.75rem;color:#A78BFA;letter-spacing:.1em;text-transform:uppercase;margin-bottom:.5rem;font-weight:700;">&#11088; Wisudawan &#11088;</div>
        <div class="night-title" style="font-family:'Playfair Display',serif;font-size:1.65rem;font-weight:700;line-height:1.3;">Muhammad Hamdan<br>Fadhlani, S.T.</div>
        <div style="margin-top:.7rem;display:inline-block;background:rgba(167,139,250,0.15);color:#A78BFA;padding:4px 14px;border-radius:20px;font-size:.82rem;font-weight:700;border:1px solid rgba(167,139,250,.35);">
            &#127891; S1 Teknik Industri
        </div>
        <div style="font-size:.85rem;color:#7C3AED;margin-top:.35rem;font-weight:600;">Universitas Andalas</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="divider">⭐ · · · 🌙 · · · ⭐</div>', unsafe_allow_html=True)

    # ── OWNER PANEL ─────────────────────────────────
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

    # ── GRID FOTO ───────────────────────────────────
    photos_meta = muat_photos()
    if photos_meta:
        cols        = st.columns(3)
        stagger_cls = ["photo-s1", "photo-s2", "photo-s3"]
        for i, meta in enumerate(photos_meta[:12]):
            filepath = os.path.join(PHOTOS_DIR, meta["filename"])
            if os.path.exists(filepath):
                with cols[i % 3]:
                    st.markdown(f'<div class="{stagger_cls[i % 3]}" style="border-radius:10px;overflow:hidden;">', unsafe_allow_html=True)
                    st.image(filepath, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
        if len(photos_meta) > 12:
            st.markdown(
                f'<div style="text-align:center;color:#A78BFA;font-size:.8rem;margin-top:.25rem;">+ {len(photos_meta)-12} foto lainnya</div>',
                unsafe_allow_html=True
            )
    else:
        st.markdown("""
        <div style="background:rgba(255,255,255,0.04);border-radius:14px;padding:1.8rem 1rem;text-align:center;border:1.5px dashed rgba(167,139,250,.30);margin:.5rem 0;">
            &#11088;<br>
            <span style="font-size:.9rem;font-weight:700;color:#A78BFA;">Belum ada foto</span><br>
            <span style="font-size:.8rem;color:#7C3AED;">Upload fotomu dan abadikan momen ini ✨</span>
        </div>
        """, unsafe_allow_html=True)

    # Credit fotografer
    st.markdown("""
    <div style="text-align:center;margin-top:.7rem;margin-bottom:.2rem;">
        <span style="font-size:.8rem;color:#7C3AED;">Photo by&nbsp;</span>
        <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none"
            stroke="#A78BFA" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
            style="vertical-align:middle;margin-right:2px;">
            <rect x="2" y="2" width="20" height="20" rx="5" ry="5"/>
            <circle cx="12" cy="12" r="4"/>
            <circle cx="17.5" cy="6.5" r="1.5" fill="#A78BFA" stroke="none"/>
        </svg>
        <a href="https://www.instagram.com/nine.moment" target="_blank"
            style="color:#A78BFA;font-size:.8rem;font-weight:700;text-decoration:none;">@nine.moment</a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="divider">✨ · · · 🌌 · · · ✨</div>', unsafe_allow_html=True)

    # ── INFO ACARA ───────────────────────────────────
    st.markdown("""
    <div class="card anim-fade-up">
        <div style="text-align:center;font-size:.75rem;color:#A78BFA;font-weight:700;letter-spacing:.1em;text-transform:uppercase;margin-bottom:.9rem;">&#11088; Detail Acara &#11088;</div>
        <div class="info-label">&#128197; Hari &amp; Tanggal</div>
        <div class="info-value">Minggu, 10 Mei 2026</div>
        <div class="info-label">&#128336; Waktu</div>
        <div class="info-value">Pukul 14.00 WIB &#8212; Selesai</div>
        <div class="info-label">&#128205; Lokasi</div>
        <div class="info-value">Gedung Teknik Industri<br>
            <span style="font-size:.85rem;color:#7C3AED;">Universitas Andalas, Padang, Sumatera Barat</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── COUNTDOWN REAL-TIME ──────────────────────────
    wisuda_dt = datetime(2026, 5, 10, 14, 0, 0)

    @st.fragment(run_every=1)
    def tampilkan_countdown():
        now        = datetime.now()
        total_secs = int((wisuda_dt - now).total_seconds())
        if total_secs <= 0:
            st.markdown("""
            <div class="countdown-box">
                <div style="font-family:'Playfair Display',serif;font-size:1.5rem;
                    background:linear-gradient(90deg,#A78BFA,#F9A8D4);
                    -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">
                    &#127881; Hari ini hari wisudanya! Selamat! &#127891;
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            days    = total_secs // 86400
            hours   = (total_secs % 86400) // 3600
            minutes = (total_secs % 3600) // 60
            seconds = total_secs % 60
            st.markdown(f"""
            <div class="countdown-box anim-fade-up">
                <div class="countdown-title">&#11088; Hitung Mundur Menuju Hari Wisuda &#11088;</div>
                <div class="countdown-numbers">
                    <div class="count-item"><span class="count-num">{days:02d}</span><span class="count-label">Hari</span></div>
                    <div class="count-sep">:</div>
                    <div class="count-item"><span class="count-num">{hours:02d}</span><span class="count-label">Jam</span></div>
                    <div class="count-sep">:</div>
                    <div class="count-item"><span class="count-num">{minutes:02d}</span><span class="count-label">Menit</span></div>
                    <div class="count-sep">:</div>
                    <div class="count-item"><span class="count-num">{seconds:02d}</span><span class="count-label">Detik</span></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    tampilkan_countdown()

    st.markdown('<div class="divider">🌙 · · · 🌙</div>', unsafe_allow_html=True)

    # ── PETA LOKASI ──────────────────────────────────
    st.markdown('<p class="section-heading anim-fade-up">&#128205; Lokasi Acara</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="anim-fade-up-2" style="border-radius:14px;overflow:hidden;border:1px solid rgba(167,139,250,.25);margin-bottom:.5rem;">
        <iframe
            src="https://maps.google.com/maps?q=Gedung+Teknik+Industri+Universitas+Andalas+Padang&output=embed"
            width="100%" height="240"
            style="border:0;display:block;"
            allowfullscreen=""
            loading="lazy"
            referrerpolicy="no-referrer-when-downgrade">
        </iframe>
    </div>
    <div style="text-align:center;margin-top:.3rem;">
        <a href="https://maps.google.com/?q=Gedung+Teknik+Industri+Universitas+Andalas+Padang"
            target="_blank" rel="noopener"
            style="font-size:.8rem;color:#A78BFA;font-weight:700;text-decoration:none;">
            &#128506;&#65039; Buka di Google Maps &#8594;
        </a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="divider">✨ · · · ✨</div>', unsafe_allow_html=True)

    # ── KUTIPAN ──────────────────────────────────────
    st.markdown("""
    <div class="card anim-fade-up">
        <div style="font-size:1.8rem;text-align:center;margin-bottom:.7rem;opacity:.8;">🌙</div>
        <div class="quote-text">
            &#8220;Setiap perjuangan panjang selalu berujung pada kebahagiaan.<br>
            Terima kasih telah menjadi bagian dari perjalanan ini. &#11088;&#8221;
        </div>
        <div style="text-align:center;margin-top:.9rem;font-size:.8rem;color:#7C3AED;">&#8212; Muhammad Hamdan Fadhlani, S.T.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="divider">⭐ · · · ⭐</div>', unsafe_allow_html=True)

    # ── UCAPAN & DOA ─────────────────────────────────
    st.markdown('<p class="section-heading anim-fade-up">&#128172; Kirim Ucapan &amp; Doa</p>', unsafe_allow_html=True)

    with st.form("ucapan_form", clear_on_submit=True):
        nama_pengirim = st.text_input("Nama Kamu", placeholder="Masukkan namamu")
        ucapan_text   = st.text_area(
            "Ucapan & Doa untuk Hamdan",
            placeholder="Tuliskan ucapan dan doamu di sini... ✨",
            height=110
        )
        submitted = st.form_submit_button("&#11088; Kirim Ucapan", use_container_width=True)

    if submitted:
        if nama_pengirim.strip() and ucapan_text.strip():
            daftar = muat_ucapan()
            daftar.insert(0, {
                "nama"  : nama_pengirim.strip(),
                "ucapan": ucapan_text.strip(),
                "waktu" : datetime.now().strftime("%d %b %Y, %H:%M"),
            })
            simpan_ucapan(daftar)
            st.balloons()
            st.success(f"✨ Terima kasih, **{nama_pengirim}**! Ucapanmu sudah terkirim.")
        else:
            st.warning("⚠️ Mohon isi nama dan ucapanmu terlebih dahulu.")

    # ── TAMPILAN UCAPAN ──────────────────────────────
    daftar_ucapan = muat_ucapan()
    jumlah_ucapan = len(daftar_ucapan)

    if is_owner:
        if jumlah_ucapan > 0:
            st.markdown(
                f'<div style="font-size:.83rem;color:#A78BFA;margin:.7rem 0 .4rem;">'
                f'&#11088; {jumlah_ucapan} ucapan telah dikirimkan</div>',
                unsafe_allow_html=True
            )
            for u in daftar_ucapan[:50]:
                st.markdown(
                    f'<div class="ucapan-item">'
                    f'<div class="ucapan-nama">&#11088; {u["nama"]}</div>'
                    f'<div class="ucapan-teks">"{u["ucapan"]}"</div>'
                    f'<div class="ucapan-waktu">&#128336; {u.get("waktu", "")}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
        else:
            st.markdown(
                '<div style="text-align:center;color:#A78BFA;font-size:.86rem;margin:.7rem 0;">Belum ada ucapan masuk.</div>',
                unsafe_allow_html=True
            )
    else:
        if jumlah_ucapan > 0:
            st.markdown(
                f'<div class="ucapan-locked">'
                f'<div style="font-size:1.4rem;margin-bottom:.35rem;">&#128274;</div>'
                f'<div style="font-weight:700;color:#A78BFA;font-size:.92rem;margin-bottom:.25rem;">'
                f'{jumlah_ucapan} ucapan telah dikirimkan</div>'
                f'<div style="font-size:.8rem;color:#7C3AED;">Ucapan bersifat pribadi dan hanya dapat dilihat oleh pemilik undangan &#11088;</div>'
                f'</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<div class="ucapan-locked">'
                '<div style="font-size:1.4rem;margin-bottom:.35rem;">&#128172;</div>'
                '<div style="font-size:.85rem;color:#7C3AED;">Jadilah yang pertama mengirim ucapan! ✨</div>'
                '</div>',
                unsafe_allow_html=True
            )

    # ── BACK & FOOTER ────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🌙 Kembali ke Halaman Awal", key="btn_back", use_container_width=True):
            st.session_state.page = "splash"
            st.rerun()

    st.markdown("""
    <div class="anim-fade-up" style="text-align:center;margin-top:1.5rem;padding:1rem 1rem .5rem;">
        <div style="font-family:'Playfair Display',serif;font-size:1.05rem;color:#CBD5E1;font-style:italic;line-height:1.8;margin-bottom:.5rem;">
            &#11088; Kehadiranmu sangat berarti bagiku &#11088;<br>
            <span style="font-size:.95rem;color:#A78BFA;">See you at Gedung Teknik Industri, Unand</span><br>
            <span style="font-size:.85rem;color:#7C3AED;">Minggu, 10 Mei 2026 &#8212; Pukul 14.00 WIB &#127769;</span>
        </div>
        <div style="margin-top:.7rem;">
            <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none"
                stroke="#A78BFA" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                style="vertical-align:middle;margin-right:3px;">
                <rect x="2" y="2" width="20" height="20" rx="5" ry="5"/>
                <circle cx="12" cy="12" r="4"/>
                <circle cx="17.5" cy="6.5" r="1.5" fill="#A78BFA" stroke="none"/>
            </svg>
            <a href="https://www.instagram.com/hamdanfdhlani" target="_blank" rel="noopener"
                style="color:#A78BFA;font-size:.85rem;font-weight:700;text-decoration:none;letter-spacing:.02em;">
                @hamdanfdhlani
            </a>
        </div>
    </div>
    <div class="footer-stars">⭐ 🌙 ✨ 🌌 ✨ 🌙 ⭐</div>
    """, unsafe_allow_html=True)