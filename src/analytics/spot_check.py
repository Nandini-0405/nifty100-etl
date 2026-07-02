import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

query = """
SELECT
company_id,
year,
net_profit_margin_pct,
return_on_equity_pct,
debt_to_equity
FROM financial_ratios
LIMIT 10;
"""

df = pd.read_sql(query, conn)

print(df)

conn.close()