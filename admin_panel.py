import streamlit as st
import sqlite3
import hashlib

# ---------------- PASSWORD HASH ----------------
def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

# ---------------- DB CONNECTION ----------------
def get_connection():
    conn = sqlite3.connect("vet_care.db")
    create_tables(conn)
    return conn

# ---------------- CREATE TABLE ----------------
def create_tables(conn):
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS consultation (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        message TEXT,
        status TEXT DEFAULT 'Pending'
    )
    """)

    conn.commit()

# ---------------- STATS ----------------
def get_doctor_stats():
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM users WHERE role='doctor'")
    total_doctors = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM users WHERE role='user'")
    total_users = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM consultation")
    total_consultations = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM consultation WHERE status='Pending'")
    pending_consultations = c.fetchone()[0]

    conn.close()

    return {
        'doctors': total_doctors,
        'users': total_users,
        'consultations': total_consultations,
        'pending': pending_consultations
    }

# ---------------- GET DOCTORS ----------------
def get_all_doctors():
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT id, name, email FROM users WHERE role='doctor'")
    data = c.fetchall()

    conn.close()
    return data

# ---------------- DELETE ----------------
def delete_doctor(doctor_id):
    conn = get_connection()
    c = conn.cursor()

    c.execute("DELETE FROM users WHERE id=?", (doctor_id,))
    conn.commit()
    conn.close()

# ---------------- MAIN APP ----------------
def app():
    st.title("🛡️ Admin Panel")

    tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "➕ Add Doctor", "👥 Doctors"])

    # -------- DASHBOARD --------
    with tab1:
        stats = get_doctor_stats()

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Doctors", stats['doctors'])
        c2.metric("Farmers", stats['users'])
        c3.metric("Consultations", stats['consultations'])
        c4.metric("Pending", stats['pending'])

    # -------- ADD DOCTOR --------
    with tab2:
        name = st.text_input("Doctor Name")
        email = st.text_input("Doctor Email")
        password = st.text_input("Password", type="password")

        if st.button("Add Doctor"):
            if not name or not email or not password:
                st.error("All fields required")
            else:
                conn = get_connection()
                c = conn.cursor()

                try:
                    c.execute("""
                    INSERT INTO users (name, email, password, role)
                    VALUES (?, ?, ?, ?)
                    """, (name, email, hash_password(password), "doctor"))

                    conn.commit()
                    st.success("Doctor added successfully")
                    st.rerun()

                except sqlite3.IntegrityError:
                    st.error("Email already exists")

                conn.close()

    # -------- VIEW DOCTORS --------
    with tab3:
        doctors = get_all_doctors()

        if doctors:
            for d in doctors:
                col1, col2, col3 = st.columns(3)

                col1.write(d[1])
                col2.write(d[2])

                if col3.button("Delete", key=d[0]):
                    delete_doctor(d[0])
                    st.rerun()
        else:
            st.info("No doctors found")

# ---------------- RUN ----------------
if __name__ == "__main__":
    app()