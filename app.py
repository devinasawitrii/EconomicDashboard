import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="Actionable Insights",
    layout="wide"
)

# Session state untuk tab
if 'main_tab' not in st.session_state:
    st.session_state.main_tab = 'Neraca Nasional'

# CSS supaya hilang scroll horizontal dan rapat
st.markdown("""
<style>
    html, body, .main {
        overflow-x: hidden !important;
        max-width: 100vw !important;
        margin: 0; padding: 0;
    }
    .block-container {
        padding: 0.5rem 1rem 0.5rem 1rem !important;
        max-width: 100vw !important;
    }
    /* Header rapat */
    .logo-title {
        color: navy;
        font-size: 24px !important;
        font-weight: bold;
        margin-bottom: 0;
        padding-bottom: 0;
        line-height: 1.1;
        text-align: center;
    }
    .subtitle {
        color: #0070c0;
        font-size: 14px !important;
        font-style: italic;
        margin-top: 0;
        margin-bottom: 0.5rem;
        text-align: center;
    }
    /* Option menu rapat dan kecil */
    .nav-link {
        padding: 6px 10px !important;
        font-size: 12px !important;
        margin: 0 1px !important;
        border-radius: 0 !important;
    }
    .nav-link-selected {
        border-bottom: 3px solid navy !important;
    }
    /* Chart container full width */
    .chart-container {
        padding: 0 !important;
        margin: 0 auto !important;
        max-width: 100vw !important;
        overflow-x: hidden !important;
    }
    /* Grafik height kecil supaya muat */
    .js-plotly-plot {
        height: 250px !important;
    }
</style>
""", unsafe_allow_html=True)

# Header sederhana
st.markdown('<div class="logo-title">ACTIONABLE INSIGHTS</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Generate wisdom from fingertip</div>', unsafe_allow_html=True)

# Main Navigation horizontal
tabs = ['Neraca Nasional', 'Indeks Harga', 'Ekspor-Impor', 'APBN', 'Ketenagakerjaan', 'Kemiskinan', 'IPM']
try:
    default_idx = tabs.index(st.session_state.main_tab)
except:
    default_idx = 0

selected_tab = option_menu(
    menu_title=None,
    options=tabs,
    default_index=default_idx,
    orientation="horizontal",
    styles={
        "container": {"padding": "0 !important", "background-color": "white", "margin-bottom": "0.5rem"},
        "nav-link": {"font-weight": "600", "color": "#333", "background-color": "#f0f0f0", "padding": "5px 10px", "margin": "0 2px"},
        "nav-link-selected": {"background-color": "#0070c0", "color": "white", "border-bottom": "3px solid navy"},
        "nav-link:hover": {"background-color": "#e0e0e0"},
    }
)

if selected_tab != st.session_state.main_tab:
    st.session_state.main_tab = selected_tab
    st.experimental_rerun()

st.markdown('<div class="chart-container">', unsafe_allow_html=True)

# Semua konten dalam satu kolom penuh (rapat)
if st.session_state.main_tab == 'Neraca Nasional':
    try:
        df = pd.read_csv('Sheet 1_Full Data_data.csv')
        df.columns = ['Period', 'Growth']
    except:
        # Data contoh jika csv tidak ditemukan
        df = pd.DataFrame({
            'Period': [f'2020 Q{i+1}' for i in range(16)],
            'Growth': [5.2, -5.3, -3.5, -2.1, -0.7, 7.1, 3.7, 5.0, 5.4, 5.1, 5.2, 5.3, 4.9, 5.0, 5.1, 4.8]
        })

    fig = px.line(df, x='Period', y='Growth', title='Pertumbuhan Ekonomi y-o-y',
                  labels={'Growth': 'Y-O-Y (%)', 'Period': 'Quarter'},
                  markers=True)
    fig.update_layout(
        margin=dict(l=30, r=30, t=30, b=30),
        plot_bgcolor='white',
        yaxis=dict(range=[-6, 8], tickvals=[-5, 0, 5]),
        xaxis=dict(tickangle=0),
        height=250  # Set tinggi kecil supaya muat
    )
    fig.update_traces(line=dict(color='navy', width=2), marker=dict(size=5, color='navy'))
    fig.update_xaxes(showgrid=True, gridcolor='lightgray')
    fig.update_yaxes(showgrid=True, gridcolor='lightgray')

    st.plotly_chart(fig, use_container_width=True)

elif st.session_state.main_tab == 'Indeks Harga':
    df = pd.DataFrame({
        'Period': pd.date_range('2023-01', periods=12, freq='M').strftime('%Y-%m'),
        'Value': np.random.uniform(-1, 5, 12)
    })
    fig = px.line(df, x='Period', y='Value', title='Inflasi y-o-y (%)', markers=True)
    fig.update_layout(margin=dict(l=30, r=30, t=30, b=30), plot_bgcolor='white', height=250)
    fig.update_traces(line=dict(color='teal', width=2), marker=dict(size=5, color='teal'))
    st.plotly_chart(fig, use_container_width=True)

elif st.session_state.main_tab == 'Ekspor-Impor':
    df = pd.DataFrame({
        'Period': pd.date_range('2023-01', periods=12, freq='M').strftime('%Y-%m'),
        'Value': np.random.uniform(10000, 30000, 12)
    })
    fig = px.line(df, x='Period', y='Value', title='Nilai ekspor (migas-non migas) (Juta USD)', markers=True)
    fig.update_layout(margin=dict(l=30, r=30, t=30, b=30), plot_bgcolor='white', height=250)
    fig.update_traces(line=dict(color='teal', width=2), marker=dict(size=5, color='teal'))
    st.plotly_chart(fig, use_container_width=True)

elif st.session_state.main_tab == 'APBN':
    df = pd.DataFrame({
        'Period': [f"2023 Q{i}" for i in range(1, 5)] + [f"2024 Q{i}" for i in range(1, 5)],
        'Value': np.random.uniform(500, 1500, 8)
    })
    fig = px.line(df, x='Period', y='Value', title='Belanja Pegawai (Triliun Rupiah)', markers=True)
    fig.update_layout(margin=dict(l=30, r=30, t=30, b=30), plot_bgcolor='white', height=250)
    fig.update_traces(line=dict(color='teal', width=2), marker=dict(size=5, color='teal'))
    st.plotly_chart(fig, use_container_width=True)

elif st.session_state.main_tab == 'Ketenagakerjaan':
    df = pd.DataFrame({
        'Period': ['Agu 2022', 'Feb 2023', 'Agu 2023', 'Feb 2024'],
        'Value': np.random.uniform(3, 7, 4)
    })
    fig = px.line(df, x='Period', y='Value', title='TPT (%)', markers=True)
    fig.update_layout(margin=dict(l=30, r=30, t=30, b=30), plot_bgcolor='white', height=250)
    fig.update_traces(line=dict(color='teal', width=2), marker=dict(size=5, color='teal'))
    st.plotly_chart(fig, use_container_width=True)

elif st.session_state.main_tab == 'Kemiskinan':
    df = pd.DataFrame({
        'Period': ['Mar 2022', 'Sep 2022', 'Mar 2023', 'Sep 2023'],
        'Value': np.random.uniform(9, 11, 4)
    })
    fig = px.line(df, x='Period', y='Value', title='Persentase penduduk miskin (%)', markers=True)
    fig.update_layout(margin=dict(l=30, r=30, t=30, b=30), plot_bgcolor='white', height=250)
    fig.update_traces(line=dict(color='teal', width=2), marker=dict(size=5, color='teal'))
    st.plotly_chart(fig, use_container_width=True)

elif st.session_state.main_tab == 'IPM':
    df = pd.DataFrame({
        'Period': [str(y) for y in range(2020, 2024)],
        'Value': np.random.uniform(70, 75, 4)
    })
    fig = px.line(df, x='Period', y='Value', title='IPM', markers=True)
    fig.update_layout(margin=dict(l=30, r=30, t=30, b=30), plot_bgcolor='white', height=250)
    fig.update_traces(line=dict(color='teal', width=2), marker=dict(size=5, color='teal'))
    st.plotly_chart(fig, use_container_width=True)

# Singkat insight supaya tidak terlalu panjang dan membuat scroll
st.markdown("### Insight")
st.markdown("- Insight 1: ...")
st.markdown("- Insight 2: ...")
st.markdown("- Insight 3: ...")

st.markdown('</div>', unsafe_allow_html=True)
