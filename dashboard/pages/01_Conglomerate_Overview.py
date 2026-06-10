"""
Module 1 - TATA Conglomerate Overview
"""

import streamlit as st
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils.data_loader import load_sectors, load_gdp
from utils.chart_factory import (
    kpi_card_html, make_treemap, make_pie_donut, make_bar_chart,
    make_dual_axis, make_line_chart, apply_layout, add_milestone_annotations
)
from utils.constants import MILESTONES, TATA_PALETTE, SECTOR_COLORS
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Conglomerate Overview | TATA Analytics", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    .stApp { font-family: 'Inter', sans-serif; }
    #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

st.markdown("# The TATA Universe")
st.markdown("*Revenue breakdown, sector dominance, and GDP contribution of India's largest conglomerate*")
st.markdown("---")

# Load data
sectors = load_sectors()
gdp = load_gdp()

# -- KPIs --
cols = st.columns(4)
kpi_data = [
    ("Total Revenue", "$180B", "+12% YoY"),
    ("Market Cap", "$328B", "+18% YoY"),
    ("Sectors", "16", "Industry verticals"),
    ("GDP Contribution", "4.57%", "Of India's GDP"),
]
for col, (label, value, delta) in zip(cols, kpi_data):
    with col:
        st.markdown(kpi_card_html(label, value, delta), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -- Revenue Treemap --
col1, col2 = st.columns(2)

with col1:
    st.subheader("Revenue by Sector (FY2025)")
    fig = px.treemap(
        sectors, path=["Sector"], values="Revenue_USD_B",
        color="Revenue_USD_B",
        color_continuous_scale=["#0D47A1", "#1565C0", "#1E88E5", "#42A5F5", "#90CAF9"],
        custom_data=["Key_Company", "Employees_K"],
    )
    fig.update_traces(
        texttemplate="<b>%{label}</b><br>$%{value}B",
        hovertemplate="<b>%{label}</b><br>Revenue: $%{value}B<br>Key: %{customdata[0]}<br>Employees: %{customdata[1]}K<extra></extra>",
    )
    fig = apply_layout(fig, "", height=480, show_legend=False)
    fig.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Market Cap Distribution")
    fig = make_pie_donut(sectors, "Sector", "Market_Cap_USD_B", title="", hole=0.5)
    st.plotly_chart(fig, use_container_width=True)

# -- Employee Distribution --
col1, col2 = st.columns(2)

with col1:
    st.subheader("Employee Distribution by Sector")
    sectors_sorted = sectors.sort_values("Employees_K", ascending=True)
    fig = go.Figure(go.Bar(
        x=sectors_sorted["Employees_K"],
        y=sectors_sorted["Sector"],
        orientation="h",
        marker=dict(
            color=sectors_sorted["Employees_K"],
            colorscale="Blues",
            line=dict(width=0),
        ),
        text=[f"{v}K" for v in sectors_sorted["Employees_K"]],
        textposition="outside",
        textfont=dict(size=11),
    ))
    fig = apply_layout(fig, "", height=500, show_legend=False)
    fig.update_layout(xaxis_title="Employees (thousands)", yaxis_title="")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Revenue vs Market Cap per Sector")
    fig = px.scatter(
        sectors, x="Revenue_USD_B", y="Market_Cap_USD_B",
        size="Employees_K", color="Sector",
        hover_name="Key_Company",
        color_discrete_sequence=TATA_PALETTE,
        size_max=50,
    )
    fig = apply_layout(fig, "", height=500)
    fig.update_layout(
        xaxis_title="Revenue ($B)",
        yaxis_title="Market Cap ($B)",
        legend=dict(font=dict(size=9)),
    )
    st.plotly_chart(fig, use_container_width=True)

# -- GDP Comparison --
st.markdown("---")
st.subheader("TATA Group Revenue vs India GDP (1991-2025)")

fig = go.Figure()

# India GDP (left axis)
fig.add_trace(go.Scatter(
    x=gdp["Year"], y=gdp["India_GDP_USD_B"],
    name="India GDP ($B)",
    fill="tozeroy",
    line=dict(color="#1E88E5", width=2),
    fillcolor="rgba(30,136,229,0.1)",
))

# TATA Revenue (right axis)
fig.add_trace(go.Scatter(
    x=gdp["Year"], y=gdp["TATA_Revenue_USD_B"],
    name="TATA Revenue ($B)",
    yaxis="y2",
    line=dict(color="#FFB300", width=3),
    mode="lines+markers",
    marker=dict(size=5),
))

fig = apply_layout(fig, "", height=500)
fig.update_layout(
    yaxis=dict(title="India GDP ($B)", gridcolor="rgba(255,255,255,0.05)"),
    yaxis2=dict(
        title="TATA Revenue ($B)", overlaying="y", side="right",
        gridcolor="rgba(255,255,255,0.03)",
    ),
)

# Add milestone annotations
milestones_with_pos = [(y, l) for y, l in MILESTONES if y <= 2025]
fig = add_milestone_annotations(fig, milestones_with_pos)

st.plotly_chart(fig, use_container_width=True)

# -- GDP Percentage --
st.subheader("TATA Revenue as % of India GDP")

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=gdp["Year"], y=gdp["TATA_Pct_GDP"],
    fill="tozeroy",
    line=dict(color="#00BCD4", width=3),
    fillcolor="rgba(0,188,212,0.15)",
    mode="lines+markers",
    marker=dict(size=4),
    hovertemplate="Year: %{x}<br>GDP Share: %{y:.2f}%<extra></extra>",
))
fig = apply_layout(fig, "", height=400, show_legend=False)
fig.update_layout(yaxis_title="% of India GDP", xaxis_title="Year")
fig = add_milestone_annotations(fig, milestones_with_pos, y_pos=0.9)
st.plotly_chart(fig, use_container_width=True)

# -- Key Milestones Table --
st.subheader("Key TATA Milestones")
milestone_data = gdp[gdp["Milestone"].notna() & (gdp["Milestone"] != "")][
    ["Year", "Milestone", "India_GDP_USD_B", "TATA_Revenue_USD_B", "TATA_Pct_GDP"]
].rename(columns={
    "India_GDP_USD_B": "India GDP ($B)",
    "TATA_Revenue_USD_B": "TATA Revenue ($B)",
    "TATA_Pct_GDP": "GDP Share (%)",
})
st.dataframe(milestone_data, use_container_width=True, hide_index=True)
