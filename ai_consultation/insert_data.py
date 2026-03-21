import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

data = [
    ("Mastitis", "Keep udder clean and apply warm compress. Monitor swelling.", "Medium"),
    ("Foot and Mouth Disease", "Isolate animal immediately. Clean mouth and hooves.", "High"),
    ("Ringworm", "Apply antifungal treatment and keep area dry.", "Low"),
    ("Healthy", "No major issues detected. Maintain hygiene and proper feeding.", "Low")
]

c.executemany(
    "INSERT INTO guidance (disease_name, ai_advice, emergency_level) VALUES (?, ?, ?)",
    data
)

conn.commit()
conn.close()

print("Guidance data inserted successfully")
