import sqlite3
import os

db_path = os.path.abspath("database.db")
conn = sqlite3.connect(db_path)
c = conn.cursor()

# ---------------- USERS TABLE ----------------
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    password TEXT,
    role TEXT
)
""")

# ---------------- CONSULTATION TABLE ----------------
c.execute("""
CREATE TABLE IF NOT EXISTS consultation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    disease TEXT,
    guidance TEXT,
    doctor_response TEXT,
    status TEXT DEFAULT 'Pending',
    created_at TEXT
)
""")

# ✅ Ensure doctor_response exists (for old DB)
try:
    c.execute("ALTER TABLE consultation ADD COLUMN doctor_response TEXT")
except:
    pass


# ---------------- BREED HISTORY TABLE ----------------
c.execute("""
CREATE TABLE IF NOT EXISTS breed_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    prediction TEXT,
    confidence REAL,
    image_path TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    deleted INTEGER DEFAULT 0
)
""")

# ---------------- DISEASE HISTORY TABLE ----------------
c.execute("""
CREATE TABLE IF NOT EXISTS disease_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    prediction TEXT,
    confidence REAL,
    image_path TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    deleted INTEGER DEFAULT 0
)
""")


# ---------------- MESSAGES TABLE (NEW) ----------------
c.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    message TEXT,
    reply TEXT,
    status TEXT DEFAULT 'Pending',
    created_at TEXT
)
""")


# ---------------- INSERT DOCTOR ----------------
c.execute("SELECT * FROM users WHERE email = 'doc@gmail.com'")
if not c.fetchone():
    c.execute("""
    INSERT INTO users (name, email, password, role)
    VALUES (?, ?, ?, ?)
    """, ("Doctor", "doc@gmail.com", "123", "doctor"))


# ---------------- INSERT USER ----------------
c.execute("SELECT * FROM users WHERE email = 'user@gmail.com'")
if not c.fetchone():
    c.execute("""
    INSERT INTO users (name, email, password, role)
    VALUES (?, ?, ?, ?)
    """, ("User", "user@gmail.com", "123", "user"))

# ---------------- INSERT ADMIN ----------------
c.execute("SELECT * FROM users WHERE email = 'admin@gmail.com'")
if not c.fetchone():
    c.execute("""
    INSERT INTO users (name, email, password, role)
    VALUES (?, ?, ?, ?)
    """, ("Admin", "admin@gmail.com", "admin123", "admin"))

conn.commit()
conn.close()

print("✅ Database ready with consultation + messaging system!")