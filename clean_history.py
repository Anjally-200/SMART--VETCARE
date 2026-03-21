import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

c.execute("DELETE FROM breed_history")

conn.commit()
conn.close()

print("History cleared")
