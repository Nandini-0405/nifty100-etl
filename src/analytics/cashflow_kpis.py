import sqlite3
import pandas as pd

DB_PATH = "db/nifty100.db"


def free_cash_flow(operating_activity, investing_activity):
    return operating_activity + investing_activity


def cfo_quality_score(cfo, pat):

    if pat == 0:
        return None

    ratio = cfo / pat

    if ratio > 1:
        return "High Quality"

    elif ratio >= 0.5:
        return "Moderate"

    else:
        return "Accrual Risk"


def capex_intensity(investing_activity, sales):

    if sales == 0:
        return None, "Unknown"

    value = abs(investing_activity) / sales * 100

    if value < 3:

        label = "Asset Light"

    elif value <= 8:

        label = "Moderate"

    else:

        label = "Capital Intensive"

    return round(value, 2), label


def fcf_conversion_rate(fcf, operating_profit):

    if operating_profit == 0:
        return None

    return (fcf / operating_profit) * 100


def capital_allocation_pattern(cfo, cfi, cff):

    signs = (
        "+" if cfo >= 0 else "-",
        "+" if cfi >= 0 else "-",
        "+" if cff >= 0 else "-"
    )

    patterns = {

        ("+", "-", "-"): "Reinvestor",

        ("+", "+", "-"): "Liquidating Assets",

        ("-", "+", "+"): "Distress Signal",

        ("-", "-", "+"): "Growth Funded by Debt",

        ("+", "+", "+"): "Cash Accumulator",

        ("-", "-", "-"): "Pre-Revenue",

        ("+", "-", "+"): "Mixed"

    }

    return patterns.get(signs, "Unknown")


def generate_cashflow_intelligence():

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT

        cf.company_id,

        c.company_name,

        s.broad_sector,

        cf.year,

        cf.cash_from_operating_activity AS cfo,

        cf.cash_from_investing_activity AS cfi,

        cf.cash_from_financing_activity AS cff,

        bs.borrowings,

        pl.net_profit,

        pl.sales,

        pl.operating_profit,

        fr.free_cash_flow_cr

    FROM cashflow cf

    LEFT JOIN companies c
    ON cf.company_id = c.id

    LEFT JOIN sectors s
    ON cf.company_id = s.company_id

    LEFT JOIN balancesheet bs
    ON cf.company_id = bs.company_id
    AND cf.year = bs.year

    LEFT JOIN profitandloss pl
    ON cf.company_id = pl.company_id
    AND cf.year = pl.year

    LEFT JOIN financial_ratios fr
    ON cf.company_id = fr.company_id
    AND cf.year = fr.year

    ORDER BY company_id, year
    """

    df = pd.read_sql(query, conn)

    conn.close()

    results = []

    for company_id, company_df in df.groupby("company_id"):

        company_df = company_df.sort_values("year")

        latest = company_df.iloc[-1]

        ratios = []

        for _, row in company_df.tail(5).iterrows():

            pat = row["net_profit"]

            cfo = row["cfo"]

            if pd.notna(pat) and pat != 0:

                ratios.append(cfo / pat)

        avg_ratio = None

        if len(ratios) > 0:

            avg_ratio = sum(ratios) / len(ratios)

        if avg_ratio is None:

            cfo_label = "Unknown"

        elif avg_ratio > 1:

            cfo_label = "High Quality"

        elif avg_ratio >= 0.5:

            cfo_label = "Moderate"

        else:

            cfo_label = "Accrual Risk"

        capex_value, capex_label = capex_intensity(

            latest["cfi"],
            latest["sales"]

        )

        fcf_conversion = fcf_conversion_rate(

            latest["free_cash_flow_cr"],
            latest["operating_profit"]

        )

        distress_flag = (

            latest["cfo"] < 0

            and

            latest["cff"] > 0

        )

        deleveraging_flag = False

        if len(company_df) >= 2:

            previous = company_df.iloc[-2]

            deleveraging_flag = (

                latest["cff"] < 0

                and

                latest["borrowings"] < previous["borrowings"]

            )

        capital_label = capital_allocation_pattern(

            latest["cfo"],
            latest["cfi"],
            latest["cff"]

        )

        results.append({

            "company_id": company_id,

            "company_name": latest["company_name"],

            "sector": latest["broad_sector"],

            "cfo_quality_score": round(avg_ratio, 2)

            if avg_ratio is not None else None,

            "cfo_quality_label": cfo_label,

            "capex_intensity_pct": capex_value,

            "capex_label": capex_label,

            "fcf_conversion_pct": round(

                fcf_conversion, 2

            ) if fcf_conversion is not None else None,

            "distress_flag": distress_flag,

            "deleveraging_flag": deleveraging_flag,

            "capital_allocation_label": capital_label

        })

    output = pd.DataFrame(results)

    output.to_excel(

        "output/cashflow_intelligence.xlsx",

        index=False

    )

    distress = output[

        output["distress_flag"] == True

    ]

    distress.to_csv(

        "output/distress_alerts.csv",

        index=False

    )

    print("\nCash flow intelligence generated successfully.")

    print(

        f"Companies processed: {len(output)}"

    )

    print(

        f"Distress alerts: {len(distress)}"

    )


if __name__ == "__main__":

    generate_cashflow_intelligence()