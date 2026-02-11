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

# 🔴 URL WORKER
WORKER_URL = "https://jamsos-brain.arsitek-boongan.workers.dev"

# --- 2. CSS MODERN ---
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
    
    .stButton button { width: 100%; border-radius: 5px; }
    
    /* CUSTOM TABLE STYLE (MOBILE FRIENDLY) */
    .raw-table {
        width: 100%;
        border-collapse: collapse;
        font-family: sans-serif;
        font-size: 14px;
    }
    .raw-table th {
        text-align: left;
        padding: 12px 8px;
        border-bottom: 2px solid #555;
        color: #aaa;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 12px;
    }
    .raw-table td {
        padding: 12px 8px;
        border-bottom: 1px solid #333;
        vertical-align: top; /* Agar teks mulai dari atas */
        line-height: 1.5;
        color: #e0e0e0;
    }
    /* KUNCI MOBILE RESPONSIVE: Wrap Text */
    .wrap-text {
        white-space: normal !important; 
        word-wrap: break-word;
    }
    .badge {
        background: #333;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 11px;
        color: #bbb;
        white-space: nowrap;
    }
    .link-btn {
        color: #4da6ff;
        text-decoration: none;
        font-weight: bold;
    }
    .link-btn:hover { text-decoration: underline; }
</style>
""", unsafe_allow_html=True)

# --- 3. LOGIC ---
def get_wib_time():
    return (datetime.utcnow() + timedelta(hours=7)).strftime("%d %b %Y, %H:%M WIB")

def fetch_data(force_reset=False):
    url = WORKER_URL
    if force_reset:
        url += "/?reset=true"
    try:
        r = requests.get(url, timeout=45) 
        data = r.json()
        if "error" in data:
            return None, data["message"]
        return data, None
    except Exception as e:
        return None, str(e)

# --- 4. MAIN LAYOUT ---

st.title("Manpower Intel")
st.caption("Sistem Pemantauan Stabilitas Ketenagakerjaan Berbasis AI & Big Data")

# TOMBOL REFRESH
if st.button("Refresh"):
    with st.spinner("Memperbarui Data Intelijen..."):
        fresh_data, err = fetch_data(force_reset=True)
        if fresh_data:
            st.session_state["intel_data"] = fresh_data
            st.session_state["last_update_wib"] = get_wib_time()
            st.rerun()
        else:
            st.error(f"Gagal Refresh: {err}")

# Load Data
if "intel_data" not in st.session_state:
    with st.spinner("Menghubungkan ke Brain V26..."):
        data, err = fetch_data()
        if data:
            st.session_state["intel_data"] = data
            st.session_state["last_update_wib"] = get_wib_time()
        else:
            st.error(f"Koneksi Gagal: {err}")
            st.stop()

data = st.session_state["intel_data"]
last_update = st.session_state.get("last_update_wib", "-")

# --- 5. VISUALISASI ---

if data:
    status = data.get('social_stability_index', 'UNKNOWN')
    total_scanned = data.get('total_scanned', 0)
    
    if status == "HIJAU":
        bg_color = "#10B981"
        msg = "KONDUSIF"
        icon = "✅"
    elif status == "KUNING":
        bg_color = "#F59E0B"
        msg = "WASPADA / ESKALASI"
        icon = "⚠️"
    else:
        bg_color = "#EF4444"
        msg = "BAHAYA / KRISIS"
        icon = "🚨"

    # STATUS BANNER
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
            <div class="meta-text">Last Update: {last_update}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # METRICS
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.metric("📡 Total Scanning", f"{total_scanned} Feed")
    with m2: st.metric("🎯 Isu Kritis", f"{len(data.get('sources', []))} Item")
    with m3: 
        reg_count = data.get('technical_audit', {}).get('regulations_matched', '0')
        has_reg = "Ada" if "Sesuai" in str(reg_count) else "Umum"
        st.metric("⚖️ Basis Hukum", has_reg)
    with m4: st.metric("🤖 AI Engine", "Hybrid V26")

    st.markdown("---")

    # EXECUTIVE SUMMARY & SOURCES
    main, side = st.columns([2, 1])

    with main:
        st.subheader("📑 Executive Summary")
        exec_sum = data.get('executive_summary', '-')
        if "Auto-Source" in exec_sum:
            st.warning("⚠️ Mode Otomatis: AI tidak merinci sumber spesifik.")
        st.info(exec_sum)
        
        tab1, tab2, tab3 = st.tabs(["🧠 Strategis", "⚖️ Audit Hukum", "🔥 Politik"])
        
        with tab1:
            strat = data.get('strategic_analysis', {})
            st.markdown(f"**Sentimen Publik:**\n{strat.get('public_sentiment', '-')}")
        
        with tab2:
            audit = data.get('technical_audit', {})
            reg_match = audit.get('regulations_matched', 'Tidak ada data')
            if "Tidak ditemukan" in reg_match or "Gagal" in reg_match:
                st.error(reg_match)
            else:
                st.success(reg_match)
            st.markdown("**Compliance Gap:**")
            st.write(audit.get('compliance_gap', '-'))

        with tab3:
             strat = data.get('strategic_analysis', {})
             st.write(strat.get('political_impact', '-'))

    with side:
        st.subheader(f"🔗 {len(data.get('sources', []))} Sumber")
        sources = data.get('sources', [])
        
        if sources:
            for s in sources:
                with st.expander(f"📰 {s.get('title')[:40]}...", expanded=True):
                    st.caption(s.get('title'))
                    st.markdown(f"[Buka Artikel Asli]({s.get('url')})")
        else:
            st.caption("Tidak ada berita spesifik.")

    # --- D. BIG DATA RAW FEED (MOBILE RESPONSIVE HTML) ---
    st.markdown("---")
    with st.expander("📂 LIHAT DATA MENTAH (RAW BIG DATA FEED)", expanded=False):
        all_feed = data.get('all_feed', [])
        
        if all_feed:
            # Kita bangun tabel HTML manual agar bisa wrap text
            html_table = """
            <table class="raw-table">
                <thead>
                    <tr>
                        <th style="width: 15%;">Kategori</th>
                        <th style="width: 70%;">Judul Berita</th>
                        <th style="width: 15%;">Link</th>
                    </tr>
                </thead>
                <tbody>
            """
            
            for item in all_feed:
                # Bersihkan label dari kurung siku
                label = item.get('type', '').replace('[','').replace(']','')
                title = item.get('title', '-')
                url = item.get('url', '#')
                
                html_table += f"""
                <tr>
                    <td><span class="badge">{label}</span></td>
                    <td class="wrap-text">{title}</td>
                    <td><a href="{url}" target="_blank" class="link-btn">Lihat</a></td>
                </tr>
                """
            
            html_table += "</tbody></table>"
            st.markdown(html_table, unsafe_allow_html=True)
            
        else:
            st.write("Data mentah tidak tersedia.")