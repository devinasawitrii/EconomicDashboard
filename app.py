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

# Custom CSS for styling - NO SCROLL VERSION
st.markdown("""
<style>
    /* Hide scrollbars and set fixed viewport */
    html, body, [data-testid="stAppViewContainer"] {
        height: 100vh !important;
        max-height: 100vh !important;
        overflow: hidden !important;
    }
    
    .main .block-container { 
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        max-height: 100vh !important;
        overflow: hidden !important;
    }
    
    /* Compact header */
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 5px 0px;
        background-color: white;
        margin-bottom: 0.5rem;
        height: 80px;
        max-height: 80px;
    }
    
    .logo-title {
        color: navy;
        font-size: 28px;
        font-weight: bold;
        text-align: center;
        margin: 0;
        padding: 0;
    }
    
    .subtitle {
        color: #0070c0;
        font-size: 16px;
        text-align: center;
        font-style: italic;
        margin-top: -3px;
        margin-bottom: 0px;
    }
    
    .chart-container {
        border: none;
        border-radius: 0px;
        padding: 0px 15px 10px 15px;
        background-color: white;
        box-shadow: none;
        height: calc(100vh - 200px);
        max-height: calc(100vh - 200px);
        overflow: hidden;
    }
    
    .logo-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        padding-top: 5px;
    }
    
    /* Compact navigation menu */
    .stSelectbox > div > div {
        height: 35px !important;
    }
    
    /* Hide Streamlit elements that take space */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Compact plotly charts */
    .js-plotly-plot {
        height: 350px !important;
        max-height: 350px !important;
    }
    
    /* Insight column styling */
    .insight-container {
        padding: 10px;
        height: 350px;
        max-height: 350px;
        overflow-y: auto;
        border: 1px solid #e0e0e0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Compact Header with logos - reduced height
col1, col2, col3 = st.columns([1, 3, 1])

with col1:
    st.markdown("""
    <div class="logo-container">
        <img src="aig_logo.png" alt="AIG Logo" style="width: 70px; height: 70px; object-fit: contain;">
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown('<div class="logo-title">ACTIONABLE INSIGHTS</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Generate wisdom from fingertip</div>', unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="logo-container">
        <img src="bps_logo.png" alt="BPS Logo" style="width: 85px; height: 70px; object-fit: contain;">
    </div>
    """, unsafe_allow_html=True)

# Compact Navigation Menu
main_tabs_list = ['Neraca Nasional', 'Indeks Harga', 'Ekspor-Impor', 'APBN', 'Ketenagakerjaan', 'Kemiskinan', 'IPM']

try:
    default_main_index = main_tabs_list.index(st.session_state.main_tab)
except ValueError:
    default_main_index = 0

selected_main_tab = option_menu(
    menu_title=None,
    options=main_tabs_list,
    icons=None,
    menu_icon=None,
    default_index=default_main_index,
    orientation="horizontal",
    styles={
        "container": {"padding": "0px !important", "background-color": "white", "margin-bottom": "0.5rem", "height": "40px"}, 
        "nav-link": {
            "font-size": "12px", 
            "font-weight": "bold",
            "color": "#333",
            "background-color": "#f0f0f0", 
            "text-align": "center", 
            "padding": "8px 8px",
            "margin":"0px 1px !important",
            "border-radius": "0px !important",
            "border-bottom": "3px solid #0070c0",
            "transition": "background-color 0.2s, color 0.2s, border-color 0.2s",
            "white-space": "nowrap",
            "height": "35px"
        },
        "nav-link-selected": {
            "background-color": "#0070c0", 
            "color": "white",
            "border-bottom": "3px solid navy"
        }
    }
)

if selected_main_tab != st.session_state.main_tab:
    st.session_state.main_tab = selected_main_tab
    st.rerun()

# Main content area with fixed height
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
chart_col, insight_col = st.columns([2, 1])

# Chart creation function with fixed height
def create_chart(df, title, color='navy', height=350):
    fig = px.line(df, x=df.columns[0], y=df.columns[1], 
                 title=title,
                 markers=True)
    
    fig.update_layout(
        plot_bgcolor='white',
        title_font=dict(size=14),
        height=height,
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode="x unified"
    )
    
    fig.update_traces(
        line=dict(color=color, width=2),
        marker=dict(size=5, color=color),
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray', title_font=dict(size=12))
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray', title_font=dict(size=12))
    
    return fig

# Display content based on selected main tab
if st.session_state.main_tab == 'Neraca Nasional':
    try:
        df = pd.read_csv('Sheet 1_Full Data_data.csv')
        df.columns = ['Period', 'Growth']
        
        fig = create_chart(df, 'Pertumbuhan Ekonomi y-o-y', 'navy')
        
        # Custom layout for this specific chart
        fig.update_layout(
            xaxis=dict(
                tickmode='array',
                tickvals=[df['Period'][i] for i in range(0, len(df), 4)],
                ticktext=[f"{period.split()[0]} Q1" for period in df['Period'][::4]],
                title_font=dict(size=12),
            ),
            yaxis=dict(
                range=[-6, 8],
                tickvals=[-5, 0, 5],
                title_font=dict(size=12),
            )
        )
        
        with chart_col:
            st.plotly_chart(fig, use_container_width=True)
        
    except FileNotFoundError:
        sample_periods = [f"2020 Q{i%4+1}" for i in range(16)]
        sample_growth = [5.2, -5.3, -3.5, -2.1, -0.7, 7.1, 3.7, 5.0, 5.4, 5.1, 5.2, 5.3, 4.9, 5.0, 5.1, 4.8]
        
        df_sample = pd.DataFrame({
            'Period': sample_periods,
            'Growth': sample_growth
        })
        
        fig = create_chart(df_sample, 'Pertumbuhan Ekonomi y-o-y (Sample Data)', 'navy')
        
        with chart_col:
            st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error loading CSV file: {str(e)}")

elif st.session_state.main_tab == 'Indeks Harga':
    sample_data = pd.DataFrame({
        'Period': pd.date_range('2023-01', periods=12, freq='M').strftime('%Y-%m'),
        'Value': np.random.uniform(-1, 5, 12)
    })
    
    fig = create_chart(sample_data, "Inflasi y-o-y (%)", 'teal')
    
    with chart_col:
        st.plotly_chart(fig, use_container_width=True)

elif st.session_state.main_tab == 'Ekspor-Impor':
    sample_data = pd.DataFrame({
        'Period': pd.date_range('2023-01', periods=12, freq='M').strftime('%Y-%m'),
        'Value': np.random.uniform(10000, 30000, 12)
    })
    
    fig = create_chart(sample_data, "Nilai ekspor (migas-non migas) (Juta USD)", 'teal')
    
    with chart_col:
        st.plotly_chart(fig, use_container_width=True)

elif st.session_state.main_tab == 'APBN':
    sample_data = pd.DataFrame({
        'Period': [f"2023 Q{i}" for i in range(1, 5)] + [f"2024 Q{i}" for i in range(1, 5)],
        'Value': np.random.uniform(500, 1500, 8)
    })
    
    fig = create_chart(sample_data, "Belanja Pegawai (Triliun Rupiah)", 'teal')
    
    with chart_col:
        st.plotly_chart(fig, use_container_width=True)

elif st.session_state.main_tab == 'Ketenagakerjaan':
    sample_data = pd.DataFrame({
        'Period': ['Agu 2022', 'Feb 2023', 'Agu 2023', 'Feb 2024'],
        'Value': np.random.uniform(3, 7, 4)
    })
    
    fig = create_chart(sample_data, "TPT (%)", 'teal')
    
    with chart_col:
        st.plotly_chart(fig, use_container_width=True)

elif st.session_state.main_tab == 'Kemiskinan':
    sample_data = pd.DataFrame({
        'Period': ['Mar 2022', 'Sep 2022', 'Mar 2023', 'Sep 2023'],
        'Value': np.random.uniform(9, 11, 4)
    })
    
    fig = create_chart(sample_data, "Persentase penduduk miskin (%)", 'teal')
    
    with chart_col:
        st.plotly_chart(fig, use_container_width=True)

elif st.session_state.main_tab == 'IPM':
    sample_data = pd.DataFrame({
        'Period': [str(y) for y in range(2020, 2024)],
        'Value': np.random.uniform(70, 75, 4)
    })
    
    fig = create_chart(sample_data, "IPM", 'teal')
    
    with chart_col:
        st.plotly_chart(fig, use_container_width=True)

# Compact Insight Section
with insight_col:
    st.markdown("""
    <div class="insight-container">
        <h4 style="margin-top: 0; font-size: 16px;">Insight:</h4>
        <ul style="font-size: 14px; margin: 0; padding-left: 20px;">
            <li>Insight 1: Economic growth shows recovery trend</li>
            <li>Insight 2: Seasonal patterns are evident</li>
            <li>Insight 3: Policy impacts visible in data</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
