"""
Module 2 - Stock Analysis (Multi-Company)
"""

import streamlit as st
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils.data_loader import (
    load_tata_stocks_combined, load_correlation_matrix,
    load_cagr_table, load_tcs_master, load_daily_returns
)
from utils.chart_factory import (
    kpi_card_html, apply_layout, make_heatmap
)
from utils.constants import TATA_PALETTE, TATA_TICKERS
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

st.set_page_config(page_title="Stock Analysis | TATA Analytics", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    .stApp { font-family: 'Inter', sans-serif; }
    #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

st.markdown("# Stock Analysis")
st.markdown("*Multi-stock price analysis, correlation, CAGR, and volatility across TATA subsidiaries*")
st.markdown("---")

# Load data
combined = load_tata_stocks_combined()
corr_matrix = load_correlation_matrix()
cagr = load_cagr_table()
tcs_master = load_tcs_master()
daily_returns = load_daily_returns()

# Available tickers
all_tickers = sorted(combined["Ticker"].unique())
ticker_labels = {t: TATA_TICKERS.get(t, t) for t in all_tickers}

# -- Controls --
col1, col2 = st.columns([3, 1])
with col1:
    selected_tickers = st.multiselect(
        "Select stocks to compare",
        options=all_tickers,
        default=[t for t in ["TCS", "TATASTEEL", "TATAPOWER", "TATACONSUM", "TATAMOTORS_PASS"] if t in all_tickers],
        format_func=lambda t: ticker_labels.get(t, t),
    )
with col2:
    date_range = st.date_input(
        "Date range",
        value=(combined["Date"].min().date(), combined["Date"].max().date()),
        min_value=combined["Date"].min().date(),
        max_value=combined["Date"].max().date(),
    )

# Filter data
if len(date_range) == 2:
    mask = (
        combined["Ticker"].isin(selected_tickers) &
        (combined["Date"].dt.date >= date_range[0]) &
        (combined["Date"].dt.date <= date_range[1])
    )
else:
    mask = combined["Ticker"].isin(selected_tickers)

filtered = combined[mask].copy()

# -- Multi-Stock Price Chart --
st.subheader("Stock Price Comparison")

fig = go.Figure()
for i, ticker in enumerate(selected_tickers):
    df_t = filtered[filtered["Ticker"] == ticker]
    if df_t.empty:
        continue
    fig.add_trace(go.Scatter(
        x=df_t["Date"], y=df_t["Close"],
        name=ticker_labels.get(ticker, ticker),
        line=dict(color=TATA_PALETTE[i % len(TATA_PALETTE)], width=2),
        mode="lines",
        hovertemplate=f"<b>{ticker}</b><br>Date: %{{x}}<br>Close: %{{y:.2f}}<extra></extra>",
    ))
fig = apply_layout(fig, "", height=500)
fig.update_layout(
    xaxis_title="Date", yaxis_title="Close Price (INR)",
    hovermode="x unified",
)
st.plotly_chart(fig, use_container_width=True)

# -- Normalized Returns (Base 100) --
st.subheader("Normalized Returns (Base = 100)")
st.caption("Rebased performance comparison from start of selected period")

fig = go.Figure()
for i, ticker in enumerate(selected_tickers):
    df_t = filtered[filtered["Ticker"] == ticker].sort_values("Date")
    if df_t.empty or len(df_t) < 2:
        continue
    base_price = df_t.iloc[0]["Close"]
    if base_price > 0:
        normalized = (df_t["Close"] / base_price) * 100
        fig.add_trace(go.Scatter(
            x=df_t["Date"], y=normalized,
            name=ticker_labels.get(ticker, ticker),
            line=dict(color=TATA_PALETTE[i % len(TATA_PALETTE)], width=2),
        ))

fig.add_hline(y=100, line_dash="dash", line_color="rgba(255,255,255,0.3)")
fig = apply_layout(fig, "", height=450)
fig.update_layout(yaxis_title="Normalized Price (Base=100)")
st.plotly_chart(fig, use_container_width=True)

# -- CAGR Comparison --
col1, col2 = st.columns(2)

with col1:
    st.subheader("CAGR Comparison")
    if not cagr.empty:
        cagr_filtered = cagr[cagr["Ticker"].isin(selected_tickers)]
        if not cagr_filtered.empty:
            fig = px.bar(
                cagr_filtered, x="Ticker", y="CAGR_Pct", color="Period",
                barmode="group", text="CAGR_Pct",
                color_discrete_sequence=["#1E88E5", "#FFB300", "#E53935"],
            )
            fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
            fig = apply_layout(fig, "", height=450)
            fig.update_layout(xaxis_title="", yaxis_title="CAGR (%)")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No CAGR data available for selected tickers")
    else:
        st.info("CAGR data not available")

with col2:
    st.subheader("Inter-Stock Correlation Matrix")
    if not corr_matrix.empty:
        # Filter correlation matrix to selected tickers
        avail_tickers = [t for t in selected_tickers if t in corr_matrix.columns]
        if avail_tickers:
            sub_corr = corr_matrix.loc[avail_tickers, avail_tickers]
            fig = make_heatmap(sub_corr, "")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Select tickers to see correlation")
    else:
        st.info("Correlation data not available")

# -- Volatility Analysis --
st.markdown("---")
st.subheader("30-Day Rolling Volatility")

fig = go.Figure()
for i, ticker in enumerate(selected_tickers):
    df_t = filtered[filtered["Ticker"] == ticker].sort_values("Date")
    if df_t.empty:
        continue
    vol = df_t["Daily_Return_Pct"].rolling(window=30).std()
    fig.add_trace(go.Scatter(
        x=df_t["Date"], y=vol,
        name=ticker_labels.get(ticker, ticker),
        line=dict(color=TATA_PALETTE[i % len(TATA_PALETTE)], width=1.5),
        fill="tozeroy" if i == 0 else None,
        fillcolor=f"rgba({30+i*40},{136-i*10},{229-i*20},0.05)" if i == 0 else None,
    ))
fig = apply_layout(fig, "", height=400)
fig.update_layout(yaxis_title="Volatility (Std Dev of Daily Returns)")
st.plotly_chart(fig, use_container_width=True)

# -- Volume Analysis --
st.subheader("TCS Trading Volume")
if not tcs_master.empty and "Volume" in tcs_master.columns:
    tcs_vol = tcs_master.dropna(subset=["Volume"])
    if not tcs_vol.empty:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=tcs_vol["Date"], y=tcs_vol["Volume"],
            marker=dict(
                color=tcs_vol["Daily_Return_Pct"].fillna(0).apply(
                    lambda x: "rgba(76,175,80,0.5)" if x >= 0 else "rgba(244,67,54,0.5)"
                ),
            ),
            name="Volume",
        ))
        fig.add_trace(go.Scatter(
            x=tcs_vol["Date"], y=tcs_vol["Close"],
            name="Close Price",
            yaxis="y2",
            line=dict(color="#FFB300", width=2),
        ))
        fig = apply_layout(fig, "", height=400)
        fig.update_layout(
            yaxis=dict(title="Volume"),
            yaxis2=dict(title="Close Price (INR)", overlaying="y", side="right"),
        )
        st.plotly_chart(fig, use_container_width=True)

# -- Data Table --
with st.expander("View Raw CAGR Data"):
    if not cagr.empty:
        st.dataframe(cagr, use_container_width=True, hide_index=True)
