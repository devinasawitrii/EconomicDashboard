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
        padding: 20px 0;
        background-color: white;
    }
    .logo-section {
        flex: 1;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .logo-title {
        color: #000080;
        font-size: 36px;
        font-weight: bold;
        text-align: center;
        margin: 0;
        padding: 0;
    }
    .subtitle {
        color: #ff0000;
        font-size: 16px;
        text-align: center;
        font-style: italic;
        margin: 5px 0;
    }
    .main-nav {
        background-color: #000080;
        padding: 0;
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }
    .nav-button {
        background-color: #000080;
        color: white;
        border: none;
        padding: 15px 25px;
        font-weight: bold;
        cursor: pointer;
        border-right: 1px solid rgba(255,255,255,0.2);
        transition: background-color 0.3s;
    }
    .nav-button:hover {
        background-color: #0056b3;
    }
    .nav-button.active {
        background-color: #004494;
        font-weight: bold;
    }
    .sidebar-nav {
        border-radius: 0;
        overflow: hidden;
        width: 100%;
    }
    .side-nav-button {
        background-color: #87CEEB;
        color: #333;
        border: none;
        padding: 15px;
        margin-bottom: 2px;
        border-left: 5px solid #0070c0;
        font-weight: bold;
        cursor: pointer;
        width: 100%;
        text-align: left;
        transition: background-color 0.3s;
        font-size: 14px;
    }
    .side-nav-button:hover {
        background-color: #5DADE2;
    }
    .side-nav-button.active {
        background-color: #0070c0;
        color: white;
    }
    .chart-container {
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 20px;
        background-color: white;
        height: 500px;
    }
    .logo-placeholder {
        width: 120px;
        height: 80px;
        background-color: #f0f0f0;
        border: 2px solid #000080;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        color: #000080;
        border-radius: 5px;
    }
    .bps-logo {
        width: 120px;
        height: 80px;
        background: linear-gradient(to bottom, #0070c0 50%, #00B0F0 50%);
        color: white;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        font-size: 10px;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Header with logos and title
st.markdown("""
<div class="header-container">
    <div class="logo-section">
        <div class="logo-placeholder">AIG LOGO</div>
    </div>
    <div class="logo-section">
        <div>
            <div class="logo-title">ACTIONABLE INSIGHTS</div>
            <div class="subtitle">Generate wisdom from fingertip</div>
        </div>
    </div>
    <div class="logo-section">
        <div class="bps-logo">
            <div>DIREKTORAT</div>
            <div>NERACA PENGELUARAN</div>
            <div style="font-size: 18px; font-weight: bold; margin-top: 5px;">📊 BPS</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Main Navigation Menu
main_tabs = ['Neraca Nasional', 'Indeks Harga', 'Ekspor-Impor', 'APBN', 'Ketenagakerjaan', 'Kemiskinan', 'IPM']

nav_html = '<div class="main-nav">'
for tab in main_tabs:
    active_class = 'active' if st.session_state.main_tab == tab else ''
    nav_html += f'<button class="nav-button {active_class}" onclick="setMainTab(\'{tab}\')">{tab}</button>'
nav_html += '</div>'

st.markdown(nav_html, unsafe_allow_html=True)

# Handle main tab selection with buttons
col_buttons = st.columns(len(main_tabs))
for i, tab in enumerate(main_tabs):
    with col_buttons[i]:
        if st.button(tab, key=f"main_{tab}", help=f"Navigate to {tab}"):
            st.session_state.main_tab = tab
            st.rerun()

# Create layout with sidebar and main content
col1, col2 = st.columns([1, 3])

# Sidebar navigation
with col1:
    st.markdown("### Navigation")
    
    # Side navigation items based on main tab
    if st.session_state.main_tab == 'Neraca Nasional':
        side_tabs = [
            'Pertumbuhan Ekonomi y-o-y',
            'Pertumbuhan Ekonomi q-to-q', 
            'Pertumbuhan Ekonomi c-to-c',
            'Indeks Implisit y-o-y',
            'Indeks Implisit q-to-q',
            'Indeks Implisit c-to-c',
            'PDB ADHB',
            'PDB ADHK'
        ]
    else:
        side_tabs = [f'{st.session_state.main_tab} Option 1', f'{st.session_state.main_tab} Option 2']
    
    for tab in side_tabs:
        if st.button(tab, key=f"side_{tab}", use_container_width=True):
            st.session_state.side_tab = tab
            st.rerun()
        
        # Visual indicator for active tab
        if st.session_state.side_tab == tab:
            st.markdown("**← Active**")

# Main content area
with col2:
    st.markdown(f"## {st.session_state.main_tab}")
    st.markdown(f"### {st.session_state.side_tab}")
    
    # Display different content based on selection
    if st.session_state.main_tab == 'Neraca Nasional' and st.session_state.side_tab == 'Pertumbuhan Ekonomi y-o-y':
        
        # Load data from CSV file
        try:
            df = pd.read_csv('Sheet 1_Full Data_data.csv')
            df.columns = ['Period', 'Growth']
            
            # Create the economic growth chart
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
                line=dict(color='#000080', width=2),
                marker=dict(size=6, color='#000080'),
            )
            
            # Add grid lines
            fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
            
            # Display the chart
            st.plotly_chart(fig, use_container_width=True)
            
            # Show data summary
            st.markdown("#### Data Summary")
            col1_summary, col2_summary, col3_summary = st.columns(3)
            
            with col1_summary:
                st.metric("Latest Growth", f"{df['Growth'].iloc[-1]:.2f}%")
            
            with col2_summary:
                st.metric("Average Growth", f"{df['Growth'].mean():.2f}%")
            
            with col3_summary:
                st.metric("Lowest Point", f"{df['Growth'].min():.2f}%")
                
        except FileNotFoundError:
            st.error("📁 File 'Sheet 1_Full Data_data.csv' tidak ditemukan!")
            st.info("Pastikan file CSV berada di folder yang sama dengan script ini.")
            
            # Show sample data structure
            st.markdown("**Expected CSV format:**")
            st.code("""Quarter of Periode,Y-O-Y
2011 Q1,6.48
2011 Q2,6.27
...""")
            
        except Exception as e:
            st.error(f"❌ Error loading CSV file: {str(e)}")
    
    elif st.session_state.main_tab == 'Neraca Nasional':
        # Other Neraca Nasional options
        st.info(f"Displaying data for: {st.session_state.side_tab}")
        st.markdown("Data akan ditampilkan di sini sesuai dengan pilihan menu.")
        
        # Placeholder chart for other options
        sample_data = pd.DataFrame({
            'Period': ['2020 Q1', '2020 Q2', '2020 Q3', '2020 Q4', '2021 Q1'],
            'Value': [100, 95, 102, 108, 105]
        })
        
        fig = px.bar(sample_data, x='Period', y='Value', 
                    title=f'{st.session_state.side_tab} - Sample Data')
        st.plotly_chart(fig, use_container_width=True)
    
    else:
        # Other main tabs
        st.info(f"Halaman {st.session_state.main_tab} sedang dalam pengembangan.")
        st.markdown(f"**Current Selection:**")
        st.markdown(f"- Main Tab: {st.session_state.main_tab}")
        st.markdown(f"- Sub Tab: {st.session_state.side_tab}")
        
        # Sample content for other tabs
        if st.session_state.main_tab == 'Indeks Harga':
            st.markdown("🏷️ Data indeks harga akan ditampilkan di sini")
        elif st.session_state.main_tab == 'Ekspor-Impor':
            st.markdown("📦 Data ekspor-impor akan ditampilkan di sini")
        elif st.session_state.main_tab == 'APBN':
            st.markdown("💰 Data APBN akan ditampilkan di sini")
        elif st.session_state.main_tab == 'Ketenagakerjaan':
            st.markdown("👥 Data ketenagakerjaan akan ditampilkan di sini")
        elif st.session_state.main_tab == 'Kemiskinan':
            st.markdown("📊 Data kemiskinan akan ditampilkan di sini")
        elif st.session_state.main_tab == 'IPM':
            st.markdown("📈 Data IPM akan ditampilkan di sini")

# Footer
st.markdown("---")
st.markdown("**Actionable Insights Generator** - BPS Direktorat Neraca Pengeluaran")


