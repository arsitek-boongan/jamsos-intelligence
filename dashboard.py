import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import time

# --- KONFIGURASI ---
st.set_page_config(
    page_title="Jamsos Intelligence System",
    page_icon="🛡️",
    layout="wide"
)

# 🔴 GANTI INI DENGAN URL WORKER CLOUDFLARE ANDA 🔴
WORKER_URL = "https://jamsos-brain.arsitek-boongan.workers.dev"

# --- FUNGSI LOAD DATA ---
@st.cache_data(ttl=3600) # Cache data selama 1 jam biar hemat kuota
def load_data():
    try:
        response = requests.get(WORKER_URL)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Gagal mengambil data: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error koneksi: {e}")
        return None

# --- HEADER ---
st.title("🛡️ MANPOWER INTELLIGENCE SYSTEM")
st.markdown(f"*Sistem Pemantauan Dini & Analisis Strategis Ketenagakerjaan RI*")
st.divider()

# --- TOMBOL REFRESH ---
if st.button("🔄 Perbarui Analisis Intelijen"):
    st.cache_data.clear()
    st.rerun()

# --- LOAD DATA ---
with st.spinner('Sedang menghubungi satelit intelijen...'):
    data = load_data()

if data:
    # --- METRIK UTAMA ---
    col1, col2, col3 = st.columns(3)
    
    # Indikator Status
    status = data.get('social_stability_index', 'UNKNOWN')
    warna_status = "green" if status == "HIJAU" else "orange" if status == "KUNING" else "red"
    
    with col1:
        st.markdown(f"""
        <div style="background-color:{warna_status}; padding:20px; border-radius:10px; text-align:center;">
            <h2 style="color:white; margin:0;">STATUS: {status}</h2>
            <p style="color:white;">Indeks Stabilitas Sosial</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.metric(label="Tanggal Laporan", value=data.get('tanggal', '-'))
    
    with col3:
        jml_sumber = len(data.get('sources', []))
        st.metric(label="Sinyal Berita Masuk", value=f"{jml_sumber} Sumber")

    # --- EXECUTIVE SUMMARY ---
    st.subheader("📑 Executive Summary")
    st.info(data.get('executive_summary', 'Tidak ada data.'))

    # --- DUAL CORE ANALYSIS ---
    col_kiri, col_kanan = st.columns(2)

    with col_kiri:
        st.subheader("🏛️ Analisis Strategis (Eselon 1)")
        strat = data.get('strategic_analysis', {})
        with st.expander("Dampak Politik", expanded=True):
            st.write(strat.get('political_impact', '-'))
        with st.expander("Sentimen Publik", expanded=True):
            st.write(strat.get('public_sentiment', '-'))

    with col_kanan:
        st.subheader("⚙️ Audit Teknis (Eselon 2)")
        tech = data.get('technical_audit', {})
        with st.expander("Regulasi Terkait", expanded=True):
            st.write(tech.get('regulations_involved', '-'))
        with st.expander("Risiko Operasional", expanded=True):
            st.write(tech.get('operational_risks', '-'))

    # --- SUMBER BERITA ---
    st.divider()
    st.subheader("🔗 Sumber Data Intelijen")
    sources = data.get('sources', [])
    if sources:
        for s in sources:
            st.markdown(f"- [{s.get('title')}]({s.get('url')})")
    else:
        st.caption("Tidak ada berita spesifik yang menjadi trigger dalam 24 jam terakhir.")

    # --- FOOTER ---
    st.markdown("---")
    st.caption(f"Architecture by Arsitek Boongan | Powered by Gemini 2.5 Flash & Cloudflare Workers")

else:
    st.warning("Menunggu data dari Cloudflare...")