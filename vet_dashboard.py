import streamlit as st
import sqlite3
import os
from datetime import datetime

# ---------- DATABASE CONNECTION ----------
def get_connection():
    db_path = os.path.abspath("database.db")
    return sqlite3.connect(db_path)

# ---------- UPDATE STATUS ----------
def update_status(request_id, new_status):
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
    UPDATE consultation
    SET status=?
    WHERE id=?
    """, (new_status, request_id))

    conn.commit()
    conn.close()

# ---------- UPDATE DOCTOR ADVICE ----------
def update_advice(request_id, advice):
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
    UPDATE consultation
    SET doctor_response=?, status='Completed'
    WHERE id=?
    """, (advice, request_id))

    conn.commit()
    conn.close()

# ---------- DELETE REQUEST ----------
def delete_request(request_id):
    conn = get_connection()
    c = conn.cursor()

    c.execute("DELETE FROM consultation WHERE id=?", (request_id,))

    conn.commit()
    conn.close()

# ---------- GET STATISTICS ----------
def get_statistics():
    conn = get_connection()
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM consultation")
    total = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM consultation WHERE status='Pending'")
    pending = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM consultation WHERE status='Completed'")
    completed = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM consultation WHERE status='Approved'")
    approved = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM consultation WHERE status='Rejected'")
    rejected = c.fetchone()[0]
    
    conn.close()
    
    return {
        'total': total,
        'pending': pending,
        'completed': completed,
        'approved': approved,
        'rejected': rejected
    }

# ---------- MAIN APP ----------
def app():
    st.set_page_config(page_title="Vet Dashboard", layout="wide")
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin: 10px 0;
    }
    .metric-value {
        font-size: 32px;
        font-weight: bold;
        margin: 10px 0;
    }
    .metric-label {
        font-size: 14px;
        opacity: 0.9;
    }
    .consultation-card {
        border-left: 5px solid #667eea;
        padding: 20px;
        border-radius: 8px;
        margin: 15px 0;
        background-color: #f8f9fa;
    }
    .status-badge {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("# 👩‍⚕️ Veterinary Dashboard")
        st.markdown("*Manage consultation requests and provide expert guidance*")
    
    st.write("---")
    
    try:
        # Get statistics
        stats = get_statistics()
        
        # Display metrics
        st.markdown("### 📊 Dashboard Overview")
        metric_cols = st.columns(5)
        
        with metric_cols[0]:
            st.metric("📋 Total Requests", stats['total'], delta=None)
        
        with metric_cols[1]:
            st.metric("⏳ Pending", stats['pending'], delta=None)
        
        with metric_cols[2]:
            st.metric("✅ Approved", stats['approved'], delta=None)
        
        with metric_cols[3]:
            st.metric("✔ Completed", stats['completed'], delta=None)
        
        with metric_cols[4]:
            st.metric("❌ Rejected", stats['rejected'], delta=None)
        
        st.write("---")
        
        # Filter options
        st.markdown("### 🔍 Filter Requests")
        filter_cols = st.columns(3)
        
        with filter_cols[0]:
            status_filter = st.selectbox("Filter by Status", ["All", "Pending", "Approved", "Completed", "Rejected"])
        
        with filter_cols[1]:
            search_disease = st.text_input("Search by Disease", placeholder="e.g., FMD, LSD...")
        
        with filter_cols[2]:
            sort_by = st.selectbox("Sort by", ["Latest First", "Oldest First"])
        
        st.write("---")
        
        conn = get_connection()
        c = conn.cursor()

        # ---------- FETCH CONSULTATIONS ----------
        query = "SELECT id, user_id, disease, guidance, doctor_response, status, created_at FROM consultation"
        
        # Apply filters
        where_conditions = []
        if status_filter != "All":
            where_conditions.append(f"status='{status_filter}'")
        if search_disease.strip():
            where_conditions.append(f"disease LIKE '%{search_disease}%'")
        
        if where_conditions:
            query += " WHERE " + " AND ".join(where_conditions)
        
        # Apply sorting
        if sort_by == "Latest First":
            query += " ORDER BY created_at DESC"
        else:
            query += " ORDER BY created_at ASC"
        
        c.execute(query)
        rows = c.fetchall()
        conn.close()

        if rows:
            st.markdown(f"### 📝 Consultation Requests ({len(rows)})")
            
            for idx, row in enumerate(rows):
                request_id = row[0]
                user_id = row[1]
                disease = row[2]
                guidance = row[3]
                doctor_response = row[4]
                status = row[5]
                created_at = row[6]
                
                # Status color mapping
                status_colors = {
                    "Pending": "#FFA500",
                    "Approved": "#4CAF50",
                    "Completed": "#2196F3",
                    "Rejected": "#F44336"
                }
                
                status_color = status_colors.get(status, "#999999")
                
                # Create expandable card
                with st.expander(f"🐄 Request #{request_id} | Disease: {disease} | Status: {status}", expanded=False):
                    
                    # Request details
                    detail_cols = st.columns(4)
                    
                    with detail_cols[0]:
                        st.markdown(f"**👤 User ID**")
                        st.write(f"#{user_id}")
                    
                    with detail_cols[1]:
                        st.markdown(f"**🦠 Disease**")
                        st.write(f"{disease}")
                    
                    with detail_cols[2]:
                        st.markdown(f"**📅 Date**")
                        st.write(f"{created_at}")
                    
                    with detail_cols[3]:
                        st.markdown(f"**📌 Status**")
                        st.markdown(f"<div style='background-color: {status_color}; color: white; padding: 8px 12px; border-radius: 20px; text-align: center; font-weight: bold;'>{status}</div>", unsafe_allow_html=True)
                    
                    st.write("---")
                    
                    # AI Guidance
                    st.markdown("#### 🤖 AI Guidance")
                    st.info(guidance if guidance else "No AI guidance available")
                    
                    # Doctor Response
                    st.markdown("#### 👨‍⚕️ Doctor Advice")
                    if doctor_response:
                        st.success(f"✅ {doctor_response}")
                    else:
                        st.warning("⏳ No advice provided yet")
                    
                    st.write("---")
                    
                    # Action buttons
                    st.markdown("#### 🎯 Actions")
                    
                    action_col1, action_col2, action_col3 = st.columns(3)
                    
                    with action_col1:
                        if st.button("✅ Approve", key=f"approve_{request_id}", use_container_width=True):
                            update_status(request_id, "Approved")
                            st.success("Request approved!")
                            st.rerun()
                    
                    with action_col2:
                        if st.button("❌ Reject", key=f"reject_{request_id}", use_container_width=True):
                            update_status(request_id, "Rejected")
                            st.error("Request rejected!")
                            st.rerun()
                    
                    with action_col3:
                        if st.button("🗑️ Delete", key=f"delete_{request_id}", use_container_width=True):
                            delete_request(request_id)
                            st.warning("Request deleted!")
                            st.rerun()
                    
                    st.write("---")
                    
                    # Advice input
                    st.markdown("#### 💬 Provide Your Expert Advice")
                    advice = st.text_area(
                        "Write detailed medical advice and recommendations",
                        key=f"advice_box_{request_id}",
                        height=120,
                        placeholder="Enter your professional veterinary advice here..."
                    )

                    if st.button("📤 Send Advice", key=f"send_{request_id}", use_container_width=True):
                        if advice.strip():
                            update_advice(request_id, advice)
                            st.success("✅ Advice sent successfully to farmer!")
                            st.rerun()
                        else:
                            st.warning("⚠️ Please enter advice before sending")

        else:
            st.info("📭 No consultation requests. All caught up!")

    except Exception as e:
        st.error(f"❌ Database error: {e}")


# ---------- RUN ----------
if __name__ == "__main__":
    app()