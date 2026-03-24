import streamlit as st
import sqlite3
import hashlib

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def app():
    if "show_doctor_reset" not in st.session_state:
        st.session_state.show_doctor_reset = False

    if not st.session_state.show_doctor_reset:
        st.title(" Doctor Login")

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

        if st.button("Forgot Password?"):
            st.session_state.show_doctor_reset = True
            st.rerun()

    else:
        st.title(" Doctor Password Reset")

        with st.form("doctor_reset_form"):
            email = st.text_input("Registered Doctor Email")
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm New Password", type="password")
            reset_submitted = st.form_submit_button("Reset Password")

        if reset_submitted:
            if not email or not new_password or not confirm_password:
                st.error("Please complete all fields")
            elif new_password != confirm_password:
                st.error("Passwords do not match")
            else:
                conn = sqlite3.connect("database.db")
                c = conn.cursor()
                c.execute("SELECT id FROM users WHERE email=? AND role='doctor'", (email,))
                user_record = c.fetchone()
                if not user_record:
                    st.error("Doctor account not found")
                else:
                    c.execute("UPDATE users SET password=? WHERE id=?", (hash_password(new_password), user_record[0]))
                    conn.commit()
                    st.success("Doctor password reset successful. Please login.")
                    st.session_state.show_doctor_reset = False
                    st.rerun()
                conn.close()

        if st.button("Back to Login"):
            st.session_state.show_doctor_reset = False
            st.rerun()