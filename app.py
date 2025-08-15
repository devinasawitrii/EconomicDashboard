# BASIC CSS - JANGAN SENTUH YANG LAIN, FOKUS TAB-CONTENT GAP AJA
st.markdown("""
<style>
    .block-container { 
        padding-top: 0.5rem !important;
        padding-bottom: 0rem !important;
        max-width: 100% !important;
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
        margin-bottom: 0.5rem;
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
    .insight-section {
        font-size: 14px;
        line-height: 1.2;
        padding: 10px;
    }
    
    /* Hide streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
</style>

<script>
setTimeout(function() {
    // HANYA CARI KONTEN SETELAH NAV DAN PAKSA NAIK
    const charts = document.querySelectorAll('*');
    charts.forEach(el => {
        if (el.textContent && el.textContent.includes('Analisis Komprehensif')) {
            const container = el.closest('.element-container');
            if (container) {
                container.style.marginTop = '-2rem';
                container.style.paddingTop = '0px';
            }
        }
    });
}, 500);
</script>
""", unsafe_allow_html=True)
