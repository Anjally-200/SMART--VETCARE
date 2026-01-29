import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam

# ================================
# CONFIGURATION
# ================================
DATASET_DIR = "datasets/breeds"
IMG_SIZE = (224, 224)
BATCH_SIZE = 16
EPOCHS = 20   # enough with ImageNet

# ================================
# DATA GENERATORS
# ================================
train_datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2,
    rotation_range=25,
    zoom_range=0.2,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    brightness_range=[0.8, 1.2]
)

train_gen = train_datagen.flow_from_directory(
    DATASET_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training',
    shuffle=True
)

val_gen = train_datagen.flow_from_directory(
    DATASET_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation',
    shuffle=False
)

NUM_CLASSES = train_gen.num_classes
print("✅ Classes:", train_gen.class_indices)

# ================================
# MODEL (IMAGENET PRETRAINED)
# ================================
base_model = MobileNetV2(
    include_top=False,
    weights="imagenet",      # 🔥 KEY CHANGE
    input_shape=(224, 224, 3)
)

base_model.trainable = False   # 🔒 freeze pretrained backbone

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dropout(0.4)(x)
outputs = Dense(NUM_CLASSES, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=outputs)

model.compile(
    optimizer=Adam(learning_rate=1e-3),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

# ================================
# TRAIN (STAGE 1)
# ================================
history = model.fit(
    train_gen,
    epochs=EPOCHS,
    validation_data=val_gen
)

# ================================
# SAVE MODEL
# ================================
model.save("breed_model.keras")
print("✅ Breed model saved as breed_model.keras")
