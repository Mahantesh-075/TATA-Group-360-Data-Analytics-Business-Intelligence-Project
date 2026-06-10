"""
TATA Group 360 Analytics - Data Ingestion Pipeline
====================================================
Reads all raw data files (CSV + HTML-disguised XLS), standardizes
column names and date formats, merges overlapping datasets, and
exports cleaned data to data/processed/.

Usage:
    python scripts/data_ingestion.py
"""

import os
import sys
import pandas as pd
import numpy as np
from pathlib import Path

# Force UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# -- Paths --
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
RAW_DIR = PROJECT_DIR.parent  # parent TATA folder with source files
PROCESSED_DIR = PROJECT_DIR / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def parse_dates(series: pd.Series) -> pd.Series:
    """Robustly parse dates in multiple formats."""
    for fmt in ["%Y-%m-%d", "%d-%m-%Y", "%m-%d-%Y", "%d/%m/%Y", "%Y/%m/%d"]:
        try:
            return pd.to_datetime(series, format=fmt)
        except (ValueError, TypeError):
            continue
    return pd.to_datetime(series, format="mixed", errors="coerce")


def load_csv(filename: str, date_col: str = "Date") -> pd.DataFrame:
    """Load a CSV file from the raw data directory."""
    filepath = RAW_DIR / filename
    if not filepath.exists():
        print(f"  [WARN] File not found: {filepath}")
        return pd.DataFrame()
    df = pd.read_csv(filepath)
    if date_col in df.columns:
        df[date_col] = parse_dates(df[date_col])
        df = df.dropna(subset=[date_col])
        df = df.sort_values(date_col).reset_index(drop=True)
    return df


def load_html_xls(filename: str) -> pd.DataFrame:
    """Load HTML-disguised XLS files using pd.read_html()."""
    filepath = RAW_DIR / filename
    if not filepath.exists():
        print(f"  [WARN] File not found: {filepath}")
        return pd.DataFrame()
    tables = pd.read_html(str(filepath))
    if not tables:
        print(f"  [WARN] No tables found in: {filepath}")
        return pd.DataFrame()
    df = tables[0]
    df.columns = ["Date", "Close"]
    df["Date"] = parse_dates(df["Date"])
    df = df.dropna(subset=["Date"])
    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
    df = df.dropna(subset=["Close"])
    df = df.sort_values("Date").reset_index(drop=True)
    return df


def process_tcs_master():
    """
    Create a master TCS dataset by merging all TCS data sources.
    Priority: TCS_NSE_2004-2025.csv (richest) > tcs_df.csv > TCS.NS.csv > tcs.xls
    """
    print("\n[STEP] Processing TCS Master Dataset...")

    # Source 1: TCS_NSE_2004-2025.csv (5343 rows, 15 cols)
    df1 = load_csv("TCS_NSE_2004-2025.csv")
    if not df1.empty:
        df1 = df1.rename(columns={"Daily_Return_%": "Daily_Return_Pct"})
        core_cols = ["Date", "Open", "High", "Low", "Close", "Volume",
                     "Turnover", "VWAP", "Daily_Return_Pct", "MA_20", "MA_50"]
        available = [c for c in core_cols if c in df1.columns]
        df1 = df1[available]

    # Source 2: tcs_df.csv (4048 rows, 2004-2020)
    df2 = load_csv("tcs_df.csv")
    if not df2.empty:
        df2 = df2[["Date", "Open", "High", "Low", "Close", "Volume"]].copy()

    # Source 3: TCS.NS.csv (1229 rows, 2015-2020)
    df3 = load_csv("TCS.NS.csv")
    if not df3.empty:
        df3 = df3[["Date", "Open", "High", "Low", "Close", "Volume"]].copy()

    # Source 4: tcs.xls (4957 rows, Date + Close price)
    df4 = load_html_xls("tcs.xls")

    # Strategy: Use df1 as primary (richest). Fill gaps from others.
    master = df1.copy() if not df1.empty else pd.DataFrame()

    if master.empty and not df2.empty:
        master = df2.copy()
    elif not df2.empty:
        existing_dates = set(master["Date"].dt.date)
        new_rows = df2[~df2["Date"].dt.date.isin(existing_dates)]
        if not new_rows.empty:
            cols_to_use = [c for c in ["Date", "Open", "High", "Low", "Close", "Volume"] if c in new_rows.columns]
            master = pd.concat([master, new_rows[cols_to_use]], ignore_index=True)

    master = master.sort_values("Date").reset_index(drop=True)
    master = master.drop_duplicates(subset=["Date"], keep="first")

    # Compute derived columns if missing
    if "Daily_Return_Pct" not in master.columns:
        master["Daily_Return_Pct"] = master["Close"].pct_change() * 100
    if "MA_20" not in master.columns:
        master["MA_20"] = master["Close"].rolling(window=20).mean()
    if "MA_50" not in master.columns:
        master["MA_50"] = master["Close"].rolling(window=50).mean()
    if "Volatility_30d" not in master.columns:
        master["Volatility_30d"] = master["Daily_Return_Pct"].rolling(window=30).std()

    out_path = PROCESSED_DIR / "tcs_master.csv"
    master.to_csv(out_path, index=False)
    print(f"  [OK] TCS Master: {master.shape[0]} rows, {master.shape[1]} cols -> {out_path.name}")
    return master


def process_tata_stocks():
    """Process all TATA subsidiary stock data from HTML-XLS files."""
    print("\n[STEP] Processing TATA Subsidiary Stock Data...")

    xls_files = {
        "tata steel.xls": "TATASTEEL",
        "tata power.xls": "TATAPOWER",
        "tata communication.xls": "TATACOMM",
        "tata consumers.xls": "TATACONSUM",
        "tata investments.xls": "TATAINVEST",
        "tata tech.xls": "TATATECH",
        "tata moters passengers.xls": "TATAMOTORS_PASS",
        "tata moters.xls": "TATAMOTORS_COMM",
    }

    all_stocks = {}
    combined_frames = []

    for filename, ticker in xls_files.items():
        df = load_html_xls(filename)
        if df.empty:
            continue
        df["Ticker"] = ticker
        df["Daily_Return_Pct"] = df["Close"].pct_change() * 100
        df["MA_20"] = df["Close"].rolling(window=20).mean()
        df["MA_50"] = df["Close"].rolling(window=50).mean()

        all_stocks[ticker] = df
        combined_frames.append(df)
        print(f"  [OK] {ticker}: {df.shape[0]} rows, {df['Date'].min().date()} -> {df['Date'].max().date()}")

    # Also add TATAMOTORS.NS.csv (OHLCV format)
    df_motors = load_csv("TATAMOTORS.NS.csv")
    if not df_motors.empty:
        df_motors["Ticker"] = "TATAMOTORS"
        df_motors["Daily_Return_Pct"] = df_motors["Close"].pct_change() * 100
        df_motors["MA_20"] = df_motors["Close"].rolling(window=20).mean()
        df_motors["MA_50"] = df_motors["Close"].rolling(window=50).mean()
        all_stocks["TATAMOTORS"] = df_motors
        combined_frames.append(df_motors[["Date", "Close", "Ticker", "Daily_Return_Pct", "MA_20", "MA_50"]])
        print(f"  [OK] TATAMOTORS (CSV): {df_motors.shape[0]} rows")

    # Also load TCS from tcs.xls for the combined set
    df_tcs_xls = load_html_xls("tcs.xls")
    if not df_tcs_xls.empty:
        df_tcs_xls["Ticker"] = "TCS"
        df_tcs_xls["Daily_Return_Pct"] = df_tcs_xls["Close"].pct_change() * 100
        df_tcs_xls["MA_20"] = df_tcs_xls["Close"].rolling(window=20).mean()
        df_tcs_xls["MA_50"] = df_tcs_xls["Close"].rolling(window=50).mean()
        all_stocks["TCS"] = df_tcs_xls
        combined_frames.append(df_tcs_xls)
        print(f"  [OK] TCS (XLS): {df_tcs_xls.shape[0]} rows")

    # Save individual stock files
    for ticker, df in all_stocks.items():
        out_path = PROCESSED_DIR / f"{ticker.lower()}.csv"
        df.to_csv(out_path, index=False)

    # Save combined long-format file
    if combined_frames:
        combined = pd.concat(combined_frames, ignore_index=True)
        combined.to_csv(PROCESSED_DIR / "tata_stocks_combined.csv", index=False)
        print(f"  [OK] Combined: {combined.shape[0]} rows -> tata_stocks_combined.csv")

    return all_stocks


def process_infosys():
    """Process Infosys data for peer comparison."""
    print("\n[STEP] Processing Infosys Data...")

    df = load_csv("infy_df.csv")
    if df.empty:
        return df

    df["Daily_Return_Pct"] = df["Close"].pct_change() * 100
    df["MA_20"] = df["Close"].rolling(window=20).mean()
    df["MA_50"] = df["Close"].rolling(window=50).mean()
    df["Ticker"] = "INFY"

    out_path = PROCESSED_DIR / "infosys.csv"
    df.to_csv(out_path, index=False)
    print(f"  [OK] Infosys: {df.shape[0]} rows, {df['Date'].min().date()} -> {df['Date'].max().date()}")
    return df


def create_correlation_matrix():
    """Build a correlation matrix of daily returns across all TATA stocks."""
    print("\n[STEP] Building Stock Correlation Matrix...")

    combined_path = PROCESSED_DIR / "tata_stocks_combined.csv"
    if not combined_path.exists():
        print("  [WARN] Combined stocks file not found, skipping correlation")
        return pd.DataFrame()

    combined = pd.read_csv(combined_path, parse_dates=["Date"])

    # Pivot to wide format
    pivot = combined.pivot_table(index="Date", columns="Ticker", values="Close", aggfunc="first")
    returns = pivot.pct_change().dropna(how="all")

    corr = returns.corr()
    corr.to_csv(PROCESSED_DIR / "stock_correlation_matrix.csv")
    print(f"  [OK] Correlation matrix: {corr.shape[0]}x{corr.shape[1]} tickers")

    returns.to_csv(PROCESSED_DIR / "stock_daily_returns.csv")
    print(f"  [OK] Daily returns matrix: {returns.shape[0]} days x {returns.shape[1]} tickers")

    return corr


def compute_cagr_table():
    """Compute CAGR for each TATA stock over 5-year and 10-year horizons."""
    print("\n[STEP] Computing CAGR Table...")

    combined_path = PROCESSED_DIR / "tata_stocks_combined.csv"
    if not combined_path.exists():
        print("  [WARN] Combined stocks file not found, skipping CAGR")
        return pd.DataFrame()

    combined = pd.read_csv(combined_path, parse_dates=["Date"])
    tickers = combined["Ticker"].unique()

    results = []
    for ticker in tickers:
        df = combined[combined["Ticker"] == ticker].sort_values("Date")
        if df.empty:
            continue

        latest = df.iloc[-1]
        latest_price = latest["Close"]
        latest_date = latest["Date"]

        for years, label in [(5, "5Y"), (10, "10Y"), (15, "15Y")]:
            target_date = latest_date - pd.DateOffset(years=years)
            past = df[df["Date"] <= target_date]
            if past.empty:
                continue
            past_price = past.iloc[-1]["Close"]
            if past_price > 0:
                cagr = ((latest_price / past_price) ** (1 / years) - 1) * 100
                results.append({
                    "Ticker": ticker,
                    "Period": label,
                    "Start_Price": round(past_price, 2),
                    "End_Price": round(latest_price, 2),
                    "CAGR_Pct": round(cagr, 2),
                })

    cagr_df = pd.DataFrame(results)
    cagr_df.to_csv(PROCESSED_DIR / "cagr_table.csv", index=False)
    print(f"  [OK] CAGR table: {len(results)} entries")
    return cagr_df


def main():
    """Run the full data ingestion pipeline."""
    print("=" * 60)
    print("  TATA Group 360 Analytics - Data Ingestion Pipeline")
    print("=" * 60)
    print(f"  Source directory: {RAW_DIR}")
    print(f"  Output directory: {PROCESSED_DIR}")

    tcs = process_tcs_master()
    stocks = process_tata_stocks()
    infy = process_infosys()
    corr = create_correlation_matrix()
    cagr = compute_cagr_table()

    print("\n" + "=" * 60)
    print("  [DONE] Data ingestion complete!")
    print(f"  Output files in: {PROCESSED_DIR}")
    print("=" * 60)

    for f in sorted(PROCESSED_DIR.glob("*.csv")):
        size_kb = f.stat().st_size / 1024
        print(f"    {f.name:40s} {size_kb:>8.1f} KB")


if __name__ == "__main__":
    main()
