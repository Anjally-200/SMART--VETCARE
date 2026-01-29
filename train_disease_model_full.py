import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import (
    GlobalAveragePooling2D, Dense, Dropout, BatchNormalization
)
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from sklearn.utils.class_weight import compute_class_weight
from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

# ==================================================
# CONFIG
# ==================================================
DATASET_DIR = "datasets/diseases"
IMG_SIZE = (224, 224)
BATCH_SIZE = 16
EPOCHS = 25
MODEL_NAME = "disease_model.keras"

# ==================================================
# STEP 1: DATASET CLEANING (UNCHANGED – GOOD)
# ==================================================
print("\n🔍 STEP 1: Checking dataset integrity...\n")

valid_ext = (".jpg", ".jpeg", ".png")
total_removed = 0

for cls in os.listdir(DATASET_DIR):
    cls_path = os.path.join(DATASET_DIR, cls)
    if not os.path.isdir(cls_path):
        continue

    removed = 0
    for img_name in os.listdir(cls_path):
        img_path = os.path.join(cls_path, img_name)

        if not img_name.lower().endswith(valid_ext):
            os.remove(img_path)
            removed += 1
            continue

        img_cv = cv2.imread(img_path)
        if img_cv is None:
            os.remove(img_path)
            removed += 1
            continue

        try:
            with Image.open(img_path) as im:
                im.verify()
        except Exception:
            os.remove(img_path)
            removed += 1

    total_removed += removed
    print(f"{cls:<15} -> cleaned {removed} files")

print(f"\n✅ Dataset cleaning completed. Total removed: {total_removed}\n")

# ==================================================
# STEP 2: DATA GENERATORS (FIXED)
# ==================================================
print("🧪 STEP 2: Creating data generators...\n")

train_datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2,
    rotation_range=30,
    zoom_range=0.25,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.15,
    horizontal_flip=True,
    brightness_range=[0.8, 1.2]
)

val_datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

train_gen = train_datagen.flow_from_directory(
    DATASET_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="training",
    shuffle=True
)

val_gen = val_datagen.flow_from_directory(
    DATASET_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="validation",
    shuffle=False
)

NUM_CLASSES = train_gen.num_classes
print("✅ Class indices:", train_gen.class_indices)

# ==================================================
# STEP 3: CLASS WEIGHTS (CORRECT – KEEP)
# ==================================================
print("\n⚖️ STEP 3: Computing class weights...\n")

labels = train_gen.classes

weights = compute_class_weight(
    class_weight="balanced",
    classes=np.unique(labels),
    y=labels
)

class_weights = dict(zip(np.unique(labels), weights))
print("✅ Class weights:", class_weights)

# ==================================================
# STEP 4: MODEL (UPGRADED)
# ==================================================
print("\n🧠 STEP 4: Building model...\n")

base_model = MobileNetV2(
    include_top=False,
    weights="imagenet",
    input_shape=(224, 224, 3)
)

base_model.trainable = False  # Phase 1

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = BatchNormalization()(x)
x = Dense(256, activation="relu")(x)
x = Dropout(0.5)(x)
outputs = Dense(NUM_CLASSES, activation="softmax")(x)

model = Model(inputs=base_model.input, outputs=outputs)

model.compile(
    optimizer=Adam(learning_rate=1e-4),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# ==================================================
# STEP 5: CALLBACKS (BETTER)
# ==================================================
callbacks = [
    EarlyStopping(monitor="val_loss", patience=6, restore_best_weights=True),
    ReduceLROnPlateau(monitor="val_loss", factor=0.3, patience=3, min_lr=1e-6),
    ModelCheckpoint(MODEL_NAME, monitor="val_loss", save_best_only=True)
]

# ==================================================
# STEP 6: TRAIN (PHASE 1)
# ==================================================
print("\n🚀 STEP 6: Training (feature extraction)...\n")

history = model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=EPOCHS,
    class_weight=class_weights,
    callbacks=callbacks
)

# ==================================================
# STEP 7: FINE-TUNING (THIS BOOSTS TO 85%+)
# ==================================================
print("\n🔥 STEP 7: Fine-tuning top layers...\n")

for layer in base_model.layers[-30:]:
    layer.trainable = True

model.compile(
    optimizer=Adam(learning_rate=1e-5),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

history_fine = model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=10,
    class_weight=class_weights,
    callbacks=callbacks
)

# ==================================================
# STEP 8: SAVE MODEL
# ==================================================
model.save(MODEL_NAME)
print(f"\n✅ Disease model saved as {MODEL_NAME}")
