import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS breed_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    breed TEXT,
    confidence REAL,
    created_at TEXT
)
""")

conn.commit()
conn.close()

print("Breed history table created")
