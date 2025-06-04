import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Actionable Insights",
    page_icon="📊",
    layout="wide"
)

# Initialize session state for navigation
if 'main_page' not in st.session_state:
    st.session_state.main_page = 'Neraca Nasional'
if 'sub_page' not in st.session_state:
    st.session_state.sub_page = 'Pertumbuhan Ekonomi y-o-y'

# Custom CSS for styling
st.markdown("""
<style>
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20px 0;
        background-color: white;
    }
    .logo-title {
        color: #003366;
        font-size: 36px;
        font-weight: bold;
        text-align: center;
        margin: 0;
    }
    .subtitle {
        color: #cc0000;
        font-size: 18px;
        text-align: center;
        font-style: italic;
        margin-top: 5px;
    }
    .main-nav {
        background-color: #003366;
        padding: 0;
        display: flex;
        justify-content: space-around;
        margin-bottom: 20px;
    }
    .nav-button {
        background-color: #003366;
        color: white;
        border: none;
        padding: 15px 20px;
        font-weight: bold;
        cursor: pointer;
        flex: 1;
        text-align: center;
        font-size: 14px;
    }
    .nav-button:hover {
        background-color: #004080;
    }
    .nav-button.active {
        background-color: #0066cc;
    }
    .sidebar-nav {
        margin-bottom: 20px;
    }
    .nav-item {
        background-color: #e6f3ff;
        padding: 15px;
        margin-bottom: 3px;
        border-left: 5px solid #0066cc;
        font-weight: bold;
        color: #003366;
        cursor: pointer;
        border-radius: 0 5px 5px 0;
        transition: all 0.3s ease;
    }
    .nav-item:hover {
        background-color: #cce6ff;
        transform: translateX(5px);
    }
    .nav-item.active {
        background-color: #0066cc;
        color: white;
    }
    .chart-container {
        border: 2px solid #ddd;
        border-radius: 8px;
        padding: 20px;
        background-color: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .logo-container {
        text-align: center;
        padding: 10px;
    }
    .bps-logo {
        background: linear-gradient(45deg, #0066cc, #0099ff);
        color: white;
        padding: 5px;
        border-radius: 5px;
        font-size: 12px;
        margin-bottom: 5px;
    }
    .aig-logo {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: linear-gradient(45deg, #003366, #0066cc);
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto;
        color: white;
        font-weight: bold;
        font-size: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Header with logos
col1, col2, col3 = st.columns([1, 3, 1])

with col1:
    # AIG Logo
    st.markdown("""
    <div class="logo-container">
        <div class="aig-logo">
            AIG
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Title and Subtitle
    st.markdown('<div class="logo-title">ACTIONABLE INSIGHTS</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Generate wisdom from fingertip</div>', unsafe_allow_html=True)

with col3:
    # BPS Logo
    st.markdown("""
    <div class="logo-container">
        <div class="bps-logo">
            DIREKTORAT<br>NERACA PENGELUARAN
        </div>
        <div style="background-color: #0066cc; color: white; padding: 10px; border-radius: 5px; font-weight: bold; font-size: 16px;">
            📊 BPS
        </div>
    </div>
    """, unsafe_allow_html=True)

# Main Navigation Menu
st.markdown('<div class="main-nav">', unsafe_allow_html=True)

# Create navigation buttons
nav_options = ['Neraca Nasional', 'Indeks Harga', 'Ekspor-Impor', 'APBN', 'Ketenagakerjaan', 'Kemiskinan', 'IPM']

nav_cols = st.columns(len(nav_options))
for i, option in enumerate(nav_options):
    with nav_cols[i]:
        if st.button(option, key=f"nav_{option}", 
                    help=f"Go to {option} page",
                    use_container_width=True):
            st.session_state.main_page = option
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Create layout with sidebar and main content
col1, col2 = st.columns([1, 3])

with col1:
    st.markdown("### Menu")
    
    # Define sidebar options based on main page
    if st.session_state.main_page == 'Neraca Nasional':
        sidebar_options = [
            'Pertumbuhan Ekonomi y-o-y',
            'Pertumbuhan Ekonomi q-to-q', 
            'Pertumbuhan Ekonomi c-to-c',
            'Indeks Implisit y-o-y',
            'Indeks Implisit q-to-q',
            'Indeks Implisit c-to-c',
            'PDB ADHB',
            'PDB ADHK'
        ]
    elif st.session_state.main_page == 'Indeks Harga':
        sidebar_options = [
            'IHK Umum',
            'IHK Kelompok',
            'Inflasi y-o-y',
            'Inflasi m-t-m',
            'Inflasi c-to-c'
        ]
    elif st.session_state.main_page == 'Ekspor-Impor':
        sidebar_options = [
            'Nilai Ekspor',
            'Nilai Impor',
            'Neraca Perdagangan',
            'Ekspor Migas',
            'Ekspor Non-Migas'
        ]
    else:
        sidebar_options = [
            'Data 1',
            'Data 2',
            'Data 3',
            'Data 4'
        ]
    
    # Create sidebar navigation
    for option in sidebar_options:
        is_active = st.session_state.sub_page == option
        button_class = "nav-item active" if is_active else "nav-item"
        
        if st.button(option, key=f"sub_{option}", use_container_width=True):
            st.session_state.sub_page = option
            st.rerun()

with col2:
    # Main content area
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    # Display content based on selected page
    if st.session_state.main_page == 'Neraca Nasional' and st.session_state.sub_page == 'Pertumbuhan Ekonomi y-o-y':
        # Load data from CSV file
        try:
            df = pd.read_csv('Sheet 1_Full Data_data.csv')
            df.columns = ['Period', 'Growth']
            
            # Create the economic growth chart
            fig = px.line(df, x='Period', y='Growth', 
                         title='Pertumbuhan Ekonomi y-o-y',
                         labels={'Growth': 'Y-O-Y (%)', 'Period': 'Quarter of Periode'},
                         markers=True)
            
            # Update layout
            fig.update_layout(
                xaxis=dict(
                    tickmode='array',
                    tickvals=[df['Period'][i] for i in range(0, len(df), 4)],
                    ticktext=[f"{period.split()[0]} Q1" for period in df['Period'][::4]],
                    title_font=dict(size=14),
                ),
                yaxis=dict(
                    range=[-6, 8],
                    title_font=dict(size=14),
                ),
                plot_bgcolor='white',
                title_font=dict(size=18, color='#003366'),
                height=500,
                margin=dict(l=60, r=40, t=80, b=60),
                hovermode="x unified"
            )
            
            # Customize line
            fig.update_traces(
                line=dict(color='#0066cc', width=3),
                marker=dict(size=8, color='#0066cc'),
            )
            
            # Add grid lines
            fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
            
            # Display the chart
            st.plotly_chart(fig, use_container_width=True)
            
            # Show some statistics
            col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
            with col_stat1:
                st.metric("Latest Growth", f"{df['Growth'].iloc[-1]:.2f}%")
            with col_stat2:
                st.metric("Average Growth", f"{df['Growth'].mean():.2f}%")
            with col_stat3:
                st.metric("Highest Growth", f"{df['Growth'].max():.2f}%")
            with col_stat4:
                st.metric("Lowest Growth", f"{df['Growth'].min():.2f}%")
                
        except FileNotFoundError:
            st.error("File 'Sheet 1_Full Data_data.csv' tidak ditemukan. Pastikan file CSV berada di folder yang sama dengan script ini.")
        except Exception as e:
            st.error(f"Error loading CSV file: {str(e)}")
    
    elif st.session_state.main_page == 'Neraca Nasional' and st.session_state.sub_page == 'Pertumbuhan Ekonomi q-to-q':
        st.subheader("Pertumbuhan Ekonomi Quarter-to-Quarter")
        st.info("Data untuk pertumbuhan ekonomi q-to-q akan ditampilkan di sini.")
        
        # Sample chart for demonstration
        sample_data = pd.DataFrame({
            'Quarter': ['2023 Q1', '2023 Q2', '2023 Q3', '2023 Q4', '2024 Q1', '2024 Q2'],
            'Growth': [1.2, 0.8, 1.5, 0.9, 1.1, 1.3]
        })
        
        fig = px.bar(sample_data, x='Quarter', y='Growth', 
                    title='Sample Q-to-Q Growth Data',
                    color='Growth',
                    color_continuous_scale='Blues')
        
        fig.update_layout(height=400, title_font=dict(size=18, color='#003366'))
        st.plotly_chart(fig, use_container_width=True)
    
    elif st.session_state.main_page == 'Indeks Harga':
        st.subheader(f"Halaman {st.session_state.main_page}")
        st.subheader(f"Sub-menu: {st.session_state.sub_page}")
        st.info("Data indeks harga akan ditampilkan di sini sesuai dengan sub-menu yang dipilih.")
        
        # Sample content for other pages
        sample_data = pd.DataFrame({
            'Month': pd.date_range('2023-01-01', periods=12, freq='M'),
            'Index': np.random.normal(100, 5, 12).cumsum()
        })
        
        fig = px.line(sample_data, x='Month', y='Index', 
                     title=f'Sample data untuk {st.session_state.sub_page}')
        fig.update_layout(height=400, title_font=dict(size=18, color='#003366'))
        st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.subheader(f"Halaman {st.session_state.main_page}")
        st.subheader(f"Sub-menu: {st.session_state.sub_page}")
        st.info(f"Konten untuk {st.session_state.main_page} - {st.session_state.sub_page} akan ditampilkan di sini.")
        
        # Placeholder chart
        sample_data = pd.DataFrame({
            'Category': ['A', 'B', 'C', 'D', 'E'],
            'Value': np.random.randint(10, 100, 5)
        })
        
        fig = px.pie(sample_data, values='Value', names='Category', 
                    title=f'Sample data untuk {st.session_state.sub_page}')
        fig.update_layout(height=400, title_font=dict(size=18, color='#003366'))
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; font-size: 14px;'>"
    "© 2024 Badan Pusat Statistik - Direktorat Neraca Pengeluaran"
    "</div>", 
    unsafe_allow_html=True
)
