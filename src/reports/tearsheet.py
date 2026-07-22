import sqlite3
import os
import pandas as pd

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

DB_PATH = "db/nifty100.db"

OUTPUT_DIR = "reports/tearsheets"

os.makedirs(OUTPUT_DIR, exist_ok=True)

styles = getSampleStyleSheet()


def get_company_data(company_id):

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT

        c.company_name,
        s.broad_sector,
        fr.year,

        fr.sales,
        fr.net_profit,
        fr.return_on_equity_pct,
        fr.debt_to_equity,
        fr.pe_ratio,
        fr.dividend_yield_pct,
        fr.free_cash_flow_cr,
        fr.net_profit_margin_pct,
        fr.operating_profit_margin_pct

    FROM financial_ratios fr

    LEFT JOIN companies c
        ON fr.company_id = c.id

    LEFT JOIN sectors s
        ON fr.company_id = s.company_id

    WHERE fr.company_id = ?

    ORDER BY fr.year DESC

    LIMIT 1
    """

    df = pd.read_sql(query, conn, params=[company_id])

    conn.close()

    return df


def create_tearsheet(company_id):

    df = get_company_data(company_id)

    if df.empty:
        return

    row = df.iloc[0]

    company_name = str(row["company_name"])

    company_name = company_name.replace("/", "-")

    filename = os.path.join(
        OUTPUT_DIR,
        f"{company_name}.pdf"
    )

    doc = SimpleDocTemplate(filename)

    story = []

    story.append(

        Paragraph(

            f"<b>{company_name}</b>",

            styles["Title"]

        )

    )

    story.append(Spacer(1, 20))

    story.append(

        Paragraph(

            f"<b>Sector:</b> {row['broad_sector']}",

            styles["BodyText"]

        )

    )

    story.append(Spacer(1, 10))

    story.append(

        Paragraph(

            f"<b>Year:</b> {row['year']}",

            styles["BodyText"]

        )

    )

    story.append(Spacer(1, 10))

    story.append(

        Paragraph(

            f"<b>Sales:</b> ₹{row['sales']} Cr",

            styles["BodyText"]

        )

    )

    story.append(Spacer(1, 10))

    story.append(

        Paragraph(

            f"<b>Net Profit:</b> ₹{row['net_profit']} Cr",

            styles["BodyText"]

        )

    )

    story.append(Spacer(1, 10))

    story.append(

        Paragraph(

            f"<b>ROE:</b> {row['return_on_equity_pct']}%",

            styles["BodyText"]

        )

    )

    story.append(Spacer(1, 10))

    story.append(

        Paragraph(

            f"<b>Debt to Equity:</b> {row['debt_to_equity']}",

            styles["BodyText"]

        )

    )

    story.append(Spacer(1, 10))

    story.append(

        Paragraph(

            f"<b>PE Ratio:</b> {row['pe_ratio']}",

            styles["BodyText"]

        )

    )

    story.append(Spacer(1, 10))

    story.append(

        Paragraph(

            f"<b>Dividend Yield:</b> {row['dividend_yield_pct']}%",

            styles["BodyText"]

        )

    )

    story.append(Spacer(1, 10))

    story.append(

        Paragraph(

            f"<b>Net Profit Margin:</b> {row['net_profit_margin_pct']}%",

            styles["BodyText"]

        )

    )

    story.append(Spacer(1, 10))

    story.append(

        Paragraph(

            f"<b>Operating Profit Margin:</b> {row['operating_profit_margin_pct']}%",

            styles["BodyText"]

        )

    )

    story.append(Spacer(1, 10))

    story.append(

        Paragraph(

            f"<b>Free Cash Flow:</b> ₹{row['free_cash_flow_cr']} Cr",

            styles["BodyText"]

        )

    )

    doc.build(story)

    print(f"Generated: {filename}")


if __name__ == "__main__":

    conn = sqlite3.connect(DB_PATH)

    companies = pd.read_sql(

        "SELECT id FROM companies",

        conn

    )

    conn.close()

    print(

        f"Total companies: {len(companies)}"

    )

    for company_id in companies["id"]:

        try:

            create_tearsheet(company_id)

        except Exception as e:

            print(

                f"Error for company {company_id}: {e}"

            )

    print(

        "\nAll tearsheets generated successfully."

    )