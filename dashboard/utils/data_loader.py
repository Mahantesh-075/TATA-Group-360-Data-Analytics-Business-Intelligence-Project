"""
TATA Group 360 Analytics - Data Loader (cached)
"""

import pandas as pd
import streamlit as st
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
PROCESSED_DIR = DATA_DIR / "processed"
CURATED_DIR = DATA_DIR / "curated"


@st.cache_data(ttl=3600)
def load_tcs_master():
    return pd.read_csv(PROCESSED_DIR / "tcs_master.csv", parse_dates=["Date"])


@st.cache_data(ttl=3600)
def load_tata_stocks_combined():
    return pd.read_csv(PROCESSED_DIR / "tata_stocks_combined.csv", parse_dates=["Date"])


@st.cache_data(ttl=3600)
def load_infosys():
    return pd.read_csv(PROCESSED_DIR / "infosys.csv", parse_dates=["Date"])


@st.cache_data(ttl=3600)
def load_correlation_matrix():
    return pd.read_csv(PROCESSED_DIR / "stock_correlation_matrix.csv", index_col=0)


@st.cache_data(ttl=3600)
def load_cagr_table():
    return pd.read_csv(PROCESSED_DIR / "cagr_table.csv")


@st.cache_data(ttl=3600)
def load_stock(ticker: str):
    path = PROCESSED_DIR / f"{ticker.lower()}.csv"
    if path.exists():
        return pd.read_csv(path, parse_dates=["Date"])
    return pd.DataFrame()


@st.cache_data(ttl=3600)
def load_daily_returns():
    path = PROCESSED_DIR / "stock_daily_returns.csv"
    if path.exists():
        return pd.read_csv(path, parse_dates=["Date"], index_col="Date")
    return pd.DataFrame()


# -- Curated datasets --

@st.cache_data(ttl=3600)
def load_sectors():
    return pd.read_csv(CURATED_DIR / "tata_group_sectors.csv")


@st.cache_data(ttl=3600)
def load_acquisitions():
    return pd.read_csv(CURATED_DIR / "acquisitions.csv")


@st.cache_data(ttl=3600)
def load_gdp():
    return pd.read_csv(CURATED_DIR / "india_gdp.csv")


@st.cache_data(ttl=3600)
def load_it_peers():
    return pd.read_csv(CURATED_DIR / "it_peers.csv")


@st.cache_data(ttl=3600)
def load_tcs_verticals():
    return pd.read_csv(CURATED_DIR / "tcs_revenue_verticals.csv")


@st.cache_data(ttl=3600)
def load_tcs_geo():
    return pd.read_csv(CURATED_DIR / "tcs_geo_revenue.csv")


@st.cache_data(ttl=3600)
def load_ev_market():
    return pd.read_csv(CURATED_DIR / "ev_market_share.csv")


@st.cache_data(ttl=3600)
def load_jlr_roi():
    return pd.read_csv(CURATED_DIR / "jlr_roi.csv")


@st.cache_data(ttl=3600)
def load_tata_power_renewables():
    return pd.read_csv(CURATED_DIR / "tata_power_renewables.csv")


@st.cache_data(ttl=3600)
def load_ai_semiconductor():
    return pd.read_csv(CURATED_DIR / "tata_ai_semiconductor.csv")
