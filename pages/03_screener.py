import streamlit as st

from src.dashboard.utils.db import get_screener_data

st.title("🔍 Financial Screener")

df = get_screener_data()

st.sidebar.header("Filters")

roe_min = st.sidebar.slider(
    "ROE Min (%)",
    -20,
    50,
    15
)

de_max = st.sidebar.slider(
    "Debt / Equity Max",
    0.0,
    10.0,
    2.0
)

fcf_min = st.sidebar.slider(
    "Free Cash Flow Min",
    -10000,
    10000,
    0
)

filtered = df.copy()

filtered = filtered[
    filtered["return_on_equity_pct"] >= roe_min
]

filtered = filtered[
    filtered["debt_to_equity"] <= de_max
]

filtered = filtered[
    filtered["free_cash_flow_cr"] >= fcf_min
]

st.subheader(
    f"{len(filtered)} companies match your filters"
)

columns = [
    "company_id",
    "company_name",
    "broad_sector",
    "return_on_equity_pct",
    "debt_to_equity",
    "free_cash_flow_cr"
]

st.dataframe(
    filtered[columns],
    use_container_width=True
)

csv = filtered[columns].to_csv(index=False)

st.download_button(
    "⬇ Download CSV",
    csv,
    "screener_results.csv",
    "text/csv"
)