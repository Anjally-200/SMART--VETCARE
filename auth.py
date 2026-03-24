import streamlit as st
import sqlite3
import hashlib
import re

# ---------------- Helpers ----------------

def hash_password(pw: str) -> str:
    return hashlib.sha256(pw.encode("utf-8")).hexdigest()


def password_strength(pw: str):
    score = 0
    if len(pw) >= 8:
        score += 1
    if re.search(r"[0-9]", pw):
        score += 1
    if re.search(r"[A-Z]", pw):
        score += 1
    if re.search(r"[a-z]", pw):
        score += 1
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", pw):
        score += 1

    if score <= 2:
        return "Weak", "red"
    elif score <= 4:
        return "Medium", "orange"
    else:
        return "Strong", "green"


def get_connection():
    return sqlite3.connect("database.db")


# ---------------- REGISTER ----------------

def register():
    st.markdown("##  Create Account")

    with st.form("register_form"):
        name = st.text_input("Full name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")

        strength, color = password_strength(password)
        if password:
            st.markdown(f"Password strength: :{color}[{strength}]")

        submitted = st.form_submit_button("Register")

    if submitted:
        if not name or not email or not password:
            st.error("Please fill all fields")
            return

        if password != confirm:
            st.error("Passwords do not match")
            return

        conn = get_connection()
        c = conn.cursor()

        try:
            c.execute(
                "INSERT INTO users (name, email, password, role) VALUES (?,?,?,?)",
                (name, email, hash_password(password), "farmer")
            )
            conn.commit()
            st.success("Registration successful! Please login.")
        except:
            st.error("Email already exists")
        finally:
            conn.close()


# ---------------- LOGIN ----------------

def login():
    if "show_reset" not in st.session_state:
        st.session_state.show_reset = False

    if not st.session_state.show_reset:
        st.markdown("##  Login")

        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")

        if submitted:
            if not email or not password:
                st.error("Enter email and password")
                return

            conn = get_connection()
            c = conn.cursor()

            hashed = hash_password(password)

            # Try hashed password
            c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, hashed))
            user = c.fetchone()

            # Fallback for old plaintext passwords
            if not user:
                c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
                user_plain = c.fetchone()

                if user_plain:
                    # Upgrade password to hash
                    c.execute("UPDATE users SET password=? WHERE id=?", (hashed, user_plain[0]))
                    conn.commit()
                    user = user_plain
                    st.info("Password upgraded to secure hash")

            conn.close()

            if user:
                # ✅ SESSION SETUP
                st.session_state.logged_in = True
                st.session_state.user_id = user[0]
                st.session_state.user_name = user[1]

                # ✅ ROLE HANDLING
                db_role = user[4]

                if db_role == "farmer":
                    st.session_state.role = "user"
                else:
                    st.session_state.role = db_role

                st.success(f"Welcome {user[1]} ")
                st.rerun()

            else:
                st.error("Invalid email or password")

        if st.button("Forgot Password?"):
            st.session_state.show_reset = True
            st.rerun()

    else:
        st.markdown("##  Forgot Password")

        with st.form("reset_form"):
            reset_email = st.text_input("Registered Email")
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm New Password", type="password")
            reset_submitted = st.form_submit_button("Reset Password")

        if reset_submitted:
            if not reset_email or not new_password or not confirm_password:
                st.error("Please fill all fields")
            elif new_password != confirm_password:
                st.error("Passwords do not match")
            else:
                success = reset_password(reset_email, new_password)
                if success:
                    st.success("Password reset successful. Please login.")
                    st.session_state.show_reset = False
                    st.rerun()
                else:
                    st.error("No account found with that email")

        if st.button("Back to Login"):
            st.session_state.show_reset = False
            st.rerun()


def reset_password(email: str, new_password: str, role: str = None):
    """Reset password for a user (farmer or doctor)."""
    conn = get_connection()
    c = conn.cursor()

    if role:
        c.execute("SELECT id FROM users WHERE email=? AND role=?", (email, role))
    else:
        c.execute("SELECT id FROM users WHERE email=?", (email,))

    user_record = c.fetchone()

    if not user_record:
        conn.close()
        return False

    c.execute(
        "UPDATE users SET password=? WHERE id=?",
        (hash_password(new_password), user_record[0])
    )
    conn.commit()
    conn.close()

    return True


# ---------------- LOGOUT ----------------

def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

    st.success("Logged out successfully")
    st.rerun()