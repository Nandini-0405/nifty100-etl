import re
import sqlite3
import pandas as pd

DB_PATH = "db/nifty100.db"

PATTERN = r"(\d+)\s*Years?:?\s*([\d.]+)%"

conn = sqlite3.connect(DB_PATH)

df = pd.read_sql(

    """
    SELECT
        company_id,
        compounded_sales_growth,
        compounded_profit_growth,
        stock_price_cagr,
        return_on_equity
    FROM analysis
    """,

    conn

)

conn.close()

records = []

failures = []

columns = {

    "compounded_sales_growth": "sales_cagr",

    "compounded_profit_growth": "profit_cagr",

    "stock_price_cagr": "stock_price_cagr",

    "return_on_equity": "roe"

}

for _, row in df.iterrows():

    company_id = row["company_id"]

    for col, metric in columns.items():

        text = str(row[col])

        matches = re.findall(

            PATTERN,

            text

        )

        if matches:

            for period, value in matches:

                records.append(

                    {

                        "company_id": company_id,

                        "metric_type": metric,

                        "period_years": int(period),

                        "value_pct": float(value)

                    }

                )

        else:

            failures.append(

                {

                    "company_id": company_id,

                    "metric": metric,

                    "raw_text": text

                }

            )

parsed = pd.DataFrame(records)

failed = pd.DataFrame(failures)

parsed.to_csv(

    "output/analysis_parsed.csv",

    index=False

)

failed.to_csv(

    "output/parse_failures.csv",

    index=False

)

print(

    f"Parsed rows: {len(parsed)}"

)

print(

    f"Failures: {len(failed)}"

)
# ----------------------------------
# Cross Validation
# ----------------------------------

conn = sqlite3.connect(DB_PATH)

ratios = pd.read_sql(

    """
    SELECT
        company_id,
        revenue_cagr_5yr,
        profit_cagr_5yr
    FROM financial_ratios
    """,

    conn

)

conn.close()

sales_parsed = parsed[

    (parsed["metric_type"] == "sales_cagr")

    &

    (parsed["period_years"] == 5)

]

profit_parsed = parsed[

    (parsed["metric_type"] == "profit_cagr")

    &

    (parsed["period_years"] == 5)

]

sales_check = sales_parsed.merge(

    ratios[

        [

            "company_id",

            "revenue_cagr_5yr"

        ]

    ],

    on="company_id",

    how="left"

)

sales_check["difference_pct"] = (

    sales_check["value_pct"]

    -

    sales_check["revenue_cagr_5yr"]

).abs()

profit_check = profit_parsed.merge(

    ratios[

        [

            "company_id",

            "profit_cagr_5yr"

        ]

    ],

    on="company_id",

    how="left"

)

profit_check["difference_pct"] = (

    profit_check["value_pct"]

    -

    profit_check["profit_cagr_5yr"]

).abs()

review = pd.concat(

    [

        sales_check[

            sales_check["difference_pct"] > 5

        ],

        profit_check[

            profit_check["difference_pct"] > 5

        ]

    ]

)

review.to_csv(

    "output/cagr_review.csv",

    index=False

)

print(

    f"Manual review rows: {len(review)}"

)