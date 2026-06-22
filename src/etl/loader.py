import pandas as pd
import sqlite3
from pathlib import Path

print("=== Loader Started ===")

DB_PATH = "db/nifty100.db"
DATA_PATH = "data/raw"

FILES = {
    "companies": "companies.xlsx",
    "profitandloss": "profitandloss.xlsx",
    "balancesheet": "balancesheet.xlsx",
    "cashflow": "cashflow.xlsx",
    "analysis": "analysis.xlsx",
    "documents": "documents.xlsx",
    "prosandcons": "prosandcons.xlsx",
    "sectors": "sectors.xlsx",
    "stock_prices": "stock_prices.xlsx",
    "financial_ratios": "financial_ratios.xlsx",
    "peer_groups": "peer_groups.xlsx",
    "market_cap": "market_cap.xlsx"
}

conn = sqlite3.connect(DB_PATH)

audit = []

for table_name, file_name in FILES.items():

    try:
        print(f"\nLoading {table_name}...")

        file_path = Path(DATA_PATH) / file_name

        # Most files have title row in first row
        if table_name in [
            "companies",
            "profitandloss",
            "balancesheet",
            "cashflow",
            "analysis",
            "documents",
            "prosandcons"
        ]:
            df = pd.read_excel(file_path, header=1)
        else:
            df = pd.read_excel(file_path)

        print(f"Rows found: {len(df)}")

        df.to_sql(
            table_name,
            conn,
            if_exists="append",
            index=False
        )

        audit.append({
            "table_name": table_name,
            "rows_loaded": len(df),
            "status": "SUCCESS"
        })

        print(f"{table_name} loaded successfully")

    except Exception as e:

        audit.append({
            "table_name": table_name,
            "rows_loaded": 0,
            "status": f"FAILED: {str(e)}"
        })

        print(f"ERROR loading {table_name}")
        print(e)

audit_df = pd.DataFrame(audit)

audit_df.to_csv(
    "output/load_audit.csv",
    index=False
)

conn.close()

print("\n=== Data Loading Completed ===")
print("Audit file saved: output/load_audit.csv")