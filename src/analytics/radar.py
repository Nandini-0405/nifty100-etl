import os
import sqlite3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


os.makedirs(
    "reports/radar_charts",
    exist_ok=True
)

conn = sqlite3.connect(
    "db/nifty100.db"
)

df = pd.read_sql(
    """
    SELECT
        company_id,
        peer_group_name,
        return_on_equity_pct,
        net_profit_margin_pct,
        debt_to_equity,
        asset_turnover,
        interest_coverage,
        free_cash_flow_cr
    FROM peer_percentiles
    """,
    conn
)

metrics = [

    "return_on_equity_pct",

    "net_profit_margin_pct",

    "debt_to_equity",

    "asset_turnover",

    "interest_coverage",

    "free_cash_flow_cr"

]

peer_average = (

    df

    .groupby(
        "peer_group_name"
    )[metrics]

    .mean()

)

companies = df["company_id"].unique()

for company in companies:

    company_df = df[
        df["company_id"] == company
    ]

    row = company_df.iloc[0]

    peer_group = row[
        "peer_group_name"
    ]

    values = [

        row[m]

        for m in metrics

    ]

    avg_values = [

        peer_average.loc[
            peer_group,
            m
        ]

        for m in metrics

    ]

    values += values[:1]

    avg_values += avg_values[:1]

    angles = np.linspace(

        0,

        2 * np.pi,

        len(metrics),

        endpoint=False

    ).tolist()

    angles += angles[:1]

    plt.figure(
        figsize=(7, 7)
    )

    ax = plt.subplot(
        111,
        polar=True
    )

    ax.plot(
        angles,
        values
    )

    ax.fill(
        angles,
        values,
        alpha=0.25
    )

    ax.plot(
        angles,
        avg_values,
        linestyle="--"
    )

    ax.set_xticks(
        angles[:-1]
    )

    ax.set_xticklabels(
        metrics
    )

    plt.title(
        f"{company}\n{peer_group}"
    )

    plt.savefig(

        f"reports/radar_charts/{company}_radar.png"

    )

    plt.close()

print(
    "Radar charts generated!"
)

conn.close()