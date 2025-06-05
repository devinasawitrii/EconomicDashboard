import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import base64
from streamlit_option_menu import option_menu # Import the new component
import os

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

# Custom CSS for styling (Keep sidebar styles, remove old main nav styles)
st.markdown("""
<style>
    /* Remove top padding */
    .block-container { 
        padding-top: 0rem !important; 
    }
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0px;
        background-color: white;
        margin-bottom: 1rem; /* Add some space below header */
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
        color: #0070c0;
        font-size: 18px;
        text-align: center;
        font-style: italic;
        margin-top: 5px;
    }
    .chart-container {
        border: none;
        border-radius: 0px;
        padding: 20px;
        background-color: white;
        box-shadow: none;
    }
    .logo-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }
    
    /* Sidebar buttons styling - MODIFIED TO BE SMALLER AND CONSISTENT SPACING */
    .stButton > button {
        width: 90% !important; /* Reduced from 100% */
        background-color: #f0f0f0 !important;
        color: #333 !important;
        border: none !important;
        border-left: 5px solid #0070c0 !important;
        padding: 10px !important; /* Reduced from 15px */
        font-weight: bold !important;
        margin-bottom: 5px !important; /* Consistent spacing between buttons */
        border-radius: 0px !important;
        transition: all 0.3s !important;
        min-height: 40px !important; /* Reduced from 50px */
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        text-align: left !important;
        font-size: 13px !important; /* Added smaller font size */
    }
    
    .stButton > button:hover {
        background-color: #e0e0e0 !important;
        color: #333 !important;
    }
    
    .stButton > button:focus {
        background-color: #0070c0 !important;
        color: white !important;
        box-shadow: none !important;
        outline: none !important;
    }
    
    .stButton > button:active {
        background-color: #0070c0 !important;
        color: white !important;
    }
        
    /* Remove default Streamlit button focus states */
    .stButton > button:focus:not(:active) {
        border-color: transparent !important;
        box-shadow: none !important;
    }
        
    /* Hide Streamlit's default focus outline */
    button:focus {
        outline: none !important;
        box-shadow: none !important;
    }
    
    /* Insight container styling */
    .insight-container {
        background-color: #f8f9fa;
        border-left: 4px solid #0070c0;
        padding: 15px;
        margin-top: 10px;
        margin-bottom: 10px;
    }
    
    .insight-title {
        color: #0070c0;
        font-weight: bold;
        font-size: 16px;
        margin-bottom: 8px;
    }
    
    .insight-content {
        font-size: 14px;
        line-height: 1.5;
    }
    
    /* Image logos styling */
    .image-logo {
        max-width: 100%;
        height: auto;
        display: block;
        margin: 0 auto;
    }
    
    /* Main content padding adjustment */
    .main-content {
        padding-top: 10px;
    }
    
    /* Streamlit default padding adjustments */
    .css-18e3th9 {
        padding-top: 0rem !important;
    }
    
    .css-1d391kg {
        padding-top: 1rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Header with image logos instead of text
col1, col2, col3 = st.columns([1, 3, 1])

with col1:
    # AIG Image Logo - Placeholder for user to replace
    st.markdown("""
    <div class="logo-container">
        <!-- Replace with actual image path when available -->
        <img src="https://placeholder.com/80x80" alt="AIG Logo" class="image-logo" />
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Title
    st.markdown('<div class="logo-title">ACTIONABLE INSIGHTS</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Generate wisdom from fingertip</div>', unsafe_allow_html=True)

with col3:
    # BPS Image Logo - Placeholder for user to replace
    st.markdown("""
    <div class="logo-container">
        <!-- Replace with actual image path when available -->
        <img src="https://placeholder.com/100x60" alt="Direktorat Neraca Pengeluaran BPS Logo" class="image-logo" />
    </div>
    """, unsafe_allow_html=True)

# Main Navigation Menu using streamlit-option-menu
main_tabs_list = ['Neraca Nasional', 'Indeks Harga', 'Ekspor-Impor', 'APBN', 'Ketenagakerjaan', 'Kemiskinan', 'IPM']

# Find the index of the current main_tab for default_index
try:
    default_main_index = main_tabs_list.index(st.session_state.main_tab)
except ValueError:
    default_main_index = 0 # Default to first tab if not found

# Use option_menu for horizontal navigation
selected_main_tab = option_menu(
    menu_title=None,  # No title needed
    options=main_tabs_list,
    icons=None, # No icons needed
    menu_icon=None, # No menu icon needed
    default_index=default_main_index,
    orientation="horizontal",
    styles={
        "container": {"padding": "0px !important", "background-color": "white", "margin-bottom": "1rem", "flex-wrap": "nowrap"}, # Ensure it stays horizontal
        "nav-link": {
            "font-size": "14px", 
            "font-weight": "bold",
            "color": "#333",
            "background-color": "#f0f0f0", 
            "text-align": "center", 
            "padding": "15px 10px", # Adjusted padding
            "margin":"0px 2px !important", # Spacing between tabs
            "border-radius": "0px !important",
            "border-bottom": "5px solid #0070c0",
            "transition": "background-color 0.2s, color 0.2s, border-color 0.2s",
            "white-space": "nowrap" # Prevent wrapping
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

# Update session state and reset side tab if main tab changed
if selected_main_tab != st.session_state.main_tab:
    st.session_state.main_tab = selected_main_tab
    # Reset side tab when main tab changes
    if selected_main_tab == 'Neraca Nasional':
        st.session_state.side_tab = 'Pertumbuhan Ekonomi y-o-y'
    elif selected_main_tab == 'Indeks Harga':
        st.session_state.side_tab = 'IHK Umum'
    elif selected_main_tab == 'Ekspor-Impor':
        st.session_state.side_tab = 'Nilai Ekspor'
    elif selected_main_tab == 'APBN':
        st.session_state.side_tab = 'Pendapatan Negara'
    elif selected_main_tab == 'Ketenagakerjaan':
        st.session_state.side_tab = 'Tingkat Pengangguran'
    elif selected_main_tab == 'Kemiskinan':
        st.session_state.side_tab = 'Persentase Penduduk Miskin'
    elif selected_main_tab == 'IPM':
        st.session_state.side_tab = 'IPM Nasional'
    st.rerun()

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

# Create layout with sidebar and main content - MODIFIED RATIO FOR SMALLER LEFT COLUMN
col1, col2 = st.columns([1, 4])  # Changed from [1, 3] to [1, 4] to make left column smaller

with col1:
    # Get current side tabs for selected main tab
    current_side_tabs = side_tabs_config.get(st.session_state.main_tab, ['Default Tab'])
    
    # Display side navigation items using st.button (Keep existing sidebar logic)
    for tab in current_side_tabs:
        # Add custom CSS class for active state via markdown injection
        button_key = f"side_{tab}_{st.session_state.main_tab}"
        is_active = st.session_state.side_tab == tab
        
        if st.button(tab, key=button_key):
            st.session_state.side_tab = tab
            st.rerun()
        
        # Inject CSS for the active button AFTER the button is created
        if is_active:
            st.markdown(f"""
            <style>
                button[data-testid="stButton"] > button[key="{button_key}"] {{
                    background-color: #0070c0 !important;
                    color: white !important;
                    border-left: 5px solid navy !important;
                }}
            </style>
            """, unsafe_allow_html=True)

with col2:
    # Main content area - changes based on selected tabs
    st.markdown('<div class="chart-container main-content">', unsafe_allow_html=True)
    
    # Display content based on selected tabs
    if st.session_state.main_tab == 'Neraca Nasional' and st.session_state.side_tab == 'Pertumbuhan Ekonomi y-o-y':
        # Create two columns for chart and insights
        chart_col, insight_col = st.columns([3, 2])
        
        with chart_col:
            # Original economic growth chart
            try:
                # Try to load the CSV file - first check if sample_data.csv exists, otherwise use Sheet 1_Full Data_data.csv
                if os.path.exists('sample_data.csv'):
                    df = pd.read_csv('sample_data.csv')
                else:
                    df = pd.read_csv('Sheet 1_Full Data_data.csv')
                
                # Ensure columns are named correctly
                if len(df.columns) >= 2:
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
                    height=400,  # Reduced height from 500
                    margin=dict(l=40, r=40, t=60, b=40),
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
                st.error("File data tidak ditemukan. Menggunakan data sample.")
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
                fig.update_layout(height=400, plot_bgcolor='white', margin=dict(l=40, r=40, t=60, b=40))
                st.plotly_chart(fig, use_container_width=True)
                
            except Exception as e:
                st.error(f"Error loading CSV file: {str(e)}")
        
        with insight_col:
            # Actionable Insight section - now visible and positioned beside the chart
            st.markdown("""
            <div class="insight-title">ACTIONABLE INSIGHT</div>
            <div class="insight-container">
                <div class="insight-content">
                    <p>Pertumbuhan ekonomi Indonesia pada Q1 2024 mencapai 5.1%, menunjukkan tren positif dibandingkan periode yang sama tahun lalu.</p>
                    <p>Faktor pendorong utama pertumbuhan adalah konsumsi rumah tangga yang meningkat 5.3% dan investasi yang tumbuh 4.9%.</p>
                    <p>Sektor manufaktur dan perdagangan menjadi kontributor terbesar dengan pertumbuhan masing-masing 5.2% dan 5.7%.</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Additional insights or metrics can be added here
            st.markdown("""
            <div class="insight-title">REKOMENDASI</div>
            <div class="insight-container">
                <div class="insight-content">
                    <p>Fokus pada penguatan sektor manufaktur melalui insentif fiskal dan kemudahan perizinan untuk mendorong pertumbuhan lebih tinggi.</p>
                    <p>Tingkatkan program stimulus konsumsi rumah tangga untuk mempertahankan momentum pertumbuhan di tengah ketidakpastian global.</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        # Content for other tab combinations - with side-by-side layout
        chart_col, insight_col = st.columns([3, 2])
        
        with chart_col:
            # Generate appropriate sample data based on the selected tab
            if 'Pertumbuhan' in st.session_state.side_tab:
                # Growth data
                sample_data = pd.DataFrame({
                    'Period': [f"2023 Q{i}" for i in range(1, 5)] + [f"2024 Q{i}" for i in range(1, 3)],
                    'Value': np.random.uniform(-2, 6, 6)
                })
                title = f"{st.session_state.side_tab} (%)"
                
            elif 'IHK' in st.session_state.side_tab or 'Indeks' in st.session_state.side_tab:
                # Index data
                sample_data = pd.DataFrame({
                    'Period': pd.date_range('2023-01', periods=12, freq='M').strftime('%Y-%m'),
                    'Value': np.random.uniform(100, 120, 12)
                })
                title = f"{st.session_state.side_tab} (Indeks)"
                
            elif 'Inflasi' in st.session_state.side_tab:
                # Inflation data
                sample_data = pd.DataFrame({
                    'Period': pd.date_range('2023-01', periods=12, freq='M').strftime('%Y-%m'),
                    'Value': np.random.uniform(-1, 5, 12)
                })
                title = f"{st.session_state.side_tab} (%)"
                
            elif 'Ekspor' in st.session_state.side_tab or 'Impor' in st.session_state.side_tab or 'Neraca' in st.session_state.side_tab:
                # Trade data
                sample_data = pd.DataFrame({
                    'Period': pd.date_range('2023-01', periods=12, freq='M').strftime('%Y-%m'),
                    'Value': np.random.uniform(10000, 30000, 12)
                })
                title = f"{st.session_state.side_tab} (Juta USD)"
                
            elif 'APBN' in st.session_state.main_tab:
                 # APBN data
                sample_data = pd.DataFrame({
                    'Period': [f"2023 Q{i}" for i in range(1, 5)] + [f"2024 Q{i}" for i in range(1, 3)],
                    'Value': np.random.uniform(500, 1500, 6)
                })
                title = f"{st.session_state.side_tab} (Triliun Rupiah)"
                
            elif 'Ketenagakerjaan' in st.session_state.main_tab:
                # Employment data
                sample_data = pd.DataFrame({
                    'Period': ['Agu 2022', 'Feb 2023', 'Agu 2023', 'Feb 2024'],
                    'Value': np.random.uniform(3, 7, 4) if 'Tingkat' in st.session_state.side_tab else np.random.uniform(100, 200, 4)
                })
                unit = "(%)" if 'Tingkat' in st.session_state.side_tab else "(Juta Orang)"
                title = f"{st.session_state.side_tab} {unit}"
                
            else:
                # Default data
                sample_data = pd.DataFrame({
                    'Period': [f"2023 Q{i}" for i in range(1, 5)] + [f"2024 Q{i}" for i in range(1, 3)],
                    'Value': np.random.uniform(0, 10, 6)
                })
                title = st.session_state.side_tab
            
            # Create sample chart
            fig = px.line(sample_data, x='Period', y='Value', 
                         title=title,
                         markers=True)
            
            fig.update_traces(line=dict(color='navy', width=2), marker=dict(size=6, color='navy'))
            fig.update_layout(
                height=400,  # Reduced height
                plot_bgcolor='white',
                margin=dict(l=40, r=40, t=60, b=40),
                hovermode="x unified"
            )
            
            # Add grid lines
            fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
            
            st.plotly_chart(fig, use_container_width=True)
        
        with insight_col:
            # Generic Actionable Insight for other tabs
            st.markdown("""
            <div class="insight-title">ACTIONABLE INSIGHT</div>
            <div class="insight-container">
                <div class="insight-content">
                    <p>Analisis data menunjukkan tren yang perlu diperhatikan dalam periode terakhir.</p>
                    <p>Terdapat perubahan signifikan dibandingkan periode yang sama tahun sebelumnya.</p>
                    <p>Faktor-faktor yang mempengaruhi perubahan ini perlu dianalisis lebih lanjut.</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Additional insights
            st.markdown("""
            <div class="insight-title">REKOMENDASI</div>
            <div class="insight-container">
                <div class="insight-content">
                    <p>Lakukan monitoring berkelanjutan terhadap indikator-indikator utama.</p>
                    <p>Evaluasi kebijakan yang telah diterapkan dan sesuaikan dengan kondisi terkini.</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
