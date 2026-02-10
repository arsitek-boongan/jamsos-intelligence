import streamlit as st
import requests
from datetime import datetime

# --- 1. KONFIGURASI HALAMAN (DARK MODE FORCED) ---
st.set_page_config(
    page_title="Jamsos Command Center",
    page_icon="🛡️",
    layout="centered", # Centered lebih bagus untuk fokus mobile
    initial_sidebar_state="collapsed"
)

# 🔴 GANTI URL INI DENGAN WORKER ANDA 🔴
WORKER_URL = "https://jamsos-brain.arsitek-boongan.workers.dev"

# --- 2. IPHONE UI/UX CSS INJECTION ---
st.markdown("""
<style>
    /* --- TYPOGRAPHY & BASE --- */
    @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
        background-color: #000000 !important; /* OLED Black */
        color: #FFFFFF;
    }
    
    /* Hapus padding atas bawaan yang mengganggu di HP */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 5rem !important;
        max-width: 600px; /* Batasi lebar agar terlihat seperti aplikasi HP di layar besar */
    }

    /* Sembunyikan elemen Streamlit */
    #MainMenu, footer, header {visibility: hidden;}

    /* --- GLASSMORPHISM CARDS (Gaya iPhone) --- */
    .glass-card {
        background: rgba(30, 30, 30, 0.60);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-radius: 24px; /* Super rounded corners */
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        margin-bottom: 16px;
        text-align: center;
        transition: transform 0.2s;
    }
    
    /* Efek tekan di HP */
    .glass-card:active {
        transform: scale(0.98);
        background: rgba(50, 50, 50, 0.7);
    }

    /* --- HERO STATUS CARD (Yang Paling Besar) --- */
    .hero-card {
        padding: 30px 20px;
        border-radius: 32px;
        margin-bottom: 24px;
        text-align: center;
        box-shadow: 0 10px 40px -10px rgba(0,0,0,0.8);
        border: none;
    }
    .hero-title { font-size: 14px; text-transform: uppercase; letter-spacing: 1.5px; opacity: 0.8; font-weight: 600; margin-bottom: 10px;}
    .hero-status { font-size: 48px; font-weight: 800; line-height: 1; letter-spacing: -1px; margin: 0;}
    .hero-subtitle { font-size: 16px; margin-top: 15px; font-weight: 500; opacity: 0.9; display: flex; align-items: center; justify-content: center; gap: 8px;}

    /* --- METRIC MINI CARDS --- */
    .metric-box {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 110px;
    }
    .metric-icon { font-size: 28px; margin-bottom: 5px; }
    .metric-value { font-size: 22px; font-weight: 700; }
    .metric-label { font-size: 13px; opacity: 0.7; }

    /* --- MODERN TABS (iOS Segmented Control Style) --- */
    .stTabs {
        background: rgba(30, 30, 30, 0.60);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        padding: 6px;
        border-radius: 18px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 0px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        border-radius: 14px;
        border: none;
        color: #AAAAAA;
        font-weight: 600;
        flex-grow: 1; /* Agar lebar tab sama rata */
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(255,255,255,0.15) !important;
        color: white !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }

    /* --- EXPANDERS (Accordion) --- */
    .streamlit-expanderHeader {
        background-color: transparent !important;
        border: none !important;
        font-weight: 600;
        color: white !important;
    }
    .streamlit-expanderContent {
        border: none !important;
        padding-left: 1rem !important;
        border-left: 2px solid rgba(255,255,255,0.2) !important;
        margin-left: 0.5rem;
    }
    
    /* --- CUSTOM BUTTON (Refresh) --- */
    button[kind="secondary"] {
        border-radius: 50%;
        width: 45px;
        height: 45px;
        border: none;
        background: rgba(255,255,255,0.1);
        color: white;
    }
    button[kind="secondary"]:hover {
        background: rgba(255,255,255,0.2);
        border: none;
    }

</style>
""", unsafe_allow_html=True)

# --- 3. FUNGSI FETCH DATA ---
@st.cache_data(ttl=300) # Cache 5 menit agar lebih responsif
def get_data():
    try:
        response = requests.get(WORKER_URL, timeout=10)
        if response.status_code == 200:
            return response.json()
    except: return None
    return None

# --- 4. UI UTAMA (COMMAND CENTER) ---

# HEADER (Minimalis ala iOS App)
c1, c2 = st.columns([8,2])
with c1:
    st.markdown("<div style='font-weight:800; font-size:22px; letter-spacing:-0.5px;'>Jamsos Intel</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:13px; opacity:0.7;'>Mobile Command Center</div>", unsafe_allow_html=True)
with c2:
    # Tombol Refresh Bulat
    if st.button("🔄"):
        st.cache_data.clear()
        st.rerun()

st.divider()

# LOAD DATA
with st.spinner("Menghubungkan Satelit..."):
    data = get_data()

if data:
    # --- A. HERO SECTION (STATUS GLOWING) ---
    status = data.get('social_stability_index', 'UNKNOWN')
    tanggal = data.get('tanggal', '-')
    
    # Konfigurasi Warna & Ikon Berdasarkan Status
    if status == "HIJAU":
        # Neon Green Gradient
        bg_hero = "linear-gradient(135deg, #00b09b, #96c93d)"
        shadow_hero = "0 20px 50px -20px rgba(0, 176, 155, 0.6)"
        icon_hero = "shield-checkmark" # Ionicon name (simulasi)
        status_text = "AMAN TERKENDALI"
        emoji = "✅"
    elif status == "KUNING":
        # Warm Amber Gradient
        bg_hero = "linear-gradient(135deg, #f2994a, #f2c94c)"
        shadow_hero = "0 20px 50px -20px rgba(242, 153, 74, 0.6)"
        icon_hero = "alert"
        status_text = "WASPADA"
        emoji = "⚠️"
    else: # MERAH
        # Intense Red Gradient
        bg_hero = "linear-gradient(135deg, #cb2d3e, #ef473a)"
        shadow_hero = "0 20px 50px -20px rgba(203, 45, 62, 0.6)"
        icon_hero = "nuclear"
        status_text = "BAHAYA / KRISIS"
        emoji = "🚨"

    # Render Hero Card
    st.markdown(f"""
    <div class="hero-card" style="background: {bg_hero}; box-shadow: {shadow_hero};">
        <div class="hero-title">INDEKS STABILITAS SOSIAL</div>
        <h1 class="hero-status">{status}</h1>
        <div class="hero-subtitle">
            <span style="font-size:20px">{emoji}</span> {status_text}
        </div>
        <div style="font-size:12px; margin-top:15px; opacity:0.8;">Last Update: {tanggal}</div>
    </div>
    """, unsafe_allow_html=True)


    # --- B. KEY METRICS GRID (Glassmorphism) ---
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown("""
        <div class="glass-card metric-box">
            <div class="metric-icon">📅</div>
            <div class="metric-value">Harian</div>
            <div class="metric-label">Periode</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        jml_sumber = len(data.get('sources', []))
        st.markdown(f"""
        <div class="glass-card metric-box">
            <div class="metric-icon">📡</div>
            <div class="metric-value">{jml_sumber}</div>
            <div class="metric-label">Sinyal Berita</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        # Simpanan untuk fitur masa depan
        risk_lvl = "Low" if status == "HIJAU" else "Med" if status == "KUNING" else "High"
        st.markdown(f"""
        <div class="glass-card metric-box">
            <div class="metric-icon">📊</div>
            <div class="metric-value">{risk_lvl}</div>
            <div class="metric-label">Level Risiko</div>
        </div>
        """, unsafe_allow_html=True)


    # --- C. DETAIL TABS (iOS Style) ---
    tab_exec, tab_analisis, tab_sumber = st.tabs(["Executive", "Analisis", "Sumber"])

    with tab_exec:
        st.markdown('<div class="glass-card" style="text-align:left;">', unsafe_allow_html=True)
        st.subheader("Ringkasan Intelijen")
        st.write(data.get('executive_summary', 'Tidak ada data.'))
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_analisis:
        st.markdown('<div class="glass-card" style="text-align:left; padding-bottom:10px;">', unsafe_allow_html=True)
        st.subheader("Deep Dive Analysis")
        
        strat = data.get('strategic_analysis', {})
        with st.expander("🏛️ Dampak Politik & Kebijakan"):
            st.write(strat.get('political_impact', '-'))
        with st.expander("🗣️ Sentimen Publik"):
            st.write(strat.get('public_sentiment', '-'))

        st.divider()
        
        tech = data.get('technical_audit', {})
        with st.expander("⚖️ Audit Regulasi"):
            st.write(tech.get('regulations_involved', '-'))
        with st.expander("⚙️ Risiko Operasional"):
            st.write(tech.get('operational_risks', '-'))
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_sumber:
        st.markdown('<div class="glass-card" style="text-align:left;">', unsafe_allow_html=True)
        st.subheader("Sinyal Masuk (Raw Data)")
        sources = data.get('sources', [])
        if sources:
            for s in sources:
                st.markdown(f"""
                <div style="margin-bottom:15px; padding-bottom:15px; border-bottom:1px solid rgba(255,255,255,0.1);">
                    <div style="font-weight:600;">📰 {s.get('title')}</div>
                    <a href="{s.get('url')}" target="_blank" style="font-size:13px; color:#4da6ff; text-decoration:none;">Buka Tautan Eksternal →</a>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("✅ Tidak ada sinyal berita negatif yang terdeteksi oleh satelit dalam 24 jam terakhir.")
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.error("Gagal terhubung ke Jamsos Brain. Coba refresh.")