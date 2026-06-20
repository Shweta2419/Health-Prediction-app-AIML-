# create_db.py

import sqlite3

conn = sqlite3.connect("database.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS patients(
id INTEGER PRIMARY KEY AUTOINCREMENT,
full_name TEXT,
dob TEXT,
email TEXT,
glucose REAL,
haemoglobin REAL,
cholesterol REAL,
remarks TEXT
)
""")

conn.commit()
conn.close()

print("Database Created")