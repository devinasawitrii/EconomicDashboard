import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import base64

# Set page configuration
st.set_page_config(
    page_title="Actionable Insights",
    page_icon="📊",
    layout="wide"
)

# Initialize session state for navigation
if 'main_tab' not in st.session_state:
    st.session_state.main_tab = 'Neraca Nasional'
if 'side_tab' not in st.session_state:
    st.session_state.side_tab = 'Pertumbuhan Ekonomi y-o-y'

# Custom CSS for styling
st.markdown("""
<style>
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0px;
        background-color: white;
    }
    .logo-title {
        color: navy;
        font-size: 32px;
        font-weight: bold;
        text-align: center;
        margin: 0;
        padding: 0;
    }
    .subtitle {
        color: red;
        font-size: 18px;
        text-align: center;
        font-style: italic;
        margin-top: 5px;
    }
    .main-nav {
        background-color: navy;
        padding: 10px 0;
        display: flex;
        justify-content: space-around;
        margin-bottom: 20px;
    }
    .main-nav a {
        color: white;
        text-decoration: none;
        padding: 8px 16px;
        font-weight: bold;
        border-radius: 4px;
        transition: background-color 0.3s;
    }
    .main-nav a:hover {
        background-color: rgba(255,255,255,0.2);
    }
    .main-nav a.active {
        background-color: rgba(255,255,255,0.3);
    }
    .sidebar-nav {
        border-radius: 10px;
        overflow: hidden;
    }
    .nav-item {
        background-color: #f0f0f0;
        padding: 15px;
        margin-bottom: 2px;
        border-left: 5px solid #0070c0;
        font-weight: bold;
        color: #333;
        cursor: pointer;
        transition: background-color 0.3s;
        font-size: 14px;
        line-height: 1.2;
    }
    .nav-item:hover {
        background-color: #e0e0e0;
    }
    .nav-item.active {
        background-color: #0070c0;
        color: white;
    }
    .chart-container {
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 15px;
        background-color: white;
    }
    .logo-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }
    .aig-logo {
        width: 80px;
        height: 80px;
        border: 3px solid navy;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: white;
        font-size: 18px;
        font-weight: bold;
        color: navy;
        margin-bottom: 5px;
    }
    .bps-logo {
        width: 100px;
        background-color: #0070c0;
        border-radius: 5px;
        overflow: hidden;
    }
    .bps-header {
        background-color: #0070c0;
        color: white;
        padding: 5px;
        font-size: 8px;
        text-align: center;
        line-height: 1.2;
    }
    .bps-main {
        background-color: #00B0F0;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 40px;
    }
    .bps-text {
        color: white;
        font-weight: bold;
        font-size: 16px;
    }
</style>
""", unsafe_allow_html=True)

# Header with logos
col1, col2, col3 = st.columns([1, 3, 1])

with col1:
    # AIG Logo
    st.markdown("""
    <div class="logo-container">
        <div class="aig-logo">aig</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Title only (no "Generator")
    st.markdown('<div class="logo-title">ACTIONABLE INSIGHTS</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Generate wisdom from fingertip</div>', unsafe_allow_html=True)

with col3:
    # BPS Logo
    st.markdown("""
    <div class="logo-container">
        <div class="bps-logo">
            <div class="bps-header">
                DIREKTORAT<br>NERACA PENGELUARAN
            </div>
            <div class="bps-main">
                <span class="bps-text">BPS</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Define side tabs for each main tab
side_tabs_config = {
    'Neraca Nasional': [
        'Pertumbuhan Ekonomi y-o-y',
        'Pertumbuhan Ekonomi q-to-q',
        'Pertumbuhan Ekonomi c-to-c',
        'Indeks Implisit y-o-y',
        'Indeks Implisit q-to-q',
        'Indeks Implisit c-to-c',
        'PDB ADHB',
        'PDB ADHK'
    ],
    'Indeks Harga': [
        'IHK Umum',
        'IHK Makanan',
        'IHK Non-Makanan',
        'Inflasi y-o-y',
        'Inflasi m-to-m',
        'Inflasi c-to-c'
    ],
    'Ekspor-Impor': [
        'Nilai Ekspor',
        'Nilai Impor',
        'Neraca Perdagangan',
        'Pertumbuhan Ekspor',
        'Pertumbuhan Impor'
    ],
    'APBN': [
        'Pendapatan Negara',
        'Belanja Negara',
        'Surplus/Defisit',
        'Rasio Defisit'
    ],
    'Ketenagakerjaan': [
        'Tingkat Pengangguran',
        'Angkatan Kerja',
        'TPAK',
        'Pekerja Formal',
        'Pekerja Informal'
    ],
    'Kemiskinan': [
        'Persentase Penduduk Miskin',
        'Jumlah Penduduk Miskin',
        'Garis Kemiskinan',
        'Indeks Kedalaman Kemiskinan'
    ],
    'IPM': [
        'IPM Nasional',
        'IPM Provinsi',
        'Komponen Kesehatan',
        'Komponen Pendidikan',
        'Komponen Ekonomi'
    ]
}

# Main Navigation - using Streamlit tabs styled to look like the original
main_tabs = ['Neraca Nasional', 'Indeks Harga', 'Ekspor-Impor', 'APBN', 'Ketenagakerjaan', 'Kemiskinan', 'IPM']

# Create main navigation using columns with buttons
st.markdown("""
<div class="main-nav">
    <span style="width: 100%; display: flex; justify-content: space-around;">
""" + "".join([f'<a href="#" style="flex: 1; text-align: center;">{tab}</a>' for tab in main_tabs]) + """
    </span>
</div>
""", unsafe_allow_html=True)

# Main tab selection using columns
main_cols = st.columns(len(main_tabs))
for i, tab in enumerate(main_tabs):
    with main_cols[i]:
        if st.button(tab, key=f"main_tab_{i}", use_container_width=True):
            st.session_state.main_tab = tab
            # Reset side tab when main tab changes
            current_side_tabs = side_tabs_config.get(tab, ['Default Tab'])
            st.session_state.side_tab = current_side_tabs[0]
            st.rerun()

# Create layout with sidebar and main content
col1, col2 = st.columns([1, 3])

with col1:
    st.markdown('<div class="sidebar-nav">', unsafe_allow_html=True)
    
    # Get current side tabs for selected main tab
    current_side_tabs = side_tabs_config.get(st.session_state.main_tab, ['Default Tab'])
    
    # Display side navigation items
    for i, tab in enumerate(current_side_tabs):
        active_class = 'active' if st.session_state.side_tab == tab else ''
        
        # Format tab name for display (add line breaks for long names)
        if len(tab) > 15:
            display_tab = tab.replace(' ', '<br>', 1) if ' ' in tab else tab
        else:
            display_tab = tab
            
        st.markdown(f'<div class="nav-item {active_class}">{display_tab}</div>', unsafe_allow_html=True)
        
        # Button for functionality
        if st.button(f"Select {tab}", key=f"side_tab_{i}_{st.session_state.main_tab}"):
            st.session_state.side_tab = tab
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # Main content area - changes based on selected tabs
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    # Display content based on selected tabs
    if st.session_state.main_tab == 'Neraca Nasional' and st.session_state.side_tab == 'Pertumbuhan Ekonomi y-o-y':
        # Original economic growth chart
        try:
            # Try to load the CSV file
            df = pd.read_csv('Sheet 1_Full Data_data.csv')
            df.columns = ['Period', 'Growth']
            
            # Create the plot using Plotly
            fig = px.line(df, x='Period', y='Growth', 
                         title='Pertumbuhan Ekonomi y-o-y',
                         labels={'Growth': 'Y-O-Y', 'Period': 'Quarter of Periode'},
                         markers=True)
            
            # Update layout for better appearance
            fig.update_layout(
                xaxis=dict(
                    tickmode='array',
                    tickvals=[df['Period'][i] for i in range(0, len(df), 4)],
                    ticktext=[f"{period.split()[0]} Q1" for period in df['Period'][::4]],
                    title_font=dict(size=14),
                ),
                yaxis=dict(
                    range=[-6, 8],
                    tickvals=[-5, 0, 5],
                    title_font=dict(size=14),
                ),
                plot_bgcolor='white',
                title_font=dict(size=16),
                height=400,
                margin=dict(l=40, r=40, t=50, b=40),
                hovermode="x unified"
            )
            
            # Customize line
            fig.update_traces(
                line=dict(color='navy', width=2),
                marker=dict(size=6, color='navy'),
            )
            
            # Add grid lines
            fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
            
            # Display the chart
            st.plotly_chart(fig, use_container_width=True)
            
        except FileNotFoundError:
            st.error("File 'Sheet 1_Full Data_data.csv' tidak ditemukan.")
        except Exception as e:
            st.error(f"Error loading CSV file: {str(e)}")
    
    else:
        # Content for other combinations
        st.subheader(f"{st.session_state.main_tab}")
        st.write(f"**{st.session_state.side_tab}**")
        
        # Show different content based on main tab
        if st.session_state.main_tab == 'Indeks Harga':
            st.info(f"Data {st.session_state.side_tab} - Menampilkan tren inflasi dan perubahan harga konsumen.")
        elif st.session_state.main_tab == 'Ekspor-Impor':
            st.info(f"Data {st.session_state.side_tab} - Menampilkan kinerja perdagangan internasional Indonesia.")
        elif st.session_state.main_tab == 'APBN':
            st.info(f"Data {st.session_state.side_tab} - Menampilkan kondisi keuangan pemerintah.")
        elif st.session_state.main_tab == 'Ketenagakerjaan':
            st.info(f"Data {st.session_state.side_tab} - Menampilkan kondisi pasar tenaga kerja.")
        elif st.session_state.main_tab == 'Kemiskinan':
            st.info(f"Data {st.session_state.side_tab} - Menampilkan indikator kemiskinan dan kesejahteraan.")
        elif st.session_state.main_tab == 'IPM':
            st.info(f"Data {st.session_state.side_tab} - Menampilkan Indeks Pembangunan Manusia.")
        else:
            st.info(f"Konten untuk {st.session_state.side_tab} dalam kategori {st.session_state.main_tab} akan ditampilkan di sini.")
        
        # Sample chart for demonstration
        sample_data = pd.DataFrame({
            'Periode': pd.date_range('2020-01-01', periods=20, freq='Q'),
            'Nilai': np.random.randn(20).cumsum() + 100
        })
        
        fig = px.line(sample_data, x='Periode', y='Nilai', 
                     title=st.session_state.side_tab,
                     markers=True)
        fig.update_traces(line=dict(color='navy', width=2), marker=dict(size=6, color='navy'))
        fig.update_layout(height=400, plot_bgcolor='white')
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Display current selections in sidebar for debugging
with st.sidebar:
    st.write("**Current Selection:**")
    st.write(f"Main: {st.session_state.main_tab}")
    st.write(f"Side: {st.session_state.side_tab}")
    
    st.write("**Available Side Tabs:**")
    current_side_tabs = side_tabs_config.get(st.session_state.main_tab, [])
    for tab in current_side_tabs:
        st.write(f"• {tab}")
