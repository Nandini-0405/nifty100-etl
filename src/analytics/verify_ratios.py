import sqlite3

conn = sqlite3.connect("db/nifty100.db")

rows = conn.execute(
"""
SELECT COUNT(*)
FROM financial_ratios
"""
).fetchone()[0]

print("Rows in financial_ratios:", rows)

conn.close()
