"""
TATA Group 360 Analytics Dashboard
===================================
Interactive Streamlit dashboard with 5 analysis modules.

Run: streamlit run dashboard/app.py
"""

import streamlit as st
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from utils.chart_factory import kpi_card_html
from utils.constants import (
    GROUP_REVENUE_USD_B, GROUP_MARKET_CAP_USD_B, GROUP_EMPLOYEES,
    GROUP_LISTED_COMPANIES, GROUP_GDP_CONTRIBUTION, GROUP_SECTORS,
    TCS_MARKET_CAP_INR_CR, TCS_REVENUE_USD_B, TCS_EMPLOYEES_K,
    TATA_BLUE, TATA_BLUE_LIGHT
)

# -- Page config --
st.set_page_config(
    page_title="TATA Group 360 Analytics",
    page_icon="https://upload.wikimedia.org/wikipedia/commons/8/8e/Tata_logo.svg",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -- Custom CSS --
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800;900&display=swap');

    /* Global */
    .stApp {
        font-family: 'Inter', sans-serif;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #001529 0%, #002244 50%, #003366 100%);
        border-right: 1px solid rgba(30,136,229,0.2);
    }
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #4FC3F7 !important;
    }

    /* Hero section */
    .hero-container {
        background: linear-gradient(135deg, #001529 0%, #003B73 40%, #1E88E5 100%);
        border-radius: 20px;
        padding: 48px 40px;
        margin-bottom: 32px;
        border: 1px solid rgba(30,136,229,0.3);
        position: relative;
        overflow: hidden;
    }
    .hero-container::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -30%;
        width: 600px;
        height: 600px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(30,136,229,0.15) 0%, transparent 70%);
    }
    .hero-title {
        font-size: 42px;
        font-weight: 900;
        color: white;
        letter-spacing: -1.5px;
        margin-bottom: 8px;
        position: relative;
    }
    .hero-subtitle {
        font-size: 18px;
        color: rgba(255,255,255,0.7);
        font-weight: 300;
        max-width: 700px;
        line-height: 1.6;
        position: relative;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(255,179,0,0.2);
        color: #FFB300;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 16px;
        border: 1px solid rgba(255,179,0,0.3);
        position: relative;
    }

    /* KPI grid */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 16px;
        margin-bottom: 32px;
    }

    /* Section headers */
    .section-header {
        font-size: 24px;
        font-weight: 700;
        color: white;
        margin: 32px 0 16px 0;
        padding-bottom: 8px;
        border-bottom: 2px solid rgba(30,136,229,0.3);
    }

    /* Cards */
    .info-card {
        background: rgba(30,136,229,0.06);
        border: 1px solid rgba(30,136,229,0.15);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
    }

    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# -- Sidebar --
with st.sidebar:
    st.markdown("## TATA Group")
    st.markdown("### 360 Analytics")
    st.markdown("---")
    st.markdown("""
    **Modules:**
    - Conglomerate Overview
    - Stock Analysis
    - IT Dominance (TCS)
    - Acquisitions Timeline
    - Future Growth & AI

    ---
    **Author:** Mahantesh  
    **Course:** B.E. ECE 6th Sem  
    **Institution:** DR. AIT, Bengaluru  
    **Target:** TCS NQT Campus Recruitment
    """)
    st.markdown("---")
    st.markdown(
        '<p style="color:rgba(255,255,255,0.3);font-size:11px;text-align:center">'
        'Data Sources: NSE, Yahoo Finance, Kaggle, IBEF, World Bank</p>',
        unsafe_allow_html=True,
    )


# -- Hero Section --
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">Business Intelligence Dashboard</div>
    <div class="hero-title">The TATA Empire</div>
    <div class="hero-subtitle">
        A 360-degree data-driven analysis of India's largest conglomerate.
        From TCS dominating global IT to Tata Motors leading India's EV revolution,
        from semiconductor fabs to AI infrastructure &mdash; explore the $180 billion empire
        that contributes 4.57% of India's GDP.
    </div>
</div>
""", unsafe_allow_html=True)

# -- KPI Cards --
cols = st.columns(6)
kpis = [
    ("Revenue", f"${GROUP_REVENUE_USD_B}B", "+12% YoY", "$"),
    ("Market Cap", f"${GROUP_MARKET_CAP_USD_B}B", "+18% YoY", "^"),
    ("Employees", GROUP_EMPLOYEES, "Across 100+ countries", "#"),
    ("Listed Cos.", str(GROUP_LISTED_COMPANIES), "On NSE/BSE", "%"),
    ("GDP Share", GROUP_GDP_CONTRIBUTION, "Of India's GDP", "@"),
    ("Sectors", str(GROUP_SECTORS), "Industry verticals", "*"),
]

for col, (label, value, delta, icon) in zip(cols, kpis):
    with col:
        st.markdown(kpi_card_html(label, value, delta, icon), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -- Quick Stats --
st.markdown('<div class="section-header">Group Highlights (FY2025)</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="info-card">
        <h4 style="color:#4FC3F7;margin-top:0">TCS - Crown Jewel</h4>
        <ul style="color:rgba(255,255,255,0.8);line-height:2">
            <li>Market Cap: <b>INR 7,79,861 Cr</b> (~$100B)</li>
            <li>Revenue: <b>$29.5 Billion</b> (FY25)</li>
            <li>Employees: <b>608,000+</b> across 55 countries</li>
            <li>AI Services Revenue: <b>$2.4B annualized</b> (FY26)</li>
            <li>BFSI vertical: <b>31.9%</b> of revenue</li>
            <li>OpenAI partnership for enterprise AI transformation</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
        <h4 style="color:#FFB300;margin-top:0">Future Bets</h4>
        <ul style="color:rgba(255,255,255,0.8);line-height:2">
            <li>Dholera Semiconductor Fab: <b>$11B investment</b> (50% complete)</li>
            <li>ASML partnership for lithography tools (May 2026)</li>
            <li>HyperVault AI Data Centers: <b>100MW to 1GW</b></li>
            <li>Tata Motors EV: <b>48% India market share</b></li>
            <li>Tata Power: <b>9,800 MW</b> renewable capacity</li>
            <li>Intel + AMD + OpenAI strategic alliances</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown(
    '<p style="text-align:center;color:rgba(255,255,255,0.3);font-size:12px">'
    'Navigate to individual modules using the sidebar pages for deep-dive analysis.</p>',
    unsafe_allow_html=True,
)
