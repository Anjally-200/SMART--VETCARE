import os
import shutil
import random

BASE_DIR = os.getcwd()

TRAIN_RATIO = 0.7
VAL_RATIO = 0.2
TEST_RATIO = 0.1


def split_dataset(SRC_DIR, DEST_DIR, dataset_name):
    print(f"\n🔄 Preparing {dataset_name} training data...")
    print("Source:", SRC_DIR)
    print("Destination:", DEST_DIR)

    # Safety check
    if not os.path.exists(SRC_DIR):
        print("❌ Source directory does not exist:", SRC_DIR)
        return

    for class_name in os.listdir(SRC_DIR):
        class_path = os.path.join(SRC_DIR, class_name)

        if not os.path.isdir(class_path):
            continue

        images = [
            img for img in os.listdir(class_path)
            if img.lower().endswith((".jpg", ".jpeg", ".png"))
        ]

        if len(images) == 0:
            print(f"⚠️ Skipping empty class: {class_name}")
            continue

        random.shuffle(images)

        total = len(images)
        train_end = int(total * TRAIN_RATIO)
        val_end = train_end + int(total * VAL_RATIO)

        splits = {
            "train": images[:train_end],
            "val": images[train_end:val_end],
            "test": images[val_end:]
        }

        for split, files in splits.items():
            split_dir = os.path.join(DEST_DIR, split, class_name)
            os.makedirs(split_dir, exist_ok=True)

            for img in files:
                shutil.copy(
                    os.path.join(class_path, img),
                    os.path.join(split_dir, img)
                )

        print(f"✅ Split completed for: {class_name}")


# =========================
# SPLIT DISEASE DATASET
# =========================
split_dataset(
    os.path.join(BASE_DIR, "processed_data", "diseases"),
    os.path.join(BASE_DIR, "training_data", "diseases"),
    "DISEASE"
)

# =========================
# SPLIT BREED DATASET
# =========================
split_dataset(
    os.path.join(BASE_DIR, "processed_data", "breeds"),
    os.path.join(BASE_DIR, "training_data", "breeds"),
    "BREED"
)

print("\n🎉 training_data created successfully for diseases and breeds!")
