import streamlit as st
import sqlite3

def app():
    st.title(" Disease Prediction History")

    # Check if user is logged in
    if "user_id" not in st.session_state:
        st.warning("Please login first")
        return

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # ✅ UPDATED QUERY (added id + is_deleted filter)
    c.execute("""
        SELECT id, disease, confidence, created_at
        FROM disease_history
        WHERE user_id = ? AND is_deleted = 0
        ORDER BY created_at DESC
    """, (st.session_state.user_id,))

    rows = c.fetchall()
    conn.close()

    # ---------- DELETE FUNCTION ----------
    def delete_record(record_id):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute(
            "UPDATE disease_history SET is_deleted = 1 WHERE id=?",
            (record_id,)
        )
        conn.commit()
        conn.close()

    if rows:
        for row in rows:
            record_id = row[0]
            disease = row[1]

            # safe conversion
            try:
                confidence = float(row[2])
            except:
                confidence = 0.0

            date = row[3]

            st.markdown("---")
            st.write(" Disease:", disease)
            st.write(" Confidence:", f"{confidence:.2f}%")
            st.write(" Date:", date)

            # ✅ DELETE BUTTON
            if st.button("🗑 Delete", key=f"disease_del_{record_id}"):
                delete_record(record_id)
                st.success("Deleted successfully")
                st.rerun()

    else:
        st.info("No disease prediction history yet")