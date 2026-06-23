import sqlite3

conn = sqlite3.connect("db/nifty100.db")

result = conn.execute(
    "PRAGMA foreign_key_check;"
).fetchall()

print(result)

conn.close()