import sqlite3

conn = sqlite3.connect("vet_care.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    password TEXT,
    role TEXT
)
""")

# Insert admin
c.execute("""
INSERT INTO users (name, email, password, role)
VALUES (?, ?, ?, ?)
""", ("Admin", "admin@gmail.com", "admin123", "admin"))

conn.commit()
conn.close()

print("Admin created successfully")