import sqlite3
import os
import pandas as pd

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table
)

from reportlab.lib.styles import getSampleStyleSheet

DB_PATH = "db/nifty100.db"

OUTPUT_DIR = "reports/sectors"

os.makedirs(OUTPUT_DIR, exist_ok=True)

styles = getSampleStyleSheet()


def get_sector_data():

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT

        s.broad_sector,
        c.company_name,
        fr.sales,
        fr.net_profit,
        fr.return_on_equity_pct,
        fr.debt_to_equity,
        fr.pe_ratio

    FROM financial_ratios fr

    LEFT JOIN companies c
        ON fr.company_id = c.id

    LEFT JOIN sectors s
        ON fr.company_id = s.company_id
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


def create_sector_summary(df):

    summary = (
        df.groupby("broad_sector")
        .agg(
            {
                "company_name": "count",
                "sales": "mean",
                "net_profit": "mean",
                "return_on_equity_pct": "mean",
                "pe_ratio": "mean",
            }
        )
        .reset_index()
    )

    summary.rename(
        columns={
            "company_name": "num_companies"
        },
        inplace=True
    )

    summary.to_csv(
        "output/sector_summary.csv",
        index=False
    )

    return summary


def create_sector_pdfs(summary):

    for _, row in summary.iterrows():

        sector = str(row["broad_sector"]).replace("/", "-")

        filename = os.path.join(
            OUTPUT_DIR,
            f"{sector}.pdf"
        )

        doc = SimpleDocTemplate(filename)

        story = []

        story.append(
            Paragraph(
                f"<b>{sector}</b>",
                styles["Title"]
            )
        )

        story.append(
            Spacer(1, 20)
        )

        metrics = [

            ["Metric", "Value"],

            [
                "Companies",
                str(row["num_companies"])
            ],

            [
                "Average Sales",
                f"{round(row['sales'], 2)}"
            ],

            [
                "Average Net Profit",
                f"{round(row['net_profit'], 2)}"
            ],

            [
                "Average ROE",
                f"{round(row['return_on_equity_pct'], 2)}"
            ],

            [
                "Average PE Ratio",
                f"{round(row['pe_ratio'], 2)}"
            ]

        ]

        table = Table(metrics)

        story.append(table)

        doc.build(story)

        print(f"Generated: {filename}")


if __name__ == "__main__":

    df = get_sector_data()

    print(f"Rows loaded: {len(df)}")

    summary = create_sector_summary(df)

    print(summary)

    create_sector_pdfs(summary)

    print("\nSector reports generated successfully.")