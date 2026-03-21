import streamlit as st
from auth import login, register
import doctor_login
import importlib

st.set_page_config(page_title="Smart Vet", layout="centered")

# ---------------- SESSION INITIALIZATION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if "user_id" not in st.session_state:
    st.session_state.user_id = None

# PAGE STATE
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"


# ---------------- NOT LOGGED IN ----------------
if not st.session_state.logged_in:

    menu = st.sidebar.selectbox(
        "Menu",
        ["User Login", "Register", "Doctor Login", "Admin Login"]
    )

    if menu == "User Login":
        login()

    elif menu == "Register":
        register()

    elif menu == "Doctor Login":
        doctor_login.app()

    elif menu == "Admin Login":
        st.title("🛠 Admin Login")

        email = st.text_input("Admin Email")
        password = st.text_input("Admin Password", type="password")

        if st.button("Login as Admin"):
            if email == "admin@gmail.com" and password == "admin123":
                st.session_state.logged_in = True
                st.session_state.role = "admin"
                st.session_state.user_name = "Admin"
                st.rerun()
            else:
                st.error("Invalid admin credentials")


# ---------------- LOGGED IN ----------------
else:

    st.sidebar.success(f"Welcome {st.session_state.user_name}")

    # ---------------- DOCTOR PANEL ----------------
    if st.session_state.role == "doctor":

        choice = st.sidebar.radio(
            "Navigation",
            ["Vet Dashboard", "Messages", "Logout"]
        )

        if choice == "Vet Dashboard":
            import vet_dashboard
            vet_dashboard.app()

        elif choice == "Messages":
            import doctor_messages
            doctor_messages.app()

        elif choice == "Logout":
            st.session_state.clear()
            st.rerun()

    # ---------------- USER PANEL ----------------
    elif st.session_state.role == "user":

        menu_list = [
            "Dashboard",
            "Breed Prediction",
            "Breed History",
            "Disease Prediction",
            "Disease History",
            "Support",
            "Logout"
        ]

        menu = st.sidebar.radio(
            "Navigation",
            menu_list,
            index=menu_list.index(st.session_state.page)
        )

        st.session_state.page = menu

        if menu == "Dashboard":
            import farmer_dashboard
            farmer_dashboard.app()

        elif menu == "Breed Prediction":
            module = importlib.import_module("breed_predict")
            module.app()

        elif menu == "Breed History":
            module = importlib.import_module("breed_history")
            module.app()

        elif menu == "Disease Prediction":
            module = importlib.import_module("disease_predict")
            module.app()

        elif menu == "Disease History":
            module = importlib.import_module("disease_history")
            module.app()

        elif menu == "Support":
            module = importlib.import_module("support")
            module.app()

        elif menu == "Logout":
            st.session_state.clear()
            st.rerun()

    # ---------------- ADMIN PANEL ----------------
    elif st.session_state.role == "admin":

        choice = st.sidebar.radio("Navigation", ["Add Doctor", "Logout"])

        if choice == "Add Doctor":
            import admin_panel
            admin_panel.app()

        elif choice == "Logout":
            st.session_state.clear()
            st.rerun()

    else:
        st.error("⚠️ Role not set properly. Please login again.")
        st.session_state.clear()
        st.rerun()