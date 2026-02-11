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

# 🔴 URL WORKER (Endpoint Pusat Analisis)
WORKER_URL = "https://jamsos-brain.arsitek-boongan.workers.dev"

# --- 2. CSS CUSTOM (UI/UX MODERN) ---
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
    
    /* Button Style */
    .stButton button { width: 100%; border-radius: 5px; height: 3em; }
</style>
""", unsafe_allow_html=True)

# --- 3. LOGIC PENGAMBILAN DATA ---
def get_wib_time():
    """Mengambil waktu saat ini dalam format WIB"""
    return (datetime.utcnow() + timedelta(hours=7)).strftime("%d %b %Y, %H:%M WIB")

def fetch_data(force_reset=False):
    """Mengambil data dari Cloudflare Worker"""
    url = WORKER_URL
    if force_reset:
        url += "/?reset=true"
        
    try:
        # Timeout 45 detik karena AI melakukan Deep Audit pada puluhan berita
        r = requests.get(url, timeout=45) 
        data = r.json()
        if "error" in data:
            return None, data["message"]
        return data, None
    except Exception as e:
        return None, str(e)

# --- 4. HEADER & CONTROL ---

st.title("Manpower Intel")
st.caption("Intelijen Strategis Ketenagakerjaan • Real-time Monitoring & Regulatory Audit")

# Tombol Refresh (Posisi Desktop: Di bawah Judul)
if st.button("Refresh"):
    with st.spinner("Memproses Big Data & Sinkronisasi Regulasi..."):
        fresh_data, err = fetch_data(force_reset=True)
        if fresh_data:
            st.session_state["intel_data"] = fresh_data
            st.session_state["last_update_wib"] = get_wib_time()
            st.rerun()
        else:
            st.error(f"Gagal Refresh: {err}")

# Load Data Awal
if "intel_data" not in st.session_state:
    with st.spinner("Membangun Koneksi ke Brain V53..."):
        data, err = fetch_data()
        if data:
            st.session_state["intel_data"] = data
            st.session_state["last_update_wib"] = get_wib_time()
        else:
            st.error(f"Koneksi Gagal: {err}")
            st.stop()

# Gunakan data dari memori sesi
data = st.session_state["intel_data"]
last_update = st.session_state.get("last_update_wib", "-")

# --- 5. VISUALISASI UTAMA ---

if data:
    # --- [MODIFIKASI] VISUALISASI STATUS ENGINE (Supaya Terlihat) ---
    engine_status = data.get("ai_engine", "System Ready")
    if "Gemini" in engine_status:
        st.success(f"**STATUS SYSTEM:** {engine_status}", icon="⚡")
    elif "Emergency" in engine_status or "Offline" in engine_status:
        st.error(f"**STATUS SYSTEM:** {engine_status}", icon="🆘")
    else:
        st.warning(f"**STATUS SYSTEM:** {engine_status}", icon="🛡️")
    # -------------------------------------------------------------

    status = data.get('social_stability_index', 'UNKNOWN')
    total_scanned = data.get('total_scanned', 0)
    
    # Konfigurasi Banner Berdasarkan Status
    if status == "HIJAU":
        bg_color = "#10B981"
        msg = "STABIL / KONDUSIF"
        icon = "✅"
    elif status == "KUNING":
        bg_color = "#F59E0B"
        msg = "WASPADA / ESKALASI"
        icon = "⚠️"
    else:
        bg_color = "#EF4444"
        msg = "BAHAYA / KRISIS"
        icon = "🚨"

    # A. BANNER STATUS STRATEGIS
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
            <div class="meta-text">Update: {last_update}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # B. KPI SUMMARY
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.metric("📡 Scanning", f"{total_scanned} Feed")
    with m2: st.metric("🎯 Isu Kritis", f"{len(data.get('sources', []))} Item")
    with m3: 
        audit = data.get('technical_audit', {})
        reg_match = audit.get('regulations_involved', audit.get('regulations_matched', ''))
        has_reg = "Ada" if "Sesuai" in str(reg_match) or "UU" in str(reg_match) else "Umum"
        st.metric("⚖️ Basis Hukum", has_reg)
    with m4: 
            # [LOGIKA PEMENDEK TEKS] Agar muat di kotak kecil
            raw_engine = data.get('ai_engine', 'Hybrid V53')
            
            if "Gemini" in raw_engine:
                display_text = "Gemini Flash ⚡"
            elif "70B" in raw_engine:
                display_text = "Groq 70B 🛡️"
            elif "8B" in raw_engine:
                display_text = "Groq 8B (SOS)" # Singkat, Padat, Jelas
            elif "Offline" in raw_engine:
                display_text = "OFFLINE ❌"
            else:
                display_text = "Hybrid V53"
                
            st.metric("🤖 AI Engine", display_text)

    st.markdown("---")

    # C. ANALISIS MENDALAM & SUMBER BERITA
    main_col, side_col = st.columns([2, 1])

    with main_col:
        st.subheader("📑 Executive Summary")
        exec_sum = data.get('executive_summary', '-')
        if "Auto-Source" in exec_sum:
            st.warning("⚠️ Catatan: Analisis menggunakan mode sampling otomatis.")
        st.info(exec_sum)
        
        # Tabs Analisis Strategis
        t1, t2, t3 = st.tabs(["🧠 Strategis", "⚖️ Audit Regulasi", "🔥 Dampak Politik"])
        
        with t1:
            strat = data.get('strategic_analysis', {})
            st.markdown(f"**Sentimen Publik:**\n{strat.get('public_sentiment', '-')}")
        
        with t2:
            st.markdown("#### Hasil Audit Database User")
            # Logika Audit Regulasi (Pencocokan Database)
            reg_match = audit.get('regulations_matched', audit.get('regulations_involved', 'Tidak ada data'))
            if "Tidak ditemukan" in reg_match or "TIDAK ADA" in reg_match:
                st.error(reg_match)
            else:
                st.success(reg_match)
            
            st.markdown("#### Compliance Gap & Risks")
            st.write(audit.get('compliance_gap', audit.get('operational_risks', '-')))

        with t3:
             st.write(data.get('strategic_analysis', {}).get('political_impact', '-'))

    with side_col:
        st.subheader(f"🔗 {len(data.get('sources', []))} Sumber Terpilih")
        sources = data.get('sources', [])
        
        if sources:
            for s in sources:
                # Expander Default Tertutup agar tampilan samping bersih
                title_clean = s.get('title', '')[:35] + "..." if len(s.get('title', '')) > 35 else s.get('title', '')
                with st.expander(f"📰 {title_clean}", expanded=False):
                    st.caption(s.get('title'))
                    st.markdown(f"[Buka Artikel Asli]({s.get('url')})")
        else:
            st.caption("Tidak ada berita krusial yang terpilih.")

    # D. RAW BIG DATA FEED (CARD VIEW UNTUK HP)
    st.markdown("---")
    with st.expander("📂 LIHAT DATA MENTAH (RAW BIG DATA FEED)", expanded=False):
        st.caption(f"Menampilkan {total_scanned} data berita yang berhasil disedot sistem hari ini.")
        
        all_feed = data.get('all_feed', [])
        if all_feed:
            # Loop melalui feed (Batasi 50 agar tidak berat di HP)
            for item in all_feed[:50]:
                with st.container(border=True):
                    c_txt, c_lk = st.columns([5, 1])
                    with c_txt:
                        label = item.get('type', 'NEWS').replace('[','').replace(']','')
                        st.caption(f"🏷️ {label}")
                        # Judul akan otomatis wrapping ke bawah jika panjang
                        st.markdown(f"**{item.get('title', '-')}**")
                    with c_lk:
                        st.link_button("Lihat", item.get('url', '#'))
        else:
            st.info("Feed data mentah tidak tersedia.")

# Footer
st.markdown("<br><hr><center><small>Manpower Intelligence System © 2026</small></center>", unsafe_allow_html=True)