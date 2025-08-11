import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_option_menu import option_menu

# Page config
st.set_page_config(page_title="Actionable Insights", layout="wide")

# Hilangkan scroll + full height
st.markdown("""
<style>
html, body, [class*="css"] {
    overflow: hidden !important;
}
section.main > div {
    overflow-y: hidden !important;
    overflow-x: hidden !important;
}
.block-container {
    padding-top: 1rem !important;
    padding-bottom: 0rem !important;
}
.sidebar-content {
    height: 100vh;
}
.chart-container {
    border: none;
    padding: 0px 20px 20px 20px;
    background-color: white;
}
.menu-item {
    display: block;
    padding: 12px 15px;
    font-weight: bold;
    color: #333;
    background-color: #f0f0f0;
    text-decoration: none;
    transition: background-color 0.2s, color 0.2s;
}
.menu-item:hover {
    background-color: #e0e0e0;
}
.menu-item.active {
    background-color: #0070c0;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# Session state
if 'main_tab' not in st.session_state:
    st.session_state.main_tab = 'Neraca Nasional'
if 'side_tab' not in st.session_state:
    st.session_state.side_tab = 'Pertumbuhan ekonomi y-o-y'

# Header
col1, col2, col3 = st.columns([1, 3, 1])
with col1:
    st.image("aig_logo.png", width=100)
with col2:
    st.markdown('<div style="text-align:center;font-size:32px;font-weight:bold;color:navy;">ACTIONABLE INSIGHTS</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center;font-size:18px;font-style:italic;color:#0070c0;margin-top:-5px;">Generate wisdom from fingertip</div>', unsafe_allow_html=True)
with col3:
    st.image("bps_logo.png", width=120)

# Main navigation
main_tabs_list = ['Neraca Nasional', 'Indeks Harga', 'Ekspor-Impor', 'APBN', 'Ketenagakerjaan', 'Kemiskinan', 'IPM']
default_main_index = main_tabs_list.index(st.session_state.main_tab) if st.session_state.main_tab in main_tabs_list else 0
selected_main_tab = option_menu(
    None,
    options=main_tabs_list,
    default_index=default_main_index,
    orientation="horizontal",
    styles={
        "container": {"padding": "0px", "background-color": "white"},
        "nav-link": {"font-size": "14px", "font-weight": "bold", "color": "#333", "background-color": "#f0f0f0",
                     "padding": "15px 10px", "margin": "0px 2px", "border-bottom": "5px solid #0070c0"},
        "nav-link-selected": {"background-color": "#0070c0", "color": "white", "border-bottom": "5px solid navy"}
    }
)
if selected_main_tab != st.session_state.main_tab:
    st.session_state.main_tab = selected_main_tab

# Side tabs config
side_tabs_config = {
    'Neraca Nasional': ['Pertumbuhan ekonomi y-o-y', 'Pertumbuhan ekonomi q to q', 'Pertumbuhan ekonomi c to c', 'Indeks implisit', 'PDB ADHB', 'PDB ADHK'],
    'Indeks Harga': ['Inflasi y-o-y', 'Inflasi m to m', 'IHP', 'IHPB', 'Indeks Retail'],
    'Ekspor-Impor': ['Nilai ekspor (migas-non migas)', 'Volume ekspor (migas-non migas)', 'Nilai impor (migas-non migas)', 'Volume impor (migas-non migas)'],
    'APBN': ['Belanja Pegawai', 'Belanja Barang dan Jasa', 'Belanja Modal', 'Belanja Bantuan Sosial', 'Belanja Lainnya'],
    'Ketenagakerjaan': ['TPT', 'Jumlah pengangguran', 'Persentase tenaga kerja (formal-informal)', 'Proporsi lapangan kerja'],
    'Kemiskinan': ['Persentase penduduk miskin', 'Jumlah penduduk miskin', 'Gini ratio', 'Pengeluaran per kapita', 'Konsumsi per kapita', 'PDB per kapita'],
    'IPM': ['IPM', 'Indeks Pendidikan', 'Indeks kesehatan', 'Daya Beli']
}

# Layout
col1, col2 = st.columns([1, 4])

# Sidebar menu custom tanpa button abu
with col1:
    for tab in side_tabs_config[st.session_state.main_tab]:
        active_class = "active" if st.session_state.side_tab == tab else ""
        if st.markdown(f'<a class="menu-item {active_class}" href="?side={tab}">{tab}</a>', unsafe_allow_html=True):
            st.session_state.side_tab = tab

# Chart & content
with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)

    # Contoh chart
    sample_data = pd.DataFrame({
        'Period': [f"2023 Q{i}" for i in range(1, 5)],
        'Value': np.random.uniform(-2, 6, 4)
    })
    fig_sample = px.line(sample_data, x='Period', y='Value', title=st.session_state.side_tab, markers=True)
    fig_sample.update_traces(line=dict(color='teal', width=2), marker=dict(size=6, color='teal'))
    fig_sample.update_layout(height=400, plot_bgcolor='white', margin=dict(l=40, r=40, t=40, b=40))
    st.plotly_chart(fig_sample, use_container_width=True)

    st.caption("Note: Data sample")

    # Insight
    st.markdown("#### Insight:")
    st.markdown("* Insight 1: ...")
    st.markdown("* Insight 2: ...")
    st.markdown("* Insight 3: ...")

    st.markdown('</div>', unsafe_allow_html=True)
