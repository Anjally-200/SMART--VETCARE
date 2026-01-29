import streamlit as st
import sqlite3

# ---------------- REGISTER ----------------
def register():
    st.title("👩‍🌾 Farmer Registration")

    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if password != confirm:
            st.error("Passwords do not match")
            return

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        try:
            c.execute(
                "INSERT INTO users VALUES (NULL,?,?,?,?)",
                (name, email, password, "farmer")
            )
            conn.commit()
            st.success("Registration successful! Please login.")
        except:
            st.error("Email already exists")
        conn.close()


# ---------------- LOGIN ----------------
def login():
    st.title("🔐 Farmer Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )
        user = c.fetchone()
        conn.close()

        if user:
            st.session_state.logged_in = True
            st.session_state.user_name = user[1]
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid email or password")
