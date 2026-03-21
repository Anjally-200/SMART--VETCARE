import streamlit as st
import sqlite3
import hashlib

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def app():
    st.title("👨‍⚕️ Doctor Login")

    with st.form("doctor_login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        submitted = st.form_submit_button("Login as Doctor")

    if submitted:
        if not email or not password:
            st.error("Please enter email and password")
            return

        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        hashed = hash_password(password)

        c.execute("""
        SELECT id, name FROM users 
        WHERE email=? AND password=? AND role='doctor'
        """, (email, hashed))

        doctor = c.fetchone()
        conn.close()

        if doctor:
            st.session_state.logged_in = True
            st.session_state.role = "doctor"
            st.session_state.user_id = doctor[0]
            st.session_state.user_name = doctor[1]

            st.success("Doctor login successful")
            st.rerun()
        else:
            st.error("Invalid doctor credentials")