import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import streamlit as st
import numpy as np
import tensorflow as tf
from PIL import Image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

@st.cache_resource
def load_disease_model():
    return tf.keras.models.load_model("disease_model.keras")

model = load_disease_model()

# Update these class names EXACTLY as used during training
class_names = [
    "FMD",
    "Healthy",
    "LSD"
]

def app():
    st.title("🦠 Disease Prediction")

    st.write("Upload a cattle image to detect disease")

    uploaded_file = st.file_uploader(
        "Upload cattle image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(
            image,
            caption="Uploaded Image",
            use_container_width=True
        )

        if st.button("🩺 Predict Disease"):
            with st.spinner("Analyzing image..."):
                # Preprocessing (match training exactly)
                img = image.convert('RGB')  # ensure RGB, removes alpha
                img = img.resize((224, 224))
                img_array = np.array(img, dtype=np.float32)
                
                # Apply MobileNetV2 preprocessing (CRITICAL!)
                img_array = preprocess_input(img_array)
                img_array = np.expand_dims(img_array, axis=0)

                # Prediction
                predictions = model.predict(img_array, verbose=0)
                predicted_index = np.argmax(predictions)
                confidence = predictions[0][predicted_index] * 100

            # Results
            st.success(
                f"🧪 Predicted Disease: **{class_names[predicted_index]}**"
            )
            st.info(
                f"Confidence: **{confidence:.2f}%**"
            )
