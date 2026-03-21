import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

# ---------- breed_history ----------
try:
    c.execute("ALTER TABLE breed_history ADD COLUMN is_deleted INTEGER DEFAULT 0")
except:
    print("breed_history column already exists")

# ---------- disease_history ----------
try:
    c.execute("ALTER TABLE disease_history ADD COLUMN is_deleted INTEGER DEFAULT 0")
except:
    print("disease_history column already exists")

# ---------- consultations ----------
try:
    c.execute("ALTER TABLE consultations ADD COLUMN is_deleted INTEGER DEFAULT 0")
except:
    print("consultations column already exists")

# ✅ ---------- messages (IMPORTANT FIX) ----------
try:
    c.execute("ALTER TABLE messages ADD COLUMN is_deleted INTEGER DEFAULT 0")
except:
    print("messages column already exists")

conn.commit()
conn.close()

print("Database updated successfully")