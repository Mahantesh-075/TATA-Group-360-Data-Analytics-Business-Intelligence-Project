"""
Module 5 - Future Growth Vectors & AI/Semiconductor Strategy
"""

import streamlit as st
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils.data_loader import (
    load_ev_market, load_tata_power_renewables,
    load_tcs_master, load_ai_semiconductor, load_it_peers
)
from utils.chart_factory import kpi_card_html, apply_layout
from utils.constants import TATA_PALETTE
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

st.set_page_config(page_title="Future Growth & AI | TATA Analytics", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    .stApp { font-family: 'Inter', sans-serif; }
    #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

st.markdown("# Future Growth Vectors & AI Strategy")
st.markdown("*Semiconductors, AI infrastructure, EV dominance, and clean energy — TATA's next-decade bets*")
st.markdown("---")

# Load data
ev = load_ev_market()
tata_power = load_tata_power_renewables()
tcs = load_tcs_master()
ai_semi = load_ai_semiconductor()
peers = load_it_peers()

# -- KPIs --
cols = st.columns(5)
kpi_data = [
    ("Dholera Fab", "$11B", "50% Complete"),
    ("AI Revenue", "$2.4B", "TCS FY26"),
    ("EV Share", "48%", "India Market"),
    ("Renewables", "9.8 GW", "Tata Power"),
    ("AI Infra", "1 GW", "HyperVault Target"),
]
for col, (label, value, delta) in zip(cols, kpi_data):
    with col:
        st.markdown(kpi_card_html(label, value, delta), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# SECTION 1: SEMICONDUCTOR & AI ECOSYSTEM
# ═══════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown("## Semiconductor & AI Ecosystem")
st.markdown("*From chips to applications — TATA's end-to-end AI value chain*")

# -- AI & Semiconductor Initiatives Map --
if not ai_semi.empty:
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Strategic Initiatives & Partnerships")

        # Group by category
        categories = ai_semi["Category"].unique()
        cat_colors = {
            "Semiconductor": "#1E88E5",
            "Electronics": "#43A047",
            "AI": "#FFB300",
            "AI Infrastructure": "#E53935",
            "AI + Energy": "#00BCD4",
            "AI + Automotive": "#8E24AA",
        }

        fig = go.Figure()

        for cat in categories:
            cat_data = ai_semi[ai_semi["Category"] == cat]
            sizes = cat_data["Investment_INR_Cr"].fillna(0).apply(
                lambda x: max(np.sqrt(x) * 0.8, 15) if x > 0 else 15
            )
            fig.add_trace(go.Scatter(
                x=cat_data["Year"],
                y=cat_data["Category"],
                mode="markers+text",
                name=cat,
                marker=dict(
                    size=sizes,
                    color=cat_colors.get(cat, "#78909C"),
                    opacity=0.7,
                    line=dict(width=2, color="white"),
                ),
                text=cat_data["Initiative"].apply(lambda x: x[:25] + "..." if len(str(x)) > 25 else x),
                textposition="top center",
                textfont=dict(size=9, color="rgba(255,255,255,0.7)"),
                customdata=cat_data[["Initiative", "Partner", "Status", "Details", "Investment_USD_B"]].values,
                hovertemplate=(
                    "<b>%{customdata[0]}</b><br>"
                    "Partner: %{customdata[1]}<br>"
                    "Status: %{customdata[2]}<br>"
                    "Investment: $%{customdata[4]:.1f}B<br>"
                    "Details: %{customdata[3]}<extra></extra>"
                ),
            ))

        fig = apply_layout(fig, "", height=500)
        fig.update_layout(xaxis_title="Year", yaxis_title="")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Key Partnerships")

        partnerships = [
            ("ASML", "Lithography tools for Dholera fab; workforce training & R&D infra", "#1E88E5", "May 2026"),
            ("OpenAI", "ChatGPT Enterprise + Codex; 1M youth AI skilling", "#FFB300", "Feb 2026"),
            ("PSMC", "Taiwan tech partner for 300mm fab; 28-110nm nodes", "#43A047", "Jan 2024"),
            ("Intel", "Manufacturing Intel products; AI PC solutions", "#E53935", "Dec 2025"),
            ("AMD", "High-density sustainable AI compute infra", "#8E24AA", "2026"),
            ("TPG", "INR 18,000 Cr co-investment in AI data centers", "#00BCD4", "2026"),
        ]

        for name, desc, color, date in partnerships:
            st.markdown(f"""
            <div style="background:rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},0.08);
                        border-left:4px solid {color};border-radius:8px;padding:12px 16px;margin-bottom:10px">
                <div style="display:flex;justify-content:space-between;align-items:center">
                    <b style="color:{color};font-size:15px">{name}</b>
                    <span style="color:rgba(255,255,255,0.4);font-size:11px">{date}</span>
                </div>
                <div style="color:rgba(255,255,255,0.7);font-size:12px;margin-top:4px">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

# -- Investment Breakdown --
st.subheader("Semiconductor & AI Investment Breakdown")

if not ai_semi.empty:
    invested = ai_semi[ai_semi["Investment_INR_Cr"] > 0].copy()
    if not invested.empty:
        invested_sorted = invested.sort_values("Investment_INR_Cr", ascending=True)

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=invested_sorted["Investment_INR_Cr"] / 1000,
            y=invested_sorted["Initiative"],
            orientation="h",
            marker=dict(
                color=[cat_colors.get(c, "#78909C") for c in invested_sorted["Category"]],
                line=dict(width=0),
            ),
            text=[f"INR {v/1000:.0f}K Cr (${u:.1f}B)" for v, u in
                  zip(invested_sorted["Investment_INR_Cr"], invested_sorted["Investment_USD_B"])],
            textposition="outside",
            textfont=dict(size=11),
            customdata=invested_sorted[["Partner", "Status"]].values,
            hovertemplate="<b>%{y}</b><br>Partner: %{customdata[0]}<br>Status: %{customdata[1]}<extra></extra>",
        ))
        fig = apply_layout(fig, "", height=350, show_legend=False)
        fig.update_layout(xaxis_title="Investment (INR '000 Crore)")
        st.plotly_chart(fig, use_container_width=True)

# -- Dholera Fab Deep-Dive --
st.markdown("---")
st.markdown("## Dholera Semiconductor Fab — India's First")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(kpi_card_html("Investment", "$11 Billion", "INR 91,000 Cr"), unsafe_allow_html=True)
with col2:
    st.markdown(kpi_card_html("Capacity", "50K wafers/mo", "300mm (12-inch)"), unsafe_allow_html=True)
with col3:
    st.markdown(kpi_card_html("Jobs", "21,000", "In Gujarat SEZ"), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="background:rgba(30,136,229,0.06);border:1px solid rgba(30,136,229,0.15);
                border-radius:12px;padding:24px">
        <h4 style="color:#4FC3F7;margin-top:0">ASML Partnership (May 2026)</h4>
        <ul style="color:rgba(255,255,255,0.8);line-height:2.2">
            <li><b>Lithography Tools:</b> Full suite of advanced patterning equipment</li>
            <li><b>Workforce Training:</b> Lithography-intensive skill development for local talent</li>
            <li><b>R&D Infrastructure:</b> Collaborative research facilities</li>
            <li><b>Supply Chain:</b> Building resilience for long-term fab operations</li>
            <li><b>Technology Nodes:</b> 28nm to 110nm process capabilities</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Fab timeline
    fab_timeline = pd.DataFrame({
        "Phase": ["Announcement", "Ground Breaking", "50% Construction", "Cleanroom Setup",
                  "ASML MoU", "Trial Production", "Commercial Ops"],
        "Date": ["Jan 2024", "Mar 2024", "Apr 2026", "Q2 2026",
                 "May 2026", "Late 2026", "2027-28"],
        "Status": ["Done", "Done", "Done", "In Progress",
                   "Done", "Upcoming", "Planned"],
    })

    colors_map = {"Done": "#43A047", "In Progress": "#FFB300", "Upcoming": "#1E88E5", "Planned": "#78909C"}

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(range(len(fab_timeline))),
        y=[1] * len(fab_timeline),
        mode="markers+text",
        marker=dict(
            size=25,
            color=[colors_map.get(s, "#78909C") for s in fab_timeline["Status"]],
            line=dict(width=2, color="white"),
        ),
        text=fab_timeline["Phase"],
        textposition="top center",
        textfont=dict(size=10),
        customdata=fab_timeline[["Date", "Status"]].values,
        hovertemplate="<b>%{text}</b><br>Date: %{customdata[0]}<br>Status: %{customdata[1]}<extra></extra>",
    ))
    # Connect with line
    fig.add_trace(go.Scatter(
        x=list(range(len(fab_timeline))),
        y=[1] * len(fab_timeline),
        mode="lines",
        line=dict(color="rgba(255,255,255,0.2)", width=2),
        showlegend=False,
    ))
    fig = apply_layout(fig, "Dholera Fab Progress Timeline", height=250, show_legend=False)
    fig.update_layout(
        xaxis=dict(showticklabels=False, showgrid=False),
        yaxis=dict(showticklabels=False, showgrid=False, range=[0.8, 1.3]),
    )
    st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════════════════════
# SECTION 2: EV MARKET
# ═══════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown("## Tata Motors EV — India's Market Leader")

col1, col2 = st.columns(2)

with col1:
    st.subheader("India EV Market Share (2020-2025)")
    if not ev.empty:
        ev_cols = [c for c in ev.columns if c.endswith("_Pct")]
        ev_labels = [c.replace("_Pct", "").replace("_", " ") for c in ev_cols]

        fig = go.Figure()
        for i, (col, label) in enumerate(zip(ev_cols, ev_labels)):
            fig.add_trace(go.Scatter(
                x=ev["Year"], y=ev[col],
                name=label,
                fill="tonexty" if i > 0 else "tozeroy",
                line=dict(color=TATA_PALETTE[i % len(TATA_PALETTE)], width=1.5),
                stackgroup="one",
            ))
        fig = apply_layout(fig, "", height=450)
        fig.update_layout(yaxis_title="Market Share (%)", yaxis=dict(range=[0, 100]))
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("India EV Total Sales Growth")
    if not ev.empty:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=ev["Year"], y=ev["Total_EV_Sales_K"],
            marker=dict(
                color=ev["Total_EV_Sales_K"],
                colorscale=[[0, "#0D47A1"], [1, "#42A5F5"]],
            ),
            text=[f"{v}K" for v in ev["Total_EV_Sales_K"]],
            textposition="outside",
        ))
        fig = apply_layout(fig, "", height=450, show_legend=False)
        fig.update_layout(yaxis_title="Total EV Sales (thousands)")
        st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════════════════════
# SECTION 3: TATA POWER RENEWABLES
# ═══════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown("## Tata Power — Clean Energy Transition")

if not tata_power.empty:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Renewable Energy Capacity (MW)")
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=tata_power["Year"], y=tata_power["Renewable_MW"],
            marker=dict(color="#43A047", opacity=0.8),
            text=[f"{v:,}" for v in tata_power["Renewable_MW"]],
            textposition="outside",
        ))
        fig = apply_layout(fig, "", height=400, show_legend=False)
        fig.update_layout(yaxis_title="Capacity (MW)")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("EV Charging Network Growth")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=tata_power["Year"], y=tata_power["EV_Charging_Stations"],
            fill="tozeroy",
            line=dict(color="#00BCD4", width=3),
            fillcolor="rgba(0,188,212,0.1)",
            mode="lines+markers",
            marker=dict(size=8),
            text=[f"{v:,}" for v in tata_power["EV_Charging_Stations"]],
            textposition="top center",
        ))
        fig = apply_layout(fig, "", height=400, show_legend=False)
        fig.update_layout(yaxis_title="Number of Stations")
        st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════════════════════
# SECTION 4: TCS STOCK PRICE FORECAST (ARIMA)
# ═══════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown("## TCS Stock Price Forecast (ARIMA)")
st.markdown("*Statistical time-series forecast with 95% confidence interval*")

if not tcs.empty:
    try:
        from statsmodels.tsa.arima.model import ARIMA

        # Use monthly close prices for smoother forecast
        tcs_monthly = tcs.set_index("Date")["Close"].resample("ME").last().dropna()

        # Fit ARIMA(2,1,2) — common for stock data
        model = ARIMA(tcs_monthly, order=(2, 1, 2))
        fitted = model.fit()

        # Forecast 36 months ahead
        forecast_steps = 36
        forecast = fitted.get_forecast(steps=forecast_steps)
        fc_mean = forecast.predicted_mean
        fc_ci = forecast.conf_int(alpha=0.05)

        fig = go.Figure()

        # Historical
        fig.add_trace(go.Scatter(
            x=tcs_monthly.index, y=tcs_monthly.values,
            name="Historical Close",
            line=dict(color="#1E88E5", width=2),
        ))

        # Forecast
        fig.add_trace(go.Scatter(
            x=fc_mean.index, y=fc_mean.values,
            name="ARIMA Forecast",
            line=dict(color="#FFB300", width=3, dash="dash"),
        ))

        # Confidence interval
        fig.add_trace(go.Scatter(
            x=list(fc_ci.index) + list(fc_ci.index[::-1]),
            y=list(fc_ci.iloc[:, 1]) + list(fc_ci.iloc[:, 0][::-1]),
            fill="toself",
            fillcolor="rgba(255,179,0,0.1)",
            line=dict(width=0),
            name="95% Confidence Interval",
        ))

        fig = apply_layout(fig, "", height=500)
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="TCS Close Price (INR)",
            hovermode="x unified",
        )
        st.plotly_chart(fig, use_container_width=True)

        # Model diagnostics
        with st.expander("ARIMA Model Summary"):
            st.text(str(fitted.summary()))

    except Exception as e:
        st.warning(f"ARIMA forecasting encountered an issue: {e}")
        st.info("Showing historical TCS data instead.")

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=tcs["Date"], y=tcs["Close"],
            line=dict(color="#1E88E5", width=2),
            name="TCS Close",
        ))
        fig = apply_layout(fig, "TCS Historical Close Price", height=400)
        st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════════════════════
# SECTION 5: AI FUTURE ROADMAP SUMMARY
# ═══════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown("## TATA Group AI Roadmap — Chips to Applications")

st.markdown("""
<div style="background:linear-gradient(135deg,rgba(30,136,229,0.08),rgba(255,179,0,0.05));
            border:1px solid rgba(30,136,229,0.2);border-radius:16px;padding:32px;margin:16px 0">

<h4 style="color:#4FC3F7;margin-top:0">The Full Stack AI Play</h4>

<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:24px;margin-top:16px">

<div style="border-left:3px solid #1E88E5;padding-left:16px">
    <h5 style="color:#1E88E5;margin:0">HARDWARE LAYER</h5>
    <ul style="color:rgba(255,255,255,0.7);font-size:13px;line-height:2">
        <li>Dholera Fab: $11B, 50K wafers/mo</li>
        <li>ASML lithography partnership</li>
        <li>OSAT Jagiroad: $3.3B</li>
        <li>Intel manufacturing alliance</li>
        <li>Apple iPhone assembly (Hosur)</li>
    </ul>
</div>

<div style="border-left:3px solid #FFB300;padding-left:16px">
    <h5 style="color:#FFB300;margin:0">INFRASTRUCTURE LAYER</h5>
    <ul style="color:rgba(255,255,255,0.7);font-size:13px;line-height:2">
        <li>HyperVault: 100MW to 1GW DCs</li>
        <li>TPG co-investment: INR 18K Cr</li>
        <li>AMD GPU-optimized design</li>
        <li>Sovereign AI-ready, liquid-cooled</li>
        <li>OpenAI as anchor customer</li>
    </ul>
</div>

<div style="border-left:3px solid #43A047;padding-left:16px">
    <h5 style="color:#43A047;margin:0">APPLICATIONS LAYER</h5>
    <ul style="color:rgba(255,255,255,0.7);font-size:13px;line-height:2">
        <li>TCS AI Revenue: $2.4B (FY26)</li>
        <li>580+ AI projects in Q4 FY25</li>
        <li>150+ agentic AI solutions</li>
        <li>OpenAI Codex for engineering</li>
        <li>GVIC: AI-native GCC unit</li>
    </ul>
</div>

</div>

<div style="margin-top:24px;padding-top:16px;border-top:1px solid rgba(255,255,255,0.1);
            text-align:center;color:rgba(255,255,255,0.5);font-size:12px">
    Target: Every TCS revenue stream to have an AI component by 2028 |
    1 Million Indian youth AI skilling (OpenAI Foundation + TCS)
</div>

</div>
""", unsafe_allow_html=True)

# -- Full AI/Semi Data Table --
with st.expander("View Full AI & Semiconductor Initiatives Data"):
    if not ai_semi.empty:
        st.dataframe(ai_semi, use_container_width=True, hide_index=True)
