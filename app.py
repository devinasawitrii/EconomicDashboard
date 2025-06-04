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
    .main-nav-item {
        background: none;
        border: none;
        color: white;
        text-decoration: none;
        padding: 8px 16px;
        font-weight: bold;
        cursor: pointer;
        border-radius: 4px;
        transition: background-color 0.3s;
        font-size: 14px;
    }
    .main-nav-item:hover {
        background-color: rgba(255,255,255,0.2);
    }
    .main-nav-item.active {
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
        border: none;
        width: 100%;
        text-align: left;
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
    /* Hide Streamlit default elements */
    .stButton > button {
        display: none;
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

# Main Navigation Menu with functionality
main_tabs = ['Neraca Nasional', 'Indeks Harga', 'Ekspor-Impor', 'APBN', 'Ketenagakerjaan', 'Kemiskinan', 'IPM']

# Create clickable main navigation
main_nav_html = '<div class="main-nav">'
for tab in main_tabs:
    active_class = 'active' if st.session_state.main_tab == tab else ''
    main_nav_html += f'<span class="main-nav-item {active_class}" onclick="selectMainTab(\'{tab}\')">{tab}</span>'
main_nav_html += '</div>'

st.markdown(main_nav_html, unsafe_allow_html=True)

# Handle main tab selection with invisible buttons
main_cols = st.columns(len(main_tabs))
for i, tab in enumerate(main_tabs):
    with main_cols[i]:
        if st.button(f"select_{tab}", key=f"main_tab_{i}"):
            st.session_state.main_tab = tab
            # Reset side tab when main tab changes
            if tab == 'Neraca Nasional':
                st.session_state.side_tab = 'Pertumbuhan Ekonomi y-o-y'
            elif tab == 'Indeks Harga':
                st.session_state.side_tab = 'IHK Umum'
            elif tab == 'Ekspor-Impor':
                st.session_state.side_tab = 'Nilai Ekspor'
            else:
                st.session_state.side_tab = f'{tab} Tab 1'
            st.rerun()

# Define side tabs for each main tab
side_tabs_config = {
    'Neraca Nasional': [
        'Pertumbuhan<br>Ekonomi y-o-y',
        'Pertumbuhan<br>Ekonomi q-to-q',
        'Pertumbuhan<br>Ekonomi c-to-c',
        'Indeks Implisit<br>y-o-y',
        'Indeks Implisit<br>q-to-q',
        'Indeks Implisit<br>c-to-c',
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
        'Persentase Penduduk<br>Miskin',
        'Jumlah Penduduk<br>Miskin',
        'Garis Kemiskinan',
        'Indeks Kedalaman<br>Kemiskinan'
    ],
    'IPM': [
        'IPM Nasional',
        'IPM Provinsi',
        'Komponen Kesehatan',
        'Komponen Pendidikan',
        'Komponen Ekonomi'
    ]
}

# Create layout with sidebar and main content
col1, col2 = st.columns([1, 3])

with col1:
    st.markdown('<div class="sidebar-nav">', unsafe_allow_html=True)
    
    # Get current side tabs for selected main tab
    current_side_tabs = side_tabs_config.get(st.session_state.main_tab, ['Default Tab'])
    
    # Display side navigation items
    for i, tab_display in enumerate(current_side_tabs):
        tab_key = tab_display.replace('<br>', ' ').replace('\n', ' ')
        active_class = 'active' if st.session_state.side_tab == tab_key else ''
        
        st.markdown(f'<div class="nav-item {active_class}" onclick="selectSideTab(\'{tab_key}\')">{tab_display}</div>', unsafe_allow_html=True)
        
        # Hidden button for functionality
        if st.button(f"side_select_{i}", key=f"side_tab_{i}_{st.session_state.main_tab}"):
            st.session_state.side_tab = tab_key
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
        # Placeholder for other combinations
        st.subheader(f"{st.session_state.main_tab} - {st.session_state.side_tab}")
        st.info(f"Konten untuk {st.session_state.side_tab} dalam kategori {st.session_state.main_tab} akan ditampilkan di sini.")
        
        # Sample chart for demonstration
        sample_data = pd.DataFrame({
            'x': range(10),
            'y': np.random.randn(10).cumsum()
        })
        fig = px.line(sample_data, x='x', y='y', title=st.session_state.side_tab.replace('<br>', ' '))
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# JavaScript for handling clicks (though Streamlit buttons handle the actual functionality)
st.markdown("""
<script>
function selectMainTab(tab) {
    // Visual feedback - Streamlit buttons handle actual functionality
    console.log('Main tab selected:', tab);
}

function selectSideTab(tab) {
    // Visual feedback - Streamlit buttons handle actual functionality  
    console.log('Side tab selected:', tab);
}
</script>
""", unsafe_allow_html=True)
