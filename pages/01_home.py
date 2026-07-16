import streamlit as st
import plotly.express as px

from src.dashboard.utils.db import get_dashboard_data


st.title("🏠 Home")

df = get_dashboard_data()

years = sorted(
    df["year"].dropna().unique()
)

selected_year = st.sidebar.selectbox(
    "Select Year",
    years
)

df = df[
    df["year"] == selected_year
]

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(

        "Average ROE",

        round(
            df[
                "return_on_equity_pct"
            ].mean(),
            2
        )
    )

with col2:

    st.metric(

        "Median D/E",

        round(
            df[
                "debt_to_equity"
            ].median(),
            2
        )
    )

with col3:

    st.metric(

        "Companies",

        len(
            df[
                "company_id"
            ].unique()
        )
    )

col4, col5, col6 = st.columns(3)

with col4:

    st.metric(

        "Median P/E",

        round(
            df[
                "pe_ratio"
            ].median(),
            2
        )
    )

with col5:

    debt_free = len(

        df[
            df[
                "debt_to_equity"
            ] == 0
        ]

    )

    st.metric(

        "Debt-Free Companies",

        debt_free

    )

with col6:

    st.metric(

        "Median FCF",

        round(

            df[
                "free_cash_flow_cr"
            ].median(),

            2

        )

    )

st.subheader(
    "Sector Breakdown"
)

sector_data = (

    df

    .groupby(
        "broad_sector"
    )

    .size()

    .reset_index(
        name="count"
    )

)

fig = px.pie(

    sector_data,

    values="count",

    names="broad_sector",

    hole=0.5

)

st.plotly_chart(

    fig,

    use_container_width=True

)

st.subheader(

    "Top Companies by ROE"

)

top = (

    df

    .sort_values(

        "return_on_equity_pct",

        ascending=False

    )

    [

        [

            "company_id",

            "return_on_equity_pct",

            "debt_to_equity",

            "free_cash_flow_cr"

        ]

    ]

    .head(5)

)

st.dataframe(

    top,

    use_container_width=True

)