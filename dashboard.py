import streamlit as st
import requests
from datetime import datetime, timedelta

# --- 1. CONFIG ---
st.set_page_config(
    page_title="Manpower Intel",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 🔴 URL WORKER
WORKER_URL = "https://jamsos-brain.arsitek-boongan.workers.dev"

# --- 2. CSS MODERN & RESPONSIF ---
st.markdown("""
<style>
    /* Hapus Jarak Berlebih */
    .block-container { padding-top: 2rem; padding-bottom: 5rem; }
    
    /* Sembunyikan "Running" */
    .stStatusWidget { visibility: hidden; }
    
    /* Status Banner Style */
    .status-box {
        padding: 25px;
        border-radius: 12px;
        color: white;
        margin-bottom: 25px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* MEDIA QUERY (HP Fix) */
    @media (max-width: 600px) {
        .status-box {
            flex-direction: column;
            text-align: center;
            gap: 15px;
        }
        .status-box > div { width: 100%; text-align: center !important; }
    }

    /* Typography */
    .big-stat { font-size: 2.5rem; font-weight: 800; line-height: 1.2; }
    .sub-stat { font-size: 1rem; opacity: 0.9; font-weight: 500; letter-spacing: 1px; }
    .meta-text { font-size: 0.8rem; opacity: 0.7; text-transform: uppercase; }
    
    /* Card Container */
    .content-card {
        background-color: #262730;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #444;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. LOGIC (DENGAN PENANGANAN ERROR KUOTA) ---
@st.cache_data(ttl=300, show_spinner=False)
def fetch_intel():
    try:
        r = requests.get(WORKER_URL, timeout=25)
        data = r.json()
        
        # Cek jika Google Marah (Kuota Habis)
        if "error" in data:
            return {"system_error": True, "message": data["message"]}
            
        return data
    except Exception as e:
        return {"system_error": True, "message": str(e)}

# --- 4. UI STRUCTURE ---

# Header & Refresh
st.markdown("<h1 style='margin-bottom: 5px;'>Manpower Intel</h1>", unsafe_allow_html=True)

if st.button("Refresh Data"):
    st.cache_data.clear()
    st.rerun()

st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

# Load Data
with st.spinner("Menghubungkan ke Satelit Intelijen..."):
    data = fetch_intel()

# --- LOGIKA TAMPILAN ---

# Skenario 1: Error Kuota / Sistem
if data and data.get("system_error"):
    st.error("⚠️ SISTEM SEDANG SIBUK (Cooling Down)")
    st.warning(f"Google API Rate Limit Reached. Mohon tunggu 1 menit sebelum refresh lagi.\n\nDetail: {data.get('message')}")

# Skenario 2: Data Berhasil
elif data:
    status = data.get('social_stability_index', 'UNKNOWN')
    tanggal = data.get('tanggal', '-')
    
    # Hitung Waktu WIB (UTC + 7)
    wib_now = datetime.utcnow() + timedelta(hours=7)
    jam_wib = wib_now.strftime('%H:%M') + " WIB"

    # Logic Warna Flat
    if status == "HIJAU":
        bg_color = "#10B981" # Green
        msg = "STABIL / AMAN"
    elif status == "KUNING":
        bg_color = "#F59E0B" # Amber
        msg = "WASPADA"
    else:
        bg_color = "#EF4444" # Red
        msg = "BAHAYA"

    # --- A. STATUS BANNER (WIB FIXED) ---
    st.markdown(f"""
    <div class="status-box" style="background-color: {bg_color};">
        <div style="text-align: left;">
            <div class="meta-text">INDEKS STABILITAS SOSIAL</div>
            <div class="big-stat">{status}</div>
            <div class="sub-stat">{msg}</div>
        </div>
        <div style="text-align: right;">
            <div class="big-stat">{jam_wib}</div>
            <div class="meta-text">Live Monitoring • {tanggal}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- B. KPI GRID ---
    k1, k2, k3, k4 = st.columns(4)
    with k1: st.metric("📅 Laporan", tanggal)
    with k2: st.metric("📡 Sinyal", f"{len(data.get('sources', []))} Berita")
    with k3: st.metric("🤖 AI Status", "Active")
    with k4: st.metric("📊 Risiko", "Rendah" if status=="HIJAU" else "Tinggi")

    st.markdown("---")

    # --- C. MAIN CONTENT ---
    main_col, side_col = st.columns([2, 1])

    with main_col:
        st.subheader("📑 Executive Summary")
        st.info(data.get('executive_summary', 'Tidak ada data.'))
        
        st.subheader("🧠 Analisis Strategis")
        strat = data.get('strategic_analysis', {})
        
        with st.expander("🏛️ Dampak Politik", expanded=True):
            st.write(strat.get('political_impact', '-'))
        with st.expander("🗣️ Sentimen Publik"):
            st.write(strat.get('public_sentiment', '-'))
        with st.expander("⚖️ Audit Regulasi"):
            tech = data.get('technical_audit', {})
            st.write(f"**Regulasi:** {tech.get('regulations_involved', '-')}")
            st.write(f"**Risiko:** {tech.get('operational_risks', '-')}")

    with side_col:
        st.subheader("🔗 Sumber Data")
        sources = data.get('sources', [])
        if sources:
            for s in sources:
                with st.container(border=True):
                    st.markdown(f"**{s.get('title')}**")
                    st.markdown(f"[Buka Link ↗️]({s.get('url')})")
        else:
            st.caption("Tidak ada berita negatif signifikan.")
            st.markdown("""
            <div style="padding:20px; border:1px dashed #555; border-radius:10px; text-align:center; color:#777; font-size:12px;">
                System Scanning...<br>No Threats Found
            </div>
            """, unsafe_allow_html=True)

else:
    st.warning("⚠️ Gagal terhubung ke Jamsos Brain. Silakan Refresh.")