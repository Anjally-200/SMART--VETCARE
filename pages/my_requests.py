import streamlit as st
import sqlite3
import os


def get_connection():
    db_path = os.path.abspath("database.db")
    return sqlite3.connect(db_path)


def app():
    st.title("📋 My Requests")

    # ✅ SAFETY CHECK
    if "user_id" not in st.session_state:
        st.warning("Please login first")
        st.stop()

    user_id = st.session_state.user_id

    try:
        conn = get_connection()
        c = conn.cursor()

        c.execute("""
        SELECT disease, guidance, doctor_response, status, created_at
        FROM consultation
        WHERE user_id=?
        ORDER BY created_at DESC
        """, (user_id,))

        rows = c.fetchall()
        conn.close()

        if rows:
            for row in rows:
                st.markdown("---")

                disease, ai_guidance, doctor_response, status, date = row

                st.write("🦠 Disease:", disease)
                st.write("🤖 AI Guidance:", ai_guidance)

                if doctor_response:
                    st.write("👨‍⚕️ Doctor Advice:", doctor_response)
                else:
                    st.write("👨‍⚕️ Doctor Advice: Waiting for doctor response...")

                st.write("🕒 Date:", date)

                if status == "Pending":
                    st.warning("📌 Pending")
                elif status == "Approved":
                    st.info("✅ Approved")
                elif status == "Completed":
                    st.success("✔ Completed")
                elif status == "Rejected":
                    st.error("❌ Rejected")

        else:
            st.info("No requests yet")

    except Exception as e:
        st.error(f"Error: {e}")


if __name__ == "__main__":
    app()