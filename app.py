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
    /* Custom styling for Streamlit buttons */
    .stButton > button {
        width: 100%;
        background-color: #f0f0f0;
        color: #333;
        border: none;
        border-left: 5px solid #0070c0;
        padding: 15px;
        font-weight: bold;
        margin-bottom: 2px;
        border-radius: 0px;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background-color: #e0e0e0;
        color: #333;
    }
    .stButton > button:focus {
        background-color: #0070c0;
        color: white;
        box-shadow: none;
    }
    .main-tab-button {
        background-color: navy !important;
        color: white !important;
        border: none !important;
        padding: 8px 16px !important;
        font-weight: bold !important;
        border-radius: 4px !important;
        margin: 0 2px !important;
        transition: background-color 0.3s !important;
    }
    .main-tab-button:hover {
        background-color: rgba(0, 0, 139, 0.8) !important;
        color: white !important;
    }
    .main-tab-button:focus {
        background-color: rgba(255, 255, 255, 0.3) !important;
        color: white !important;
        box-shadow: none !important;
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
    # Title
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

# Main Navigation Menu
st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)

main_tabs = ['Neraca Nasional', 'Indeks Harga', 'Ekspor-Impor', 'APBN', 'Ketenagakerjaan', 'Kemiskinan', 'IPM']

# Create main navigation with columns
main_nav_cols = st.columns(len(main_tabs))

for i, tab in enumerate(main_tabs):
    with main_nav_cols[i]:
        if st.button(tab, key=f"main_{tab}", help=f"Pilih {tab}"):
            st.session_state.main_tab = tab
            # Reset side tab when main tab changes
            if tab == 'Neraca Nasional':
                st.session_state.side_tab = 'Pertumbuhan Ekonomi y-o-y'
            elif tab == 'Indeks Harga':
                st.session_state.side_tab = 'IHK Umum'
            elif tab == 'Ekspor-Impor':
                st.session_state.side_tab = 'Nilai Ekspor'
            elif tab == 'APBN':
                st.session_state.side_tab = 'Pendapatan Negara'
            elif tab == 'Ketenagakerjaan':
                st.session_state.side_tab = 'Tingkat Pengangguran'
            elif tab == 'Kemiskinan':
                st.session_state.side_tab = 'Persentase Penduduk Miskin'
            elif tab == 'IPM':
                st.session_state.side_tab = 'IPM Nasional'
            st.rerun()

# Add custom CSS for main navigation buttons
st.markdown("""
<style>
    div[data-testid="column"] > div > div > div > div > button {
        background-color: navy !important;
        color: white !important;
        border: none !important;
        padding: 8px 16px !important;
        font-weight: bold !important;
        border-radius: 4px !important;
        width: 100% !important;
        transition: all 0.3s !important;
    }
    div[data-testid="column"] > div > div > div > div > button:hover {
        background-color: rgba(0, 0, 139, 0.8) !important;
        color: white !important;
    }
</style>
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

st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)

# Create layout with sidebar and main content
col1, col2 = st.columns([1, 3])

with col1:
    st.markdown("### Menu Navigasi")
    
    # Get current side tabs for selected main tab
    current_side_tabs = side_tabs_config.get(st.session_state.main_tab, ['Default Tab'])
    
    # Display side navigation items
    for tab in current_side_tabs:
        if st.button(tab, key=f"side_{tab}_{st.session_state.main_tab}"):
            st.session_state.side_tab = tab
            st.rerun()

with col2:
    # Main content area - changes based on selected tabs
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    # Display current selection
    st.markdown(f"**Kategori:** {st.session_state.main_tab}")
    st.markdown(f"**Sub-kategori:** {st.session_state.side_tab}")
    
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
                         labels={'Growth': 'Y-O-Y (%)', 'Period': 'Quarter of Periode'},
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
            
            fig.update_traces(line=dict(color='navy', width=2), marker=dict(size=6, color='navy'))
            fig.update_layout(height=400, plot_bgcolor='white')
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error loading CSV file: {str(e)}")
    
    else:
        # Content for other tab combinations
        st.subheader(f"{st.session_state.side_tab}")
        
        # Generate appropriate sample data based on the selected tab
        if 'Pertumbuhan' in st.session_state.side_tab:
            # Growth data
            sample_data = pd.DataFrame({
                'Period': [f"2023 Q{i}" for i in range(1, 5)] + [f"2024 Q{i}" for i in range(1, 5)],
                'Value': np.random.uniform(-2, 6, 8)
            })
            title = f"{st.session_state.side_tab} (%)"
            
        elif 'IHK' in st.session_state.side_tab or 'Indeks' in st.session_state.side_tab:
            # Index data
            sample_data = pd.DataFrame({
                'Period': pd.date_range('2023-01', periods=12, freq='M').strftime('%Y-%m'),
                'Value': np.random.uniform(100, 120, 12)
            })
            title = f"{st.session_state.side_tab}"
            
        elif 'Nilai' in st.session_state.side_tab:
            # Value data (in billions)
            sample_data = pd.DataFrame({
                'Period': pd.date_range('2023-01', periods=12, freq='M').strftime('%Y-%m'),
                'Value': np.random.uniform(15, 25, 12)
            })
            title = f"{st.session_state.side_tab} (Miliar USD)"
            
        elif 'Tingkat' in st.session_state.side_tab or 'Persentase' in st.session_state.side_tab:
            # Percentage data
            sample_data = pd.DataFrame({
                'Period': [f"2023 Q{i}" for i in range(1, 5)] + [f"2024 Q{i}" for i in range(1, 5)],
                'Value': np.random.uniform(3, 12, 8)
            })
            title = f"{st.session_state.side_tab} (%)"
            
        else:
            # Default data
            sample_data = pd.DataFrame({
                'Period': pd.date_range('2023-01', periods=12, freq='M').strftime('%Y-%m'),
                'Value': np.random.randn(12).cumsum() + 100
            })
            title = st.session_state.side_tab
        
        # Create chart
        fig = px.line(sample_data, x='Period', y='Value', 
                     title=title,
                     markers=True)
        
        fig.update_traces(line=dict(color='navy', width=2), marker=dict(size=6, color='navy'))
        fig.update_layout(
            height=400,
            plot_bgcolor='white',
            xaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray'),
            yaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray')
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Add some insights
        st.markdown("---")
        st.markdown("**Insight:**")
        st.info(f"Analisis untuk {st.session_state.side_tab} menunjukkan tren yang perlu diperhatikan untuk pengambilan keputusan strategis.")
    
    st.markdown('</div>', unsafe_allow_html=True)
