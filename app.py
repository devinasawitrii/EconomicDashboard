import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

# --- Setup halaman ---
st.set_page_config(page_title="Actionable Insights", layout="wide")

# Inisialisasi state untuk tab
if 'main_tab' not in st.session_state:
    st.session_state.main_tab = 'Neraca Nasional'

# Navigasi horizontal
main_tabs_list = ['Neraca Nasional', 'Indeks Harga', 'Ekspor-Impor', 'APBN', 'Ketenagakerjaan', 'Kemiskinan', 'IPM']

selected_main_tab = option_menu(
    menu_title=None,
    options=main_tabs_list,
    default_index=main_tabs_list.index(st.session_state.main_tab),
    orientation="horizontal",
    styles={
        "container": {"padding": "0px !important", "background-color": "white", "margin-bottom": "0.5rem"},
        "nav-link": {
            "font-size": "14px",
            "font-weight": "bold",
            "color": "#333",
            "background-color": "#f0f0f0",
            "text-align": "center",
            "padding": "15px 10px",
            "margin": "0px 2px !important",
            "border-radius": "0px !important",
            "border-bottom": "5px solid #0070c0",
        },
        "nav-link-selected": {
            "background-color": "#0070c0",
            "color": "white",
            "border-bottom": "5px solid navy"
        }
    }
)

# Update tab di session state dan rerun app jika berubah
if selected_main_tab != st.session_state.main_tab:
    st.session_state.main_tab = selected_main_tab
    st.experimental_rerun()

# Judul utama
st.title("Actionable Insights")

if st.session_state.main_tab == 'Neraca Nasional':
    # Load data CSV
    try:
        df = pd.read_csv('pdb_growth.csv')

        # Cek kolom wajib
        expected_cols = {'Tahun', 'Triwulan', 'y-o-y'}
        if not expected_cols.issubset(df.columns):
            st.error(f"CSV harus mengandung kolom: {expected_cols}")
        else:
            # Buat kolom Periode: "2020 Q1"
            df['Periode'] = df['Tahun'].astype(str) + " Q" + df['Triwulan']

            # Drop data kosong di y-o-y
            df_plot = df.dropna(subset=['y-o-y'])

            # Plot grafik garis y-o-y
            fig = px.line(
                df_plot,
                x='Periode',
                y='y-o-y',
                title='Pertumbuhan Ekonomi Indonesia y-o-y (%) per Triwulan',
                markers=True,
                labels={'y-o-y': 'Pertumbuhan y-o-y (%)', 'Periode': 'Periode'}
            )
            fig.update_layout(
                xaxis_tickangle=-45,
                height=350,
                margin=dict(l=40, r=40, t=50, b=90),
                yaxis_range=[df_plot['y-o-y'].min() - 1, df_plot['y-o-y'].max() + 1],
                plot_bgcolor='white'
            )
            fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')

            st.plotly_chart(fig, use_container_width=True)

            # Insight singkat
            st.markdown("""
            **Insight Neraca Nasional:**
            - Pertumbuhan ekonomi relatif stabil sebelum pandemi.
            - Kontraksi besar terlihat di saat pandemi (2020).
            - Pemulihan ekonomi setelah pandemi.
            - Fluktuasi antar triwulan normal dalam tren positif.
            """)
    except FileNotFoundError:
        st.error("File 'pdb_growth.csv' tidak ditemukan. Pastikan file ada di folder project.")
    except Exception as e:
        st.error(f"Error saat memuat data: {e}")

else:
    st.write(f"Tab '{st.session_state.main_tab}' masih dalam pengembangan.")
