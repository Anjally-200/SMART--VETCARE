import streamlit as st
import sqlite3

def app():
    st.title(" Breed Prediction History")

    # ---------- DB CONNECTION ----------
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # ✅ SHOW ONLY NOT DELETED
    c.execute("""
    SELECT id, breed, confidence, created_at
    FROM breed_history
    WHERE user_id = ? AND is_deleted = 0
    ORDER BY created_at DESC
    """, (st.session_state.user_id,))

    rows = c.fetchall()
    conn.close()

    # ---------- SOFT DELETE FUNCTION ----------
    def delete_record(record_id):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("UPDATE breed_history SET is_deleted = 1 WHERE id=?", (record_id,))
        conn.commit()
        conn.close()

    # ---------- CLEAR ALL (SOFT DELETE) ----------
    def clear_all():
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute(
            "UPDATE breed_history SET is_deleted = 1 WHERE user_id=?",
            (st.session_state.user_id,)
        )
        conn.commit()
        conn.close()

    # ---------- UI ----------
    if rows:

        # 🔥 Clear all button
        if st.button("🗑 Clear All History"):
            clear_all()
            st.success("All history cleared!")
            st.rerun()

        for row in rows:
            record_id = row[0]
            breed = row[1]

            # Safe conversion
            try:
                confidence = float(row[2])
            except:
                confidence = 0.0

            date = row[3]

            st.markdown("---")
            st.write(" Breed:", breed)
            st.write(" Confidence:", f"{confidence:.2f}%")
            st.write(" Date:", date)

            # 🔥 DELETE BUTTON
            if st.button("🗑 Delete", key=f"del_{record_id}"):
                delete_record(record_id)
                st.success("Deleted successfully")
                st.rerun()

    else:
        st.info("No prediction history yet")