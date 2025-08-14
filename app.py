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
    # Create 3 visualizations in compact layout
    
    # Chart 1: Time Series Analysis (Top)
    st.markdown("#### 📈 Tren Pertumbuhan Ekonomi Indonesia")
    fig1 = go.Figure()
    
    # Filter data yang valid
    df_valid = df_pdb[df_pdb['y_o_y'].notna()].copy()
    
    # Y-o-Y line (primary)
    fig1.add_trace(go.Scatter(
        x=df_valid['Date'],
        y=df_valid['y_o_y'],
        name='Y-o-Y Growth',
        line=dict(color='navy', width=2.5),
        marker=dict(size=4, color='navy'),
        hovertemplate='<b>%{text}</b><br>Y-o-Y: %{y:.2f}%<extra></extra>',
        text=df_valid['Period']
    ))
    
    # Q-to-Q line (secondary)
    df_qtq_valid = df_valid[df_valid['q_to_q'].notna()]
    fig1.add_trace(go.Scatter(
        x=df_qtq_valid['Date'],
        y=df_qtq_valid['q_to_q'],
        name='Q-to-Q Growth',
        line=dict(color='#0070c0', width=2, dash='dot'),
        marker=dict(size=3, color='#0070c0'),
        hovertemplate='<b>%{text}</b><br>Q-to-Q: %{y:.2f}%<extra></extra>',
        text=df_qtq_valid['Period']
    ))
    
    # Add shaded areas untuk periode khusus
    fig1.add_vrect(x0="2020-01-01", x1="2020-12-31", fillcolor="red", opacity=0.1, line_width=0)
    fig1.add_vrect(x0="2021-01-01", x1="2021-12-31", fillcolor="green", opacity=0.1, line_width=0)
    
    # Zero line reference
    fig1.add_hline(y=0, line_dash="solid", line_color="gray", line_width=1, opacity=0.5)
    
    fig1.update_layout(
        height=200,  # Compact height
        plot_bgcolor='white',
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=40, t=30, b=30),
        showlegend=True
    )
    
    fig1.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray', title="")
    fig1.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray', title="Growth (%)")
    
    st.plotly_chart(fig1, use_container_width=True)
    
    # Create two columns for remaining charts
    col1, col2 = st.columns(2)
    
    # Chart 2: Dual-Axis Growth vs Scale (Left)
    with col1:
        st.markdown("#### 📊 Scale vs Growth")
        fig2 = go.Figure()
        
        # Bar chart untuk PDB Harga Konstan
        colors = ['lightcoral' if x < 0 else 'lightblue' if x < 3 else 'lightgreen' if x < 5 else 'darkgreen' 
                 for x in df_valid['y_o_y']]
        
        fig2.add_trace(go.Bar(
            x=df_valid['Period'][::2],  # Show every 2nd period
            y=(df_valid['PDB_HK']/1000)[::2],  # Konversi ke triliun, every 2nd
            name='PDB HK (T Rp)',
            marker_color=[colors[i] for i in range(0, len(colors), 2)],
            opacity=0.7,
            yaxis='y',
            hovertemplate='<b>%{x}</b><br>PDB HK: %{y:.0f}T Rp<extra></extra>'
        ))
        
        # Line chart untuk Y-o-Y growth
        fig2.add_trace(go.Scatter(
            x=df_valid['Period'],
            y=df_valid['y_o_y'],
            name='Y-o-Y Growth',
            line=dict(color='red', width=2),
            marker=dict(size=3, color='red'),
            yaxis='y2',
            hovertemplate='<b>%{x}</b><br>Growth: %{y:.2f}%<extra></extra>'
        ))
        
        fig2.update_layout(
            height=220,  # Compact height
            plot_bgcolor='white',
            hovermode='x unified',
            yaxis=dict(title='PDB (T Rp)', side='left', showgrid=True, gridcolor='lightgray'),
            yaxis2=dict(title='Growth (%)', side='right', overlaying='y', showgrid=False, zeroline=True),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
            margin=dict(l=40, r=40, t=40, b=40)
        )
        
        fig2.update_xaxes(tickangle=45, tickmode='array', tickvals=df_valid['Period'][::8])
        
        st.plotly_chart(fig2, use_container_width=True)
    
    # Chart 3: Seasonal Heatmap (Right) - Fixed
    with col2:
        st.markdown("#### 🔥 Pola Musiman")
        
        # Create heatmap data manually to avoid pivot errors
        df_valid = df_pdb[df_pdb['y_o_y'].notna()].copy()
        
        # Create matrix manually
        years = sorted(df_valid['Tahun'].unique())
        quarters = ['I', 'II', 'III', 'IV']
        
        z_data = []
        y_labels = []
        
        for year in years:
            row_data = []
            year_data = df_valid[df_valid['Tahun'] == year]
            
            for quarter in quarters:
                quarter_data = year_data[year_data['Triwulan'] == quarter]
                if len(quarter_data) > 0:
                    value = quarter_data['y_o_y'].iloc[0]
                    row_data.append(value)
                else:
                    row_data.append(None)
            
            # Only add row if it has at least one valid value
            if any(x is not None for x in row_data):
                z_data.append(row_data)
                y_labels.append(str(year))
        
        fig3 = go.Figure(data=go.Heatmap(
            z=z_data,
            x=['Q1', 'Q2', 'Q3', 'Q4'],
            y=y_labels,
            colorscale=[
                [0.0, '#d73027'], [0.2, '#f46d43'], [0.4, '#fdae61'], 
                [0.6, '#fee08b'], [0.8, '#d9ef8b'], [1.0, '#66bd63']
            ],
            zmid=3,
            colorbar=dict(title="Growth (%)", titleside="right", len=0.7),
            hovertemplate='<b>%{y} %{x}</b><br>Growth: %{z:.2f}%<extra></extra>',
            showscale=True
        ))
        
        fig3.update_layout(
            height=220,  # Compact height
            plot_bgcolor='white',
            margin=dict(l=40, r=60, t=40, b=40),
            yaxis=dict(autorange='reversed')  # Latest year on top
        )
        
        fig3.update_xaxes(side='top')
        
        st.plotly_chart(fig3, use_container_width=True)
    
    # Compact insights section at bottom
    st.markdown("#### 🎯 Key Insights")
    insight_cols = st.columns(3)
    
    with insight_cols[0]:
        st.markdown("**Tren & Recovery:**")
        st.markdown("• Krisis 2020: -5.32% di Q2")
        st.markdown("• V-shape recovery 2021")
        st.markdown("• Stabilisasi 5%+ sejak 2022")
    
    with insight_cols[1]:
        st.markdown("**Scale & Growth:**")
        st.markdown("• PDB riil: 1.8T→5.5T Rp")
        st.markdown("• Ekonomi besar = growth stabil")
        st.markdown("• Target 5% sustainable")
    
    with insight_cols[2]:
        st.markdown("**Pola Musiman:**")
        st.markdown("• Q2 konsisten kuat (hijau)")
        st.markdown("• Q4 cenderung melambat")
        st.markdown("• 2020 anomaly sangat jelas")

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
