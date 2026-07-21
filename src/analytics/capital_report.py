import sqlite3
import pandas as pd

DB_PATH = "db/nifty100.db"

conn = sqlite3.connect(DB_PATH)

query = """
SELECT

    company_id,

    year,

    capital_allocation_label

FROM cashflow_intelligence

ORDER BY company_id, year
"""

df = pd.read_sql(query, conn)

conn.close()

latest_year = df["year"].max()

latest = df[
    df["year"] == latest_year
]

distribution = (

    latest["capital_allocation_label"]

    .value_counts()

    .reset_index()

)

distribution.columns = [

    "capital_pattern",

    "company_count"

]

distribution.to_csv(

    "output/capital_distribution.csv",

    index=False

)

print(distribution)

changes = []

for company_id, company_df in df.groupby("company_id"):

    company_df = company_df.sort_values("year")

    previous = None

    for _, row in company_df.iterrows():

        current = row["capital_allocation_label"]

        if previous is not None and previous != current:

            changes.append({

                "company_id": company_id,

                "year": row["year"],

                "old_pattern": previous,

                "new_pattern": current

            })

        previous = current

changes = pd.DataFrame(changes)

changes.to_csv(

    "output/pattern_changes.csv",

    index=False

)

print(

    f"Pattern changes: {len(changes)}"

)