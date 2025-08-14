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
    # Add visualization selector for Neraca Nasional
    st.markdown('<div class="viz-selector">', unsafe_allow_html=True)
    viz_option = st.selectbox(
        "Pilih Visualisasi:",
        ["📈 Time Series Trend Analysis", "📊 Dual-Axis Growth vs Scale", "🔥 Seasonal Heatmap Pattern"],
        key="neraca_viz_selector"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    chart_col, insight_col = st.columns([2.5, 1])
    
    if viz_option == "📈 Time Series Trend Analysis":
        # Chart 1: Multi-line time series dengan annotations
        with chart_col:
            fig = go.Figure()
            
            # Filter data yang valid
            df_valid = df_pdb[df_pdb['y_o_y'].notna()].copy()
            
            # Y-o-Y line (primary)
            fig.add_trace(go.Scatter(
                x=df_valid['Date'],
                y=df_valid['y_o_y'],
                name='Pertumbuhan Y-o-Y',
                line=dict(color='navy', width=3),
                marker=dict(size=6, color='navy'),
                hovertemplate='<b>%{text}</b><br>Y-o-Y: %{y:.2f}%<extra></extra>',
                text=df_valid['Period']
            ))
            
            # Q-to-Q line (secondary)
            df_qtq_valid = df_valid[df_valid['q_to_q'].notna()]
            fig.add_trace(go.Scatter(
                x=df_qtq_valid['Date'],
                y=df_qtq_valid['q_to_q'],
                name='Pertumbuhan Q-to-Q',
                line=dict(color='#0070c0', width=2, dash='dot'),
                marker=dict(size=4, color='#0070c0'),
                hovertemplate='<b>%{text}</b><br>Q-to-Q: %{y:.2f}%<extra></extra>',
                text=df_qtq_valid['Period']
            ))
            
            # Add shaded areas untuk periode khusus
            # Krisis 2020
            fig.add_vrect(
                x0="2020-01-01", x1="2020-12-31",
                fillcolor="red", opacity=0.1,
                line_width=0,
                annotation_text="Pandemi COVID-19",
                annotation_position="top left"
            )
            
            # Recovery period
            fig.add_vrect(
                x0="2021-01-01", x1="2021-12-31",
                fillcolor="green", opacity=0.1,
                line_width=0,
                annotation_text="Pemulihan Ekonomi",
                annotation_position="top left"
            )
            
            # Zero line reference
            fig.add_hline(y=0, line_dash="solid", line_color="gray", line_width=1, opacity=0.5)
            
            fig.update_layout(
                title='Analisis Tren Pertumbuhan Ekonomi Indonesia (2011-2024)',
                xaxis_title='Periode',
                yaxis_title='Pertumbuhan (%)',
                height=400,
                plot_bgcolor='white',
                hovermode='x unified',
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                margin=dict(l=50, r=50, t=80, b=50)
            )
            
            fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
            
            st.plotly_chart(fig, use_container_width=True)
            
        with insight_col:
            st.markdown('<div class="insight-section">', unsafe_allow_html=True)
            st.markdown("#### 🎯 Key Insights:")
            st.markdown("• **Krisis 2020**: Kontraksi terdalam -5.32% di Q2")
            st.markdown("• **Pemulihan V-Shape**: Recovery cepat mulai Q2 2021 (7.08%)")
            st.markdown("• **Stabilisasi**: Pertumbuhan 5-5.2% sejak 2022")
            st.markdown("• **Pola Musiman**: Q4 cenderung melambat, Q2-Q3 kuat")
            st.markdown("• **Volatilitas Q-to-Q**: Fluktuasi triwulanan normal")
            st.markdown("• **Target Tercapai**: Konsisten di atas 5% pasca-pandemi")
            st.markdown('</div>', unsafe_allow_html=True)
    
    elif viz_option == "📊 Dual-Axis Growth vs Scale":
        # Chart 2: Combination chart
        with chart_col:
            fig = go.Figure()
            
            df_valid = df_pdb[df_pdb['y_o_y'].notna()].copy()
            
            # Bar chart untuk PDB Harga Konstan
            colors = ['lightcoral' if x < 0 else 'lightblue' if x < 3 else 'lightgreen' if x < 5 else 'darkgreen' 
                     for x in df_valid['y_o_y']]
            
            fig.add_trace(go.Bar(
                x=df_valid['Period'],
                y=df_valid['PDB_HK']/1000,  # Konversi ke triliun
                name='PDB Harga Konstan',
                marker_color=colors,
                opacity=0.7,
                yaxis='y',
                hovertemplate='<b>%{x}</b><br>PDB HK: %{y:.0f}T Rp<extra></extra>'
            ))
            
            # Line chart untuk Y-o-Y growth
            fig.add_trace(go.Scatter(
                x=df_valid['Period'],
                y=df_valid['y_o_y'],
                name='Pertumbuhan Y-o-Y',
                line=dict(color='red', width=3),
                marker=dict(size=6, color='red'),
                yaxis='y2',
                hovertemplate='<b>%{x}</b><br>Growth: %{y:.2f}%<extra></extra>'
            ))
            
            fig.update_layout(
                title='Pertumbuhan Ekonomi vs Skala PDB Indonesia',
                xaxis_title='Periode',
                height=400,
                plot_bgcolor='white',
                hovermode='x unified',
                yaxis=dict(
                    title='PDB Harga Konstan (Triliun Rp)',
                    side='left',
                    showgrid=True,
                    gridcolor='lightgray'
                ),
                yaxis2=dict(
                    title='Pertumbuhan Y-o-Y (%)',
                    side='right',
                    overlaying='y',
                    showgrid=False,
                    zeroline=True,
                    zerolinecolor='gray'
                ),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                margin=dict(l=60, r=60, t=80, b=80)
            )
            
            # Update x-axis untuk menampilkan label yang lebih baik
            fig.update_xaxes(
                tickangle=45,
                tickmode='array',
                tickvals=df_valid['Period'][::4],  # Show every 4th label
                showgrid=True,
                gridcolor='lightgray'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        with insight_col:
            st.markdown('<div class="insight-section">', unsafe_allow_html=True)
            st.markdown("#### 📊 Scale & Growth:")
            st.markdown("• **Ukuran Ekonomi**: PDB riil naik dari 1.8T (2011) ke 5.5T Rp (2024)")
            st.markdown("• **Growth-Scale Paradox**: Semakin besar ekonomi, pertumbuhan cenderung stabil")
            st.markdown("• **Momentum Expansion**: Periode hijau tua = pertumbuhan >5%")
            st.markdown("• **Crisis Impact**: Merah = kontraksi 2020 sangat terlihat")
            st.markdown("• **Recovery Pattern**: Bar biru muda = pemulihan bertahap")
            st.markdown("• **Sustainable Growth**: Target 5% realistis untuk ekonomi sebesar ini")
            st.markdown('</div>', unsafe_allow_html=True)
    
    elif viz_option == "🔥 Seasonal Heatmap Pattern":
        # Chart 3: Seasonal heatmap
        with chart_col:
            # Prepare data untuk heatmap
            df_valid = df_pdb[df_pdb['y_o_y'].notna()].copy()
            
            # Create pivot table
            heatmap_data = df_valid.pivot(index='Tahun', columns='Triwulan', values='y_o_y')
            heatmap_data = heatmap_data[['I', 'II', 'III', 'IV']]  # Ensure correct order
            
            # Create custom colorscale
            colorscale = [
                [0.0, '#d73027'],    # Red for negative/low growth
                [0.2, '#f46d43'],    # Orange-red
                [0.4, '#fdae61'],    # Orange
                [0.6, '#fee08b'],    # Yellow
                [0.8, '#d9ef8b'],    # Light green
                [1.0, '#66bd63']     # Green for high growth
            ]
            
            fig = go.Figure(data=go.Heatmap(
                z=heatmap_data.values,
                x=['Q1', 'Q2', 'Q3', 'Q4'],
                y=heatmap_data.index,
                colorscale=colorscale,
                zmid=3,  # Center around 3%
                colorbar=dict(
                    title="Pertumbuhan Y-o-Y (%)",
                    titleside="right",
                    tickmode="linear",
                    tick0=-6,
                    dtick=2
                ),
                hovertemplate='<b>%{y} %{x}</b><br>Growth: %{z:.2f}%<extra></extra>',
                text=heatmap_data.round(2),
                texttemplate="%{text}%",
                textfont={"size": 10},
                showscale=True
            ))
            
            # Add annotations untuk nilai-nilai penting
            annotations = []
            for i, year in enumerate(heatmap_data.index):
                for j, quarter in enumerate(['I', 'II', 'III', 'IV']):
                    value = heatmap_data.loc[year, quarter]
                    if not pd.isna(value):
                        color = 'white' if abs(value) > 4 else 'black'
                        annotations.append(
                            dict(
                                x=j, y=i,
                                text=f'{value:.1f}%',
                                showarrow=False,
                                font=dict(color=color, size=9, family="Arial Black")
                            )
                        )
            
            fig.update_layout(
                title='Pola Musiman Pertumbuhan Ekonomi Indonesia (2011-2024)',
                xaxis_title='Triwulan',
                yaxis_title='Tahun',
                height=500,
                plot_bgcolor='white',
                annotations=annotations,
                margin=dict(l=60, r=100, t=80, b=50)
            )
            
            fig.update_xaxes(side='top')
            fig.update_yaxes(autorange='reversed')  # Latest year on top
            
            st.plotly_chart(fig, use_container_width=True)
            
        with insight_col:
            st.markdown('<div class="insight-section">', unsafe_allow_html=True)
            st.markdown("#### 🔥 Seasonal Patterns:")
            st.markdown("• **Q2 Strength**: Konsisten hijau, didukung konsumsi & ekspor")
            st.markdown("• **Q4 Weakness**: Pola kuning-oranye, seasonal adjustment")
            st.markdown("• **2020 Anomaly**: Merah terang Q2-Q3, lockdown effect")
            st.markdown("• **Recovery 2021**: Hijau terang Q2, stimulus fiskal")
            st.markdown("• **Normalisasi**: 2022-2024 kembali hijau stabil")
            st.markdown("• **Q1 Pattern**: Cenderung moderat, new year effect")
            st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.main_tab == 'Indeks Harga':
    chart_col, insight_col = st.columns([2.5, 1])
    sample_data = pd.DataFrame({
        'Period': pd.date_range('2023-01', periods=12, freq='M').strftime('%Y-%m'),
        'Value': np.random.uniform(-1, 5, 12)
    })
    title = "Inflasi y-o-y (%)"
    
    fig_sample = px.line(sample_data, x='Period', y='Value', title=title, markers=True)
    fig_sample.update_traces(line=dict(color='teal', width=2), marker=dict(size=5, color='teal'))
    fig_sample.update_layout(height=320, plot_bgcolor='white', margin=dict(l=30, r=30, t=40, b=30))
    
    with chart_col:
        st.plotly_chart(fig_sample, use_container_width=True)
        
    with insight_col:
        st.markdown('<div class="insight-section">', unsafe_allow_html=True)
        st.markdown("#### Insight:")
        st.markdown("• Inflasi masih dalam target Bank Indonesia 2-4%")
        st.markdown("• Tekanan inflasi inti relatif terkendali") 
        st.markdown("• Volatile food prices menjadi perhatian utama")
        st.markdown("• Kebijakan moneter masih akomodatif")
        st.markdown("• Perlu monitoring harga komoditas global")
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.main_tab == 'Ekspor-Impor':
    chart_col, insight_col = st.columns([2.5, 1])
    sample_data = pd.DataFrame({
        'Period': pd.date_range('2023-01', periods=12, freq='M').strftime('%Y-%m'),
        'Value': np.random.uniform(10000, 30000, 12)
    })
    title = "Nilai ekspor (migas-non migas) (Juta USD)"
    
    fig_sample = px.line(sample_data, x='Period', y='Value', title=title, markers=True)
    fig_sample.update_traces(line=dict(color='teal', width=2), marker=dict(size=5, color='teal'))
    fig_sample.update_layout(height=320, plot_bgcolor='white', margin=dict(l=30, r=30, t=40, b=30))
    
    with chart_col:
        st.plotly_chart(fig_sample, use_container_width=True)
        
    with insight_col:
        st.markdown('<div class="insight-section">', unsafe_allow_html=True)
        st.markdown("#### Insight:")
        st.markdown("• Nilai ekspor menunjukkan tren positif year-on-year")
        st.markdown("• Komoditas unggulan masih mendominasi ekspor")
        st.markdown("• Impor bahan baku industri terus meningkat") 
        st.markdown("• Neraca perdagangan masih surplus namun menyempit")
        st.markdown("• Diversifikasi pasar ekspor perlu diperkuat")
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.main_tab == 'APBN':
    chart_col, insight_col = st.columns([2.5, 1])
    sample_data = pd.DataFrame({
        'Period': [f"2023 Q{i}" for i in range(1, 5)] + [f"2024 Q{i}" for i in range(1, 5)],
        'Value': np.random.uniform(500, 1500, 8)
    })
    title = "Belanja Pegawai (Triliun Rupiah)"
    
    fig_sample = px.line(sample_data, x='Period', y='Value', title=title, markers=True)
    fig_sample.update_traces(line=dict(color='teal', width=2), marker=dict(size=5, color='teal'))
    fig_sample.update_layout(height=320, plot_bgcolor='white', margin=dict(l=30, r=30, t=40, b=30))
    
    with chart_col:
        st.plotly_chart(fig_sample, use_container_width=True)
        
    with insight_col:
        st.markdown('<div class="insight-section">', unsafe_allow_html=True)
        st.markdown("#### Insight:")
        st.markdown("• Belanja pegawai tumbuh seiring dengan reformasi birokrasi")
        st.markdown("• Efisiensi anggaran masih dapat dioptimalkan")
        st.markdown("• Alokasi untuk infrastruktur dan SDM prioritas")
        st.markdown("• Fiscal sustainability tetap terjaga")
        st.markdown("• Ruang fiskal masih tersedia untuk stimulus")
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.main_tab == 'Ketenagakerjaan':
    chart_col, insight_col = st.columns([2.5, 1])
    sample_data = pd.DataFrame({
        'Period': ['Agu 2022', 'Feb 2023', 'Agu 2023', 'Feb 2024'],
        'Value': np.random.uniform(3, 7, 4)
    })
    title = "TPT (%)"
    
    fig_sample = px.line(sample_data, x='Period', y='Value', title=title, markers=True)
    fig_sample.update_traces(line=dict(color='teal', width=2), marker=dict(size=5, color='teal'))
    fig_sample.update_layout(height=320, plot_bgcolor='white', margin=dict(l=30, r=30, t=40, b=30))
    
    with chart_col:
        st.plotly_chart(fig_sample, use_container_width=True)
        
    with insight_col:
        st.markdown('<div class="insight-section">', unsafe_allow_html=True)
        st.markdown("#### Insight:")
        st.markdown("• Tingkat Pengangguran Terbuka menunjukkan tren menurun")
        st.markdown("• Job creation di sektor formal masih terbatas")
        st.markdown("• Skills mismatch menjadi tantangan struktural")
        st.markdown("• Program pelatihan kerja perlu diperkuat")
        st.markdown("• Digitalisasi ekonomi membuka peluang kerja baru")
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.main_tab == 'Kemiskinan':
    chart_col, insight_col = st.columns([2.5, 1])
    sample_data = pd.DataFrame({
        'Period': ['Mar 2022', 'Sep 2022', 'Mar 2023', 'Sep 2023'],
        'Value': np.random.uniform(9, 11, 4)
    })
    title = "Persentase penduduk miskin (%)"
    
    fig_sample = px.line(sample_data, x='Period', y='Value', title=title, markers=True)
    fig_sample.update_traces(line=dict(color='teal', width=2), marker=dict(size=5, color='teal'))
    fig_sample.update_layout(height=320, plot_bgcolor='white', margin=dict(l=30, r=30, t=40, b=30))
    
    with chart_col:
        st.plotly_chart(fig_sample, use_container_width=True)
        
    with insight_col:
        st.markdown('<div class="insight-section">', unsafe_allow_html=True)
        st.markdown("#### Insight:")
        st.markdown("• Angka kemiskinan menunjukkan tren penurunan gradual")
        st.markdown("• Kesenjangan urban-rural masih signifikan")
        st.markdown("• Program bantuan sosial efektif mengurangi kemiskinan")
        st.markdown("• Pemberdayaan ekonomi mikro perlu diperkuat")
        st.markdown("• Investasi SDM kunci pengentasan kemiskinan jangka panjang")
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.main_tab == 'IPM':
    chart_col, insight_col = st.columns([2.5, 1])
    sample_data = pd.DataFrame({
        'Period': [str(y) for y in range(2020, 2024)],
        'Value': np.random.uniform(70, 75, 4)
    })
    title = "IPM"
    
    fig_sample = px.line(sample_data, x='Period', y='Value', title=title, markers=True)
    fig_sample.update_traces(line=dict(color='teal', width=2), marker=dict(size=5, color='teal'))
    fig_sample.update_layout(height=320, plot_bgcolor='white', margin=dict(l=30, r=30, t=40, b=30))
    
    with chart_col:
        st.plotly_chart(fig_sample, use_container_width=True)
        
    with insight_col:
        st.markdown('<div class="insight-section">', unsafe_allow_html=True)
        st.markdown("#### Insight:")
        st.markdown("• Indeks Pembangunan Manusia terus mengalami peningkatan")
        st.markdown("• Komponen pendidikan menunjukkan progress signifikan")
        st.markdown("• Angka harapan hidup terus membaik")
        st.markdown("• Kesenjangan IPM antar daerah masih perlu perhatian")
        st.markdown("• Investasi kesehatan dan pendidikan harus berkelanjutan")
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
