import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import streamlit as st
import numpy as np
import tensorflow as tf
from PIL import Image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

import sqlite3
from datetime import datetime

# ---------------- MODEL ----------------
@st.cache_resource
def load_disease_model():
    return tf.keras.models.load_model("disease_model.keras")

model = load_disease_model()

class_names = ["FMD", "Healthy", "LSD"]

# ---------------- DISEASE DETAILS ----------------
disease_details = {
    "FMD": {
        "cause": [
            "Foot and Mouth Disease virus",
            "Spreads through air, saliva, and contaminated feed"
        ],
        "guidance": [
            "Isolate infected animal immediately",
            "Clean mouth and foot lesions",
            "Provide soft food and water",
            "Consult veterinarian urgently"
        ],
        "prevention": [
            "Regular vaccination",
            "Maintain farm hygiene",
            "Disinfect equipment",
            "Avoid infected animals"
        ],
        "severity": "High"
    },

    "LSD": {
        "cause": [
            "Lumpy Skin Disease virus",
            "Spread by mosquitoes, flies, ticks"
        ],
        "guidance": [
            "Isolate infected cattle",
            "Keep animal hydrated",
            "Clean wounds properly",
            "Consult veterinarian"
        ],
        "prevention": [
            "Vaccinate cattle",
            "Control insects",
            "Maintain hygiene",
            "Avoid animal mixing"
        ],
        "severity": "Medium"
    },

    "Healthy": {
        "cause": ["No disease detected"],
        "guidance": ["Maintain regular care and monitoring"],
        "prevention": [
            "Provide good nutrition",
            "Clean water",
            "Regular vaccination"
        ],
        "severity": "Low"
    }
}


# ---------------- MAIN APP ----------------
def app():
    st.title(" Disease Prediction")
    st.write("Upload a cattle image to detect disease")

    uploaded_file = st.file_uploader(
        "Upload cattle image",
        type=["jpg", "jpeg", "png"]
    )

    # -------- IMAGE PREVIEW --------
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)

        # -------- PREDICT BUTTON --------
        if st.button(" Predict Disease"):

            with st.spinner("Analyzing image..."):
                img = image.convert('RGB')
                img = img.resize((224, 224))
                img_array = np.array(img, dtype=np.float32)

                img_array = preprocess_input(img_array)
                img_array = np.expand_dims(img_array, axis=0)

                predictions = model.predict(img_array, verbose=0)
                predicted_index = np.argmax(predictions)
                confidence = predictions[0][predicted_index] * 100

            # SAVE TO SESSION
            st.session_state.predicted_disease = class_names[predicted_index]
            st.session_state.confidence = confidence

            # -------- SAVE HISTORY --------
            try:
                conn = sqlite3.connect("database.db")
                c = conn.cursor()

                c.execute("""
                CREATE TABLE IF NOT EXISTS disease_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    disease TEXT,
                    confidence REAL,
                    created_at TEXT
                )
                """)

                c.execute("""
                INSERT INTO disease_history (user_id, disease, confidence, created_at)
                VALUES (?, ?, ?, ?)
                """, (
                    st.session_state.user_id,
                    st.session_state.predicted_disease,
                    float(confidence),
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ))

                conn.commit()
                conn.close()

            except Exception as e:
                st.error(f"Database error: {e}")

    # -------- SHOW RESULT --------
    if "predicted_disease" in st.session_state:

        disease = st.session_state.predicted_disease
        confidence = st.session_state.confidence

        st.success(f" Predicted Disease: **{disease}**")
        st.info(f"Confidence: **{confidence:.2f}%**")

        details = disease_details.get(disease)

        if details:
            st.markdown("##  AI Instant Guidance")

            # Cause
            st.markdown("###  Cause")
            for c in details["cause"]:
                st.write("•", c)

            # Guidance
            st.markdown("###  What You Should Do")
            for g in details["guidance"]:
                st.write("•", g)

            # Prevention
            st.markdown("###  Prevention")
            for p in details["prevention"]:
                st.write("•", p)

            # Severity
            st.markdown("###  Severity Level")
            severity = details["severity"]

            if severity == "High":
                st.error(f" {severity} - Immediate action required!")
            elif severity == "Medium":
                st.warning(f" {severity} - Monitor carefully")
            else:
                st.success(f" {severity} - Low risk")

        # -------- CONSULTATION BUTTON --------
        st.markdown("---")

        if st.button(" Request Veterinary Consultation"):

            try:
                conn = sqlite3.connect("database.db")
                c = conn.cursor()

                c.execute("""
                CREATE TABLE IF NOT EXISTS consultation (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    disease TEXT,
                    guidance TEXT,
                    status TEXT,
                    created_at TEXT
                )
                """)

                c.execute("""
                INSERT INTO consultation (user_id, disease, guidance, status, created_at)
                VALUES (?, ?, ?, ?, ?)
                """, (
                    st.session_state.user_id,
                    disease,
                    "AI Guidance Provided",
                    "Pending",
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ))

                conn.commit()
                conn.close()

                st.success(" Consultation request sent successfully!")
                st.rerun()

            except Exception as e:
                st.error(f"Database error: {e}")