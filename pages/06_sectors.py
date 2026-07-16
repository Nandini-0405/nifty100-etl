import streamlit as st
import plotly.express as px

from src.dashboard.utils.db import get_sector_analysis

st.title("🏭 Sector Analysis")

df = get_sector_analysis()

sector = st.selectbox(

    "Select Sector",

    sorted(
        df["broad_sector"]
        .dropna()
        .unique()
    )

)

sector_df = df[
    df["broad_sector"] == sector
]

fig = px.scatter(

    sector_df,

    x="sales",

    y="return_on_equity_pct",

    size="market_cap_crore",

    hover_name="company_id"

)

st.plotly_chart(

    fig,

    use_container_width=True

)

st.subheader(
    "Sector Median KPIs"
)

st.write(

    sector_df[
        [
            "sales",
            "return_on_equity_pct",
            "market_cap_crore"
        ]
    ].median()

)