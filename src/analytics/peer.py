import sqlite3
import pandas as pd

conn = sqlite3.connect(
    "db/nifty100.db"
)

# -------------------------
# Load financial ratios
# -------------------------

ratios = pd.read_sql(
    """
    SELECT
        company_id,
        year,
        return_on_equity_pct,
        net_profit_margin_pct,
        debt_to_equity,
        asset_turnover,
        interest_coverage,
        free_cash_flow_cr
    FROM financial_ratios
    """,
    conn
)

# -------------------------
# Load peer groups
# -------------------------

peers = pd.read_sql(
    """
    SELECT
        company_id,
        peer_group_name,
        is_benchmark
    FROM peer_groups
    """,
    conn
)

print(
    "Ratios rows:",
    len(ratios)
)

print(
    "Peer rows:",
    len(peers)
)
# -------------------------
# Merge tables
# -------------------------

df = ratios.merge(
    peers,
    on="company_id",
    how="left"
)

df["peer_group_name"] = df[
    "peer_group_name"
].fillna(
    "No peer group assigned"
)

print(
    "\nUnique Peer Groups:"
)

print(
    df["peer_group_name"]
    .unique()
)
# -------------------------
# Metrics to rank
# -------------------------

metrics = [

    "return_on_equity_pct",

    "net_profit_margin_pct",

    "debt_to_equity",

    "asset_turnover",

    "interest_coverage",

    "free_cash_flow_cr"

]

results = []

# -------------------------
# Compute percentile ranks
# -------------------------

for group in df["peer_group_name"].unique():

    group_df = df[
        df["peer_group_name"] == group
    ].copy()

    print(
        f"\nProcessing: {group}"
    )

    for metric in metrics:

        if metric not in group_df.columns:

            continue

        # Debt-to-equity inverse ranking

        if metric == "debt_to_equity":

            group_df[
                metric + "_percentile"
            ] = 1 - group_df[
                metric
            ].rank(
                pct=True
            )

        else:

            group_df[
                metric + "_percentile"
            ] = group_df[
                metric
            ].rank(
                pct=True
            )

    results.append(
        group_df
    )

# -------------------------
# Combine all groups
# -------------------------

final_df = pd.concat(

    results,

    ignore_index=True

)

print(
    "\nFinal rows:",
    len(final_df)
)

# -------------------------
# Save to SQLite
# -------------------------

final_df.to_sql(

    "peer_percentiles",

    conn,

    if_exists="replace",

    index=False

)

print(
    "\npeer_percentiles table created successfully!"
)

conn.close()