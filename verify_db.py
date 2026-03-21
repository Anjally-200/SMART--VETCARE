import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = c.fetchall()
print("✅ Database Tables Created:")
for table in tables:
    print(f"  - {table[0]}")
    
# Check breed_history table structure
print("\nbreed_history columns:")
c.execute("PRAGMA table_info(breed_history)")
cols = c.fetchall()
for col in cols:
    print(f"  - {col[1]} ({col[2]})")

# Check disease_history table structure
print("\ndisease_history columns:")
c.execute("PRAGMA table_info(disease_history)")
cols = c.fetchall()
for col in cols:
    print(f"  - {col[1]} ({col[2]})")

conn.close()
