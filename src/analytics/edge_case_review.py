import os
import sqlite3
import pandas as pd

# Create output folder if it doesn't exist
os.makedirs("output", exist_ok=True)

# Connect to database
conn = sqlite3.connect("db/nifty100.db")

# Read company information
companies = pd.read_sql("""
SELECT
    companies.id AS company_id,
    companies.company_name,
    sectors.broad_sector,
    companies.roce_percentage,
    companies.roe_percentage
FROM companies
LEFT JOIN sectors
ON companies.id = sectors.company_id;
""", conn)

# Read computed ratios
ratios = pd.read_sql("""
SELECT
    company_id,
    year,
    return_on_equity_pct
FROM financial_ratios;
""", conn)

# Merge datasets
merged = pd.merge(
    ratios,
    companies,
    on="company_id",
    how="left"
)

# Create log file
with open("output/ratio_edge_cases.log", "w") as log:

    log.write("=========================================\n")
    log.write("RATIO EDGE CASE REVIEW\n")
    log.write("=========================================\n\n")

    for _, row in merged.iterrows():

        # Financial companies
        if row["broad_sector"] == "Financials":

            log.write(
                f"{row['company_id']} | {row['year']} | "
                "Financial Sector - D/E Warning Suppressed\n"
            )

        # ROE comparison
        if pd.notna(row["roe_percentage"]) and pd.notna(row["return_on_equity_pct"]):

            difference = abs(
                row["return_on_equity_pct"] -
                row["roe_percentage"]
            )

            if difference > 5:

                log.write(
                    f"{row['company_id']} | "
                    f"{row['year']} | "
                    f"ROE Difference = {difference:.2f}% | "
                    "Category: Source Value Difference\n"
                )

print("===================================")
print("Edge Case Review Completed")
print("Log File Created:")
print("output/ratio_edge_cases.log")
print("===================================")

conn.close()