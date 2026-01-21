# ============================================================
# Project: AlphaPulse
# Week 1: Data Acquisition & Cleaning
# ============================================================

import yfinance as yf
import pandas as pd
import time

# -----------------------------
# Portfolio Planning
# -----------------------------
TICKERS = [
    "AAPL", "MSFT", "META", "AMZN", "TSLA",
    "JPM", "XOM", "NKE", "JNJ", "^GSPC"
]

START_DATE = "2019-01-01"
END_DATE = "2024-01-01"

# -----------------------------
# Robust Data Fetching Function
# -----------------------------
def fetch_data(ticker, retries=3, delay=5):
    for attempt in range(retries):
        try:
            df = yf.download(
                ticker,
                start=START_DATE,
                end=END_DATE,
                auto_adjust=False,   # keeps splits & dividends
                progress=False
            )
            if not df.empty:
                return df
        except Exception as e:
            print(f"[{ticker}] Attempt {attempt+1} failed: {e}")
            time.sleep(delay)
    print(f"[{ticker}] Failed after retries.")
    return None

# -----------------------------
# Fetch Data
# -----------------------------
print("Fetching historical market data...")
raw_data = {}

for ticker in TICKERS:
    raw_data[ticker] = fetch_data(ticker)

# -----------------------------
# Build Adjusted Close DataFrame
# -----------------------------
adj_close = pd.DataFrame()

for ticker, df in raw_data.items():
    if df is not None and "Adj Close" in df.columns:
        adj_close[ticker] = df["Adj Close"]
    else:
        print(f"Skipping {ticker} due to missing data")

# -----------------------------
# Data Cleaning
# -----------------------------
adj_close = adj_close.sort_index()
adj_close = adj_close.ffill().dropna()

# -----------------------------
# Data Quality Checks
# -----------------------------
assert not adj_close.empty, "Adjusted Close data is empty"
assert adj_close.isnull().sum().sum() == 0, "Missing values found"
assert adj_close.index.is_monotonic_increasing, "Date index error"

# -----------------------------
# Save Cleaned Data
# -----------------------------
adj_close.to_csv("../data/cleaned_adjusted_prices.csv")

print("Week 1 completed successfully.")
print("Output file: cleaned_adjusted_prices.csv")
