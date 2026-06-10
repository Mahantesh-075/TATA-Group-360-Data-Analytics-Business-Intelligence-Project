"""
Module 4 - Acquisitions Timeline & M&A Analysis
"""

import streamlit as st
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils.data_loader import load_acquisitions, load_jlr_roi
from utils.chart_factory import kpi_card_html, apply_layout
from utils.constants import TATA_PALETTE, SECTOR_COLORS
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

st.set_page_config(page_title="Acquisitions Timeline | TATA Analytics", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    .stApp { font-family: 'Inter', sans-serif; }
    #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

st.markdown("# Acquisitions Timeline")
st.markdown("*25 years of strategic M&A that built a global conglomerate*")
st.markdown("---")

# Load data
acq = load_acquisitions()
jlr = load_jlr_roi()

# -- KPIs --
total_deals = len(acq)
total_value = acq["Value_USD_M"].sum() / 1000  # Convert to Billions
ratan_deals = len(acq[acq["Era"] == "Ratan Tata"])
nc_deals = len(acq[acq["Era"] == "N. Chandrasekaran"])

cols = st.columns(4)
kpi_data = [
    ("Total Deals", str(total_deals), "Since 2000"),
    ("Total Value", f"${total_value:.1f}B", "Combined M&A"),
    ("Ratan Tata Era", str(ratan_deals), "2000-2012"),
    ("NC Era", str(nc_deals), "2017-Present"),
]
for col, (label, value, delta) in zip(cols, kpi_data):
    with col:
        st.markdown(kpi_card_html(label, value, delta), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -- Interactive Timeline --
st.subheader("Acquisition Timeline (2000-2024)")

fig = go.Figure()

# Create timeline scatter
for era, color in [("Ratan Tata", "#1E88E5"), ("N. Chandrasekaran", "#FFB300")]:
    era_data = acq[acq["Era"] == era]
    sizes = era_data["Value_USD_M"].fillna(100).clip(lower=100)
    sizes_scaled = np.sqrt(sizes) * 2

    fig.add_trace(go.Scatter(
        x=era_data["Year"],
        y=era_data["Sector"],
        mode="markers+text",
        name=f"{era} Era",
        marker=dict(
            size=sizes_scaled,
            color=color,
            opacity=0.7,
            line=dict(width=2, color="white"),
        ),
        text=era_data["Target"],
        textposition="top center",
        textfont=dict(size=10, color="rgba(255,255,255,0.8)"),
        customdata=era_data[["Target", "Value_USD_M", "Outcome", "Country"]].values,
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "Year: %{x}<br>"
            "Sector: %{y}<br>"
            "Value: $%{customdata[1]:.0f}M<br>"
            "Country: %{customdata[3]}<br>"
            "Outcome: %{customdata[2]}<extra></extra>"
        ),
    ))

fig = apply_layout(fig, "", height=600)
fig.update_layout(
    xaxis=dict(title="Year", dtick=2),
    yaxis=dict(title=""),
)
st.plotly_chart(fig, use_container_width=True)

# -- Bubble Chart: Deal Value --
col1, col2 = st.columns(2)

with col1:
    st.subheader("Deal Value Distribution")
    acq_valued = acq[acq["Value_USD_M"] > 0].copy()
    if not acq_valued.empty:
        fig = px.scatter(
            acq_valued, x="Year", y="Sector",
            size="Value_USD_M", color="Era",
            hover_name="Target",
            size_max=80,
            color_discrete_map={"Ratan Tata": "#1E88E5", "N. Chandrasekaran": "#FFB300"},
            custom_data=["Target", "Value_USD_M", "Country"],
        )
        fig.update_traces(
            hovertemplate="<b>%{customdata[0]}</b><br>$%{customdata[1]:.0f}M<br>%{customdata[2]}<extra></extra>"
        )
        fig = apply_layout(fig, "", height=450)
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Sector Diversification")
    sector_counts = acq.groupby("Sector").agg(
        Deals=("Target", "count"),
        Total_Value=("Value_USD_M", "sum")
    ).reset_index().sort_values("Deals", ascending=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=sector_counts["Deals"],
        y=sector_counts["Sector"],
        orientation="h",
        marker=dict(
            color=[SECTOR_COLORS.get(s, "#78909C") for s in sector_counts["Sector"]],
        ),
        text=[f"{d} deals (${v/1000:.1f}B)" for d, v in zip(sector_counts["Deals"], sector_counts["Total_Value"])],
        textposition="outside",
        textfont=dict(size=11),
    ))
    fig = apply_layout(fig, "", height=450, show_legend=False)
    fig.update_layout(xaxis_title="Number of Deals")
    st.plotly_chart(fig, use_container_width=True)

# -- Era Comparison --
st.markdown("---")
st.subheader("Leadership Era Comparison")

col1, col2 = st.columns(2)

with col1:
    era_summary = acq.groupby("Era").agg(
        Deals=("Target", "count"),
        Total_Value_M=("Value_USD_M", "sum"),
        Sectors=("Sector", "nunique"),
        Countries=("Country", "nunique"),
    ).reset_index()

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Deal Count",
        x=era_summary["Era"],
        y=era_summary["Deals"],
        marker=dict(color=["#1E88E5", "#FFB300"]),
        text=era_summary["Deals"],
        textposition="outside",
    ))
    fig = apply_layout(fig, "Deals per Era", height=350)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Total Value ($B)",
        x=era_summary["Era"],
        y=era_summary["Total_Value_M"] / 1000,
        marker=dict(color=["#1E88E5", "#FFB300"]),
        text=[f"${v/1000:.1f}B" for v in era_summary["Total_Value_M"]],
        textposition="outside",
    ))
    fig = apply_layout(fig, "Total M&A Investment per Era", height=350)
    fig.update_layout(yaxis_title="Total Value ($B)")
    st.plotly_chart(fig, use_container_width=True)

# -- Cumulative M&A Investment --
st.subheader("Cumulative M&A Investment Over Time")

acq_sorted = acq.sort_values("Year")
acq_sorted["Cumulative_USD_B"] = acq_sorted["Value_USD_M"].fillna(0).cumsum() / 1000

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=acq_sorted["Year"], y=acq_sorted["Cumulative_USD_B"],
    fill="tozeroy",
    line=dict(color="#00BCD4", width=3),
    fillcolor="rgba(0,188,212,0.1)",
    mode="lines+markers",
    marker=dict(size=8, color="#00BCD4"),
    text=acq_sorted["Target"],
    hovertemplate="<b>%{text}</b><br>Year: %{x}<br>Cumulative: $%{y:.1f}B<extra></extra>",
))
fig = apply_layout(fig, "", height=400, show_legend=False)
fig.update_layout(yaxis_title="Cumulative Investment ($B)", xaxis_title="Year")
st.plotly_chart(fig, use_container_width=True)

# -- JLR ROI Case Study --
st.markdown("---")
st.subheader("Case Study: Jaguar Land Rover (JLR) Turnaround")
st.markdown("""
> *Acquired for GBP 1.15 Billion in 2008 from Ford — widely questioned as reckless. 
> By 2024, JLR generates GBP 29B in revenue, making it one of the most successful 
> acquisitions in Indian corporate history.*
""")

if not jlr.empty:
    col1, col2 = st.columns([2, 1])

    with col1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=jlr["Year"], y=jlr["JLR_Revenue_GBP_B"],
            name="JLR Revenue (GBP B)",
            line=dict(color="#1E88E5", width=3),
            fill="tozeroy",
            fillcolor="rgba(30,136,229,0.1)",
        ))
        fig.add_trace(go.Scatter(
            x=jlr["Year"], y=jlr["JLR_Profit_GBP_M"] / 1000,
            name="JLR Profit (GBP B)",
            line=dict(color="#FFB300", width=2.5, dash="dot"),
            yaxis="y2",
        ))
        fig.add_hline(y=0, line_dash="dash", line_color="rgba(255,255,255,0.2)")
        fig = apply_layout(fig, "", height=450)
        fig.update_layout(
            yaxis=dict(title="Revenue (GBP B)"),
            yaxis2=dict(title="Profit (GBP B)", overlaying="y", side="right"),
        )
        # Add acquisition marker
        fig.add_annotation(
            x=2008, y=0, text="<b>Acquired</b><br>GBP 1.15B",
            showarrow=True, arrowhead=2, arrowcolor="#E53935",
            font=dict(color="#E53935", size=12),
            bgcolor="rgba(0,0,0,0.6)", bordercolor="#E53935",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("""
        <div style="background:rgba(30,136,229,0.08);border:1px solid rgba(30,136,229,0.2);
                    border-radius:12px;padding:20px">
            <h4 style="color:#4FC3F7;margin-top:0">JLR By Numbers</h4>
            <ul style="color:rgba(255,255,255,0.8);line-height:2.2">
                <li>Acquisition: <b>GBP 1.15B</b> (2008)</li>
                <li>Peak Revenue: <b>GBP 29B</b> (2024)</li>
                <li>Peak Units: <b>604K</b> (2017)</li>
                <li>Peak Profit: <b>GBP 2.6B</b> (2024)</li>
                <li>ROI: <b>~25x</b> revenue vs cost</li>
                <li>COVID Impact: Revenue fell 20%</li>
                <li>Recovery: Full by 2024</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# -- Full Acquisitions Table --
with st.expander("View Full Acquisitions Database"):
    st.dataframe(acq, use_container_width=True, hide_index=True)
