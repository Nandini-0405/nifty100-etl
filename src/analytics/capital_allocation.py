import os
import sys
import sqlite3
import pandas as pd

# Allow importing from the current folder
sys.path.append(os.path.dirname(__file__))

from cashflow_kpis import capital_allocation_pattern


# Connect to SQLite database
conn = sqlite3.connect("db/nifty100.db")

# Read cashflow table
query = """
SELECT
    company_id,
    year,
    operating_activity,
    investing_activity,
    financing_activity
FROM cashflow;
"""

df = pd.read_sql(query, conn)

# Determine signs
df["cfo_sign"] = df["operating_activity"].apply(lambda x: "+" if x >= 0 else "-")
df["cfi_sign"] = df["investing_activity"].apply(lambda x: "+" if x >= 0 else "-")
df["cff_sign"] = df["financing_activity"].apply(lambda x: "+" if x >= 0 else "-")

# Generate pattern label
df["pattern_label"] = df.apply(
    lambda row: capital_allocation_pattern(
        row["operating_activity"],
        row["investing_activity"],
        row["financing_activity"]
    ),
    axis=1
)

# Keep only required columns
output = df[
    [
        "company_id",
        "year",
        "cfo_sign",
        "cfi_sign",
        "cff_sign",
        "pattern_label"
    ]
]

# Create output folder if it doesn't exist
os.makedirs("output", exist_ok=True)

# Save CSV
output.to_csv(
    "output/capital_allocation.csv",
    index=False
)

print("===================================")
print("Capital Allocation Report Generated")
print("Saved to output/capital_allocation.csv")
print("Total Records:", len(output))
print("===================================")

conn.close()