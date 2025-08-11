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

# Custom CSS for styling
st.markdown("""
<style>
    /* Adjust top padding to show title properly */
    .block-container { 
        padding-top: 2rem !important;
    }
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 0px;
        background-color: white;
        margin-bottom: 1rem;
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
        margin-top: -5px; /* Move closer to title */
        margin-bottom: 0px;
    }
    .chart-container {
        border: none;
        border-radius: 0px;
        padding: 0px 20px 20px 20px;
        background-color: white;
        box-shadow: none;
    }
    .logo-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        padding-top: 20px; /* Add top padding to push logos down */
    }
</style>
""", unsafe_allow_html=True)

# Header with logos
col1, col2, col3 = st.columns([1, 3, 1])

with col1:
    # AIG Logo - Image file
    st.markdown("""
    <div class="logo-container">
        <img src="aig_logo.png" alt="AIG Logo" style="width: 100px; height: 100px; object-fit: contain;">
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Title and subtitle with reduced spacing
    st.markdown('<div class="logo-title">ACTIONABLE INSIGHTS</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Generate wisdom from fingertip</div>', unsafe_allow_html=True)

with col3:
    # BPS Logo - Image file
    st.markdown("""
    <div class="logo-container">
        <img src="bps_logo.png" alt="BPS Logo" style="width: 120px; height: 100px; object-fit: contain;">
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

# Update session state if main tab changed
if selected_main_tab != st.session_state.main_tab:
    st.session_state.main_tab = selected_main_tab
    st.rerun()

# Main content area - full width since no sidebar
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
chart_col, insight_col = st.columns([2, 1])

# Display content based on selected main tab
if st.session_state.main_tab == 'Neraca Nasional':
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
            margin=dict(l=40, r=40, t=40, b=40),
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
        
        fig.update_traces(line=dict(color='navy', width=2), marker=dict(size=6, color='navy'))
        fig.update_layout(height=400, plot_bgcolor='white', margin=dict(l=40, r=40, t=40, b=40))
        
        with chart_col:
            st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error loading CSV file: {str(e)}")

elif st.session_state.main_tab == 'Indeks Harga':
    # Sample inflation data
    sample_data = pd.DataFrame({
        'Period': pd.date_range('2023-01', periods=12, freq='M').strftime('%Y-%m'),
        'Value': np.random.uniform(-1, 5, 12)
    })
    title = "Inflasi y-o-y (%)"
    
    fig_sample = px.line(sample_data, x='Period', y='Value', title=title, markers=True)
    fig_sample.update_traces(line=dict(color='teal', width=2), marker=dict(size=6, color='teal'))
    fig_sample.update_layout(height=400, plot_bgcolor='white', margin=dict(l=40, r=40, t=40, b=40))
    
    with chart_col:
        st.plotly_chart(fig_sample, use_container_width=True)
        st.caption("Note: Sample inflation data")

elif st.session_state.main_tab == 'Ekspor-Impor':
    # Sample trade data
    sample_data = pd.DataFrame({
        'Period': pd.date_range('2023-01', periods=12, freq='M').strftime('%Y-%m'),
        'Value': np.random.uniform(10000, 30000, 12)
    })
    title = "Nilai ekspor (migas-non migas) (Juta USD)"
    
    fig_sample = px.line(sample_data, x='Period', y='Value', title=title, markers=True)
    fig_sample.update_traces(line=dict(color='teal', width=2), marker=dict(size=6, color='teal'))
    fig_sample.update_layout(height=400, plot_bgcolor='white', margin=dict(l=40, r=40, t=40, b=40))
    
    with chart_col:
        st.plotly_chart(fig_sample, use_container_width=True)
        st.caption("Note: Sample trade data")

elif st.session_state.main_tab == 'APBN':
    # Sample APBN data
    sample_data = pd.DataFrame({
        'Period': [f"2023 Q{i}" for i in range(1, 5)] + [f"2024 Q{i}" for i in range(1, 5)],
        'Value': np.random.uniform(500, 1500, 8)
    })
    title = "Belanja Pegawai (Triliun Rupiah)"
    
    fig_sample = px.line(sample_data, x='Period', y='Value', title=title, markers=True)
    fig_sample.update_traces(line=dict(color='teal', width=2), marker=dict(size=6, color='teal'))
    fig_sample.update_layout(height=400, plot_bgcolor='white', margin=dict(l=40, r=40, t=40, b=40))
    
    with chart_col:
        st.plotly_chart(fig_sample, use_container_width=True)
        st.caption("Note: Sample APBN data")

elif st.session_state.main_tab == 'Ketenagakerjaan':
    # Sample employment data
    sample_data = pd.DataFrame({
        'Period': ['Agu 2022', 'Feb 2023', 'Agu 2023', 'Feb 2024'],
        'Value': np.random.uniform(3, 7, 4)
    })
    title = "TPT (%)"
    
    fig_sample = px.line(sample_data, x='Period', y='Value', title=title, markers=True)
    fig_sample.update_traces(line=dict(color='teal', width=2), marker=dict(size=6, color='teal'))
    fig_sample.update_layout(height=400, plot_bgcolor='white', margin=dict(l=40, r=40, t=40, b=40))
    
    with chart_col:
        st.plotly_chart(fig_sample, use_container_width=True)
        st.caption("Note: Sample employment data")

elif st.session_state.main_tab == 'Kemiskinan':
    # Sample poverty data
    sample_data = pd.DataFrame({
        'Period': ['Mar 2022', 'Sep 2022', 'Mar 2023', 'Sep 2023'],
        'Value': np.random.uniform(9, 11, 4)
    })
    title = "Persentase penduduk miskin (%)"
    
    fig_sample = px.line(sample_data, x='Period', y='Value', title=title, markers=True)
    fig_sample.update_traces(line=dict(color='teal', width=2), marker=dict(size=6, color='teal'))
    fig_sample.update_layout(height=400, plot_bgcolor='white', margin=dict(l=40, r=40, t=40, b=40))
    
    with chart_col:
        st.plotly_chart(fig_sample, use_container_width=True)
        st.caption("Note: Sample poverty data")

elif st.session_state.main_tab == 'IPM':
    # Sample IPM data
    sample_data = pd.DataFrame({
        'Period': [str(y) for y in range(2020, 2024)],
        'Value': np.random.uniform(70, 75, 4)
    })
    title = "IPM"
    
    fig_sample = px.line(sample_data, x='Period', y='Value', title=title, markers=True)
    fig_sample.update_traces(line=dict(color='teal', width=2), marker=dict(size=6, color='teal'))
    fig_sample.update_layout(height=400, plot_bgcolor='white', margin=dict(l=40, r=40, t=40, b=40))
    
    with chart_col:
        st.plotly_chart(fig_sample, use_container_width=True)
        st.caption("Note: Sample IPM data")

# Global Insight Section
with insight_col:
    st.markdown("#### Insight:")
    st.markdown("*   Insight 1: ...")
    st.markdown("*   Insight 2: ...")
    st.markdown("*   Insight 3: ...")

st.markdown("</div>", unsafe_allow_html=True)
