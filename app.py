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
    .main-nav button {
        background: none;
        border: none;
        color: white;
        padding: 8px 16px;
        font-weight: bold;
        cursor: pointer;
        border-radius: 4px;
        transition: background-color 0.3s;
    }
    .main-nav button:hover {
        background-color: rgba(255,255,255,0.2);
    }
    .main-nav button.active {
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

# Main Navigation Menu with functionality
main_tabs = ['Neraca Nasional', 'Indeks Harga', 'Ekspor-Impor', 'APBN', 'Ketenagakerjaan', 'Kemiskinan', 'IPM']

nav_html = '<div class="main-nav">'
for i, tab in enumerate(main_tabs):
    active_class = 'active' if st.session_state.main_tab == tab else ''
    nav_html += f'<button class="{active_class}" onclick="setMainTab(\'{tab}\')">{tab}</button>'
nav_html += '</div>'

st.markdown(nav_html, unsafe_allow_html=True)

# JavaScript for tab functionality
st.markdown("""
<script>
function setMainTab(tab) {
    // This would need to be handled by Streamlit's session state
    console.log('Selected tab:', tab);
}
</script>
""", unsafe_allow_html=True)

# Create main tab buttons using Streamlit
col_tabs = st.columns(len(main_tabs))
for i, tab in enumerate(main_tabs):
    with col_tabs[i]:
        if st.button(tab, key=f"main_tab_{i}", use_container_width=True):
            st.session_state.main_tab = tab
            st.rerun()

# Create layout with sidebar and main content
col1, col2 = st.columns([1, 3])

with col1:
    st.markdown('<div class="sidebar-nav">', unsafe_allow_html=True)
    
    # Sidebar navigation items with functionality
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
    
    for tab in side_tabs:
        active_class = 'active' if st.session_state.side_tab == tab else ''
        if st.button(tab.replace(' ', '\n'), key=f"side_tab_{tab}", use_container_width=True):
            st.session_state.side_tab = tab
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # Main content area - changes based on selected tabs
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    # Display content based on selected main tab
    if st.session_state.main_tab == 'Neraca Nasional':
        # Display content based on selected side tab
        if st.session_state.side_tab == 'Pertumbuhan Ekonomi y-o-y':
            # Load data from CSV file
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
                        tickvals=[df['Period'][i] for i in range(0, len(df), 4)],  # Show only Q1 for each year
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
                st.error("File 'Sheet 1_Full Data_data.csv' tidak ditemukan. Pastikan file CSV berada di folder yang sama dengan script ini.")
            except Exception as e:
                st.error(f"Error loading CSV file: {str(e)}")
        
        else:
            # Placeholder for other Neraca Nasional tabs
            st.subheader(st.session_state.side_tab)
            st.info(f"Konten untuk {st.session_state.side_tab} akan ditampilkan di sini.")
            
            # Sample chart for demonstration
            sample_data = pd.DataFrame({
                'x': range(10),
                'y': np.random.randn(10).cumsum()
            })
            fig = px.line(sample_data, x='x', y='y', title=st.session_state.side_tab)
            st.plotly_chart(fig, use_container_width=True)
    
    else:
        # Placeholder for other main tabs
        st.subheader(st.session_state.main_tab)
        st.info(f"Konten untuk {st.session_state.main_tab} akan ditampilkan di sini.")
        
        # Sample chart for demonstration
        sample_data = pd.DataFrame({
            'Category': ['A', 'B', 'C', 'D'],
            'Value': [23, 45, 56, 78]
        })
        fig = px.bar(sample_data, x='Category', y='Value', title=f"Data {st.session_state.main_tab}")
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Display current selections for debugging
st.sidebar.write(f"Main Tab: {st.session_state.main_tab}")
st.sidebar.write(f"Side Tab: {st.session_state.side_tab}")
