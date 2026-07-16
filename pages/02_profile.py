import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from src.dashboard.utils.db import (
    get_companies,
    get_ratios,
    get_pl
)

st.title("👤 Company Profile")

companies = get_companies()

ticker = st.selectbox(
    "Select Company",
    sorted(companies["id"].unique())
)

ratios = get_ratios(ticker)
pl = get_pl(ticker)

if ratios.empty:

    st.warning(
        "Ticker not found — please try another."
    )

    st.stop()

latest = ratios.sort_values(
    "year"
).iloc[-1]

st.subheader(f"📌 {ticker}")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "ROE",
        round(
            latest["return_on_equity_pct"],
            2
        )
    )

with col2:

    st.metric(
        "Net Profit Margin",
        round(
            latest["net_profit_margin_pct"],
            2
        )
    )

with col3:

    st.metric(
        "Debt / Equity",
        round(
            latest["debt_to_equity"],
            2
        )
    )

col4, col5, col6 = st.columns(3)

with col4:

    st.metric(
        "Asset Turnover",
        round(
            latest["asset_turnover"],
            2
        )
    )

with col5:

    st.metric(
        "Interest Coverage",
        round(
            latest["interest_coverage"],
            2
        )
    )

with col6:

    st.metric(
        "Free Cash Flow",
        round(
            latest["free_cash_flow_cr"],
            2
        )
    )

st.subheader("Revenue Trend")

fig1 = px.bar(
    pl,
    x="year",
    y="sales"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

st.subheader("Net Profit Trend")

fig2 = px.bar(
    pl,
    x="year",
    y="net_profit"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.subheader("ROE Trend")

fig3 = go.Figure()

fig3.add_trace(

    go.Scatter(

        x=ratios["year"],

        y=ratios["return_on_equity_pct"],

        mode="lines+markers",

        name="ROE"

    )

)

st.plotly_chart(
    fig3,
    use_container_width=True
)