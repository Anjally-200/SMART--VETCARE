import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go


def get_db_connection():
    """Create database connection"""
    return sqlite3.connect('database.db')


def get_recent_predictions(user_id, days=7):
    """Get recent predictions for dashboard stats"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT COUNT(*), AVG(confidence)
        FROM breed_history
        WHERE user_id = ? 
        AND created_at >= datetime('now', '-{days} days')
        AND is_deleted = 0
    """, (user_id,))
    breed_data = cursor.fetchone()

    cursor.execute(f"""
        SELECT COUNT(*), AVG(confidence)
        FROM disease_history
        WHERE user_id = ? 
        AND created_at >= datetime('now', '-{days} days')
        AND is_deleted = 0
    """, (user_id,))
    disease_data = cursor.fetchone()

    cursor.execute(f"""
        SELECT COUNT(*)
        FROM disease_history
        WHERE user_id = ? 
        AND created_at >= datetime('now', '-{days} days')
        AND disease != 'Healthy' 
        AND is_deleted = 0
    """, (user_id,))
    alerts_data = cursor.fetchone()

    conn.close()

    return {
        'breed_count': breed_data[0] or 0,
        'breed_avg_confidence': round((breed_data[1] or 0) * 100, 1),
        'disease_count': disease_data[0] or 0,
        'disease_avg_confidence': round((disease_data[1] or 0) * 100, 1),
        'alerts_count': alerts_data[0] or 0
    }


def get_recent_history(user_id, limit=5):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 'breed', breed, confidence, created_at
        FROM breed_history
        WHERE user_id = ? AND is_deleted = 0
        UNION ALL
        SELECT 'disease', disease, confidence, created_at
        FROM disease_history
        WHERE user_id = ? AND is_deleted = 0
        ORDER BY created_at DESC
        LIMIT ?
    """, (user_id, user_id, limit))

    history = cursor.fetchall()
    conn.close()
    return history


def get_prediction_trends(user_id, days=30):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT DATE(created_at),
               COUNT(CASE WHEN type = 'breed' THEN 1 END),
               COUNT(CASE WHEN type = 'disease' THEN 1 END)
        FROM (
            SELECT 'breed' as type, created_at FROM breed_history
            WHERE user_id = ? AND is_deleted = 0 
            AND created_at >= datetime('now', '-{days} days')
            UNION ALL
            SELECT 'disease' as type, created_at FROM disease_history
            WHERE user_id = ? AND is_deleted = 0 
            AND created_at >= datetime('now', '-{days} days')
        )
        GROUP BY DATE(created_at)
        ORDER BY DATE(created_at)
    """, (user_id, user_id))

    trends = cursor.fetchall()
    conn.close()
    return trends


def app():
    st.markdown(f"## 🐄 Farmer Dashboard — Welcome {st.session_state.user_name}")
    st.write("---")

    user_id = st.session_state.user_id

    stats = get_recent_predictions(user_id)
    recent_history = get_recent_history(user_id)
    trends = get_prediction_trends(user_id)

    # Metrics
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Breed Predictions", stats['breed_count'])
    with col2:
        st.metric("Disease Checks", stats['disease_count'])
    with col3:
        st.metric("Health Alerts", stats['alerts_count'])
    with col4:
        st.metric("Avg Breed Confidence", f"{stats['breed_avg_confidence']}%")
    with col5:
        st.metric("Avg Disease Confidence", f"{stats['disease_avg_confidence']}%")

    st.write("---")

    # Buttons
    st.markdown("### Quick Actions")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🧾 Breed Prediction", use_container_width=True):
            st.session_state.page = "Breed Prediction"
            st.rerun()

    with col2:
        if st.button("🦠 Disease Prediction", use_container_width=True):
            st.session_state.page = "Disease Prediction"
            st.rerun()

    with col3:
        if st.button("📞 Consultation", use_container_width=True):
            st.session_state.page = "Support"
            st.rerun()

    with col4:
        if st.button("📊 History", use_container_width=True):
            st.session_state.page = "Breed History"
            st.rerun()

    st.write("---")

    # Recent Activity
    if recent_history:
        st.markdown("### Recent Activity")
        for pred_type, prediction, confidence, created_at in recent_history:
            icon = "🐄" if pred_type == "breed" else "🦠"
            confidence_pct = confidence * 100 if isinstance(confidence, float) else float(confidence) * 100
            st.write(f"{icon} **{pred_type.upper()}**: {prediction} ({confidence_pct:.1f}%) — {created_at}")

    # Chart
    if trends:
        st.markdown("### Prediction Trends")

        dates = [row[0] for row in trends]
        breed_counts = [row[1] for row in trends]
        disease_counts = [row[2] for row in trends]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=breed_counts, mode='lines+markers', name='Breed', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=dates, y=disease_counts, mode='lines+markers', name='Disease', line=dict(color='red')))
        fig.update_layout(height=300, hovermode='x unified')

        st.plotly_chart(fig, use_container_width=True)

    # Tips
    st.markdown("### 💡 Health Tips")
    tips_col1, tips_col2 = st.columns(2)
    
    with tips_col1:
        st.info("✓ Check cattle health regularly to catch diseases early.")
    with tips_col2:
        st.info("✓ Maintain clean feeding and watering areas.")

    # Alerts
    if stats['alerts_count'] > 0:
        st.error(f"⚠️ {stats['alerts_count']} health alerts detected! Consider consulting a veterinarian.")


# ✅ FIXED HERE (removed invalid tag)
if __name__ == "__main__":
    app()