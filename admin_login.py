import streamlit as st
import sqlite3

import auth


def app():
    if 'show_admin_reset' not in st.session_state:
        st.session_state.show_admin_reset = False

    if not st.session_state.show_admin_reset:
        st.title('Admin Login')

        with st.form('admin_login_form'):
            email = st.text_input('Email')
            password = st.text_input('Password', type='password')
            submitted = st.form_submit_button('Login as Admin')

        if submitted:
            if not email or not password:
                st.error('Please enter email and password')
                return

            conn = sqlite3.connect('database.db')
            c = conn.cursor()

            hashed = auth.hash_password(password)
            c.execute(
                'SELECT id, name FROM users WHERE email=? AND password=? AND role=?',
                (email, hashed, 'admin')
            )
            admin = c.fetchone()

            if not admin:
                c.execute(
                    'SELECT id, name FROM users WHERE email=? AND password=? AND role=?',
                    (email, password, 'admin')
                )
                admin_plain = c.fetchone()
                if admin_plain:
                    c.execute(
                        'UPDATE users SET password=? WHERE id=?',
                        (hashed, admin_plain[0])
                    )
                    conn.commit()
                    admin = admin_plain
                    st.info('Password upgraded to secure hash')

            conn.close()

            if admin:
                st.session_state.logged_in = True
                st.session_state.role = 'admin'
                st.session_state.user_id = admin[0]
                st.session_state.user_name = admin[1]
                st.success('Admin login successful')
                st.rerun()
            else:
                st.error('Invalid admin credentials')

        if st.button('Forgot Password?'):
            st.session_state.show_admin_reset = True
            st.rerun()

    else:
        st.title('Admin Password Reset')

        with st.form('admin_reset_form'):
            email = st.text_input('Registered Admin Email')
            new_password = st.text_input('New Password', type='password')
            confirm_password = st.text_input('Confirm New Password', type='password')
            reset_submitted = st.form_submit_button('Reset Password')

        if reset_submitted:
            if not email or not new_password or not confirm_password:
                st.error('Please complete all fields')
            elif new_password != confirm_password:
                st.error('Passwords do not match')
            else:
                if auth.reset_password(email, new_password, role='admin'):
                    st.success('Password reset successful. Please login.')
                    st.session_state.show_admin_reset = False
                    st.rerun()
                else:
                    st.error('No admin account found with that email')

        if st.button('Back to Login'):
            st.session_state.show_admin_reset = False
            st.rerun()
