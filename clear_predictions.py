import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

# Delete all prediction data
c.execute("DELETE FROM breed_history")
c.execute("DELETE FROM disease_history")

conn.commit()
conn.close()

print("All predictions cleared ✅")