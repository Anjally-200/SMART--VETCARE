import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import streamlit as st
import numpy as np
import tensorflow as tf
from PIL import Image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# -------- DATABASE IMPORTS --------
import sqlite3
from datetime import datetime

@st.cache_resource
def load_breed_model():
    return tf.keras.models.load_model("breed_model.keras")

model = load_breed_model()

class_names = [
    "Ayrshire cattle",
    "Brown Swiss cattle",
    "Holstein Friesian cattle",
    "Jersey cattle",
    "Red Dane cattle"
]

def app():
    st.title("🐄 Breed Prediction")

    uploaded_file = st.file_uploader(
        "Upload cattle image",
        type=["jpg", "png", "jpeg"]
    )

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)

        if st.button("🔍 Predict Breed"):
            with st.spinner("Analyzing image..."):
                # Preprocessing
                img = image.convert('RGB')
                img = img.resize((224, 224))
                img_array = np.array(img, dtype=np.float32)
                
                img_array = preprocess_input(img_array)
                img_array = np.expand_dims(img_array, axis=0)

                prediction = model.predict(img_array, verbose=0)
                index = np.argmax(prediction)
                confidence = prediction[0][index] * 100

                # Check if confidence is low, classify as "others"
                if confidence < 50.0:
                    predicted_breed = "others"
                else:
                    predicted_breed = class_names[index]

            st.success(f"🐮 Predicted Breed: **{predicted_breed}**")
            st.info(f"Confidence: {confidence:.2f}%")

            # -------- SAVE TO HISTORY --------
            try:
                conn = sqlite3.connect("database.db")
                c = conn.cursor()

                c.execute("""
                INSERT INTO breed_history (user_id, breed, confidence, created_at)
                VALUES (?, ?, ?, ?)
                """, (
                    st.session_state.user_id,
                    predicted_breed,
                    float(confidence),   # ⭐ FIX: ensure float
                    datetime.now()
                ))

                conn.commit()
                conn.close()

            except Exception as e:
                st.error(f"Database error: {e}")
