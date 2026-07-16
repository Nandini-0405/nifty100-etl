import streamlit as st
import plotly.express as px

from src.dashboard.utils.db import (
    get_companies,
    get_ratios
)

st.title("📈 Trend Analysis")

companies = get_companies()

ticker = st.selectbox(
    "Select Company",
    sorted(companies["id"].unique())
)

df = get_ratios(ticker)

metric_map = {

    "ROE": "return_on_equity_pct",

    "Net Profit Margin": "net_profit_margin_pct",

    "Debt to Equity": "debt_to_equity",

    "Asset Turnover": "asset_turnover",

    "Interest Coverage": "interest_coverage",

    "Free Cash Flow": "free_cash_flow_cr"

}

selected_metrics = st.multiselect(

    "Select up to 3 metrics",

    list(metric_map.keys()),

    default=["ROE"]

)

if len(selected_metrics) > 3:

    st.warning(
        "Select only 3 metrics."
    )

else:

    chart_df = df[
        ["year"] +
        [
            metric_map[m]
            for m in selected_metrics
        ]
    ]

    fig = px.line(

        chart_df,

        x="year",

        y=[
            metric_map[m]
            for m in selected_metrics
        ],

        markers=True

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )