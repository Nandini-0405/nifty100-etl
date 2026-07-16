import streamlit as st
import plotly.graph_objects as go

from src.dashboard.utils.db import get_peer_data

st.title("🤝 Peer Comparison")

df = get_peer_data()

groups = sorted(
    df["peer_group_name"]
    .dropna()
    .unique()
)

selected_group = st.selectbox(
    "Peer Group",
    groups
)

group_df = df[
    df["peer_group_name"] == selected_group
]

companies = sorted(
    group_df["company_id"].unique()
)

selected_company = st.selectbox(
    "Company",
    companies
)

row = group_df[
    group_df["company_id"] == selected_company
].iloc[0]

metrics = [
    "return_on_equity_pct",
    "net_profit_margin_pct",
    "debt_to_equity",
    "asset_turnover",
    "interest_coverage",
    "free_cash_flow_cr"
]

company_values = [
    row[m]
    for m in metrics
]

peer_values = [
    group_df[m].mean()
    for m in metrics
]

fig = go.Figure()

fig.add_trace(
    go.Scatterpolar(
        r=company_values,
        theta=metrics,
        fill="toself",
        name=selected_company
    )
)

fig.add_trace(
    go.Scatterpolar(
        r=peer_values,
        theta=metrics,
        name="Peer Average"
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.dataframe(
    group_df,
    use_container_width=True
)