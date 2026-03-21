import sqlite3

def get_guidance(disease):

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    SELECT ai_advice, emergency_level
    FROM guidance
    WHERE disease_name = ?
    """, (disease,))

    result = c.fetchone()
    conn.close()

    if result:
        return result[0], result[1]
    else:
        return "Consult veterinarian for accurate diagnosis", "Medium"
