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

OUTPUT_FILE = "reports/portfolio_summary.pdf"

styles = getSampleStyleSheet()


def load_data():

    conn = sqlite3.connect(DB_PATH)

    companies = pd.read_sql(
        "SELECT COUNT(*) AS total FROM companies",
        conn
    )

    sectors = pd.read_sql(
        """
        SELECT
            broad_sector,
            COUNT(*) AS num_companies
        FROM sectors
        GROUP BY broad_sector
        ORDER BY num_companies DESC
        """,
        conn
    )

    metrics = pd.read_sql(
        """
        SELECT
            AVG(pe_ratio) AS avg_pe,
            AVG(return_on_equity_pct) AS avg_roe
        FROM financial_ratios
        """,
        conn
    )

    top_companies = pd.read_sql(
        """
        SELECT
            c.company_name,
            mc.market_cap_crore
        FROM market_cap mc

        LEFT JOIN companies c
        ON mc.company_id = c.id

        ORDER BY mc.market_cap_crore DESC

        LIMIT 10
        """,
        conn
    )

    conn.close()

    return companies, sectors, metrics, top_companies


def build_pdf():

    companies, sectors, metrics, top_companies = load_data()

    doc = SimpleDocTemplate(OUTPUT_FILE)

    story = []

    story.append(
        Paragraph(
            "<b>Nifty-100 Portfolio Summary Report</b>",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            f"Total Companies Analysed: {companies.iloc[0]['total']}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"Total Sectors: {len(sectors)}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"Average PE Ratio: {round(metrics.iloc[0]['avg_pe'], 2)}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"Average ROE: {round(metrics.iloc[0]['avg_roe'], 2)}%",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "<b>Top 5 Sectors by Company Count</b>",
            styles["Heading2"]
        )
    )

    sector_table = [["Sector", "Companies"]]

    for _, row in sectors.head(5).iterrows():

        sector_table.append(
            [
                row["broad_sector"],
                str(row["num_companies"])
            ]
        )

    story.append(Table(sector_table))

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "<b>Top 10 Companies by Market Cap</b>",
            styles["Heading2"]
        )
    )

    company_table = [["Company", "Market Cap (Cr)"]]

    for _, row in top_companies.iterrows():

        company_table.append(
            [
                row["company_name"],
                str(row["market_cap_crore"])
            ]
        )

    story.append(Table(company_table))

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            """
            This report summarizes the Nifty-100 analytics project,
            including financial ratios, sector insights, capital allocation,
            cash-flow intelligence and PDF tearsheets.
            """,
            styles["BodyText"]
        )
    )

    doc.build(story)

    print(f"Generated: {OUTPUT_FILE}")


if __name__ == "__main__":

    build_pdf()