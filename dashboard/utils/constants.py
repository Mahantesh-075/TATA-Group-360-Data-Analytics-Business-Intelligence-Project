"""
TATA Group 360 Analytics - Constants & Configuration
"""

# -- TATA Brand Colors --
TATA_BLUE = "#003B73"
TATA_BLUE_LIGHT = "#1E88E5"
TATA_BLUE_DARK = "#002244"
TATA_ACCENT = "#00BCD4"
TATA_GOLD = "#FFB300"
TATA_RED = "#E53935"
TATA_GREEN = "#43A047"
TATA_GRAY = "#78909C"

# Plotly color sequences
TATA_PALETTE = [
    "#1E88E5", "#E53935", "#43A047", "#FFB300", "#8E24AA",
    "#00ACC1", "#F4511E", "#6D4C41", "#3949AB", "#78909C",
    "#AD1457", "#00897B", "#FF6F00", "#546E7A", "#7CB342", "#D81B60"
]

SECTOR_COLORS = {
    "Technology": "#1E88E5",
    "Automotive": "#E53935",
    "Steel": "#757575",
    "Consumer & Retail": "#FB8C00",
    "Energy & Power": "#43A047",
    "Chemicals": "#8E24AA",
    "Financial Services": "#00ACC1",
    "Hospitality & Tourism": "#F4511E",
    "Telecom & Media": "#3949AB",
    "Infrastructure": "#6D4C41",
    "Aerospace & Defence": "#546E7A",
    "Trading & Investment": "#78909C",
    "Electronics & Semicon": "#AD1457",
    "Aviation": "#FF6F00",
    "E-commerce & Digital": "#00897B",
    "Healthcare": "#7CB342",
}

IT_PEER_COLORS = {
    "TCS": "#1E88E5",
    "Infosys": "#43A047",
    "Wipro": "#8E24AA",
    "HCL": "#E53935",
}

# -- Ticker mapping --
TATA_TICKERS = {
    "TCS": "Tata Consultancy Services",
    "TATASTEEL": "Tata Steel",
    "TATAPOWER": "Tata Power",
    "TATACOMM": "Tata Communications",
    "TATACONSUM": "Tata Consumer Products",
    "TATAINVEST": "Tata Investment Corp",
    "TATATECH": "Tata Technologies",
    "TATAMOTORS": "Tata Motors",
    "TATAMOTORS_PASS": "Tata Motors (Passengers)",
    "TATAMOTORS_COMM": "Tata Motors (Commercial)",
}

# -- KPI Values (FY2025) --
GROUP_REVENUE_USD_B = 180
GROUP_MARKET_CAP_USD_B = 328
GROUP_EMPLOYEES = "1,000,000+"
GROUP_LISTED_COMPANIES = 26
GROUP_GDP_CONTRIBUTION = "4.57%"
GROUP_SECTORS = 16
TCS_MARKET_CAP_INR_CR = "7,79,861"
TCS_REVENUE_USD_B = 29.5
TCS_EMPLOYEES_K = 608

# -- Chart layout defaults --
CHART_TEMPLATE = "plotly_dark"
CHART_FONT = dict(family="Inter, sans-serif", size=13)
CHART_BG = "rgba(0,0,0,0)"
CHART_PAPER_BG = "rgba(0,0,0,0)"
CHART_MARGIN = dict(l=40, r=40, t=60, b=40)

# -- Milestone events for annotations --
MILESTONES = [
    (1991, "Liberalization"),
    (2000, "Dot-com Bubble"),
    (2004, "TCS IPO"),
    (2007, "Corus $12.1B"),
    (2008, "JLR Acquired"),
    (2016, "Leadership Change"),
    (2020, "COVID-19"),
    (2022, "Air India Reacq."),
    (2024, "Dholera Fab"),
    (2026, "ASML + OpenAI"),
]
