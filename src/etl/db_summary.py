import sqlite3

conn = sqlite3.connect("db/nifty100.db")

tables = conn.execute(
"""
SELECT name
FROM sqlite_master
WHERE type='table';
"""
).fetchall()

print("\n=== DATABASE TABLES ===")

for table in tables:
    print(table[0])

conn.close()
