import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# --- 1. KONFIGURASI HALAMAN (MODERN) ---
st.set_page_config(
    page_title="Jamsos Intel",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 🔴 PENTING: GANTI URL INI DENGAN WORKER ANDA 🔴
WORKER_URL = "https://jamsos-brain.arsitek-boongan.workers.dev"

# --- 2. CUSTOM CSS (UNTUK TAMPILAN PREMIUM) ---
st.markdown("""
<style>
    /* Hapus Padding Berlebih di HP */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 5rem;
    }
    
    /* Card Style (Kotak Cantik) */
    .stCard {
        background-color: #1E1E1E;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        margin-bottom: 15px;
        border: 1px solid #333;
    }
    
    /* Status Banner yang Menyala */
    .status-banner {
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 0 20px rgba(0,0,0,0.5);
    }
    
    /* Typography */
    h1, h2, h3 { font-family: 'Inter', sans-serif; }
    .big-font { font-size: 24px !important; font-weight: bold; }
    .small-font { font-size: 14px !important; color: #888; }
    
    /* Sembunyikan Elemen Bawaan Streamlit yang Mengganggu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #0E1117;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #262730;
        border-bottom: 2px solid #FF4B4B;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. FUNGSI LOAD DATA ---
@st.cache_data(ttl=600) # Cache 10 menit
def get_data():
    try:
        response = requests.get(WORKER_URL)
        if response.status_code == 200:
            return response.json()
    except:
        return None
    return None

# --- 4. UI UTAMA ---

# Header Minimalis
col_logo, col_refresh = st.columns([8, 2])
with col_logo:
    st.markdown("### 🛡️ Jamsos Intel")
    st.caption("Manpower Early Warning System")
with col_refresh:
    if st.button("🔄", help="Refresh Data"):
        st.cache_data.clear()
        st.rerun()

# Load Data
data = get_data()

if data:
    # --- A. HERO SECTION (STATUS) ---
    status = data.get('social_stability_index', 'UNKNOWN')
    tanggal = data.get('tanggal', datetime.now().strftime("%Y-%m-%d"))
    
    # Logika Warna Modern
    if status == "HIJAU":
        bg_color = "linear-gradient(90deg, #05472A 0%, #00FF94 100%)"
        text_color = "white"
        icon = "✅"
    elif status == "KUNING":
        bg_color = "linear-gradient(90deg, #4A3B00 0%, #FFD700 100%)"
        text_color = "black"
        icon = "⚠️"
    else: # MERAH
        bg_color = "linear-gradient(90deg, #4A0000 0%, #FF0000 100%)"
        text_color = "white"
        icon = "🚨"

    # Tampilkan Banner Status
    st.markdown(f"""
    <div class="status-banner" style="background: {bg_color}; color: {text_color};">
        <div class="small-font" style="color: {text_color}; opacity: 0.8;">STATUS STABILITAS SOSIAL</div>
        <div style="font-size: 3rem; font-weight: 800; line-height: 1.2;">{status}</div>
        <div style="margin-top: 10px; font-weight: 500;">{icon} Update: {tanggal}</div>
    </div>
    """, unsafe_allow_html=True)

    # --- B. KEY METRICS (GRID) ---
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown('<div class="stCard" style="text-align:center;"><h4>📅</h4><p>Harian</p></div>', unsafe_allow_html=True)
    with m2:
        jml_sumber = len(data.get('sources', []))
        st.markdown(f'<div class="stCard" style="text-align:center;"><h4>📡 {jml_sumber}</h4><p>Sinyal</p></div>', unsafe_allow_html=True)
    with m3:
        # Mock Risk Score (Bisa dikembangkan nanti)
        risk_score = "Low" if status == "HIJAU" else "High"
        st.markdown(f'<div class="stCard" style="text-align:center;"><h4>📊 {risk_score}</h4><p>Risiko</p></div>', unsafe_allow_html=True)

    # --- C. MAIN CONTENT (TABS FOR MOBILE) ---
    # Menggunakan Tabs agar tidak scroll panjang di HP
    tab1, tab2, tab3 = st.tabs(["📑 Executive", "🧠 Analisis", "🔗 Sumber"])

    with tab1:
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.subheader("Executive Summary")
        st.write(data.get('executive_summary', '-'))
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        # Strategic Analysis
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.caption("STRATEGIC IMPACT")
        strat = data.get('strategic_analysis', {})
        with st.expander("🏛️ Dampak Politik", expanded=True):
            st.write(strat.get('political_impact', '-'))
        with st.expander("🗣️ Sentimen Publik"):
            st.write(strat.get('public_sentiment', '-'))
        st.markdown('</div>', unsafe_allow_html=True)

        # Technical Audit
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.caption("TECHNICAL AUDIT")
        tech = data.get('technical_audit', {})
        with st.expander("⚖️ Regulasi Terkait"):
            st.write(tech.get('regulations_involved', '-'))
        with st.expander("⚙️ Risiko Operasional"):
            st.write(tech.get('operational_risks', '-'))
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        sources = data.get('sources', [])
        if sources:
            for s in sources:
                st.markdown(f"**🔗 [{s.get('title')}]({s.get('url')})**")
        else:
            st.info("Tidak ada trigger berita signifikan hari ini.")
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # Skeleton Loading Animation (Biar terlihat canggih saat loading)
    st.warning("Menghubungkan ke Satelit Intelijen...")
    st.progress(30)