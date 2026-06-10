# The TATA Empire: A 360-Degree Data-Driven Analysis

> **A comprehensive data analytics & business intelligence project on India's largest conglomerate**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit)](https://streamlit.io)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive-3F4F75?logo=plotly)](https://plotly.com)

---

## Project Overview

This project delivers a **5-module interactive dashboard** analyzing the TATA Group across:
- **16 industry sectors** generating **$180B revenue**
- **26 listed companies** with **$328B combined market cap**
- **1 million+ employees** across 100+ countries
- **20 years** of stock market data (2004–2026)

### Why This Project?

The TATA Group is not just a company — it contributes **4.57% of India's GDP**. This project treats the conglomerate as a business intelligence case study, the kind of work TCS delivers to Fortune 500 clients globally.

---

## Dashboard Modules

### Module 1: Conglomerate Overview
- Revenue treemap by sector (16 sectors)
- Market cap and employee distribution
- TATA Revenue vs India GDP (1991–2025) with milestone annotations
- GDP contribution percentage timeline

### Module 2: Stock Analysis
- Multi-stock price comparison (9 TATA subsidiaries)
- Normalized returns (Base 100) analysis
- CAGR comparison (5Y, 10Y, 15Y)
- Inter-stock correlation matrix heatmap
- 30-day rolling volatility analysis
- Volume/price overlay for TCS

### Module 3: IT Sector Dominance (TCS Deep-Dive)
- TCS vs Infosys vs Wipro vs HCL: Revenue, profit, margins (FY05–FY25)
- Employee headcount & revenue-per-employee efficiency
- TCS revenue by industry vertical (BFSI 31.9%, Consumer 15.4%, etc.)
- TCS geographic revenue split (North America 32.4%, UK 15.2%, etc.)
- Revenue gap analysis: TCS vs nearest competitor

### Module 4: Acquisitions Timeline
- Interactive M&A timeline (2000–2024, 18 deals)
- Deal value bubble chart by sector
- Leadership era comparison (Ratan Tata vs N. Chandrasekaran)
- Cumulative M&A investment curve ($27B+)
- **JLR Turnaround Case Study** — from GBP 1.15B acquisition to GBP 29B revenue

### Module 5: Future Growth & AI Strategy
- **ASML-Tata Electronics partnership** (May 2026) — Dholera fab lithography
- **OpenAI partnership** (Feb 2026) — Enterprise AI transformation
- **Dholera Semiconductor Fab** — $11B, 50K wafers/month, construction timeline
- EV market share: Tata Motors dominance (48% India share)
- Tata Power renewables & EV charging network growth
- **TCS ARIMA stock price forecast** with 95% confidence interval
- Full AI roadmap: Hardware → Infrastructure → Applications layers

---

## Tech Stack

| Category | Technologies |
|----------|-------------|
| **Core** | Python 3.10+, pandas, numpy |
| **Visualization** | Plotly, Matplotlib, Seaborn |
| **Dashboard** | Streamlit |
| **Forecasting** | statsmodels (ARIMA) |
| **Data** | xlrd, lxml, html5lib, openpyxl |

---

## Quick Start

```bash
# Clone repository
git clone <repo-url>
cd tata-analytics

# Install dependencies
pip install -r requirements.txt

# Run data ingestion pipeline
python scripts/data_ingestion.py

# Launch dashboard
streamlit run dashboard/app.py
```

---

## Project Structure

```
tata-analytics/
├── .gitignore
├── README.md
├── requirements.txt
├── data/
│   ├── raw/                    # Source CSV/XLS files
│   ├── processed/              # Cleaned data (auto-generated)
│   │   ├── tcs_master.csv      # 5224 rows, 12 columns
│   │   ├── tata_stocks_combined.csv  # 36K+ rows, all subsidiaries
│   │   ├── stock_correlation_matrix.csv
│   │   ├── cagr_table.csv
│   │   └── ...
│   └── curated/                # Hand-built analysis datasets
│       ├── acquisitions.csv    # 18 major M&A deals (2000-2024)
│       ├── india_gdp.csv       # GDP vs TATA revenue (1991-2025)
│       ├── it_peers.csv        # TCS/Infosys/Wipro/HCL (21 years)
│       ├── tata_ai_semiconductor.csv  # AI & semiconductor initiatives
│       ├── ev_market_share.csv
│       ├── jlr_roi.csv
│       └── ...
├── scripts/
│   └── data_ingestion.py       # Full ETL pipeline
├── dashboard/
│   ├── app.py                  # Streamlit entry point (Home)
│   ├── pages/
│   │   ├── 01_Conglomerate_Overview.py
│   │   ├── 02_Stock_Analysis.py
│   │   ├── 03_IT_Dominance.py
│   │   ├── 04_Acquisitions_Timeline.py
│   │   └── 05_Future_Growth_AI.py
│   └── utils/
│       ├── constants.py        # Colors, tickers, KPIs
│       ├── data_loader.py      # Cached data functions
│       └── chart_factory.py    # Reusable Plotly builders
└── assets/
    └── plots/                  # Static exports
```

---

## Data Sources

| Source | Type | Usage |
|--------|------|-------|
| NSE India / Yahoo Finance | Stock OHLCV | 8 TATA subsidiaries (2004-2026) |
| Kaggle (TCS Market Data) | Stock Dataset | TCS daily data with engineered features |
| Screener.in / Macrotrends | Financials | TCS, Infosys, Wipro, HCL peer data |
| World Bank | GDP Data | India GDP 1991-2025 |
| TATA Annual Reports | Revenue | Group financials, sector breakdown |
| IBEF / NASSCOM | Industry Reports | IT sector sizing, EV market data |
| TCS Investor Relations | Quarterly | Revenue verticals, geographic split |
| ASML / OpenAI / Tata.com | Press Releases | AI & semiconductor partnerships |

---

## Key Findings

### Boom Factors
1. **TCS 20-year growth**: From INR 7,000 Cr to $100B market cap (20x+)
2. **JLR turnaround**: GBP 1.15B "risky bet" → GBP 29B revenue by 2024
3. **GDP contribution**: TATA Group net worth grew 45x vs India GDP 15x since 1991
4. **EV dominance**: Tata Motors holds 48% of India's EV market
5. **AI infrastructure**: $11B Dholera fab + 1GW HyperVault data centers

### Pitfalls Identified
1. **Corus Steel overpayment**: $12.1B acquisition required major restructuring
2. **Commodity exposure**: Steel and power segments vulnerable to price cycles
3. **EV market share erosion**: Down from 73% (2022) to 48% (2025) as Mahindra, BYD enter
4. **Semiconductor execution risk**: India's first fab carries significant technology transfer challenges

---

## Author

**Mahantesh** (1DA23EC075)  
B.E. ECE, 6th Semester  
DR. AIT, Bengaluru  
*Portfolio project for TCS NQT Campus Recruitment*

---

## License

This project is for educational and portfolio purposes. Data sourced from public datasets and APIs.
