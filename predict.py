import tensorflow as tf
import numpy as np
import cv2

model = tf.keras.models.load_model("disease_model.h5")

class_names = ["FMD_Cattle", "Lumpy Skin", "Normal Skin"]

img = cv2.imread("test_image.jpg")
img = cv2.resize(img, (224, 224))
img = img / 255.0
img = np.expand_dims(img, axis=0)

prediction = model.predict(img)
print("Predicted Disease:", class_names[np.argmax(prediction)])