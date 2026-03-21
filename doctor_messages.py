import streamlit as st
import sqlite3
import os

def get_connection():
    db_path = os.path.abspath("database.db")
    return sqlite3.connect(db_path)

def app():
    st.title("💬 Farmer Messages")

    conn = get_connection()
    c = conn.cursor()

    # ✅ SHOW ONLY NOT DELETED MESSAGES
    c.execute("""
    SELECT id, user_id, message, reply, created_at
    FROM messages
    WHERE is_deleted = 0
    ORDER BY created_at DESC
    """)

    messages = c.fetchall()
    conn.close()

    # ✅ DELETE FUNCTION
    def delete_message(msg_id):
        conn = get_connection()
        c = conn.cursor()
        c.execute(
            "UPDATE messages SET is_deleted = 1 WHERE id=?",
            (msg_id,)
        )
        conn.commit()
        conn.close()

    if messages:
        for msg in messages:
            msg_id, user_id, message, reply, date = msg

            st.markdown("---")
            st.write("👤 User ID:", user_id)
            st.write("💬 Message:", message)
            st.write("🕒 Date:", date)

            if reply:
                st.success(f"👨‍⚕️ Reply: {reply}")

            # ✍ Reply box
            reply_input = st.text_area(
                "Write Reply",
                key=f"reply_{msg_id}"
            )

            col1, col2 = st.columns(2)

            # ✅ SEND REPLY
            with col1:
                if st.button("Send Reply", key=f"send_{msg_id}"):
                    if reply_input.strip():
                        conn = get_connection()
                        c = conn.cursor()

                        c.execute("""
                        UPDATE messages
                        SET reply=?, status='Answered'
                        WHERE id=?
                        """, (reply_input, msg_id))

                        conn.commit()
                        conn.close()

                        st.success("✅ Reply sent!")
                        st.rerun()
                    else:
                        st.warning("⚠️ Enter reply first")

            # ✅ DELETE BUTTON
            with col2:
                if st.button("🗑 Delete", key=f"delete_{msg_id}"):
                    delete_message(msg_id)
                    st.warning("Message deleted")
                    st.rerun()

    else:
        st.info("No messages yet")