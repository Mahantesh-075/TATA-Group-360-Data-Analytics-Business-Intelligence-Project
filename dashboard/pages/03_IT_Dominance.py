"""
Module 3 - IT Sector Dominance (TCS Deep-Dive)
"""

import streamlit as st
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils.data_loader import load_it_peers, load_tcs_verticals, load_tcs_geo
from utils.chart_factory import (
    kpi_card_html, apply_layout, make_pie_donut
)
from utils.constants import IT_PEER_COLORS, TATA_PALETTE
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="IT Dominance | TATA Analytics", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    .stApp { font-family: 'Inter', sans-serif; }
    #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

st.markdown("# IT Sector Dominance")
st.markdown("*TCS vs Infosys vs Wipro vs HCL Tech - 20 years of competitive intelligence*")
st.markdown("---")

# Load data
peers = load_it_peers()
verticals = load_tcs_verticals()
geo = load_tcs_geo()

# -- KPIs --
cols = st.columns(4)
kpi_data = [
    ("TCS Revenue", "$29.5B", "Largest Indian IT Co."),
    ("TCS Employees", "608K", "Across 55 countries"),
    ("AI Revenue", "$2.4B", "Annualized FY26"),
    ("Profit Margin", "20.2%", "Industry-leading"),
]
for col, (label, value, delta) in zip(cols, kpi_data):
    with col:
        st.markdown(kpi_card_html(label, value, delta), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -- Revenue Comparison --
st.subheader("Revenue Trajectory: TCS vs Peers (FY2005-FY2025)")

fig = go.Figure()
for company, color in IT_PEER_COLORS.items():
    col_name = f"{company}_Revenue_B_USD"
    if col_name in peers.columns:
        fig.add_trace(go.Scatter(
            x=peers["FY"], y=peers[col_name],
            name=company,
            line=dict(color=color, width=3),
            mode="lines+markers",
            marker=dict(size=4),
        ))
fig = apply_layout(fig, "", height=500)
fig.update_layout(
    xaxis_title="Fiscal Year",
    yaxis_title="Revenue ($ Billion)",
    hovermode="x unified",
)
st.plotly_chart(fig, use_container_width=True)

# -- Profit & Margin Comparison --
col1, col2 = st.columns(2)

with col1:
    st.subheader("Net Profit Comparison")
    fig = go.Figure()
    for company, color in IT_PEER_COLORS.items():
        col_name = f"{company}_Profit_B_USD"
        if col_name in peers.columns:
            fig.add_trace(go.Scatter(
                x=peers["FY"], y=peers[col_name],
                name=company,
                line=dict(color=color, width=2.5),
                fill="tozeroy" if company == "TCS" else None,
                fillcolor="rgba(30,136,229,0.08)" if company == "TCS" else None,
            ))
    fig = apply_layout(fig, "", height=420)
    fig.update_layout(yaxis_title="Net Profit ($ Billion)")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Profit Margin % Trends")
    fig = go.Figure()
    for company, color in IT_PEER_COLORS.items():
        col_name = f"{company}_Margin_Pct"
        if col_name in peers.columns:
            fig.add_trace(go.Scatter(
                x=peers["FY"], y=peers[col_name],
                name=company,
                line=dict(color=color, width=2.5),
            ))
    fig = apply_layout(fig, "", height=420)
    fig.update_layout(yaxis_title="Net Profit Margin (%)")
    st.plotly_chart(fig, use_container_width=True)

# -- Employee Headcount --
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Employee Headcount Growth")
    fig = go.Figure()
    for company, color in IT_PEER_COLORS.items():
        col_name = f"{company}_Employees_K"
        if col_name in peers.columns:
            fig.add_trace(go.Bar(
                x=peers["FY"], y=peers[col_name],
                name=company,
                marker=dict(color=color, opacity=0.8),
            ))
    fig = apply_layout(fig, "", height=420)
    fig.update_layout(
        barmode="group",
        yaxis_title="Employees (thousands)",
        xaxis_title="Fiscal Year",
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Revenue Per Employee Efficiency")
    # Compute revenue per employee
    peers_eff = peers.copy()
    for company in ["TCS", "Infosys", "Wipro", "HCL"]:
        rev_col = f"{company}_Revenue_B_USD"
        emp_col = f"{company}_Employees_K"
        if rev_col in peers_eff.columns and emp_col in peers_eff.columns:
            peers_eff[f"{company}_Rev_Per_Emp_K"] = (
                peers_eff[rev_col] * 1000 / peers_eff[emp_col]
            ).round(2)  # Revenue per employee in $M

    fig = go.Figure()
    for company, color in IT_PEER_COLORS.items():
        col_name = f"{company}_Rev_Per_Emp_K"
        if col_name in peers_eff.columns:
            fig.add_trace(go.Scatter(
                x=peers_eff["FY"], y=peers_eff[col_name],
                name=company,
                line=dict(color=color, width=2.5),
                mode="lines+markers",
                marker=dict(size=4),
            ))
    fig = apply_layout(fig, "", height=420)
    fig.update_layout(yaxis_title="Revenue per Employee ($M)")
    st.plotly_chart(fig, use_container_width=True)

# -- TCS Revenue Breakdown --
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.subheader("TCS Revenue by Industry Vertical")
    if not verticals.empty:
        fig = go.Figure(data=[go.Pie(
            labels=verticals["Vertical"],
            values=verticals["Revenue_Pct"],
            hole=0.5,
            marker=dict(colors=TATA_PALETTE[:len(verticals)]),
            textinfo="label+percent",
            textfont=dict(size=11),
        )])
        fig = apply_layout(fig, "", height=450, show_legend=False)
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("TCS Geographic Revenue Split")
    if not geo.empty:
        fig = make_pie_donut(geo, "Region", "Revenue_Pct", title="", hole=0.5)
        st.plotly_chart(fig, use_container_width=True)

# -- Market Cap Timeline --
st.markdown("---")
st.subheader("Market Dominance: Revenue Gap TCS vs Next Peer")

if not peers.empty:
    peers_gap = peers[["FY"]].copy()
    peers_gap["TCS"] = peers["TCS_Revenue_B_USD"]
    peers_gap["Infosys"] = peers["Infosys_Revenue_B_USD"]
    peers_gap["Gap"] = peers_gap["TCS"] - peers_gap["Infosys"]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=peers_gap["FY"], y=peers_gap["TCS"],
        name="TCS Revenue",
        line=dict(color="#1E88E5", width=3),
        fill="tonexty",
    ))
    fig.add_trace(go.Scatter(
        x=peers_gap["FY"], y=peers_gap["Infosys"],
        name="Infosys Revenue",
        line=dict(color="#43A047", width=3),
    ))
    fig.add_trace(go.Bar(
        x=peers_gap["FY"], y=peers_gap["Gap"],
        name="Revenue Gap",
        marker=dict(color="rgba(255,179,0,0.3)"),
        yaxis="y2",
    ))
    fig = apply_layout(fig, "", height=450)
    fig.update_layout(
        yaxis=dict(title="Revenue ($B)"),
        yaxis2=dict(title="Gap ($B)", overlaying="y", side="right"),
    )
    st.plotly_chart(fig, use_container_width=True)

# -- Peer Comparison Table --
with st.expander("View Full IT Peers Data Table"):
    st.dataframe(peers, use_container_width=True, hide_index=True)
