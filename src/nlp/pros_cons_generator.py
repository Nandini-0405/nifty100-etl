import sqlite3
import pandas as pd

DB_PATH = "db/nifty100.db"

conn = sqlite3.connect(DB_PATH)

query = """
SELECT
    company_id,
    year,
    return_on_equity_pct,
    debt_to_equity,
    free_cash_flow_cr,
    operating_margin_pct,
    interest_coverage,
    dividend_yield_pct,
    revenue_cagr_5yr,
    profit_cagr_5yr
FROM financial_ratios
"""

df = pd.read_sql(query, conn)

conn.close()

latest = (

    df.sort_values(
        ["company_id", "year"]
    )

    .groupby(
        "company_id"
    )

    .tail(1)

)

results = []

for _, row in latest.iterrows():

    company_id = row["company_id"]

    # -------------------------
    # PRO RULES
    # -------------------------

    # P1

    if pd.notna(row["return_on_equity_pct"]) and row["return_on_equity_pct"] > 20:

        results.append({

            "company_id": company_id,

            "type": "pro",

            "rule_id": "P1",

            "text": "Consistently high return on equity above 20% demonstrates exceptional capital efficiency",

            "confidence_pct": 85

        })

    # P2

    if pd.notna(row["free_cash_flow_cr"]) and row["free_cash_flow_cr"] > 0:

        results.append({

            "company_id": company_id,

            "type": "pro",

            "rule_id": "P2",

            "text": "Strong free cash flow generation signals healthy business fundamentals",

            "confidence_pct": 80

        })

    # P3

    if pd.notna(row["debt_to_equity"]) and row["debt_to_equity"] == 0:

        results.append({

            "company_id": company_id,

            "type": "pro",

            "rule_id": "P3",

            "text": "Debt-free balance sheet provides financial flexibility and eliminates interest burden",

            "confidence_pct": 90

        })

    # P4

    if pd.notna(row["revenue_cagr_5yr"]) and row["revenue_cagr_5yr"] > 15:

        results.append({

            "company_id": company_id,

            "type": "pro",

            "rule_id": "P4",

            "text": "Revenue growing above 15% CAGR reflects strong business momentum",

            "confidence_pct": 82

        })
    # P5

if row["operating_margin_pct"] > 25:

    results.append({

        "company_id": company_id,

        "type": "pro",

        "rule_id": "P5",

        "text": "Operating profit margin above 25% indicates strong pricing power and cost discipline",

        "confidence_pct": 85

    })


# P6

if row["profit_cagr_5yr"] > 20:

    results.append({

        "company_id": company_id,

        "type": "pro",

        "rule_id": "P6",

        "text": "Net profit compounding at above 20% over 5 years creates significant shareholder value",

        "confidence_pct": 88

    })


# P7

if row["interest_coverage"] > 10 or row["debt_to_equity"] == 0:

    results.append({

        "company_id": company_id,

        "type": "pro",

        "rule_id": "P7",

        "text": "Very high interest coverage ratio reflects negligible financial stress from debt servicing",

        "confidence_pct": 90

    })


# P8

if row["dividend_yield_pct"] > 2 and row["free_cash_flow_cr"] > 0:

    results.append({

        "company_id": company_id,

        "type": "pro",

        "rule_id": "P8",

        "text": "Consistent dividend yield above 2% backed by positive free cash flow",

        "confidence_pct": 80

    })


# P9

if row["eps_cagr_5yr"] > 15:

    results.append({

        "company_id": company_id,

        "type": "pro",

        "rule_id": "P9",

        "text": "Earnings per share growing above 15% CAGR indicates strong earnings quality and compounding",

        "confidence_pct": 85

    })


# P10

if row["return_on_equity_pct"] > 15:

    results.append({

        "company_id": company_id,

        "type": "pro",

        "rule_id": "P10",

        "text": "Return on equity improving for multiple years shows strengthening business quality",

        "confidence_pct": 75

    })


# P11

if row["profit_cagr_5yr"] > row["revenue_cagr_5yr"]:

    results.append({

        "company_id": company_id,

        "type": "pro",

        "rule_id": "P11",

        "text": "Revenue growing slower than profits shows improving operating leverage and scale benefits",

        "confidence_pct": 82

    })


# P12

if row["assets_cagr_5yr"] > 10 and row["borrowings_cagr_5yr"] < 0:

    results.append({

        "company_id": company_id,

        "type": "pro",

        "rule_id": "P12",

        "text": "Growing asset base funded by internal accruals reflects self-sustaining growth",

        "confidence_pct": 85

    })

    # -------------------------
    # CON RULES
    # -------------------------

    # C1

    if pd.notna(row["debt_to_equity"]) and row["debt_to_equity"] > 2:

        results.append({

            "company_id": company_id,

            "type": "con",

            "rule_id": "C1",

            "text": f"Debt-to-equity ratio of {row['debt_to_equity']:.2f} is elevated and warrants monitoring",

            "confidence_pct": 85

        })

    # C2

    if pd.notna(row["free_cash_flow_cr"]) and row["free_cash_flow_cr"] < 0:

        results.append({

            "company_id": company_id,

            "type": "con",

            "rule_id": "C2",

            "text": "Negative free cash flow raises concerns about cash generation quality",

            "confidence_pct": 78

        })

    # C3

    if pd.notna(row["operating_margin_pct"]) and row["operating_margin_pct"] < 10:

        results.append({

            "company_id": company_id,

            "type": "con",

            "rule_id": "C3",

            "text": "Weak operating margins indicate pricing or cost pressure",

            "confidence_pct": 75

        })

    # C4

    if pd.notna(row["interest_coverage"]) and row["interest_coverage"] < 1.5:

        results.append({

            "company_id": company_id,

            "type": "con",

            "rule_id": "C4",

            "text": "Low interest coverage suggests debt servicing risk",

            "confidence_pct": 90

        })
    # C5

if row["revenue_cagr_5yr"] < 0:

    results.append({

        "company_id": company_id,

        "type": "con",

        "rule_id": "C5",

        "text": "Revenue contraction indicates demand weakness or market share loss",

        "confidence_pct": 85

    })


# C6

if row["interest_coverage"] < 1.5:

    results.append({

        "company_id": company_id,

        "type": "con",

        "rule_id": "C6",

        "text": "Interest coverage ratio below 1.5x indicates debt servicing risk",

        "confidence_pct": 90

    })


# C7

if row["dividend_payout_ratio_pct"] > 100:

    results.append({

        "company_id": company_id,

        "type": "con",

        "rule_id": "C7",

        "text": "Dividend payout ratio above 100% is unsustainable",

        "confidence_pct": 88

    })


# C8

if row["debt_to_equity"] > 1:

    results.append({

        "company_id": company_id,

        "type": "con",

        "rule_id": "C8",

        "text": "Rising debt levels suggest increasing financial leverage risk",

        "confidence_pct": 75

    })


# C9

if row["eps_cagr_5yr"] < 0:

    results.append({

        "company_id": company_id,

        "type": "con",

        "rule_id": "C9",

        "text": "Earnings deterioration reflects weakening profitability",

        "confidence_pct": 82

    })


# C10

if row["roce_pct"] < 10:

    results.append({

        "company_id": company_id,

        "type": "con",

        "rule_id": "C10",

        "text": "Return on capital employed below 10% suggests poor capital efficiency",

        "confidence_pct": 80

    })


# C11

if row["net_debt_to_ebitda"] > 3:

    results.append({

        "company_id": company_id,

        "type": "con",

        "rule_id": "C11",

        "text": "Net debt exceeding 3 times EBITDA limits financial flexibility",

        "confidence_pct": 90

    })


# C12

if row["revenue_cagr_5yr"] < 5:

    results.append({

        "company_id": company_id,

        "type": "con",

        "rule_id": "C12",

        "text": "Revenue growth below 5% over 5 years suggests limited business momentum",

        "confidence_pct": 80

    })

output = pd.DataFrame(results)

output = output[
    output["confidence_pct"] > 60
]

output.to_csv(

    "output/pros_cons_generated.csv",

    index=False

)

print("\nGenerated Pros/Cons:\n")

print(output.head())

print(

    f"\nRows generated: {len(output)}"

)
pros_count = output[output["type"] == "pro"].groupby(
    "company_id"
).size()

cons_count = output[output["type"] == "con"].groupby(
    "company_id"
).size()

print(

    f"Companies with pros: {len(pros_count)}"

)

print(

    f"Companies with cons: {len(cons_count)}"

)
summary = output.pivot_table(
    index="company_id",
    columns="type",
    values="rule_id",
    aggfunc="count",
    fill_value=0
)

summary["has_pro"] = summary["pro"] > 0
summary["has_con"] = summary["con"] > 0

missing = summary[
    (~summary["has_pro"]) |
    (~summary["has_con"])
]

missing.to_csv(
    "output/missing_pros_cons.csv"
)

print(
    f"Companies missing pro/con: {len(missing)}"
)