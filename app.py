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
    }
    .subtitle {
        color: red;
        font-size: 18px;
        text-align: center;
        font-style: italic;
    }
    .main-nav {
        background-color: navy;
        padding: 10px 0;
        display: flex;
        justify-content: space-around;
    }
    .nav-button {
        background: none;
        border: none;
        color: white;
        padding: 8px 16px;
        font-weight: bold;
        cursor: pointer;
        border-radius: 4px;
    }
    .nav-button:hover {
        background-color: rgba(255,255,255,0.2);
    }
    .nav-button.active {
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
        justify-content: center;
        align-items: center;
        height: 100px;
    }
</style>
""", unsafe_allow_html=True)

# Header with logos
col1, col2, col3 = st.columns([1, 3, 1])

with col1:
    # AIG Logo (placeholder image)
    st.markdown("""
    <div class="logo-container">
        <svg width="80" height="80" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#0070c0;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#003d82;stop-opacity:1" />
                </linearGradient>
            </defs>
            <circle cx="40" cy="40" r="35" fill="url(#grad1)" stroke="#fff" stroke-width="2"/>
            <text x="20" y="32" fill="white" font-size="16px" font-weight="bold">A</text>
            <text x="20" y="48" fill="white" font-size="16px" font-weight="bold">I</text>
            <text x="32" y="48" fill="white" font-size="16px" font-weight="bold">G</text>
        </svg>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Title and Subtitle
    st.markdown('<div class="logo-title">ACTIONABLE INSIGHTS</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Generate wisdom from fingertip</div>', unsafe_allow_html=True)

with col3:
    # BPS Logo (placeholder image)
    st.markdown("""
    <div class="logo-container">
        <svg width="120" height="80" xmlns="http://www.w3.org/2000/svg">
            <rect x="0" y="0" width="120" height="25" fill="#0070c0"/>
            <text x="60" y="12" fill="white" font-size="8px" text-anchor="middle" font-weight="bold">DIREKTORAT</text>
            <text x="60" y="22" fill="white" font-size="8px" text-anchor="middle" font-weight="bold">NERACA PENGELUARAN</text>
            
            <rect x="0" y="25" width="120" height="55" fill="#00B0F0"/>
            <rect x="10" y="35" width="25" height="25" fill="#FF6600" rx="3"/>
            <rect x="40" y="35" width="25" height="25" fill="#FF9900" rx="3"/>
            <rect x="70" y="35" width="25" height="25" fill="#FFCC00" rx="3"/>
            <text x="60" y="72" fill="white" font-size="14px" text-anchor="middle" font-weight="bold">BADAN PUSAT STATISTIK</text>
        </svg>
    </div>
    """, unsafe_allow_html=True)

# Main Navigation Menu with better styling
st.markdown("""
<div style="background-color: navy; padding: 15px 0; margin-bottom: 20px;">
    <div style="display: flex; justify-content: space-around; max-width: 1200px; margin: 0 auto;">""", unsafe_allow_html=True)

main_tabs = ['Neraca Nasional', 'Indeks Harga', 'Ekspor-Impor', 'APBN', 'Ketenagakerjaan', 'Kemiskinan', 'IPM']

# Create navigation buttons in columns
nav_cols = st.columns(7)
for i, tab in enumerate(main_tabs):
    with nav_cols[i]:
        button_style = """
        <style>
        div.stButton > button {
            background-color: """ + ("rgba(255,255,255,0.3)" if st.session_state.main_tab == tab else "transparent") + """;
            color: white;
            border: 1px solid rgba(255,255,255,0.3);
            border-radius: 5px;
            padding: 8px 12px;
            font-weight: bold;
            width: 100%;
            transition: all 0.3s;
        }
        div.stButton > button:hover {
            background-color: rgba(255,255,255,0.2);
            border-color: rgba(255,255,255,0.5);
        }
        </style>
        """
        st.markdown(button_style, unsafe_allow_html=True)
        if st.button(tab, key=f'nav_{i}', help=f'Navigate to {tab}'):
            st.session_state.main_tab = tab

st.markdown("</div></div>", unsafe_allow_html=True)

# Menu Navigasi Section
st.markdown("---")
st.markdown("### 🎯 **Menu Navigasi**")
st.markdown(f"**Kategori:** {st.session_state.main_tab}")
st.markdown(f"**Sub-kategori:** {st.session_state.side_tab}")
st.markdown("---")

# Create layout with sidebar and main content
col1, col2 = st.columns([1, 3])

with col1:
    st.markdown('<div class="sidebar-nav">', unsafe_allow_html=True)
    
    # Sidebar navigation items with buttons
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
    
    for i, tab in enumerate(side_tabs):
        if st.button(tab.replace(' ', '\n'), key=f'side_{i}', help=f'Navigate to {tab}'):
            st.session_state.side_tab = tab
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # Main content area - shows different content based on selected tabs
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    # Show different content based on selected side tab
    if st.session_state.side_tab == 'Pertumbuhan Ekonomi y-o-y':
        # Load data from CSV file for y-o-y growth
        try:
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
            st.error("File 'Sheet 1_Full Data_data.csv' tidak ditemukan. Pastikan file CSV berada di folder yang sama dengan script ini.")
        except Exception as e:
            st.error(f"Error loading CSV file: {str(e)}")
    
    else:
        # Placeholder content for other tabs
        st.info(f"📊 Halaman {st.session_state.side_tab} sedang dalam pengembangan.")
        st.write("Data dan visualisasi untuk kategori ini akan segera tersedia.")
        
        # Sample placeholder chart
        sample_data = pd.DataFrame({
            'Period': ['2022 Q1', '2022 Q2', '2022 Q3', '2022 Q4', '2023 Q1', '2023 Q2'],
            'Value': [4.2, 4.5, 4.8, 5.1, 4.9, 5.2]
        })
        
        fig_placeholder = px.bar(sample_data, x='Period', y='Value', 
                                title=f'{st.session_state.side_tab} - Sample Data')
        fig_placeholder.update_layout(height=300)
        st.plotly_chart(fig_placeholder, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
