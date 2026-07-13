import sqlite3
import pandas as pd

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    debt_to_equity,
    interest_coverage,
    asset_turnover
)

from src.analytics.cashflow_kpis import free_cash_flow


# -----------------------------
# Database Connection
# -----------------------------

conn = sqlite3.connect("db/nifty100.db")


# -----------------------------
# Load Tables
# -----------------------------

pl = pd.read_sql(
    "SELECT * FROM profitandloss",
    conn
)

bs = pd.read_sql(
    "SELECT * FROM balancesheet",
    conn
)

cf = pd.read_sql(
    "SELECT * FROM cashflow",
    conn
)

mc = pd.read_sql(
    "SELECT * FROM market_cap",
    conn
)


# -----------------------------
# Fix Year Columns
# -----------------------------

pl["year"] = (
    pl["year"]
    .astype(str)
    .str.extract(r"(\d{4})")[0]
)

bs["year"] = (
    bs["year"]
    .astype(str)
    .str.extract(r"(\d{4})")[0]
)

cf["year"] = (
    cf["year"]
    .astype(str)
    .str.extract(r"(\d{4})")[0]
)

mc["year"] = mc["year"].astype(str)


# -----------------------------
# Merge Tables
# -----------------------------

df = pl.merge(
    bs,
    on=["company_id", "year"],
    suffixes=("_pl", "_bs")
)

df = df.merge(
    cf,
    on=["company_id", "year"]
)

df = df.merge(
    mc,
    on=["company_id", "year"],
    suffixes=("", "_mc")
)


# -----------------------------
# Compute Ratios
# -----------------------------

df["net_profit_margin_pct"] = df.apply(
    lambda x: net_profit_margin(
        x["net_profit"],
        x["sales"]
    ),
    axis=1
)

df["operating_profit_margin_pct"] = df.apply(
    lambda x: operating_profit_margin(
        x["operating_profit"],
        x["sales"]
    ),
    axis=1
)

df["return_on_equity_pct"] = df.apply(
    lambda x: return_on_equity(
        x["net_profit"],
        x["equity_capital"],
        x["reserves"]
    ),
    axis=1
)

df["debt_to_equity"] = df.apply(
    lambda x: debt_to_equity(
        x["borrowings"],
        x["equity_capital"],
        x["reserves"]
    ),
    axis=1
)

df["interest_coverage"] = df.apply(
    lambda x: interest_coverage(
        x["operating_profit"],
        x["other_income"],
        x["interest"]
    ),
    axis=1
)

df["asset_turnover"] = df.apply(
    lambda x: asset_turnover(
        x["sales"],
        x["total_assets"]
    ),
    axis=1
)

df["free_cash_flow_cr"] = df.apply(
    lambda x: free_cash_flow(
        x["operating_activity"],
        x["investing_activity"]
    ),
    axis=1
)


# -----------------------------
# Extra Metrics
# -----------------------------

df["dividend_payout_ratio_pct"] = df[
    "dividend_payout"
]

df["pe_ratio"] = df[
    "pe_ratio"
]

df["pb_ratio"] = df[
    "pb_ratio"
]

df["dividend_yield_pct"] = df[
    "dividend_yield_pct"
]


# -----------------------------
# Save to Database
# -----------------------------

df.to_sql(
    "financial_ratios",
    conn,
    if_exists="replace",
    index=False
)

print("\nfinancial_ratios updated successfully!")

print(
    "Rows inserted:",
    len(df)
)

print(
    "\nColumns:"
)

print(
    df.columns.tolist()
)

conn.close()
