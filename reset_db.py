import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

# Delete old consultation table
c.execute("DROP TABLE IF EXISTS consultation")

conn.commit()
conn.close()

print("Old consultation table deleted ✅")