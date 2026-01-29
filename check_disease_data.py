import os

base_dir = "datasets/diseases"

print("📂 DISEASE DATASET CHECK")
print("-" * 35)

for cls in sorted(os.listdir(base_dir)):
    cls_path = os.path.join(base_dir, cls)
    if os.path.isdir(cls_path):
        count = len([
            f for f in os.listdir(cls_path)
            if f.lower().endswith(('.jpg', '.jpeg', '.png'))
        ])
        print(f"{cls:<15} -> {count} images")
