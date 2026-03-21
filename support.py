import streamlit as st
import sqlite3
from datetime import datetime

def app():
    st.title("💬 Ask a Veterinarian")

    # ✅ Check login
    if "user_id" not in st.session_state:
        st.warning("Please login first")
        st.stop()

    # ---------------- SEND MESSAGE ----------------
    message = st.text_area("Enter your question")

    if st.button("Send Message"):
        if message.strip():
            conn = sqlite3.connect("database.db")
            c = conn.cursor()

            c.execute("""
            INSERT INTO messages (user_id, message, created_at)
            VALUES (?, ?, ?)
            """, (
                st.session_state.user_id,
                message,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))

            conn.commit()
            conn.close()

            st.success("✅ Message sent to doctor!")
            st.rerun()
        else:
            st.warning("⚠️ Please enter a message")

    # ---------------- VIEW MESSAGES ----------------
    st.markdown("---")
    st.subheader("📩 Your Messages")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # ✅ UPDATED QUERY (added id + is_deleted filter)
    c.execute("""
    SELECT id, message, reply, status, created_at
    FROM messages
    WHERE user_id=? AND is_deleted = 0
    ORDER BY created_at DESC
    """, (st.session_state.user_id,))

    rows = c.fetchall()
    conn.close()

    # ✅ DELETE FUNCTION
    def delete_message(msg_id):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute(
            "UPDATE messages SET is_deleted = 1 WHERE id=?",
            (msg_id,)
        )
        conn.commit()
        conn.close()

    if rows:
        for row in rows:
            msg_id = row[0]
            user_msg = row[1]
            reply = row[2]
            status = row[3]
            date = row[4]

            st.markdown("---")

            st.write("💬 You:", user_msg)

            if reply:
                st.success(f"👨‍⚕️ Doctor: {reply}")
            else:
                st.warning("⏳ Waiting for doctor reply...")

            st.write("📅 Date:", date)

            # ✅ DELETE BUTTON
            if st.button("🗑 Delete", key=f"user_msg_del_{msg_id}"):
                delete_message(msg_id)
                st.warning("Message deleted")
                st.rerun()

    else:
        st.info("No messages yet")