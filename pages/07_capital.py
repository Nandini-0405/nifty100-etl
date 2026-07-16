import streamlit as st
import plotly.express as px
import pandas as pd

st.title("💰 Capital Allocation")

patterns = pd.DataFrame(

    {

        "pattern": [

            "Growth",

            "Dividend",

            "Debt Reduction",

            "Capex",

            "Turnaround"

        ],

        "count": [

            20,

            18,

            15,

            25,

            14

        ]

    }

)

fig = px.treemap(

    patterns,

    path=["pattern"],

    values="count"

)

st.plotly_chart(

    fig,

    use_container_width=True

)