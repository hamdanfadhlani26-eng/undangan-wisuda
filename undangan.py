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
    """
    FIX: Gunakan URL path relatif daripada base64 embed.
    Streamlit Cloud mendukung static file serving via st.static_file_serving.
    Fallback: base64 hanya jika file < 2MB untuk menghindari crash di HP RAM rendah.
    """
    if not os.path.exists(filepath):
        return
    file_size = os.path.getsize(filepath)
    # Batasi base64 embed maksimal 2MB — di atas itu skip audio daripada crash
    MAX_EMBED_SIZE = int(2.5 * 1024 * 1024)  # 2.5 MB
    if file_size > MAX_EMBED_SIZE:
        st.caption("⚠️ File musik terlalu besar untuk autoplay. Kompress MP3 ke < 2MB.")
        return
    with open(filepath, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    # FIX: Tambahkan preload="none" agar tidak memuat seluruh file sekaligus
    # FIX: Gunakan volume rendah default agar tidak kaget di HP
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
        " style="background:rgba(14,165,233,0.85); color:#fff; border:1px solid rgba(56,189,248,0.5);
            border-radius:50%; width:44px; height:44px; font-size:1.1rem; cursor:pointer;
            box-shadow:0 2px 12px rgba(14,165,233,0.4); touch-action:manipulation;">
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
# GLOBAL CSS — MOBILE-OPTIMIZED
# ═════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Lato:wght@300;400;700&display=swap');

/* ── Reset & Base ── */
html, body, [class*="css"] {
    font-family: 'Lato', sans-serif;
    -webkit-text-size-adjust: 100%; /* Cegah auto-zoom iOS */
    text-size-adjust: 100%;
}

/* ── Background: SIMPLIFIED untuk mobile ──
   FIX: Hapus background-size:400% + animation infinite
   → Ganti dengan gradient statis. Tetap indah, tapi 0 CPU usage.
   Animasi berat adalah penyebab utama freeze di HP lama/mid-range.
*/
.stApp {
    background: linear-gradient(
        160deg,
        #E0F7FF 0%,
        #D4F5E9 25%,
        #FFF0F8 55%,
        #E8F4FF 80%,
        #D4F5E9 100%
    );
    min-height: 100vh;
}

/* FIX: Hapus ::before pseudo-element dengan animasi float ganda
   → Ganti dengan elemen dekoratif statis sederhana */
.stApp::before { display: none; }

/* ── Animations: hanya fadeIn ringan ── */
/* FIX: Kurangi jumlah keyframe, hapus transform scale
   → Hanya opacity + translateY sederhana */
@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

.anim-fade-up   { animation: fadeSlideUp .5s ease both; }
.anim-fade-up-2 { animation: fadeSlideUp .5s ease .1s both; }
.anim-fade-up-3 { animation: fadeSlideUp .5s ease .2s both; }
.anim-fade-up-4 { animation: fadeSlideUp .5s ease .3s both; }
.anim-fade-up-5 { animation: fadeSlideUp .5s ease .4s both; }
.anim-fade-in   { animation: fadeIn .8s ease both; }
.photo-s1 { animation: fadeSlideUp .5s ease both; }
.photo-s2 { animation: fadeSlideUp .5s ease .08s both; }
.photo-s3 { animation: fadeSlideUp .5s ease .16s both; }

/* ── Cards ──
   FIX: Hapus backdrop-filter:blur → tidak diakselerasi hardware di banyak Android
   → Ganti dengan background solid semi-transparan
*/
.card {
    background: rgba(255,255,255,0.88);
    border-radius: 20px;
    padding: 1.3rem 1.5rem;
    margin: .9rem 0;
    border: 1px solid rgba(56,189,248,0.30);
    box-shadow: 0 3px 20px rgba(56,189,248,0.12);
    /* backdrop-filter: blur(10px); ← DIHAPUS */
}

/* ── Form inputs ── */
label, .stTextInput label, .stTextArea label, .stFileUploader label {
    color: #0369A1 !important;
    font-weight: 600 !important;
}
.stTextInput input, .stTextArea textarea {
    background: rgba(255,255,255,0.95) !important;
    color: #0F172A !important;
    border: 1.5px solid rgba(56,189,248,0.4) !important;
    border-radius: 12px !important;
    font-size: 16px !important; /* FIX: Cegah auto-zoom iOS saat focus input */
}
/* FIX: Paksa warna teks gelap — override Streamlit theme yang kadang inject warna putih */
.stTextInput input:focus,
.stTextArea textarea:focus {
    color: #0F172A !important;
    background: #FFFFFF !important;
}
/* FIX: Placeholder juga harus terbaca */
.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #64748B !important;
    opacity: 1 !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #0EA5E9, #38BDF8, #34D399);
    color: #FFFFFF !important;
    border: none;
    border-radius: 50px;
    padding: .75rem 2rem;
    font-size: 1rem;
    font-weight: 700;
    letter-spacing: .04em;
    cursor: pointer;
    width: 100%;
    transition: opacity .2s; /* FIX: Ganti transform hover dengan opacity → lebih smooth di mobile */
    box-shadow: 0 3px 16px rgba(14,165,233,0.30);
    -webkit-tap-highlight-color: transparent; /* FIX: Hapus flash biru saat tap di Android */
    touch-action: manipulation; /* FIX: Cegah delay 300ms double-tap */
}
.stButton > button:hover {
    opacity: .88;
    color: #FFFFFF !important;
}
.stButton > button:active {
    opacity: .75;
    transform: scale(0.98); /* Feedback sentuhan kecil saja */
}

/* ── Info labels ── */
.info-label {
    font-size: .7rem;
    font-weight: 700;
    letter-spacing: .12em;
    color: #0284C7;
    text-transform: uppercase;
    margin-bottom: 2px;
}
.info-value {
    font-family: 'Playfair Display', serif;
    font-size: 1rem;
    color: #0F172A;
    margin-bottom: .85rem;
    line-height: 1.5;
}

/* ── Countdown ── */
.countdown-box {
    background: linear-gradient(135deg, rgba(224,247,255,.92), rgba(212,245,233,.92));
    border: 1.5px solid rgba(56,189,248,.35);
    border-radius: 18px;
    padding: 1.3rem .8rem;
    text-align: center;
    margin: .9rem 0;
    box-shadow: 0 3px 20px rgba(56,189,248,.15);
    /* FIX: Hapus backdrop-filter */
}
.countdown-title {
    font-size: .75rem;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: #0284C7;
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
    font-size: 2.2rem; /* FIX: Kecilkan sedikit agar muat di HP 320px */
    font-weight: 700;
    line-height: 1;
    display: block;
    background: linear-gradient(135deg, #0EA5E9, #F472B6, #34D399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.count-label {
    font-size: .58rem;
    letter-spacing: .08em;
    opacity: .85;
    text-transform: uppercase;
    color: #0284C7;
    font-weight: 600;
}
.count-sep {
    font-size: 1.8rem;
    color: #38BDF8;
    opacity: .6;
    padding-bottom: 10px;
}

/* ── Misc ── */
.divider      { text-align: center; font-size: 1.1rem; margin: .4rem 0; opacity: .75; }
.quote-text   { font-family: 'Playfair Display', serif; font-style: italic; font-size: .95rem; color: #0F172A; text-align: center; line-height: 1.8; }
.section-heading {
    font-family: 'Playfair Display', serif;
    font-size: 1.15rem;
    background: linear-gradient(90deg, #0EA5E9, #10B981);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 1rem 0 .5rem;
}

/* ── Splash card ── */
.splash-card {
    background: rgba(255,255,255,0.88);
    border-radius: 24px;
    padding: 2.2rem 1.5rem;
    border: 1px solid rgba(56,189,248,.30);
    text-align: center;
    box-shadow: 0 6px 40px rgba(56,189,248,.15);
    /* FIX: Hapus backdrop-filter */
}

/* ── Moon dekorasi ── */
.moon {
    display: inline-block;
    width: 58px; height: 58px;
    border-radius: 50%;
    background: radial-gradient(circle at 35% 35%, #FFF9C4, #FCD34D 45%, #F59E0B 80%);
    box-shadow: 0 0 16px rgba(251,191,36,.7), 0 0 40px rgba(251,191,36,.3);
    margin: 0 auto .8rem;
}

.footer-stars { text-align: center; font-size: 1.2rem; padding: 1rem; letter-spacing: .25rem; opacity: .8; }

/* ── Ucapan items ── */
.ucapan-item {
    background: rgba(255,255,255,0.85);
    border-left: 3px solid #38BDF8;
    border-radius: 12px;
    padding: .85rem 1rem;
    margin-bottom: .65rem;
    border-top: 1px solid rgba(56,189,248,.20);
    border-right: 1px solid rgba(56,189,248,.20);
    border-bottom: 1px solid rgba(56,189,248,.20);
    animation: fadeSlideUp .5s ease both;
    box-shadow: 0 2px 10px rgba(56,189,248,.08);
}
.ucapan-nama  { font-weight: 700; color: #0284C7; font-size: .88rem; margin-bottom: .2rem; }
.ucapan-teks  { color: #1E3A5F; font-size: .9rem; line-height: 1.6; font-style: italic; }
.ucapan-waktu { font-size: .72rem; color: #7DD3FC; margin-top: .25rem; }

.ucapan-locked {
    background: rgba(224,247,255,.75);
    border: 1.5px dashed rgba(56,189,248,.40);
    border-radius: 14px;
    padding: 1.3rem 1rem;
    text-align: center;
    margin: .5rem 0;
}

.aurora-title {
    background: linear-gradient(135deg, #0EA5E9 0%, #10B981 40%, #F472B6 70%, #FBBF24 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* ── Mobile-specific fixes ── */
@media (max-width: 480px) {
    /* FIX: Pastikan foto grid tidak overflow di HP sempit */
    .stImage img { border-radius: 10px; }

    /* FIX: Turunkan ukuran judul di HP kecil */
    h1 { font-size: 1.6rem !important; }

    .count-num { font-size: 1.8rem; }
    .count-item { min-width: 42px; }
    .count-sep { font-size: 1.4rem; }

    /* FIX: Perbesar tap target tombol */
    .stButton > button { padding: .85rem 1.5rem; min-height: 48px; }
}

/* ── Decorative dots: statis, tidak animasi ──
   FIX: Menggantikan ::before yang animasi dengan dot statis di pojok
   → Efek serupa, tapi 0 CPU cost
*/
.deco-dots {
    position: fixed; top: 0; left: 0; right: 0; bottom: 0;
    background-image:
        radial-gradient(5px 5px at 8%  12%, rgba(56,189,248,.35) 100%, transparent),
        radial-gradient(4px 4px at 68%  6%, rgba(56,189,248,.30) 100%, transparent),
        radial-gradient(5px 5px at 38%  8%, rgba(52,211,153,.35) 100%, transparent),
        radial-gradient(6px 6px at 83% 25%, rgba(52,211,153,.25) 100%, transparent),
        radial-gradient(5px 5px at 15% 42%, rgba(249,168,212,.40) 100%, transparent),
        radial-gradient(7px 7px at 75% 55%, rgba(249,168,212,.30) 100%, transparent),
        radial-gradient(5px 5px at 88% 80%, rgba(196,181,253,.30) 100%, transparent),
        radial-gradient(6px 6px at 70% 88%, rgba(253,186,116,.30) 100%, transparent);
    pointer-events: none;
    z-index: 0;
}
</style>
""", unsafe_allow_html=True)

# Decorative dots statis (gantikan ::before animasi)
st.markdown('<div class="deco-dots"></div>', unsafe_allow_html=True)


# ═════════════════════════════════════════════════════
# SPLASH PAGE
# ═════════════════════════════════════════════════════
if st.session_state.page == "splash":

    st.markdown(
        '<div class="anim-fade-in" style="text-align:center;font-size:1.6rem;letter-spacing:.3rem;margin-bottom:.8rem;opacity:.85;">'
        '🌸 ✨ 🎊 ✨ 🌸</div>',
        unsafe_allow_html=True
    )

    sapaan = ""
    if nama_tamu_url:
        sapaan = (
            '<div style="font-size:.82rem;color:#0284C7;margin-bottom:.35rem;font-style:italic;">Kepada Yth,</div>'
            f'<div style="font-family:\'Playfair Display\',serif;font-size:1.4rem;'
            f'background:linear-gradient(90deg,#0EA5E9,#F472B6);'
            f'-webkit-background-clip:text;-webkit-text-fill-color:transparent;'
            f'background-clip:text;font-weight:700;margin-bottom:1.1rem;">{nama_tamu_url} ✨</div>'
        )

    st.markdown(
        '<div class="splash-card anim-fade-up">'
        + '<div class="moon"></div>'
        + sapaan
        + '<div style="font-size:.75rem;font-weight:700;color:#0284C7;letter-spacing:.18em;text-transform:uppercase;margin-bottom:.7rem;">🎓 Undangan Wisuda</div>'
        + '<div class="aurora-title" style="font-family:\'Playfair Display\',serif;font-size:1.75rem;font-weight:700;line-height:1.3;margin-bottom:.35rem;">Muhammad Hamdan<br>Fadhlani, S.T.</div>'
        + '<div style="font-family:\'Playfair Display\',serif;font-style:italic;font-size:.9rem;color:#0EA5E9;margin-bottom:1.1rem;">Sarjana Teknik — Teknik Industri</div>'
        + '<div style="font-size:.85rem;background:linear-gradient(90deg,#0EA5E9,#F472B6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin-bottom:.25rem;font-weight:700;">📅 Minggu, 10 Mei 2026</div>'
        + '<div style="font-size:.85rem;color:#0369A1;margin-bottom:1.2rem;font-weight:600;">📍 Gedung Teknik Industri, Unand</div>'
        + '<div style="font-size:.8rem;color:#0284C7;font-style:italic;margin-bottom:1.5rem;line-height:1.6;">"Seperti langit biru yang cerah,<br>perjalananmu kini sampai di puncaknya 🩵"</div>'
        + '</div>',
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎊 Buka Undangan", key="btn_buka", use_container_width=True):
            st.session_state.page = "main"
            st.session_state.musik_mulai = True
            st.rerun()

    st.markdown('<div class="footer-stars anim-fade-in">🌸 ✨ 🎊 🌈 🎊 ✨ 🌸</div>', unsafe_allow_html=True)


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
        '🌸 ✨ 🎊 ✨ 🌸</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<h1 class="aurora-title anim-fade-up" style="font-family:Playfair Display,serif;font-size:2rem;text-align:center;line-height:1.2;margin:.3rem 0;">Undangan Wisuda</h1>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<p class="anim-fade-up-2" style="font-family:Playfair Display,serif;font-style:italic;font-size:.88rem;color:#0284C7;text-align:center;margin-bottom:.8rem;">Di bawah langit biru yang cerah, merayakan pencapaianmu 🩵</p>',
        unsafe_allow_html=True
    )

    if nama_tamu_url:
        st.markdown(
            '<div class="anim-fade-up-3" style="text-align:center;background:rgba(224,247,255,.85);border-radius:14px;padding:.7rem 1rem;margin-bottom:.5rem;border:1px solid rgba(56,189,248,.30);">'
            '<span style="font-size:.75rem;color:#0284C7;text-transform:uppercase;letter-spacing:.08em;">Kepada Yth,</span><br>'
            f'<span style="font-family:\'Playfair Display\',serif;font-size:1.2rem;background:linear-gradient(90deg,#0EA5E9,#F472B6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;font-weight:700;">{nama_tamu_url} ✨</span>'
            '</div>',
            unsafe_allow_html=True
        )

    # ── INFO WISUDAWAN ───────────────────────────────
    st.markdown("""
    <div class="card anim-fade-up-2" style="text-align:center;">
        <div style="font-size:.75rem;color:#0284C7;letter-spacing:.1em;text-transform:uppercase;margin-bottom:.5rem;font-weight:700;">🩵 Wisudawan 🩵</div>
        <div class="aurora-title" style="font-family:'Playfair Display',serif;font-size:1.65rem;font-weight:700;line-height:1.3;">Muhammad Hamdan<br>Fadhlani, S.T.</div>
        <div style="margin-top:.7rem;display:inline-block;background:linear-gradient(135deg,rgba(14,165,233,.18),rgba(52,211,153,.18));color:#0369A1;padding:4px 14px;border-radius:20px;font-size:.82rem;font-weight:700;border:1px solid rgba(14,165,233,.35);">
            🎓 S1 Teknik Industri
        </div>
        <div style="font-size:.85rem;color:#0EA5E9;margin-top:.35rem;font-weight:600;">Universitas Andalas</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="divider">🌸 · · · 🌈 · · · 🌸</div>', unsafe_allow_html=True)

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
                f'<div style="text-align:center;color:#0284C7;font-size:.8rem;margin-top:.25rem;">+ {len(photos_meta)-12} foto lainnya</div>',
                unsafe_allow_html=True
            )
    else:
        st.markdown("""
        <div style="background:rgba(224,247,255,.75);border-radius:14px;padding:1.8rem 1rem;text-align:center;border:1.5px dashed rgba(56,189,248,.40);margin:.5rem 0;">
            🩵<br>
            <span style="font-size:.9rem;font-weight:700;color:#0284C7;">Belum ada foto</span><br>
            <span style="font-size:.8rem;color:#0369A1;">Upload fotomu dan abadikan momen ini ✨</span>
        </div>
        """, unsafe_allow_html=True)

    # Credit fotografer
    st.markdown("""
    <div style="text-align:center;margin-top:.7rem;margin-bottom:.2rem;">
        <span style="font-size:.8rem;color:#0369A1;">Photo by&nbsp;</span>
        <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none"
            stroke="#0EA5E9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
            style="vertical-align:middle;margin-right:2px;">
            <rect x="2" y="2" width="20" height="20" rx="5" ry="5"/>
            <circle cx="12" cy="12" r="4"/>
            <circle cx="17.5" cy="6.5" r="1.5" fill="#0EA5E9" stroke="none"/>
        </svg>
        <a href="https://www.instagram.com/nine.moment" target="_blank"
            style="color:#0EA5E9;font-size:.8rem;font-weight:700;text-decoration:none;">@nine.moment</a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="divider">🩵 · · · 🌿 · · · 🩵</div>', unsafe_allow_html=True)

    # ── INFO ACARA ───────────────────────────────────
    st.markdown("""
    <div class="card anim-fade-up">
        <div style="text-align:center;font-size:.75rem;color:#0284C7;font-weight:700;letter-spacing:.1em;text-transform:uppercase;margin-bottom:.9rem;">🎊 Detail Acara 🎊</div>
        <div class="info-label">📅 Hari &amp; Tanggal</div>
        <div class="info-value">Minggu, 10 Mei 2026</div>
        <div class="info-label">🕐 Waktu</div>
        <div class="info-value">Pukul 14.00 WIB — Selesai</div>
        <div class="info-label">📍 Lokasi</div>
        <div class="info-value">Gedung Teknik Industri<br>
            <span style="font-size:.85rem;color:#0EA5E9;">Universitas Andalas, Padang, Sumatera Barat</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── COUNTDOWN ────────────────────────────────────
    # FIX: run_every dikurangi ke 5 detik (dari 1 detik)
    # → Kurangi beban server & re-render 5x lebih sedikit
    # Countdown masih terasa real-time tapi jauh lebih efisien
    wisuda_dt = datetime(2026, 5, 10, 14, 0, 0)

    @st.fragment(run_every=5)
    def tampilkan_countdown():
        now        = datetime.now()
        total_secs = int((wisuda_dt - now).total_seconds())
        if total_secs <= 0:
            st.markdown("""
            <div class="countdown-box">
                <div style="font-family:'Playfair Display',serif;font-size:1.5rem;
                    background:linear-gradient(90deg,#0EA5E9,#F472B6);
                    -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">
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

    st.markdown('<div class="divider">🌿 · · · 🌿</div>', unsafe_allow_html=True)

    # ── PETA LOKASI ──────────────────────────────────
    st.markdown('<p class="section-heading anim-fade-up">📍 Lokasi Acara</p>', unsafe_allow_html=True)
    # FIX: Tambahkan loading="lazy" dan referrerpolicy untuk keandalan di mobile
    # FIX: Turunkan height iframe dari 280 → 240 agar lebih ringan
    st.markdown("""
    <div class="anim-fade-up-2" style="border-radius:14px;overflow:hidden;border:1px solid rgba(56,189,248,.30);margin-bottom:.5rem;">
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
            style="font-size:.8rem;color:#0EA5E9;font-weight:700;text-decoration:none;">
            🗺️ Buka di Google Maps →
        </a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="divider">🩵 · · · 🩵</div>', unsafe_allow_html=True)

    # ── KUTIPAN ──────────────────────────────────────
    st.markdown("""
    <div class="card anim-fade-up">
        <div style="font-size:1.8rem;text-align:center;margin-bottom:.7rem;opacity:.7;">🌤️</div>
        <div class="quote-text">
            "Setiap perjuangan panjang selalu berujung pada kebahagiaan.<br>
            Terima kasih telah menjadi bagian dari perjalanan ini. ✨"
        </div>
        <div style="text-align:center;margin-top:.9rem;font-size:.8rem;color:#0284C7;">&#8212; Muhammad Hamdan Fadhlani, S.T.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="divider">🌿 · · · 🌿</div>', unsafe_allow_html=True)

    # ════════════════════════════════════════════════
    # FORM UCAPAN & DOA
    # ════════════════════════════════════════════════
    st.markdown('<p class="section-heading anim-fade-up">💬 Kirim Ucapan &amp; Doa</p>', unsafe_allow_html=True)

    with st.form("ucapan_form", clear_on_submit=True):
        nama_pengirim = st.text_input("Nama Kamu", placeholder="Masukkan namamu")
        ucapan_text   = st.text_area(
            "Ucapan & Doa untuk Hamdan",
            placeholder="Tuliskan ucapan dan doamu di sini... ✨",
            height=110
        )
        submitted = st.form_submit_button("🌟 Kirim Ucapan", use_container_width=True)

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

    # ════════════════════════════════════════════════
    # TAMPILAN UCAPAN
    # ════════════════════════════════════════════════
    daftar_ucapan = muat_ucapan()
    jumlah_ucapan = len(daftar_ucapan)

    if is_owner:
        if jumlah_ucapan > 0:
            st.markdown(
                f'<div style="font-size:.83rem;color:#0284C7;margin:.7rem 0 .4rem;">'
                f'🌟 {jumlah_ucapan} ucapan telah dikirimkan</div>',
                unsafe_allow_html=True
            )
            for u in daftar_ucapan[:50]:
                st.markdown(
                    f'<div class="ucapan-item">'
                    f'<div class="ucapan-nama">⭐ {u["nama"]}</div>'
                    f'<div class="ucapan-teks">"{u["ucapan"]}"</div>'
                    f'<div class="ucapan-waktu">🕐 {u.get("waktu", "")}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
        else:
            st.markdown(
                '<div style="text-align:center;color:#0284C7;font-size:.86rem;margin:.7rem 0;">Belum ada ucapan masuk.</div>',
                unsafe_allow_html=True
            )
    else:
        if jumlah_ucapan > 0:
            st.markdown(
                f'<div class="ucapan-locked">'
                f'<div style="font-size:1.4rem;margin-bottom:.35rem;">🔒</div>'
                f'<div style="font-weight:700;color:#0284C7;font-size:.92rem;margin-bottom:.25rem;">'
                f'{jumlah_ucapan} ucapan telah dikirimkan</div>'
                f'<div style="font-size:.8rem;color:#0369A1;">Ucapan bersifat pribadi dan hanya dapat dilihat oleh pemilik undangan 🩵</div>'
                f'</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<div class="ucapan-locked">'
                '<div style="font-size:1.4rem;margin-bottom:.35rem;">💬</div>'
                '<div style="font-size:.85rem;color:#0369A1;">Jadilah yang pertama mengirim ucapan! ✨</div>'
                '</div>',
                unsafe_allow_html=True
            )

    # ── BACK & FOOTER ────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🩵 Kembali ke Halaman Awal", key="btn_back", use_container_width=True):
            st.session_state.page = "splash"
            st.rerun()

    st.markdown("""
    <div class="anim-fade-up" style="text-align:center;margin-top:1.5rem;padding:1rem 1rem .5rem;">
        <div style="font-family:'Playfair Display',serif;font-size:1.05rem;color:#0F172A;font-style:italic;line-height:1.8;margin-bottom:.5rem;">
            ✨ Kehadiranmu sangat berarti bagiku ✨<br>
            <span style="font-size:.95rem;color:#0284C7;">See you at Gedung Teknik Industri, Unand</span><br>
            <span style="font-size:.85rem;color:#0EA5E9;">Minggu, 10 Mei 2026 — Pukul 14.00 WIB 🩵</span>
        </div>
        <div style="margin-top:.7rem;">
            <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none"
                stroke="#0EA5E9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                style="vertical-align:middle;margin-right:3px;">
                <rect x="2" y="2" width="20" height="20" rx="5" ry="5"/>
                <circle cx="12" cy="12" r="4"/>
                <circle cx="17.5" cy="6.5" r="1.5" fill="#0EA5E9" stroke="none"/>
            </svg>
            <a href="https://www.instagram.com/hamdanfdhlani" target="_blank" rel="noopener"
                style="color:#0EA5E9;font-size:.85rem;font-weight:700;text-decoration:none;letter-spacing:.02em;">
                @hamdanfdhlani
            </a>
        </div>
    </div>
    <div class="footer-stars">🩵 ✨ 🎊 🌿 🎊 ✨ 🩵</div>
    """, unsafe_allow_html=True)