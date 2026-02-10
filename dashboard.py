import streamlit as st
import requests
from datetime import datetime

# --- 1. SETUP HALAMAN (FORCE WIDE TAPI DI-LIMIT CSS) ---
st.set_page_config(
    page_title="Jamsos Intel",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 🔴 URL WORKER (PASTIKAN BENAR) 🔴
WORKER_URL = "https://jamsos-brain.arsitek-boongan.workers.dev"

# --- 2. CSS ENGINE: TOTAL OVERHAUL (APPLE DARK MODE STYLE) ---
st.markdown("""
<style>
    /* RESET TOTAL - PAKSA BACKGROUND HITAM PEKAT */
    .stApp {
        background-color: #000000 !important;
    }
    
    /* Hapus Header & Footer Bawaan Streamlit */
    header, footer, #MainMenu {visibility: hidden !important;}
    
    /* MOBILE CONTAINER LIMITER */
    /* Di layar besar, batasi lebar agar seperti aplikasi HP. Di HP, full width. */
    .block-container {
        max-width: 500px !important;
        padding-top: 2rem !important;
        padding-bottom: 5rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        margin: auto !important;
    }

    /* TYPOGRAPHY (Apple Style) */
    html, body, p, div, h1, h2, h3, span {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
        color: #FFFFFF !important; /* Paksa teks putih */
    }
    
    /* CARD SYSTEM (Apple Dark Gray) */
    .ios-card {
        background-color: #1C1C1E; /* Warna standar card iPhone Dark Mode */
        border-radius: 18px;
        padding: 20px;
        margin-bottom: 16px;
        border: 1px solid #2C2C2E; /* Border halus */
    }
    
    /* STATUS HEADER (Big & Bold) */
    .status-container {
        text-align: center;
        padding: 30px 20px;
        border-radius: 24px;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }
    
    /* ANIMASI PULSING (Indikator Live) */
    @keyframes pulse-dot {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(255, 255, 255, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(255, 255, 255, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(255, 255, 255, 0); }
    }
    .live-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background-color: #FF3B30; /* Apple Red */
        margin-right: 8px;
        animation: pulse-dot 2s infinite;
    }
    
    /* TEXT STYLES */
    .text-subtle { color: #8E8E93 !important; font-size: 13px; font-weight: 500; }
    .text-bold { font-weight: 700; font-size: 18px; }
    .text-huge { font-weight: 800; font-size: 42px; letter-spacing: -1px; line-height: 1.1; margin: 10px 0; }
    
    /* GRID METRICS */
    .metric-grid {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 10px;
        margin-bottom: 20px;
    }
    .metric-item {
        background-color: #1C1C1E;
        border-radius: 14px;
        padding: 15px 10px;
        text-align: center;
        border: 1px solid #2C2C2E;
    }
    
    /* TOMBOL REFRESH MINIMALIS */
    .stButton > button {
        background-color: #2C2C2E !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        width: 100%;
        padding: 10px;
        font-weight: 600;
    }
    .stButton > button:active {
        background-color: #3A3A3C !important;
    }

    /* CUSTOM TABS OVERRIDE */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #1C1C1E;
        padding: 5px;
        border-radius: 12px;
        gap: 0;
    }
    .stTabs [data-baseweb="tab"] {
        height: 35px;
        background-color: transparent;
        border: none;
        color: #8E8E93;
        font-size: 14px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #3A3A3C !important;
        color: white !important;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    /* REMOVE DEFAULT STREAMLIT PADDING */
    .css-18e3th9 { padding: 0 !important; }
    
    /* LINK STYLING */
    a { color: #0A84FF !important; text-decoration: none; }
</style>
""", unsafe_allow_html=True)

# --- 3. LOGIC ---
@st.cache_data(ttl=300)
def get_data():
    try:
        r = requests.get(WORKER_URL, timeout=5)
        return r.json() if r.status_code == 200 else None
    except: return None

# --- 4. UI CONSTRUCTION ---

# Top Bar (Logo & Refresh)
c1, c2 = st.columns([4, 1])
with c1:
    st.markdown("""
    <div style="display:flex; align-items:center;">
        <span style="font-size:20px; margin-right:10px;">🛡️</span>
        <div>
            <div style="font-weight:700; font-size:16px;">JAMSOS INTEL</div>
            <div class="text-subtle">Command Center</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
with c2:
    if st.button("🔄"):
        st.cache_data.clear()
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# Load Data
data = get_data()

if data:
    status = data.get('social_stability_index', 'UNKNOWN')
    tanggal = data.get('tanggal', '-')
    
    # Color Logic (Hardcoded Hex Codes for Consistency)
    if status == "HIJAU":
        bg_color = "#004d26" # Dark Green background
        accent_color = "#30D158" # Apple Green text
        status_msg = "SITUASI KONDUSIF"
        icon = "checkmark.shield.fill"
    elif status == "KUNING":
        bg_color = "#4d3a00"
        accent_color = "#FFD60A" # Apple Yellow
        status_msg = "PERLU ATENSI"
        icon = "exclamationmark.triangle.fill"
    else: # MERAH
        bg_color = "#4d0000"
        accent_color = "#FF453A" # Apple Red
        status_msg = "BAHAYA / KRISIS"
        icon = "exclamationmark.octagon.fill"

    # --- A. STATUS HERO (The "Face") ---
    st.markdown(f"""
    <div class="status-container" style="background: radial-gradient(circle at top right, {bg_color}, #000000);">
        <div class="text-subtle" style="text-transform:uppercase; letter-spacing:1px; margin-bottom:5px;">Indeks Stabilitas</div>
        <div class="text-huge" style="color: {accent_color} !important;">{status}</div>
        <div style="margin-top:10px; display:flex; align-items:center; justify-content:center;">
            <span class="live-indicator" style="background-color: {accent_color};"></span>
            <span style="font-weight:600; font-size:14px;">{status_msg}</span>
        </div>
        <div class="text-subtle" style="margin-top:15px; opacity:0.6;">Update: {tanggal}</div>
    </div>
    """, unsafe_allow_html=True)

    # --- B. METRICS GRID (Compact) ---
    jml_sumber = len(data.get('sources', []))
    risk_display = "Low" if status == "HIJAU" else "High"
    risk_color = "#30D158" if status == "HIJAU" else "#FF453A"

    st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-item">
            <div style="font-size:24px;">📅</div>
            <div class="text-subtle" style="margin-top:5px;">Harian</div>
        </div>
        <div class="metric-item">
            <div style="font-size:24px; font-weight:700;">{jml_sumber}</div>
            <div class="text-subtle" style="margin-top:5px;">Sinyal</div>
        </div>
        <div class="metric-item">
            <div style="font-size:24px; font-weight:700; color:{risk_color} !important;">{risk_display}</div>
            <div class="text-subtle" style="margin-top:5px;">Risiko</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- C. CONTENT TABS ---
    t1, t2, t3 = st.tabs(["Executive", "Analisis", "Raw Data"])

    with t1:
        st.markdown(f"""
        <div class="ios-card">
            <div class="text-subtle" style="margin-bottom:10px;">RINGKASAN INTELIJEN</div>
            <div style="line-height:1.6; font-size:15px; opacity:0.9;">
                {data.get('executive_summary', '-')}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with t2:
        strat = data.get('strategic_analysis', {})
        tech = data.get('technical_audit', {})
        
        # Custom "Details" View using HTML instead of st.expander for better style control
        st.markdown(f"""
        <div class="ios-card">
            <div class="text-subtle" style="margin-bottom:10px;">DAMPAK POLITIK</div>
            <div style="font-size:14px; margin-bottom:20px;">{strat.get('political_impact', '-')}</div>
            <div style="height:1px; background-color:#2C2C2E; margin-bottom:20px;"></div>
            <div class="text-subtle" style="margin-bottom:10px;">SENTIMEN PUBLIK</div>
            <div style="font-size:14px;">{strat.get('public_sentiment', '-')}</div>
        </div>
        <div class="ios-card">
            <div class="text-subtle" style="margin-bottom:10px;">AUDIT REGULASI</div>
            <div style="font-size:14px;">{tech.get('regulations_involved', '-')}</div>
        </div>
        """, unsafe_allow_html=True)

    with t3:
        sources = data.get('sources', [])
        st.markdown('<div class="ios-card">', unsafe_allow_html=True)
        if sources:
            for s in sources:
                st.markdown(f"""
                <div style="padding-bottom:12px; margin-bottom:12px; border-bottom:1px solid #2C2C2E;">
                    <div style="font-weight:600; font-size:14px; margin-bottom:4px;">{s.get('title')}</div>
                    <a href="{s.get('url')}" target="_blank" style="font-size:12px;">🔗 Buka Sumber Asli</a>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<div style="text-align:center; opacity:0.5; font-size:14px;">Tidak ada sinyal berita negatif.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # Loading State (Clean)
    st.markdown("""
    <div style="text-align:center; padding-top:50px;">
        <div style="font-size:14px; color:#8E8E93;">Menghubungkan ke Jamsos Brain...</div>
    </div>
    """, unsafe_allow_html=True)