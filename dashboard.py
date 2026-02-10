import streamlit as st
import requests
from datetime import datetime

# --- 1. CONFIG: WIDE MODE (Standar Dashboard Profesional) ---
st.set_page_config(
    page_title="Manpower Intel",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 🔴 URL WORKER ---
WORKER_URL = "https://jamsos-brain.arsitek-boongan.workers.dev"

# --- 2. MINIMALIST CSS (Hanya untuk merapikan, bukan memaksa) ---
st.markdown("""
<style>
    /* Hapus padding atas yang kosong */
    .block-container { padding-top: 1rem; padding-bottom: 5rem; }
    
    /* Styling Banner Status agar Modern & Flat */
    .status-box {
        padding: 20px;
        border-radius: 12px;
        color: white;
        margin-bottom: 25px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Typography yang bersih */
    .big-stat { font-size: 3rem; font-weight: 800; line-height: 1; }
    .sub-stat { font-size: 1rem; opacity: 0.9; font-weight: 500; }
    .meta-text { font-size: 0.8rem; opacity: 0.7; }
    
    /* Card Container untuk konten */
    .content-card {
        background-color: #262730; /* Streamlit Dark Grey */
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #333;
        height: 100%;
    }
    
    /* Divider halus */
    hr { margin-top: 10px; margin-bottom: 10px; border-color: #444; }
</style>
""", unsafe_allow_html=True)

# --- 3. LOGIC (Robust Error Handling) ---
@st.cache_data(ttl=300)
def fetch_intel():
    try:
        # Timeout 20 detik cukup untuk Gemini Flash
        r = requests.get(WORKER_URL, timeout=20)
        if r.status_code == 200:
            return r.json()
    except Exception as e:
        return None
    return None

# --- 4. UI STRUCTURE ---

# HEADER SEDERHANA
c1, c2 = st.columns([6, 1])
with c1:
    st.title("🛡️ Manpower Intel")
with c2:
    if st.button("Refresh 🔄", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# LOAD DATA
data = fetch_intel()

if data:
    # --- A. STATUS BANNER (HEADS UP DISPLAY) ---
    status = data.get('social_stability_index', 'UNKNOWN')
    tanggal = data.get('tanggal', '-')
    
    # Warna Flat Modern (Bukan Gradient Norak)
    if status == "HIJAU":
        bg_color = "#10B981" # Emerald Green
        icon = "✅"
        msg = "STABIL / AMAN"
    elif status == "KUNING":
        bg_color = "#F59E0B" # Amber
        icon = "⚠️"
        msg = "WASPADA"
    else:
        bg_color = "#EF4444" # Red
        icon = "🚨"
        msg = "KRISIS / BAHAYA"

    # Tampilan Banner (HTML)
    st.markdown(f"""
    <div class="status-box" style="background-color: {bg_color};">
        <div>
            <div class="meta-text">INDEKS STABILITAS SOSIAL</div>
            <div class="big-stat">{icon} {status}</div>
            <div class="sub-stat">{msg}</div>
        </div>
        <div style="text-align:right;">
            <div class="big-stat">{datetime.now().strftime('%H:%M')}</div>
            <div class="meta-text">Live Monitoring</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- B. KPI GRID (NATIVE STREAMLIT) ---
    # Menggunakan native columns agar responsif otomatis di HP
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    with kpi1:
        st.metric("📅 Tanggal Laporan", tanggal)
    with kpi2:
        jml = len(data.get('sources', []))
        st.metric("📡 Sinyal Masuk", f"{jml} Berita")
    with kpi3:
        # Dummy Logic untuk contoh
        st.metric("🤖 AI Confidence", "98%")
    with kpi4:
        risk = "Rendah" if status == "HIJAU" else "Tinggi"
        st.metric("📊 Tingkat Risiko", risk)

    st.markdown("---")

    # --- C. MAIN CONTENT (SPLIT VIEW) ---
    # Di Desktop: Kiri (Analisis), Kanan (Berita)
    # Di HP: Otomatis Atas-Bawah
    
    col_main, col_side = st.columns([2, 1])

    with col_main:
        st.subheader("📑 Executive Summary")
        st.info(data.get('executive_summary', 'Data tidak tersedia.'))
        
        st.subheader("🧠 Analisis Strategis")
        strat = data.get('strategic_analysis', {})
        
        with st.expander("🏛️ Dampak Politik & Kebijakan", expanded=True):
            st.write(strat.get('political_impact', '-'))
            
        with st.expander("🗣️ Sentimen Publik"):
            st.write(strat.get('public_sentiment', '-'))
            
        with st.expander("⚖️ Audit Regulasi & Risiko"):
            tech = data.get('technical_audit', {})
            st.markdown(f"**Regulasi:** {tech.get('regulations_involved', '-')}")
            st.markdown(f"**Risiko:** {tech.get('operational_risks', '-')}")

    with col_side:
        st.subheader("🔗 Sumber Data")
        sources = data.get('sources', [])
        
        if sources:
            for s in sources:
                with st.container(border=True):
                    st.markdown(f"**{s.get('title')}**")
                    st.markdown(f"[Buka Sumber ↗️]({s.get('url')})")
        else:
            st.caption("Tidak ada anomali berita yang terdeteksi dalam 24 jam terakhir.")
            st.markdown("""
            <div style="padding:20px; border:1px dashed #555; border-radius:10px; text-align:center; color:#777;">
                Scanning System Active...
            </div>
            """, unsafe_allow_html=True)

else:
    # Tampilan Loading / Error yang rapi
    st.warning("⚠️ Sedang menghubungi Jamsos Brain...")
    st.markdown("Jika loading > 30 detik, silakan refresh halaman.")