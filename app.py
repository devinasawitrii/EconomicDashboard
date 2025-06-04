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
    page_title="Actionable Insights Generator",
    page_icon="📊",
    layout="wide"
)

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
    .main-nav a {
        color: white;
        text-decoration: none;
        padding: 8px 16px;
        font-weight: bold;
    }
    .main-nav a:hover {
        background-color: rgba(255,255,255,0.2);
        border-radius: 4px;
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
    }
    .nav-item:hover {
        background-color: #e0e0e0;
        cursor: pointer;
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
</style>
""", unsafe_allow_html=True)

# Header with logos
col1, col2, col3 = st.columns([1, 3, 1])

with col1:
    # AIG Logo placeholder (using a simple text placeholder)
    st.markdown("""
    <div style="text-align: center;">
        <svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">
            <circle cx="50" cy="50" r="40" stroke="navy" stroke-width="4" fill="white" />
            <text x="35" y="60" fill="navy" font-size="24px" font-weight="bold">aig</text>
        </svg>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Title and Subtitle
    st.markdown('<div class="logo-title">ACTIONABLE INSIGHTS GENERATOR</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Generate wisdom from fingertip</div>', unsafe_allow_html=True)

with col3:
    # BPS Logo placeholder
    st.markdown("""
    <div style="text-align: center;">
        <div style="background-color: #0070c0; color: white; padding: 5px; font-size: 10px; text-align: center;">
            DIREKTORAT<br>NERACA PENGELUARAN
        </div>
        <div style="background-color: #00B0F0; display: flex; justify-content: center; align-items: center; height: 50px;">
            <span style="color: white; font-weight: bold;">BPS</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Main Navigation Menu
st.markdown("""
<div class="main-nav">
    <a href="#">Neraca Nasional</a>
    <a href="#">Indeks Harga</a>
    <a href="#">Ekspor-Impor</a>
    <a href="#">APBN</a>
    <a href="#">Ketenagakerjaan</a>
    <a href="#">Kemiskinan</a>
    <a href="#">IPM</a>
</div>
""", unsafe_allow_html=True)

# Create layout with sidebar and main content
col1, col2 = st.columns([1, 3])

with col1:
    st.markdown('<div class="sidebar-nav">', unsafe_allow_html=True)
    
    # Sidebar navigation items 
    st.markdown('<div class="nav-item active">Pertumbuhan<br>Ekonomi y-o-y</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-item">Pertumbuhan<br>Ekonomi q-to-q</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-item">Pertumbuhan<br>Ekonomi c-to-c</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-item">Indeks Implisit<br>y-o-y</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-item">Indeks Implisit<br>q-to-q</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-item">Indeks Implisit<br>c-to-c</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-item">PDB ADHB</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-item">PDB ADHK</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # Main content - Economic Growth chart
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    # Load data from CSV file
    try:
        # Try to load the CSV file
        df = pd.read_csv('Sheet 1_Full Data_data.csv')
        df.columns = ['Period', 'Growth']
    except FileNotFoundError:
        st.error("File 'Sheet 1_Full Data_data.csv' tidak ditemukan. Pastikan file CSV berada di folder yang sama dengan script ini.")
        st.stop()
    except Exception as e:
        st.error(f"Error loading CSV file: {str(e)}")
        st.stop()
    
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
    
    st.markdown('</div>', unsafe_allow_html=True)
