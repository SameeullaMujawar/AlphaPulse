# ============================================================
# Project: AlphaPulse
# Week 2: Quantitative Analysis
# ============================================================

import pandas as pd
import numpy as np
from scipy.stats import skew, kurtosis

# -----------------------------
# Load Cleaned Data (from Week 1)
# -----------------------------
prices_df = pd.read_csv("../data/cleaned_adjusted_prices.csv", index_col=0, parse_dates=True)

print("Loaded cleaned price data.")

# -----------------------------
# Daily Log Returns
# -----------------------------
prices = prices_df.values
log_returns = np.log(prices[1:] / prices[:-1])

# -----------------------------
# Portfolio Statistics
# -----------------------------
mu = np.mean(log_returns, axis=0)
sigma = np.std(log_returns, axis=0)

portfolio_mu = np.mean(mu)
portfolio_sigma = np.mean(sigma)

# -----------------------------
# Monte Carlo Simulation
# -----------------------------
np.random.seed(42)

TRADING_DAYS = 252
SIMULATIONS = 10000

simulated_returns = np.random.normal(
    portfolio_mu,
    portfolio_sigma,
    (TRADING_DAYS, SIMULATIONS)
)

price_paths = np.exp(simulated_returns.cumsum(axis=0))
final_prices = price_paths[-1]

print("Monte Carlo simulation completed.")

# -----------------------------
# Statistical Validation
# -----------------------------
sim_skewness = skew(final_prices)
sim_kurtosis = kurtosis(final_prices)

print("\nStatistical Validation Results:")
print(f"Skewness : {sim_skewness:.4f}")
print(f"Kurtosis : {sim_kurtosis:.4f}")

# -----------------------------
# Value at Risk (95%)
# -----------------------------
VaR_95 = np.percentile(final_prices, 5)

print(f"\n95% Value at Risk (VaR): {VaR_95:.4f}")

# -----------------------------
# Summary
# -----------------------------
print("\nWeek 2 completed successfully.")
print("Simulations:", SIMULATIONS)
print("Time Horizon:", TRADING_DAYS, "trading days")
