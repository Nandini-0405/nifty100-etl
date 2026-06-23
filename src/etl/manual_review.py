import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

print("\n=== 5 Random Companies ===")

query = """
SELECT id, company_name
FROM companies
ORDER BY RANDOM()
LIMIT 5;
"""

df = pd.read_sql(query, conn)

print(df)

conn = sqlite3.connect("db/nifty100.db")

print("\n=== Year Coverage ===")

query = """
SELECT company_id,
COUNT(DISTINCT year) AS years_available
FROM profitandloss
GROUP BY company_id
ORDER BY years_available;
"""

df = pd.read_sql(query, conn)

print(df.head(20))

conn = sqlite3.connect("db/nifty100.db")

print("\n=== Companies with <5 years ===")

query = """
SELECT company_id,
COUNT(DISTINCT year) AS years_available
FROM profitandloss
GROUP BY company_id
HAVING COUNT(DISTINCT year) < 5;
"""

df = pd.read_sql(query, conn)

print(df)

conn.close()