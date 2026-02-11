import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

# --- 1. CONFIG ---
st.set_page_config(
    page_title="Manpower Intel",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 🔴 URL WORKER (Pastikan tidak ada slash di akhir)
WORKER_URL = "https://jamsos-brain.arsitek-boongan.workers.dev"

# --- 2. CSS MODERN (Dark & Clean) ---
st.markdown("""
<style>
    .block-container { padding-top: 2rem; padding-bottom: 5rem; }
    
    /* Status Box Style */
    .status-box {
        padding: 20px;
        border-radius: 12px;
        color: white;
        margin-bottom: 25px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .big-stat { font-size: 2.8rem; font-weight: 800; line-height: 1.1; letter-spacing: -1px; }
    .sub-stat { font-size: 1.1rem; opacity: 0.95; font-weight: 600; letter-spacing: 1px; }
    .meta-text { font-size: 0.85rem; opacity: 0.8; text-transform: uppercase; margin-top: 5px; }
    
    /* Card Style */
    .stCard {
        background-color: #1E1E1E;
        border: 1px solid #333;
        padding: 15px;
        border-radius: 8px;
    }
    
    /* Metric Style override */
    [data-testid="stMetricValue"] { font-size: 1.8rem !important; }
</style>
""", unsafe_allow_html=True)

# --- 3. LOGIC SMART FETCH ---
def fetch_data(force_reset=False):
    """
    Mengambil data dari Worker.
    force_reset=True akan mengirim ?reset=true untuk memaksa AI mikir ulang.
    """
    url = WORKER_URL
    if force_reset:
        url += "/?reset=true"
        
    try:
        # Timeout agak lama karena AI mikir keras (V26)
        r = requests.get(url, timeout=45) 
        data = r.json()
        
        if "error" in data:
            return None, data["message"]
            
        return data, None
    except Exception as e:
        return None, str(e)

# --- 4. MAIN LAYOUT ---

# Header & Control
c1, c2 = st.columns([5, 1])
with c1:
    st.title("Manpower Intel")
    st.caption("Sistem Pemantauan Stabilitas Ketenagakerjaan Berbasis AI & Big Data")

with c2:
    # Tombol Hard Reset
    if st.button("🔄 SCAN ULANG", type="primary", use_container_width=True):
        with st.spinner("Memaksa Satelit Scan Ulang (30-60 detik)..."):
            fresh_data, err = fetch_data(force_reset=True)
            if fresh_data:
                st.session_state["intel_data"] = fresh_data
                st.rerun()
            else:
                st.error(f"Gagal Scan: {err}")

# Load Data (Cache Session)
if "intel_data" not in st.session_state:
    with st.spinner("Menghubungkan ke Brain V26..."):
        data, err = fetch_data()
        if data:
            st.session_state["intel_data"] = data
        else:
            st.error(f"Koneksi Gagal: {err}")
            st.stop()
else:
    data = st.session_state["intel_data"]

# --- 5. VISUALISASI DATA ---

if data:
    # Parsing Data Utama
    status = data.get('social_stability_index', 'UNKNOWN')
    tanggal = data.get('tanggal', '-')
    total_scanned = data.get('total_scanned', 0) # Fitur V26
    
    # Warna Status
    if status == "HIJAU":
        bg_color = "#10B981" # Green
        msg = "KONDUSIF"
        icon = "✅"
    elif status == "KUNING":
        bg_color = "#F59E0B" # Amber
        msg = "WASPADA / ESKALASI"
        icon = "⚠️"
    else:
        bg_color = "#EF4444" # Red
        msg = "BAHAYA / KRISIS"
        icon = "🚨"

    # A. STATUS BANNER
    st.markdown(f"""
    <div class="status-box" style="background-color: {bg_color};">
        <div>
            <div class="meta-text">INDEKS STABILITAS SOSIAL</div>
            <div class="big-stat">{icon} {status}</div>
            <div class="sub-stat">{msg}</div>
        </div>
        <div style="text-align: right;">
            <div class="big-stat">{total_scanned}</div>
            <div class="sub-stat">Sinyal Terdeteksi</div>
            <div class="meta-text">Last Update: {tanggal}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # B. METRICS GRID
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.metric("📡 Total Scanning", f"{total_scanned} Feed", help="Total berita mentah yang dibaca sistem hari ini.")
    with m2: st.metric("🎯 Isu Kritis", f"{len(data.get('sources', []))} Item", help="Jumlah isu yang lolos filter AI.")
    with m3: 
        reg_count = data.get('technical_audit', {}).get('regulations_matched', '0')
        has_reg = "Ada" if "Sesuai" in str(reg_count) else "Umum"
        st.metric("⚖️ Basis Hukum", has_reg)
    with m4: st.metric("🤖 AI Engine", "Hybrid V26")

    st.markdown("---")

    # C. ANALISIS & SUMBER
    main, side = st.columns([2, 1])

    with main:
        st.subheader("📑 Executive Summary (Deep Analysis)")
        exec_sum = data.get('executive_summary', '-')
        if "Auto-Source" in exec_sum:
            st.warning("⚠️ Catatan: Analisis menggunakan mode otomatis karena AI tidak memilih spesifik.")
        st.info(exec_sum)
        
        # Tab Analisis
        tab1, tab2, tab3 = st.tabs(["🧠 Strategis", "⚖️ Audit Hukum (Evidence)", "🔥 Dampak Politik"])
        
        with tab1:
            strat = data.get('strategic_analysis', {})
            st.markdown(f"**Sentimen Publik:**\n{strat.get('public_sentiment', '-')}")
        
        with tab2:
            audit = data.get('technical_audit', {})
            st.markdown("#### 📜 Pencocokan Regulasi (Database User)")
            # Fitur V25/V26: Regulations Matched
            reg_match = audit.get('regulations_matched', 'Tidak ada data')
            if "Tidak ditemukan" in reg_match:
                st.error(reg_match)
            else:
                st.success(reg_match)
                
            st.markdown("#### ⚠️ Celah Kepatuhan (Compliance Gap)")
            st.write(audit.get('compliance_gap', audit.get('operational_risks', '-')))

        with tab3:
             strat = data.get('strategic_analysis', {})
             st.write(strat.get('political_impact', '-'))

    with side:
        st.subheader(f"🔗 {len(data.get('sources', []))} Sumber Terpilih")
        sources = data.get('sources', [])
        
        if sources:
            for s in sources:
                with st.expander(f"📰 {s.get('title')[:40]}...", expanded=True):
                    st.caption(s.get('title'))
                    st.markdown(f"[Buka Artikel Asli ↗️]({s.get('url')})")
        else:
            st.caption("Tidak ada berita spesifik terpilih.")

    # D. BIG DATA RAW FEED (Fitur V26)
    st.markdown("---")
    with st.expander("📂 LIHAT DATA MENTAH (RAW BIG DATA FEED)", expanded=False):
        st.caption("Ini adalah seluruh data yang masuk ke mesin penggilingan AI sebelum disaring.")
        
        all_feed = data.get('all_feed', [])
        if all_feed:
            # Buat DataFrame agar rapi
            df = pd.DataFrame(all_feed)
            if not df.empty and 'title' in df.columns:
                st.dataframe(
                    df[['type', 'title', 'url']], 
                    column_config={
                        "url": st.column_config.LinkColumn("Link Asli"),
                        "type": "Kategori",
                        "title": "Judul Berita"
                    },
                    use_container_width=True,
                    hide_index=True
                )
        else:
            st.write("Data mentah tidak disertakan dalam respon ini.")