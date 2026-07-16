import streamlit as st

from src.dashboard.utils.db import get_companies

st.title("📄 Annual Reports")

companies = get_companies()

ticker = st.selectbox(

    "Select Company",

    sorted(
        companies["id"].unique()
    )

)

years = [

    2024,
    2023,
    2022,
    2021,
    2020

]

st.subheader(
    f"Reports for {ticker}"
)

for year in years:

    st.write(

        f"📑 Annual Report {year}"

    )

    st.caption(

        "Report unavailable"

    )