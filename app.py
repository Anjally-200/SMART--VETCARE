import streamlit as st
from auth import login, register

st.set_page_config(page_title="Smart Vet", layout="centered")

# Session initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- NOT LOGGED IN ----------------
if not st.session_state.logged_in:
    menu = st.sidebar.selectbox(
        "Menu",
        ["Login", "Register"]
    )

    if menu == "Login":
        login()
    else:
        register()

# ---------------- LOGGED IN ----------------
else:
    st.sidebar.success(f"Welcome {st.session_state.user_name}")

    choice = st.sidebar.radio(
        "Navigation",
        ["Dashboard", "Breed Prediction", "Disease Prediction", "Logout"]
    )

    if choice == "Dashboard":
        st.title("🐄 Farmer Dashboard")
        st.write("Select a service from the sidebar")

    elif choice == "Breed Prediction":
        import breed_predict
        breed_predict.app()

    elif choice == "Disease Prediction":
        import disease_predict
        disease_predict.app()

    elif choice == "Logout":
        st.session_state.logged_in = False
        st.rerun()
