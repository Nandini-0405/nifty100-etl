import sqlite3
import os

if os.path.exists("db/nifty100.db"):
    os.remove("db/nifty100.db")

conn = sqlite3.connect("db/nifty100.db")

with open("db/schema.sql", "r") as f:
    conn.executescript(f.read())

conn.commit()
conn.close()

print("Database schema created successfully")