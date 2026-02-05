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

# Custom CSS for styling - optimized for no scroll
st.markdown("""
<style>
    /* Remove all default padding and margins */
    .block-container { 
        padding-top: 0.5rem !important;
        padding-bottom: 0rem !important;
        max-width: 100% !important;
    }
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 5px 0px;
        background-color: white;
        margin-bottom: 0.5rem;
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
        padding: 0px 10px 5px 10px;
        background-color: white;
        box-shadow: none;
    }
    .logo-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        padding-top: 5px;
    }
    /* Hide streamlit elements that take up space */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Reduce spacing in sidebar and main content */
    .css-1d391kg {padding-top: 0rem;}
    .css-18e3th9 {padding-top: 0rem;}
    
    /* Make insights section more compact */
    .insight-section {
        font-size: 14px;
        line-height: 1.2;
    }
    
    /* Reduce vertical spacing for all elements */
    .stMarkdown {
        margin-bottom: 0.2rem !important;
    }
    
    /* Custom styling for viz selector */
    .viz-selector {
        background-color: #f0f8ff;
        padding: 8px;
        border-radius: 5px;
        margin-bottom: 10px;
        border-left: 4px solid #0070c0;
    }
</style>
""", unsafe_allow_html=True)

# Data PDB Indonesia
pdb_data = {
    'Tahun': [2010]*4 + [2011]*4 + [2012]*4 + [2013]*4 + [2014]*4 + [2015]*4 + [2016]*4 + [2017]*4 + [2018]*4 + [2019]*4 + [2020]*4 + [2021]*4 + [2022]*4 + [2023]*4 + [2024]*2,
    'Triwulan': ['I', 'II', 'III', 'IV']*14 + ['I', 'II'],
    'y_o_y': [None, None, None, None, 6.48, 6.27, 6.01, 5.94, 6.11, 6.21, 5.94, 5.87, 5.54, 5.59, 5.52, 5.58, 5.12, 4.94, 4.93, 5.05, 4.83, 4.74, 4.78, 5.15, 4.94, 5.21, 5.03, 4.94, 5.01, 5.01, 5.06, 5.19, 5.07, 5.27, 5.17, 5.18, 5.06, 5.05, 5.01, 4.96, 2.97, -5.32, -3.49, -2.17, -0.69, 7.08, 3.53, 5.03, 5.02, 5.46, 5.73, 5.01, 5.04, 5.17, 4.94, 5.04, 5.11, 5.05],
    'q_to_q': [None, None, None, None, 0.64, 3.86, 3.61, -2.18, 0.8, 3.96, 3.35, -2.25, 0.49, 4, 3.28, -2.18, 0.04, 3.83, 3.27, -2.07, -0.16, 3.74, 3.31, -1.73, -0.36, 4.01, 3.13, -1.81, -0.3, 4.01, 3.19, -1.7, -0.41, 4.21, 3.09, -1.69, -0.52, 4.2, 3.05, -1.74, -2.41, -4.19, 5.05, -0.4, -0.93, 3.3, 1.57, 1.05, -0.94, 3.73, 1.83, 0.36, -0.9, 3.86, 1.6, 0.45, -0.83, 3.79],
    'PDB_HB': [1642356.3, 1709132, 1775109.9, 1737534.9, 1748731.2, 1816268.2, 1881849.7, 1840786.2, 1855580.2, 1929018.7, 1993632.3, 1948852.2, 1958395.5, 2036816.6, 2103598.1, 2057687.6, 2058584.9, 2137385.6, 2207343.6, 2161552.5, 2158040, 2238704.4, 2312843.5, 2272929.2, 2264721, 2355445, 2429260.6, 2385186.8, 2378146.4, 2473512.9, 2552296.9, 2508971.9, 2498697.5, 2603852.6, 2684332.2, 2638969.6, 2625180.5, 2735414.1, 2818812.7, 2769748.1, 2703027.1, 2589769.2, 2720481.3, 2709721.7, 2684445.5, 2773065.2, 2816492.1, 2846056.9, 2819332.7, 2924441.4, 2977924.9, 2988548.9, 2961539.6, 3075776.6, 3124992.9, 3139084.5, 3113019, 3230971.1],
    'PDB_HK': [1603771.9, 1704509.9, 1786196.6, 1769654.7, 1834355.1, 1928233, 2053745.4, 2015392.5, 2061338.3, 2162036.9, 2223641.6, 2168687.7, 2235288.5, 2342589.5, 2491158.5, 2477097.5, 2506300.2, 2618947.3, 2746762.4, 2697695.4, 2728180.7, 2867948.4, 2990645, 2939558.7, 2929269, 3073536.7, 3205019, 3193903.8, 3228172.2, 3366787.3, 3504138.5, 3490727.7, 3510363.1, 3686836.4, 3842343, 3799213.5, 3782618.3, 3964074.7, 4067358, 4018606.2, 3923347.9, 3690742.2, 3897851.9, 3931411.2, 3972933, 4178022, 4327383.9, 4498412.5, 4508566.3, 4897889, 5066863.4, 5114771.2, 5071483.2, 5223368, 5294981.9, 5302543.6, 5288494.8, 5536495.2]
}

df_pdb = pd.DataFrame(pdb_data)
df_pdb['Period'] = df_pdb['Tahun'].astype(str) + ' Q' + df_pdb['Triwulan']
df_pdb['Date'] = pd.to_datetime(df_pdb['Tahun'].astype(str) + '-' + 
                               df_pdb['Triwulan'].map({'I':'01', 'II':'04', 'III':'07', 'IV':'10'}) + '-01')

# Compact Header with logos
col1, col2, col3 = st.columns([1, 3, 1])

with col1:
    # AIG Logo - Smaller size
    st.markdown("""
    <div class="logo-container">
        <img src="aig_logo.png" alt="AIG Logo" style="width: 70px; height: 70px; object-fit: contain;">
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Compact title and subtitle
    st.markdown('<div class="logo-title">ACTIONABLE INSIGHTS</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Generate wisdom from fingertip</div>', unsafe_allow_html=True)

with col3:
    # BPS Logo - Smaller size
    st.markdown("""
    <div class="logo-container">
        <img src="bps_logo.png" alt="BPS Logo" style="width: 85px; height: 70px; object-fit: contain;">
    </div>
    """, unsafe_allow_html=True)

# Main Navigation Menu - more compact
main_tabs_list = ['Neraca Nasional', 'Indeks Harga', 'Ekspor-Impor', 'APBN', 'Ketenagakerjaan', 'Kemiskinan', 'IPM']

try:
    default_main_index = main_tabs_list.index(st.session_state.main_tab)
except ValueError:
    default_main_index = 0

# Compact option menu
selected_main_tab = option_menu(
    menu_title=None,
    options=main_tabs_list,
    icons=None,
    menu_icon=None,
    default_index=default_main_index,
    orientation="horizontal",
    styles={
        "container": {"padding": "0px !important", "background-color": "white", "margin-bottom": "0.5rem", "flex-wrap": "nowrap"},
        "nav-link": {
            "font-size": "14px", 
            "font-weight": "bold",
            "color": "#333",
            "background-color": "#f0f0f0", 
            "text-align": "center", 
            "padding": "15px 10px",
            "margin":"0px 2px !important",
            "border-radius": "0px !important",
            "border-bottom": "5px solid #0070c0",
            "transition": "background-color 0.2s, color 0.2s, border-color 0.2s",
            "white-space": "nowrap"
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

# Main content area - compact layout
st.markdown('<div class="chart-container">', unsafe_allow_html=True)

# Display content based on selected main tab
if st.session_state.main_tab == 'Neraca Nasional':
    
    # Create single combined chart
    chart_col, insight_col = st.columns([2.5, 1])
    
    with chart_col:
        fig = go.Figure()
        
        # Filter data yang valid
        df_valid = df_pdb[df_pdb['y_o_y'].notna()].copy()
        
        # Bar chart untuk PDB Harga Konstan (background)
        colors = ['lightcoral' if x < 0 else 'lightblue' if x < 3 else 'lightgreen' if x < 5 else 'darkgreen' 
                 for x in df_valid['y_o_y']]
        
        fig.add_trace(go.Bar(
            x=df_valid['Period'],
            y=df_valid['PDB_HK']/1000,  # Konversi ke triliun
            name='PDB Harga Konstan (Triliun Rp)',
            marker_color=colors,
            opacity=0.6,
            yaxis='y1',
            hovertemplate='<b>%{x}</b><br>PDB HK: %{y:.0f}T Rp<extra></extra>'
        ))
        
        # Y-o-Y line (overlay on same x-axis)
        fig.add_trace(go.Scatter(
            x=df_valid['Period'],  # Pakai Period yang sama dengan bar
            y=df_valid['y_o_y'],
            name='Pertumbuhan Y-o-Y (%)',
            line=dict(color='red', width=3),
            marker=dict(size=6, color='red'),
            yaxis='y2',
            hovertemplate='<b>%{x}</b><br>Y-o-Y: %{y:.2f}%<extra></extra>'
        ))
        
        # Q-to-Q line (overlay on same x-axis)
        df_qtq_valid = df_valid[df_valid['q_to_q'].notna()]
        fig.add_trace(go.Scatter(
            x=df_qtq_valid['Period'],  # Pakai Period yang sama dengan bar
            y=df_qtq_valid['q_to_q'],
            name='Pertumbuhan Q-to-Q (%)',
            line=dict(color='navy', width=2, dash='dot'),
            marker=dict(size=4, color='navy'),
            yaxis='y2',
            hovertemplate='<b>%{x}</b><br>Q-to-Q: %{y:.2f}%<extra></extra>'
        ))
        
        # Add shaded areas untuk periode khusus
        fig.add_vrect(
            x0="2020-I", x1="2020-IV",
            fillcolor="red", opacity=0.1,
            line_width=0,
        )
        fig.add_vrect(
            x0="2021-I", x1="2021-IV",
            fillcolor="green", opacity=0.1,
            line_width=0,
        )
        
        # Zero line reference
        fig.add_hline(y=0, line_dash="solid", line_color="gray", line_width=1, opacity=0.5, yref='y2')
        
        fig.update_layout(
            title='Pertumbuhan & Skala Ekonomi Indonesia',
            xaxis_title='Periode',
            height=400,
            plot_bgcolor='white',
            hovermode='x unified',
            yaxis=dict(
                title='PDB Harga Konstan (Triliun Rp)',
                side='left',
                showgrid=True,
                gridcolor='lightgray',
                range=[0, 6000]
            ),
            yaxis2=dict(
                title='Pertumbuhan (%)',
                side='right',
                overlaying='y',
                showgrid=False,
                zeroline=True,
                zerolinecolor='gray',
                range=[-8, 8]
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(size=10)
            ),
            margin=dict(l=50, r=50, t=60, b=40)
        )
        
        # Update x-axis
        fig.update_xaxes(
            tickangle=45,
            tickmode='array',
            tickvals=df_valid['Period'][::6],  # Show every 6th label
            showgrid=True,
            gridcolor='lightgray'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    with insight_col:
        st.markdown('<div class="insight-section">', unsafe_allow_html=True)
        st.markdown("#### Analysis:")
        st.markdown("• **Economic Scale**: PDB riil 1.8T→5.5T Rp (2011-2024)")
        st.markdown("• **2020 Crisis**: Kontraksi terdalam -5.32% Q2")
        st.markdown("• **V-Recovery**: Cepat ke 7.08% Q2 2021")
        st.markdown("• **Stable Growth**: 5-5.2% sejak 2022")
        st.markdown("• **Color Code**: Merah=kontraksi, Biru=<3%, Hijau=sehat")
        st.markdown('</div>', unsafe_allow_html=True)
    
        

elif st.session_state.main_tab == 'Indeks Harga':
    chart_col, insight_col = st.columns([2.5, 1])
    sample_data = pd.DataFrame({
        'Period': ['2020', '2021', '2022', '2023'],
        'Value': np.random.uniform(-1, 5, 4)
    })
    title = "Inflasi"
    
    fig_sample = px.line(sample_data, x='Period', y='Value', title=title, markers=True)
    fig_sample.update_traces(line=dict(color='teal', width=2), marker=dict(size=5, color='teal'))
    fig_sample.update_layout(height=320, plot_bgcolor='white', margin=dict(l=30, r=30, t=40, b=30))
    fig_sample.update_xaxes(type='category')
    
    with chart_col:
        st.plotly_chart(fig_sample, use_container_width=True)
        
    with insight_col:
        st.markdown('<div class="insight-section">', unsafe_allow_html=True)
        st.markdown("#### Insight:")
        st.markdown("• ....")
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.main_tab == 'Ekspor-Impor':
    chart_col, insight_col = st.columns([2.5, 1])
    
    # Data Ekspor dan Impor per tahun 2020-2023 (random)
    np.random.seed(42)  # Agar konsisten setiap reload
    sample_data = pd.DataFrame({
        'Tahun': ['2020', '2021', '2022', '2023'],
        'Ekspor': np.random.uniform(180000, 230000, 4),  # dalam juta USD
        'Impor': np.random.uniform(160000, 200000, 4)
    })
    
    # Hitung kontribusi terhadap total perdagangan
    sample_data['Total'] = sample_data['Ekspor'] + sample_data['Impor']
    sample_data['Ekspor_Kontribusi'] = (sample_data['Ekspor'] / sample_data['Total']) * 100
    sample_data['Impor_Kontribusi'] = (sample_data['Impor'] / sample_data['Total']) * 100
    
    title = "Kontribusi Ekspor dan Impor Migas & Non Migas"
    
    # Membuat bar chart
    fig_sample = go.Figure()
    
    # Bar Ekspor
    fig_sample.add_trace(go.Bar(
        x=sample_data['Tahun'], 
        y=sample_data['Ekspor'],
        name='Ekspor',
        marker_color='teal',
        text=sample_data['Ekspor_Kontribusi'].apply(lambda x: f'{x:.1f}%'),
        textposition='outside',
        textfont=dict(size=10, color='teal'),
        hovertemplate='<b>%{x}</b><br>Nilai: %{y:,.0f} Juta USD<extra></extra>'
    ))
    
    # Bar Impor
    fig_sample.add_trace(go.Bar(
        x=sample_data['Tahun'], 
        y=sample_data['Impor'],
        name='Impor',
        marker_color='orange',
        text=sample_data['Impor_Kontribusi'].apply(lambda x: f'{x:.1f}%'),
        textposition='outside',
        textfont=dict(size=10, color='orange'),
        hovertemplate='<b>%{x}</b><br>Nilai: %{y:,.0f} Juta USD<extra></extra>'
    ))
    
    fig_sample.update_layout(
        title=title,
        height=320, 
        plot_bgcolor='white', 
        margin=dict(l=30, r=30, t=50, b=30),
        xaxis_title="Tahun",
        yaxis_title="Nilai (Juta USD)",
        barmode='group',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    with chart_col:
        st.plotly_chart(fig_sample, use_container_width=True)
        
    with insight_col:
        st.markdown('<div class="insight-section">', unsafe_allow_html=True)
        st.markdown("#### Insight:")
        latest = sample_data.iloc[-1]
        st.markdown(f"•.....")
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.main_tab == 'APBN':
    chart_col, insight_col = st.columns([2.5, 1])
    sample_data = pd.DataFrame({
        'Period': ['2020', '2021', '2022', '2023'],
        'Value': np.random.uniform(500, 1500, 4)
    })
    title = "Belanja Pegawai"
    
    fig_sample = px.line(sample_data, x='Period', y='Value', title=title, markers=True)
    fig_sample.update_traces(line=dict(color='teal', width=2), marker=dict(size=5, color='teal'))
    fig_sample.update_layout(height=320, plot_bgcolor='white', margin=dict(l=30, r=30, t=40, b=30))
    fig_sample.update_xaxes(type='category')
    
    with chart_col:
        st.plotly_chart(fig_sample, use_container_width=True)
        
    with insight_col:
        st.markdown('<div class="insight-section">', unsafe_allow_html=True)
        st.markdown("#### Insight:")
        st.markdown("• ....")
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.main_tab == 'Ketenagakerjaan':
    chart_col, insight_col = st.columns([2.5, 1])
    sample_data = pd.DataFrame({
        'Period': [2020, 2021, 2022, 2023],
        'Value': np.random.uniform(3, 7, 4)
    })
    title = "Tingkat Pengangguran Terbuka"
    
    fig_sample = px.line(sample_data, x='Period', y='Value', title=title, markers=True)
    fig_sample.update_traces(line=dict(color='teal', width=2), marker=dict(size=5, color='teal'))
    fig_sample.update_layout(height=320, plot_bgcolor='white', margin=dict(l=30, r=30, t=40, b=30))
    fig_sample.update_xaxes(type='category')
    
    with chart_col:
        st.plotly_chart(fig_sample, use_container_width=True)
        
    with insight_col:
        st.markdown('<div class="insight-section">', unsafe_allow_html=True)
        st.markdown("#### Insight:")
        st.markdown("• .....")
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.main_tab == 'Kemiskinan':
    # Data Kemiskinan Indonesia
    kemiskinan_data = {
        'Tahun': [2011, 2011, 2012, 2012, 2013, 2013, 2014, 2014, 2015, 2015, 2016, 2016, 2017, 2017, 2018, 2018, 2019, 2019, 2020, 2020, 2021, 2021, 2022, 2022, 2023, 2024, 2024],
        'Semester': ['Maret', 'September', 'Maret', 'September', 'Maret', 'September', 'Maret', 'September', 'Maret', 'September', 'Maret', 'September', 'Maret', 'September', 'Maret', 'September', 'Maret', 'September', 'Maret', 'September', 'Maret', 'September', 'Maret', 'September', 'Maret', 'Maret', 'September'],
        'Jumlah_Miskin': [30.02, 29.89, 29.13, 28.59, 28.07, 28.55, 28.28, 27.73, 28.59, 28.51, 28.01, 27.76, 27.77, 26.58, 25.95, 25.67, 25.14, 24.79, 26.42, 27.55, 27.54, 26.5, 26.16, 26.36, 25.9, 25.22, 24.06],
        'Persentase_Miskin': [12.49, 12.36, 11.96, 11.66, 11.37, 11.47, 11.25, 10.96, 11.22, 11.13, 10.86, 10.7, 10.64, 10.12, 9.82, 9.66, 9.41, 9.22, 9.78, 10.19, 10.14, 9.71, 9.54, 9.57, 9.36, 9.03, 8.57],
        'Gini_Ratio': [0.41, 0.388, 0.41, 0.413, 0.413, 0.406, 0.406, 0.414, 0.408, 0.402, 0.397, 0.394, 0.393, 0.391, 0.389, 0.384, 0.382, 0.38, 0.381, 0.385, 0.384, 0.381, 0.384, 0.381, 0.388, 0.379, 0.381]
    }
    
    df_kemiskinan = pd.DataFrame(kemiskinan_data)
    df_kemiskinan['Period'] = df_kemiskinan['Tahun'].astype(str) + ' ' + df_kemiskinan['Semester']
    df_kemiskinan['Date'] = pd.to_datetime(df_kemiskinan['Tahun'].astype(str) + '-' + 
                                         df_kemiskinan['Semester'].map({'Maret':'03', 'September':'09'}) + '-01')
    
    # Create two charts side by side
    chart1_col, chart2_col, insight_col = st.columns([1.3, 1.3, 1])
    
    with chart1_col:
        # Chart 1: Dual axis - Poverty Rate & Number of Poor
        fig1 = go.Figure()
        
        # Bar chart untuk jumlah penduduk miskin
        colors = ['lightcoral' if x > 10 else 'gold' if x > 9 else 'lightgreen' 
                 for x in df_kemiskinan['Persentase_Miskin']]
        
        # fig1.add_trace(go.Bar(
        #     x=df_kemiskinan['Date'],
        #     y=df_kemiskinan['Jumlah_Miskin'],
        #     marker_color=colors,
        #     opacity=0.6,
        #     yaxis='y',
        #     hovertemplate='<b>%{text}</b><br>Jumlah: %{y:.1f} Juta Jiwa<extra></extra>',
        #     text=df_kemiskinan['Period']
        # ))
        
        # Line untuk persentase kemiskinan
        fig1.add_trace(go.Scatter(
            x=df_kemiskinan['Date'],
            y=df_kemiskinan['Persentase_Miskin'],
            line=dict(color='red', width=3),
            marker=dict(size=6, color='red'),
            yaxis='y2',
            hovertemplate='<b>%{text}</b><br>Persentase: %{y:.2f}%<extra></extra>',
            text=df_kemiskinan['Period']
        ))
        
        # Add shaded areas untuk periode khusus
        fig1.add_vrect(
            x0="2020-01-01", x1="2021-12-31",
            fillcolor="red", opacity=0.1,
            line_width=0,
        )
        
        fig1.update_layout(
            title='Kemiskinan Indonesia: Jumlah vs Persentase (2011-2024)',
            height=300,
            plot_bgcolor='white',
            hovermode='x unified',
            yaxis=dict(
                title='Jumlah Penduduk Miskin (Juta)',
                side='left',
                showgrid=True,
                gridcolor='lightgray',
                range=[20, 32]
            ),
            yaxis2=dict(
                title='Persentase (%)',
                side='right',
                overlaying='y',
                showgrid=False,
                range=[8, 14]
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(size=9)
            ),
            margin=dict(l=40, r=40, t=50, b=30)
        )
        
        fig1.update_xaxes(
            tickangle=45,
            tickmode='array',
            tickvals=df_kemiskinan['Date'][::4],  # Show every 4th label
            ticktext=[x.split()[0] + ' ' + x.split()[1][:3] for x in df_kemiskinan['Period'][::4]]
        )
        
        st.plotly_chart(fig1, use_container_width=True)
    
    with chart2_col:
        # Chart 2: Gini Ratio Trend with color coding
        fig2 = go.Figure()
        
        # Color coding untuk Gini Ratio
        gini_colors = ['darkred' if x >= 0.41 else 'red' if x >= 0.4 else 'orange' if x >= 0.385 else 'green' 
                      for x in df_kemiskinan['Gini_Ratio']]
        
        fig2.add_trace(go.Scatter(
            x=df_kemiskinan['Date'],
            y=df_kemiskinan['Gini_Ratio'],
            mode='lines+markers',
            name='Gini Ratio',
            line=dict(color='navy', width=2),
            marker=dict(size=8, color=gini_colors, line=dict(width=2, color='navy')),
            hovertemplate='<b>%{text}</b><br>Gini Ratio: %{y:.3f}<extra></extra>',
            text=df_kemiskinan['Period']
        ))
        
        # Add threshold lines
        fig2.add_hline(y=0.4, line_dash="dash", line_color="red", line_width=1, 
                      annotation_text="High Inequality (0.4)", annotation_position="right")
        fig2.add_hline(y=0.385, line_dash="dot", line_color="orange", line_width=1,
                      annotation_text="Moderate (0.385)", annotation_position="right")
        
        # Add trend area
        fig2.add_trace(go.Scatter(
            x=df_kemiskinan['Date'],
            y=df_kemiskinan['Gini_Ratio'],
            fill='tonexty',
            fillcolor='rgba(0,0,128,0.1)',
            line=dict(color='rgba(255,255,255,0)'),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        fig2.update_layout(
            title='Indeks Gini: Ketimpangan Distribusi Pendapatan',
            height=280,
            plot_bgcolor='white',
            yaxis=dict(
                title='Gini Ratio',
                showgrid=True,
                gridcolor='lightgray',
                range=[0.37, 0.42]
            ),
            margin=dict(l=40, r=40, t=50, b=30)
        )
        
        fig2.update_xaxes(
            tickangle=45,
            tickmode='array',
            tickvals=df_kemiskinan['Date'][::4],
            ticktext=[x.split()[0] + ' ' + x.split()[1][:3] for x in df_kemiskinan['Period'][::4]]
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    
    with insight_col:
        st.markdown('<div class="insight-section">', unsafe_allow_html=True)
        st.markdown("#### Insights:")
        st.markdown("• **COVID Impact**: Naik 9.78%→10.19% (2020)")
        st.markdown("• **Swift Recovery**: Kembali turun ke <10% (2021)")
        st.markdown("• **Gini Improvement**: 0.41→0.381 (ketimpangan turun)")
        st.markdown('</div>', unsafe_allow_html=True)

        

elif st.session_state.main_tab == 'IPM':
    # IPM Gender Data
    ipm_data = {
        'Tahun': [2020, 2021, 2022, 2023],
        'IPM_Laki_laki': [76.78, 77.03, 77.47, 77.96],
        'IPM_Perempuan': [70.14, 70.56, 71.31, 71.95]
    }
    df_ipm = pd.DataFrame(ipm_data)
    
    # Calculate gender gap
    df_ipm['Gender_Gap'] = df_ipm['IPM_Laki_laki'] - df_ipm['IPM_Perempuan']
    df_ipm['IPM_Total'] = (df_ipm['IPM_Laki_laki'] + df_ipm['IPM_Perempuan']) / 2
    
    chart_col, insight_col = st.columns([2.5, 1])
    
    with chart_col:
        # Create single chart
        fig_ipm = go.Figure()
        
        # Gender Gap - filled area between lines
        fig_ipm.add_trace(go.Scatter(
            x=df_ipm['Tahun'].tolist() + df_ipm['Tahun'].tolist()[::-1],
            y=df_ipm['IPM_Laki_laki'].tolist() + df_ipm['IPM_Perempuan'].tolist()[::-1],
            fill='toself',
            fillcolor='rgba(255,0,0,0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            name='Gender Gap',
            hoverinfo='skip',
            showlegend=True,
            legendrank=1 
        ))
        
        # IPM Laki-laki line
        fig_ipm.add_trace(go.Scatter(
            x=df_ipm['Tahun'],
            y=df_ipm['IPM_Laki_laki'],
            name='IPM Laki-laki',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=8, color='#1f77b4'),
            hovertemplate='<b>%{x}</b><br>IPM Laki-laki: %{y:.2f}<extra></extra>'
        ))
        
        # IPM Perempuan line
        fig_ipm.add_trace(go.Scatter(
            x=df_ipm['Tahun'],
            y=df_ipm['IPM_Perempuan'],
            name='IPM Perempuan',
            line=dict(color='#ff7f0e', width=3),
            marker=dict(size=8, color='#ff7f0e'),
            hovertemplate='<b>%{x}</b><br>IPM Perempuan: %{y:.2f}<extra></extra>'
        ))
        
        # Add invisible points for gender gap hover info at middle position
        fig_ipm.add_trace(go.Scatter(
            x=df_ipm['Tahun'],
            y=df_ipm['IPM_Total'],
            mode='markers',
            marker=dict(size=10, color='red', opacity=0),
            name='Gap Info',
            hovertemplate='<b>%{x}</b><br>Gender Gap: %{customdata:.2f} poin<extra></extra>',
            customdata=df_ipm['Gender_Gap'],
            showlegend=False,
            legendrank=1 
        ))
        
        # Add trend line for total IPM
        fig_ipm.add_trace(go.Scatter(
            x=df_ipm['Tahun'],
            y=df_ipm['IPM_Total'],
            name='IPM Rata-rata',
            line=dict(color='green', width=2, dash='dot'),
            marker=dict(size=6, color='green'),
            hovertemplate='<b>%{x}</b><br>IPM Rata-rata: %{y:.2f}<extra></extra>'
        ))
        
        fig_ipm.update_layout(
            title='Indeks Pembangunan Manusia Indonesia',
            height=350,
            plot_bgcolor='white',
            hovermode='x unified',
            yaxis=dict(
                title='Skor IPM',
                side='left',
                showgrid=True,
                gridcolor='lightgray',
                range=[68, 80]
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=0.95,
                xanchor="right",
                x=1,
                font=dict(size=10)
            ),
            margin=dict(l=50, r=50, t=60, b=40)
        )
        
        # Update x-axis
        fig_ipm.update_xaxes(
            title='Tahun',
            showgrid=True,
            gridcolor='lightgray',
            dtick=1
        )
        
        st.plotly_chart(fig_ipm, use_container_width=True)
        
    with insight_col:
        st.markdown('<div class="insight-section">', unsafe_allow_html=True)
        st.markdown("#### Insights:")
        st.markdown(f"• ....")
