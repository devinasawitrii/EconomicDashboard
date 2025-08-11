import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import base64
from streamlit_option_menu import option_menu

# Set page configuration
st.set_page_config(
    page_title="Actionable Insights",
    layout="wide"
)

# Initialize session state for navigation
if 'main_tab' not in st.session_state:
    st.session_state.main_tab = 'Neraca Nasional'

# Custom CSS for styling - optimized for no scroll
st.markdown("""
<style>
    /* Remove all default padding and margins */
    .block-container { 
        padding-top: 0.5rem !important;
        padding-bottom: 0rem !important;
        max-width: 100% !important;
    }
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 5px 0px;
        background-color: white;
        margin-bottom: 0.5rem;
    }
    .logo-title {
        color: navy;
        font-size: 28px;
        font-weight: bold;
        text-align: center;
        margin: 0;
        padding: 0;
    }
    .subtitle {
        color: #0070c0;
        font-size: 16px;
        text-align: center;
        font-style: italic;
        margin-top: -3px;
        margin-bottom: 0px;
    }
    .chart-container {
        border: none;
        border-radius: 0px;
        padding: 0px 10px 5px 10px;
        background-color: white;
        box-shadow: none;
    }
    .logo-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        padding-top: 5px;
    }
    /* Hide streamlit elements that take up space */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Reduce spacing in sidebar and main content */
    .css-1d391kg {padding-top: 0rem;}
    .css-18e3th9 {padding-top: 0rem;}
    
    /* Make insights section more compact */
    .insight-section {
        font-size: 14px;
        line-height: 1.2;
    }
    
    /* Reduce vertical spacing for all elements */
    .stMarkdown {
        margin-bottom: 0.2rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Compact Header with logos
col1, col2, col3 = st.columns([1, 3, 1])

with col1:
    # AIG Logo - Smaller size
    st.markdown("""
    <div class="logo-container">
        <img src="aig_logo.png" alt="AIG Logo" style="width: 70px; height: 70px; object-fit: contain;">
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Compact title and subtitle
    st.markdown('<div class="logo-title">ACTIONABLE INSIGHTS</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Generate wisdom from fingertip</div>', unsafe_allow_html=True)

with col3:
    # BPS Logo - Smaller size
    st.markdown("""
    <div class="logo-container">
        <img src="bps_logo.png" alt="BPS Logo" style="width: 85px; height: 70px; object-fit: contain;">
    </div>
    """, unsafe_allow_html=True)

# Main Navigation Menu - more compact
main_tabs_list = ['Neraca Nasional', 'Indeks Harga', 'Ekspor-Impor', 'APBN', 'Ketenagakerjaan', 'Kemiskinan', 'IPM']

try:
    default_main_index = main_tabs_list.index(st.session_state.main_tab)
except ValueError:
    default_main_index = 0

# Compact option menu
selected_main_tab = option_menu(
    menu_title=None,
    options=main_tabs_list,
    icons=None,
    menu_icon=None,
    default_index=default_main_index,
    orientation="horizontal",
    styles={
        "container": {"padding": "0px !important", "background-color": "white", "margin-bottom": "0.5rem", "flex-wrap": "nowrap"},
        "nav-link": {
            "font-size": "14px", 
            "font-weight": "bold",
            "color": "#333",
            "background-color": "#f0f0f0", 
            "text-align": "center", 
            "padding": "15px 10px",
            "margin":"0px 2px !important",
            "border-radius": "0px !important",
            "border-bottom": "5px solid #0070c0",
            "transition": "background-color 0.2s, color 0.2s, border-color 0.2s",
            "white-space": "nowrap"
        },
        "nav-link-selected": {
            "background-color": "#0070c0", 
            "color": "white",
            "border-bottom": "5px solid navy"
        },
        "nav-link:hover": {
            "background-color": "#e0e0e0",
            "border-bottom-color": "#005090"
        }
    }
)

# Update session state if main tab changed
if selected_main_tab != st.session_state.main_tab:
    st.session_state.main_tab = selected_main_tab
    st.rerun()

# Main content area - compact layout
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
chart_col, insight_col = st.columns([2.5, 1])

# Display content based on selected main tab
if st.session_state.main_tab == 'Neraca Nasional':
    # Original economic growth chart - reduced height
    try:
        df = pd.read_csv('Sheet 1_Full Data_data.csv')
        df.columns = ['Period', 'Growth']
        
        fig = px.line(df, x='Period', y='Growth', 
                     title='Pertumbuhan Ekonomi y-o-y',
                     labels={'Growth': 'Y-O-Y (%)', 'Period': 'Quarter of Periode'},
                     markers=True)
        
        fig.update_layout(
            xaxis=dict(
                tickmode='array',
                tickvals=[df['Period'][i] for i in range(0, len(df), 4)],
                ticktext=[f"{period.split()[0]} Q1" for period in df['Period'][::4]],
                title_font=dict(size=12),
            ),
            yaxis=dict(
                range=[-6, 8],
                tickvals=[-5, 0, 5],
                title_font=dict(size=12),
            ),
            plot_bgcolor='white',
            title_font=dict(size=14),
            height=320,  # Reduced height significantly
            margin=dict(l=30, r=30, t=40, b=30),  # Reduced margins
            hovermode="x unified"
        )
        
        fig.update_traces(
            line=dict(color='navy', width=2),
            marker=dict(size=5, color='navy'),
        )
        
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
        
        with chart_col:
            st.plotly_chart(fig, use_container_width=True)
        
    except FileNotFoundError:
        st.error("File 'Sheet 1_Full Data_data.csv' tidak ditemukan.")
        # Generate sample data for demo
        sample_periods = [f"2020 Q{i%4+1}" for i in range(16)]
        sample_growth = [5.2, -5.3, -3.5, -2.1, -0.7, 7.1, 3.7, 5.0, 5.4, 5.1, 5.2, 5.3, 4.9, 5.0, 5.1, 4.8]
        
        df_sample = pd.DataFrame({
            'Period': sample_periods,
            'Growth': sample_growth
        })
        
        fig = px.line(df_sample, x='Period', y='Growth', 
                     title='Pertumbuhan Ekonomi y-o-y (Sample Data)',
                     labels={'Growth': 'Y-O-Y (%)', 'Period': 'Quarter of Periode'},
                     markers=True)
        
        fig.update_traces(line=dict(color='navy', width=2), marker=dict(size=5, color='navy'))
        fig.update_layout(height=320, plot_bgcolor='white', margin=dict(l=30, r=30, t=40, b=30))
        
        with chart_col:
            st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error loading CSV file: {str(e)}")

elif st.session_state.main_tab == 'Indeks Harga':
    sample_data = pd.DataFrame({
        'Period': pd.date_range('2023-01', periods=12, freq='M').strftime('%Y-%m'),
        'Value': np.random.uniform(-1, 5, 12)
    })
    title = "Inflasi y-o-y (%)"
    
    fig_sample = px.line(sample_data, x='Period', y='Value', title=title, markers=True)
    fig_sample.update_traces(line=dict(color='teal', width=2), marker=dict(size=5, color='teal'))
    fig_sample.update_layout(height=320, plot_bgcolor='white', margin=dict(l=30, r=30, t=40, b=30))
    
    with chart_col:
        st.plotly_chart(fig_sample, use_container_width=True)

elif st.session_state.main_tab == 'Ekspor-Impor':
    sample_data = pd.DataFrame({
        'Period': pd.date_range('2023-01', periods=12, freq='M').strftime('%Y-%m'),
        'Value': np.random.uniform(10000, 30000, 12)
    })
    title = "Nilai ekspor (migas-non migas) (Juta USD)"
    
    fig_sample = px.line(sample_data, x='Period', y='Value', title=title, markers=True)
    fig_sample.update_traces(line=dict(color='teal', width=2), marker=dict(size=5, color='teal'))
    fig_sample.update_layout(height=320, plot_bgcolor='white', margin=dict(l=30, r=30, t=40, b=30))
    
    with chart_col:
        st.plotly_chart(fig_sample, use_container_width=True)

elif st.session_state.main_tab == 'APBN':
    sample_data = pd.DataFrame({
        'Period': [f"2023 Q{i}" for i in range(1, 5)] + [f"2024 Q{i}" for i in range(1, 5)],
        'Value': np.random.uniform(500, 1500, 8)
    })
    title = "Belanja Pegawai (Triliun Rupiah)"
    
    fig_sample = px.line(sample_data, x='Period', y='Value', title=title, markers=True)
    fig_sample.update_traces(line=dict(color='teal', width=2), marker=dict(size=5, color='teal'))
    fig_sample.update_layout(height=320, plot_bgcolor='white', margin=dict(l=30, r=30, t=40, b=30))
    
    with chart_col:
        st.plotly_chart(fig_sample, use_container_width=True)

elif st.session_state.main_tab == 'Ketenagakerjaan':
    sample_data = pd.DataFrame({
        'Period': ['Agu 2022', 'Feb 2023', 'Agu 2023', 'Feb 2024'],
        'Value': np.random.uniform(3, 7, 4)
    })
    title = "TPT (%)"
    
    fig_sample = px.line(sample_data, x='Period', y='Value', title=title, markers=True)
    fig_sample.update_traces(line=dict(color='teal', width=2), marker=dict(size=5, color='teal'))
    fig_sample.update_layout(height=320, plot_bgcolor='white', margin=dict(l=30, r=30, t=40, b=30))
    
    with chart_col:
        st.plotly_chart(fig_sample, use_container_width=True)

elif st.session_state.main_tab == 'Kemiskinan':
    sample_data = pd.DataFrame({
        'Period': ['Mar 2022', 'Sep 2022', 'Mar 2023', 'Sep 2023'],
        'Value': np.random.uniform(9, 11, 4)
    })
    title = "Persentase penduduk miskin (%)"
    
    fig_sample = px.line(sample_data, x='Period', y='Value', title=title, markers=True)
    fig_sample.update_traces(line=dict(color='teal', width=2), marker=dict(size=5, color='teal'))
    fig_sample.update_layout(height=320, plot_bgcolor='white', margin=dict(l=30, r=30, t=40, b=30))
    
    with chart_col:
        st.plotly_chart(fig_sample, use_container_width=True)

elif st.session_state.main_tab == 'IPM':
    sample_data = pd.DataFrame({
        'Period': [str(y) for y in range(2020, 2024)],
        'Value': np.random.uniform(70, 75, 4)
    })
    title = "IPM"
    
    fig_sample = px.line(sample_data, x='Period', y='Value', title=title, markers=True)
    fig_sample.update_traces(line=dict(color='teal', width=2), marker=dict(size=5, color='teal'))
    fig_sample.update_layout(height=320, plot_bgcolor='white', margin=dict(l=30, r=30, t=40, b=30))
    
    with chart_col:
        st.plotly_chart(fig_sample, use_container_width=True)

# Dynamic Insight Section based on selected tab
with insight_col:
    st.markdown('<div class="insight-section">', unsafe_allow_html=True)
    st.markdown("#### Insight:")
    
    if st.session_state.main_tab == 'Neraca Nasional':
        st.markdown("• Pertumbuhan ekonomi menunjukkan tren pemulihan yang konsisten")
        st.markdown("• Volatilitas triwulanan masih terlihat namun dalam koridor normal")  
        st.markdown("• Recovery pascapandemi berjalan sesuai proyeksi pemerintah")
        st.markdown("• Sektor konsumsi rumah tangga menjadi penopang utama")
        st.markdown("• Diperlukan stimulus untuk memperkuat momentum pertumbuhan")
        
    elif st.session_state.main_tab == 'Indeks Harga':
        st.markdown("• Inflasi masih dalam target Bank Indonesia 2-4%")
        st.markdown("• Tekanan inflasi inti relatif terkendali") 
        st.markdown("• Volatile food prices menjadi perhatian utama")
        st.markdown("• Kebijakan moneter masih akomodatif")
        st.markdown("• Perlu monitoring harga komoditas global")
        
    elif st.session_state.main_tab == 'Ekspor-Impor':
        st.markdown("• Nilai ekspor menunjukkan tren positif year-on-year")
        st.markdown("• Komoditas unggulan masih mendominasi ekspor")
        st.markdown("• Impor bahan baku industri terus meningkat") 
        st.markdown("• Neraca perdagangan masih surplus namun menyempit")
        st.markdown("• Diversifikasi pasar ekspor perlu diperkuat")
        
    elif st.session_state.main_tab == 'APBN':
        st.markdown("• Belanja pegawai tumbuh seiring dengan reformasi birokrasi")
        st.markdown("• Efisiensi anggaran masih dapat dioptimalkan")
        st.markdown("• Alokasi untuk infrastruktur dan SDM prioritas")
        st.markdown("• Fiscal sustainability tetap terjaga")
        st.markdown("• Ruang fiskal masih tersedia untuk stimulus")
        
    elif st.session_state.main_tab == 'Ketenagakerjaan':
        st.markdown("• Tingkat Pengangguran Terbuka menunjukkan tren menurun")
        st.markdown("• Job creation di sektor formal masih terbatas")
        st.markdown("• Skills mismatch menjadi tantangan struktural")
        st.markdown("• Program pelatihan kerja perlu diperkuat")
        st.markdown("• Digitalisasi ekonomi membuka peluang kerja baru")
        
    elif st.session_state.main_tab == 'Kemiskinan':
        st.markdown("• Angka kemiskinan menunjukkan tren penurunan gradual")
        st.markdown("• Kesenjangan urban-rural masih signifikan")
        st.markdown("• Program bantuan sosial efektif mengurangi kemiskinan")
        st.markdown("• Pemberdayaan ekonomi mikro perlu diperkuat")
        st.markdown("• Investasi SDM kunci pengentasan kemiskinan jangka panjang")
        
    elif st.session_state.main_tab == 'IPM':
        st.markdown("• Indeks Pembangunan Manusia terus mengalami peningkatan")
        st.markdown("• Komponen pendidikan menunjukkan progress signifikan")
        st.markdown("• Angka harapan hidup terus membaik")
        st.markdown("• Kesenjangan IPM antar daerah masih perlu perhatian")
        st.markdown("• Investasi kesehatan dan pendidikan harus berkelanjutan")
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
