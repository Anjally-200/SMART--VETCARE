import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

# Guidance table
c.execute("""
CREATE TABLE IF NOT EXISTS guidance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    disease_name TEXT,
    ai_advice TEXT,
    emergency_level TEXT
)
""")

# Consultation table
c.execute("""
CREATE TABLE IF NOT EXISTS consultation (
    consultation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    disease TEXT,
    guidance TEXT,
    status TEXT,
    created_at TEXT
)
""")

conn.commit()
conn.close()

print("Tables created successfully")
