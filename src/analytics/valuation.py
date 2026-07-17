import sqlite3
import pandas as pd


DB_PATH = "db/nifty100.db"

conn = sqlite3.connect(DB_PATH)


query = """
SELECT
    fr.company_id,
    c.company_name,
    s.broad_sector,

    fr.pe_ratio,
    fr.pb_ratio,
    fr.ev_ebitda,

    fr.free_cash_flow_cr,

    mc.market_cap_crore

FROM financial_ratios fr

LEFT JOIN companies c
ON fr.company_id = c.id

LEFT JOIN sectors s
ON fr.company_id = s.company_id

LEFT JOIN market_cap mc
ON fr.company_id = mc.company_id
"""

df = pd.read_sql(query, conn)

conn.close()


# -----------------------------------
# Keep latest year
# -----------------------------------

df["year_rank"] = (

    df.groupby("company_id")

    .cumcount()

)

df = (

    df.sort_values("company_id")

    .drop_duplicates(

        subset=["company_id"],

        keep="last"

    )

)


# -----------------------------------
# FCF Yield
# -----------------------------------

df["fcf_yield_pct"] = (

    df["free_cash_flow_cr"]

    / df["market_cap_crore"]

) * 100


# -----------------------------------
# Sector median PE
# -----------------------------------

sector_median = (

    df.groupby(

        "broad_sector"

    )["pe_ratio"]

    .median()

    .reset_index()

)

sector_median.columns = [

    "broad_sector",

    "sector_median_pe"

]

df = df.merge(

    sector_median,

    on="broad_sector",

    how="left"

)


# -----------------------------------
# PE vs sector
# -----------------------------------

df["pe_vs_sector_median_pct"] = (

    df["pe_ratio"]

    / df["sector_median_pe"]

) * 100


# -----------------------------------
# Valuation flag
# -----------------------------------

def classify(row):

    pe = row["pe_ratio"]

    median = row["sector_median_pe"]

    if pd.isna(pe):

        return "Fair"

    if pe > median * 1.5:

        return "Caution"

    if pe < median * 0.7:

        return "Discount"

    return "Fair"


df["flag"] = df.apply(

    classify,

    axis=1

)


# -----------------------------------
# Final columns
# -----------------------------------

output = df[

    [

        "company_id",

        "company_name",

        "broad_sector",

        "pe_ratio",

        "pb_ratio",

        "ev_ebitda",

        "fcf_yield_pct",

        "sector_median_pe",

        "pe_vs_sector_median_pct",

        "flag"

    ]

]


# -----------------------------------
# Save files
# -----------------------------------

output.to_excel(

    "output/valuation_summary.xlsx",

    index=False

)

flags = output[

    output["flag"] != "Fair"

]

flags.to_csv(

    "output/valuation_flags.csv",

    index=False

)

print(

    "Valuation files generated successfully."

)

print(

    f"Rows: {len(output)}"

)