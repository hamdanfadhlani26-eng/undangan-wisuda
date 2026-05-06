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
if "musik_mulai" not in st.session_state:
    st.session_state.musik_mulai = False

OWNER_URL_KEY = "hamdan2026"
OWNER_PASSWORD = "hamdan123"

if params.get("owner", "") == OWNER_URL_KEY:
    st.session_state.owner_url_valid = True
else:
    if "owner_url_valid" not in st.session_state:
        st.session_state.owner_url_valid = False

UCAPAN_FILE = "ucapan.json"
MUSIC_FILE  = "music.mp3"

def autoplay_audio(filepath: str):
    if not os.path.exists(filepath):
        return
    with open(filepath, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    st.markdown(
        f'<audio autoplay loop style="display:none;">\n'
        f'  <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">\n'
        f'</audio>',
        unsafe_allow_html=True
    )

def mute_button_html():
    return """
    <div style="position:fixed; bottom:18px; right:18px; z-index:9999;">
        <button id="mute-btn" onclick="
            var a=document.querySelector('audio');
            if(a){ a.muted=!a.muted; this.textContent=a.muted ? '🔇' : '🔊'; }
        " style="background:rgba(20,10,50,0.85); color:#C084FC; border:1px solid rgba(192,132,252,0.5);
            border-radius:50%; width:40px; height:40px; font-size:1.1rem; cursor:pointer;">
            🔊
        </button>
    </div>
    """

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
    if os.path.exists(PHOTOS_FILE):
        with open(PHOTOS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def simpan_photos(data):
    with open(PHOTOS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def upload_foto(uploaded_files, pengunggah="Tamu"):
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

# ════════════════════════════════════════════════════════
# GLOBAL CSS — Sky & Fresh Theme (cheerful, light)
# ════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Lato:wght@300;400;700&display=swap');

html, body, [class*="css"] { font-family: 'Lato', sans-serif; }

/* ── Sky animated background ── */
@keyframes sky-shift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.stApp {
    background: linear-gradient(
        135deg,
        #E0F7FF 0%,
        #B3ECFF 15%,
        #D4F5E9 30%,
        #FFF0F8 50%,
        #B3ECFF 65%,
        #E8F4FF 80%,
        #D4F5E9 90%,
        #E0F7FF 100%
    );
    background-size: 400% 400%;
    animation: sky-shift 20s ease infinite;
    min-height: 100vh;
}

/* ── Floating bubbles / confetti dots ── */
@keyframes float-up {
    0%   { transform: translateY(0px)   scale(1);   opacity: 0.7; }
    50%  { transform: translateY(-18px) scale(1.1); opacity: 1;   }
    100% { transform: translateY(0px)   scale(1);   opacity: 0.7; }
}
@keyframes float-up-2 {
    0%   { transform: translateY(0px)   scale(1);   opacity: 0.5; }
    50%  { transform: translateY(-22px) scale(1.15); opacity: 0.9; }
    100% { transform: translateY(0px)   scale(1);   opacity: 0.5; }
}

.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image:
        /* Sky-blue dots */
        radial-gradient(6px 6px at 8%   12%, rgba(56,189,248,0.55)  100%, transparent),
        radial-gradient(4px 4px at 22%  30%, rgba(56,189,248,0.40)  100%, transparent),
        radial-gradient(8px 8px at 68%   6%, rgba(56,189,248,0.50)  100%, transparent),
        /* Mint-green dots */
        radial-gradient(5px 5px at 38%   8%, rgba(52,211,153,0.55)  100%, transparent),
        radial-gradient(7px 7px at 83%  25%, rgba(52,211,153,0.45)  100%, transparent),
        radial-gradient(4px 4px at 55%  18%, rgba(52,211,153,0.50)  100%, transparent),
        /* Pink dots */
        radial-gradient(5px 5px at 15%  42%, rgba(249,168,212,0.60) 100%, transparent),
        radial-gradient(8px 8px at 75%  55%, rgba(249,168,212,0.50) 100%, transparent),
        radial-gradient(4px 4px at 90%  40%, rgba(249,168,212,0.55) 100%, transparent),
        /* Yellow dots */
        radial-gradient(6px 6px at 30%  58%, rgba(252,211,77,0.55)  100%, transparent),
        radial-gradient(4px 4px at 60%  48%, rgba(252,211,77,0.45)  100%, transparent),
        radial-gradient(7px 7px at 48%  72%, rgba(252,211,77,0.50)  100%, transparent),
        /* Lavender dots */
        radial-gradient(5px 5px at  5%  68%, rgba(196,181,253,0.55) 100%, transparent),
        radial-gradient(6px 6px at 88%  80%, rgba(196,181,253,0.50) 100%, transparent),
        radial-gradient(4px 4px at 25%  82%, rgba(196,181,253,0.45) 100%, transparent),
        /* Peach dots */
        radial-gradient(7px 7px at 70%  88%, rgba(253,186,116,0.50) 100%, transparent),
        radial-gradient(5px 5px at 42%  92%, rgba(253,186,116,0.45) 100%, transparent),
        radial-gradient(4px 4px at 95%  95%, rgba(253,186,116,0.40) 100%, transparent);
    opacity: 0.9;
    pointer-events: none;
    z-index: 0;
    animation: float-up 5s ease-in-out infinite, float-up-2 7s ease-in-out infinite 2s;
}

/* ── Fade-in & slide-up animations ── */
@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(28px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}
@keyframes fadeSlideUp-stagger-1 {
    0%,10% { opacity: 0; transform: translateY(24px); }
    100%   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeSlideUp-stagger-2 {
    0%,25% { opacity: 0; transform: translateY(24px); }
    100%   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeSlideUp-stagger-3 {
    0%,40% { opacity: 0; transform: translateY(24px); }
    100%   { opacity: 1; transform: translateY(0); }
}

.anim-fade-up   { animation: fadeSlideUp 0.7s ease both; }
.anim-fade-up-2 { animation: fadeSlideUp 0.7s ease 0.15s both; }
.anim-fade-up-3 { animation: fadeSlideUp 0.7s ease 0.30s both; }
.anim-fade-up-4 { animation: fadeSlideUp 0.7s ease 0.45s both; }
.anim-fade-up-5 { animation: fadeSlideUp 0.7s ease 0.60s both; }
.anim-fade-in   { animation: fadeIn 1s ease both; }

/* Photo grid stagger */
.photo-s1 { animation: fadeSlideUp-stagger-1 0.8s ease both; }
.photo-s2 { animation: fadeSlideUp-stagger-2 0.8s ease both; }
.photo-s3 { animation: fadeSlideUp-stagger-3 0.8s ease both; }

/* ── Shared card ── */
.card {
    background: rgba(255,255,255,0.75);
    border-radius: 24px;
    padding: 1.5rem 1.8rem;
    margin: 1rem 0;
    border: 1px solid rgba(56,189,248,0.30);
    box-shadow: 0 4px 32px rgba(56,189,248,0.15), inset 0 1px 0 rgba(255,255,255,0.9);
    backdrop-filter: blur(10px);
}

/* ── Labels / form ── */
label, .stTextInput label, .stTextArea label, .stFileUploader label {
    color: #0369A1 !important;
    font-weight: 600 !important;
}

/* Input fields */
.stTextInput input, .stTextArea textarea {
    background: rgba(255,255,255,0.9) !important;
    color: #0F172A !important;
    border: 1.5px solid rgba(56,189,248,0.4) !important;
    border-radius: 12px !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #0EA5E9, #38BDF8, #34D399);
    color: #FFFFFF !important;
    border: none;
    border-radius: 50px;
    padding: 0.7rem 2rem;
    font-size: 1rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    cursor: pointer;
    width: 100%;
    transition: all 0.25s;
    box-shadow: 0 4px 20px rgba(14,165,233,0.35);
}
.stButton > button:hover {
    background: linear-gradient(135deg, #0284C7, #0EA5E9, #10B981);
    color: #FFFFFF !important;
    box-shadow: 0 6px 28px rgba(14,165,233,0.5);
    transform: translateY(-1px);
}

/* ── Info labels ── */
.info-label {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    color: #0284C7;
    text-transform: uppercase;
    margin-bottom: 2px;
}
.info-value {
    font-family: 'Playfair Display', serif;
    font-size: 1.05rem;
    color: #0F172A;
    margin-bottom: 0.9rem;
    line-height: 1.5;
}

/* ── Countdown ── */
.countdown-box {
    background: linear-gradient(135deg, rgba(224,247,255,0.9), rgba(212,245,233,0.9), rgba(255,240,248,0.9));
    border: 1.5px solid rgba(56,189,248,0.40);
    border-radius: 20px;
    padding: 1.5rem 1rem;
    text-align: center;
    margin: 1rem 0;
    box-shadow: 0 4px 30px rgba(56,189,248,0.20);
    backdrop-filter: blur(6px);
}
.countdown-title {
    font-size: 0.78rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #0284C7;
    margin-bottom: 1rem;
    font-weight: 700;
}
.countdown-numbers {
    display: flex;
    justify-content: center;
    gap: 0.5rem;
    flex-wrap: nowrap;
    align-items: center;
}
.count-item  { text-align: center; min-width: 55px; }
.count-num {
    font-family: 'Playfair Display', serif;
    font-size: 2.4rem;
    font-weight: 700;
    line-height: 1;
    display: block;
    background: linear-gradient(135deg, #0EA5E9, #F472B6, #34D399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.count-label {
    font-size: 0.62rem;
    letter-spacing: 0.1em;
    opacity: 0.85;
    text-transform: uppercase;
    color: #0284C7;
    font-weight: 600;
}
.count-sep {
    font-size: 2rem;
    color: #38BDF8;
    opacity: 0.6;
    padding-bottom: 12px;
}

/* ── Misc ── */
.divider {
    text-align: center;
    font-size: 1.2rem;
    margin: 0.4rem 0;
    opacity: 0.8;
}
.quote-text {
    font-family: 'Playfair Display', serif;
    font-style: italic;
    font-size: 1rem;
    color: #0F172A;
    text-align: center;
    line-height: 1.8;
}
.section-heading {
    font-family: 'Playfair Display', serif;
    font-size: 1.2rem;
    background: linear-gradient(90deg, #0EA5E9, #10B981);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 1.2rem 0 0.6rem;
}

/* ── Splash card ── */
.splash-card {
    background: rgba(255,255,255,0.80);
    border-radius: 28px;
    padding: 2.5rem 1.8rem;
    border: 1px solid rgba(56,189,248,0.35);
    box-shadow: 0 8px 50px rgba(56,189,248,0.20), inset 0 1px 0 rgba(255,255,255,0.95);
    text-align: center;
    backdrop-filter: blur(12px);
}

/* ── Sun / cheerful orb replacing moon ── */
.moon {
    display: inline-block;
    width: 64px; height: 64px;
    border-radius: 50%;
    background: radial-gradient(circle at 35% 35%, #FFF9C4, #FCD34D 45%, #F59E0B 80%);
    box-shadow: 0 0 20px rgba(251,191,36,0.8), 0 0 50px rgba(251,191,36,0.4), 0 0 90px rgba(251,191,36,0.15);
    position: relative;
    margin: 0 auto 0.8rem;
}

/* ── Footer ── */
.footer-stars {
    text-align: center;
    font-size: 1.3rem;
    padding: 1rem;
    letter-spacing: 0.3rem;
    opacity: 0.8;
}

/* ── Ucapan items ── */
.ucapan-item {
    background: rgba(255,255,255,0.80);
    border-left: 3px solid #38BDF8;
    border-radius: 12px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.75rem;
    border-top: 1px solid rgba(56,189,248,0.20);
    border-right: 1px solid rgba(56,189,248,0.20);
    border-bottom: 1px solid rgba(56,189,248,0.20);
    animation: fadeSlideUp 0.6s ease both;
    box-shadow: 0 2px 12px rgba(56,189,248,0.10);
}
.ucapan-nama {
    font-weight: 700;
    color: #0284C7;
    font-size: 0.9rem;
    margin-bottom: 0.25rem;
}
.ucapan-teks {
    color: #1E3A5F;
    font-size: 0.93rem;
    line-height: 1.6;
    font-style: italic;
}
.ucapan-waktu {
    font-size: 0.75rem;
    color: #7DD3FC;
    margin-top: 0.3rem;
}

/* ── Sky gradient title text ── */
.aurora-title {
    background: linear-gradient(135deg, #0EA5E9 0%, #10B981 40%, #F472B6 70%, #FBBF24 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════
# SPLASH PAGE
# ════════════════════════════════════════════════════════
if st.session_state.page == "splash":

    st.markdown(
        '<div class="anim-fade-in" style="text-align:center; font-size:1.8rem; letter-spacing:0.4rem; margin-bottom:1rem; opacity:0.9;">'
        '🌸 ✨ 🎊 ✨ 🌸'
        '</div>',
        unsafe_allow_html=True
    )

    if nama_tamu_url:
        sapaan = (
            '<div style="font-size:0.85rem; color:#0284C7; margin-bottom:0.4rem; font-style:italic;">Kepada Yth,</div>'
            + f'<div style="font-family:\'Playfair Display\',serif; font-size:1.5rem; background:linear-gradient(90deg,#0EA5E9,#F472B6); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; font-weight:700; margin-bottom:1.2rem;">{nama_tamu_url} ✨</div>'
        )
    else:
        sapaan = ""

    isi_splash = (
        '<div class="splash-card anim-fade-up">'
        + '<div class="moon"></div>'
        + sapaan
        + '<div style="font-size:0.78rem; font-weight:700; color:#0284C7; letter-spacing:0.2em; text-transform:uppercase; margin-bottom:0.8rem;">🎓 Undangan Wisuda</div>'
        + '<div class="aurora-title" style="font-family:\'Playfair Display\',serif; font-size:1.9rem; font-weight:700; line-height:1.3; margin-bottom:0.4rem;">Muhammad Hamdan<br>Fadhlani, S.T.</div>'
        + '<div style="font-family:\'Playfair Display\',serif; font-style:italic; font-size:0.95rem; color:#0EA5E9; margin-bottom:1.3rem;">Sarjana Teknik &#8212; Teknik Industri</div>'
        + '<div style="font-size:0.88rem; background:linear-gradient(90deg,#0EA5E9,#F472B6); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; margin-bottom:0.3rem; font-weight:700;">📅 Minggu, 10 Mei 2026</div>'
        + '<div style="font-size:0.88rem; color:#0369A1; margin-bottom:1.4rem; font-weight:600;">📍 Gedung Teknik Industri, Unand</div>'
        + '<div style="font-size:0.82rem; color:#0284C7; font-style:italic; margin-bottom:1.8rem; line-height:1.6;">"Seperti langit biru yang cerah,<br>perjalananmu kini sampai di puncaknya 🩵"</div>'
        + '</div>'
    )
    st.markdown(isi_splash, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🎊 Buka Undangan", key="btn_buka", use_container_width=True):
            st.session_state.page = "main"
            st.session_state.musik_mulai = True
            st.rerun()

    st.markdown('<div class="footer-stars anim-fade-in">🌸 ✨ 🎊 🌈 🎊 ✨ 🌸</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════
# MAIN INVITATION PAGE
# ════════════════════════════════════════════════════════
elif st.session_state.page == "main":

    if st.session_state.musik_mulai:
        autoplay_audio(MUSIC_FILE)
        st.markdown(mute_button_html(), unsafe_allow_html=True)

    # ── HEADER ──────────────────────────────────────────
    st.markdown(
        '<div class="anim-fade-in" style="text-align:center; font-size:1.5rem; padding:1.2rem 0 0.3rem; letter-spacing:0.4rem; opacity:0.85;">'
        '🌸 ✨ 🎊 ✨ 🌸'
        '</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<h1 class="aurora-title anim-fade-up" style="font-family:Playfair Display,serif; font-size:2.2rem; text-align:center; line-height:1.2; margin:0.3rem 0;">Undangan Wisuda</h1>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<p class="anim-fade-up-2" style="font-family:Playfair Display,serif; font-style:italic; font-size:0.9rem; color:#0284C7; text-align:center; margin-bottom:1rem;">Di bawah langit biru yang cerah, merayakan pencapaianmu 🩵</p>',
        unsafe_allow_html=True
    )

    if nama_tamu_url:
        st.markdown(
            '<div class="anim-fade-up-3" style="text-align:center; background:rgba(224,247,255,0.8); border-radius:16px; padding:0.8rem 1rem; margin-bottom:0.5rem; border:1px solid rgba(56,189,248,0.35);">'
            + '<span style="font-size:0.78rem; color:#0284C7; text-transform:uppercase; letter-spacing:0.1em;">Kepada Yth,</span><br>'
            + f'<span style="font-family:\'Playfair Display\',serif; font-size:1.3rem; background:linear-gradient(90deg,#0EA5E9,#F472B6); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; font-weight:700;">{nama_tamu_url} ✨</span>'
            + '</div>',
            unsafe_allow_html=True
        )

    # ── INFO WISUDAWAN ───────────────────────────────────
    st.markdown("""
    <div class="card anim-fade-up-2" style="text-align:center;">
        <div style="font-size:0.78rem; color:#0284C7; letter-spacing:0.12em; text-transform:uppercase; margin-bottom:0.5rem; font-weight:700;">🩵 Wisudawan 🩵</div>
        <div class="aurora-title" style="font-family:'Playfair Display',serif; font-size:1.8rem; font-weight:700; line-height:1.3;">Muhammad Hamdan<br>Fadhlani, S.T.</div>
        <div style="margin-top:0.8rem; display:inline-block; background:linear-gradient(135deg,rgba(14,165,233,0.2),rgba(52,211,153,0.2)); color:#0369A1; padding:5px 16px; border-radius:20px; font-size:0.85rem; font-weight:700; border:1px solid rgba(14,165,233,0.40);">
            🎓 S1 Teknik Industri
        </div>
        <div style="font-size:0.88rem; color:#0EA5E9; margin-top:0.4rem; font-weight:600;">Universitas Andalas</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="divider">🌸 · · · 🌈 · · · 🌸</div>', unsafe_allow_html=True)

    # ── FOTO WISUDA — no heading, grid only ─────────────
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

    # Grid foto — tanpa heading
    photos_meta = muat_photos()
    if photos_meta:
        # Wrapper dengan stagger animation per kolom
        cols = st.columns(3)
        stagger_cls = ["photo-s1", "photo-s2", "photo-s3"]
        for i, meta in enumerate(photos_meta[:12]):
            filepath = os.path.join(PHOTOS_DIR, meta["filename"])
            if os.path.exists(filepath):
                with cols[i % 3]:
                    # Bungkus image dengan div animasi
                    st.markdown(f'<div class="{stagger_cls[i % 3]}" style="border-radius:12px; overflow:hidden;">', unsafe_allow_html=True)
                    st.image(filepath, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
        if len(photos_meta) > 12:
            st.markdown(
                f'<div style="text-align:center; color:#0284C7; font-size:0.82rem; margin-top:0.3rem;">+ {len(photos_meta)-12} foto lainnya</div>',
                unsafe_allow_html=True
            )
    else:
        st.markdown("""
        <div style="background:rgba(224,247,255,0.7); border-radius:16px; padding:2rem 1rem; text-align:center; border:1.5px dashed rgba(56,189,248,0.45); margin:0.5rem 0;">
            🩵<br>
            <span style="font-size:0.95rem; font-weight:700; color:#0284C7;">Belum ada foto</span><br>
            <span style="font-size:0.82rem; color:#0369A1;">Upload fotomu dan abadikan momen ini ✨</span>
        </div>
        """, unsafe_allow_html=True)

    # Credit fotografer
    st.markdown("""
    <div style="text-align:center; margin-top:0.8rem; margin-bottom:0.2rem;">
        <span style="font-size:0.82rem; color:#0369A1;">Photo by&nbsp;</span><svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#0EA5E9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle; margin-right:3px;"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1.5" fill="#0EA5E9" stroke="none"/></svg><a href="https://www.instagram.com/nine.moment" target="_blank" style="color:#0EA5E9; font-size:0.82rem; font-weight:700; text-decoration:none; letter-spacing:0.02em;">@nine.moment</a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="divider">🩵 · · · 🌿 · · · 🩵</div>', unsafe_allow_html=True)

    # ── INFO ACARA ───────────────────────────────────────
    st.markdown("""
    <div class="card anim-fade-up">
        <div style="text-align:center; font-size:0.78rem; color:#0284C7; font-weight:700; letter-spacing:0.12em; text-transform:uppercase; margin-bottom:1rem;">🎊 Detail Acara 🎊</div>
        <div class="info-label">📅 Hari &amp; Tanggal</div>
        <div class="info-value">Minggu, 10 Mei 2026</div>
        <div class="info-label">🕐 Waktu</div>
        <div class="info-value">Pukul 14.00 WIB — Selesai</div>
        <div class="info-label">📍 Lokasi</div>
        <div class="info-value">Gedung Teknik Industri<br>
        <span style="font-size:0.88rem; color:#0EA5E9;">Universitas Andalas, Padang, Sumatera Barat</span></div>
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
                <div style="font-family:'Playfair Display',serif; font-size:1.6rem; background:linear-gradient(90deg,#0EA5E9,#F472B6); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;">
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
            <div class="countdown-box anim-fade-up">
                <div class="countdown-title">🩵 Hitung Mundur Menuju Hari Wisuda 🩵</div>
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

    st.markdown('<div class="divider">🌿 · · · 🌿</div>', unsafe_allow_html=True)

    # ── PETA LOKASI ──────────────────────────────────────
    st.markdown('<p class="section-heading anim-fade-up">📍 Lokasi Acara</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="anim-fade-up-2" style="border-radius:16px; overflow:hidden; border:1px solid rgba(56,189,248,0.35); margin-bottom:0.5rem;">
    <iframe
        src="https://maps.google.com/maps?q=Gedung+Teknik+Industri+Universitas+Andalas+Padang&output=embed"
        width="100%" height="280" style="border:0; display:block;"
        allowfullscreen="" loading="lazy">
    </iframe>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="divider">🩵 · · · 🩵</div>', unsafe_allow_html=True)

    # ── KUTIPAN ──────────────────────────────────────────
    st.markdown("""
    <div class="card anim-fade-up">
        <div style="font-size:2rem; text-align:center; margin-bottom:0.8rem; opacity:0.75;">🌤️</div>
        <div class="quote-text">
            "Setiap perjuangan panjang selalu berujung pada kebahagiaan.<br>
            Terima kasih telah menjadi bagian dari perjalanan ini. ✨"
        </div>
        <div style="text-align:center; margin-top:1rem; font-size:0.82rem; color:#0284C7;">&#8212; Muhammad Hamdan Fadhlani, S.T.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="divider">🌿 · · · 🌿</div>', unsafe_allow_html=True)

    # ── FORM UCAPAN & DOA ────────────────────────────────
    st.markdown('<p class="section-heading anim-fade-up">💬 Kirim Ucapan &amp; Doa</p>', unsafe_allow_html=True)

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
            f'<div style="font-size:0.85rem; color:#0284C7; margin:0.8rem 0 0.4rem;">'
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
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🩵 Kembali ke Halaman Awal", key="btn_back", use_container_width=True):
            st.session_state.page = "splash"
            st.rerun()

    st.markdown("""
    <div class="anim-fade-up" style="text-align:center; margin-top:1.8rem; padding:1.2rem 1rem 0.5rem;">
        <div style="font-family:'Playfair Display',serif; font-size:1.15rem; color:#0F172A; font-style:italic; line-height:1.8; margin-bottom:0.6rem;">
            ✨ Kehadiranmu sangat berarti bagiku ✨<br>
            <span style="font-size:1rem; color:#0284C7;">See you at Gedung Teknik Industri, Unand</span><br>
            <span style="font-size:0.88rem; color:#0EA5E9;">Minggu, 10 Mei 2026 — Pukul 14.00 WIB 🩵</span>
        </div>
        <div style="margin-top:0.8rem;">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none"
                stroke="#0EA5E9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                style="vertical-align:middle; margin-right:4px;">
                <rect x="2" y="2" width="20" height="20" rx="5" ry="5"/>
                <circle cx="12" cy="12" r="4"/>
                <circle cx="17.5" cy="6.5" r="1.5" fill="#0EA5E9" stroke="none"/>
            </svg>
            <a href="https://www.instagram.com/hamdanfdhlani" target="_blank"
                style="color:#0EA5E9; font-size:0.88rem; font-weight:700; text-decoration:none; letter-spacing:0.03em;">
                @hamdanfdhlani
            </a>
        </div>
    </div>
    <div class="footer-stars">🩵 ✨ 🎊 🌿 🎊 ✨ 🩵</div>
    """, unsafe_allow_html=True)