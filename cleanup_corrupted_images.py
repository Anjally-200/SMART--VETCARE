import os
import cv2

def check_and_remove_corrupted_images(directory):
    """Check all image files and remove corrupted ones using OpenCV."""
    corrupted_count = 0
    valid_count = 0
    extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(extensions):
                filepath = os.path.join(root, file)
                try:
                    img = cv2.imread(filepath)
                    if img is None:
                        print(f"Removing corrupted: {filepath}")
                        os.remove(filepath)
                        corrupted_count += 1
                    else:
                        valid_count += 1
                except Exception as e:
                    print(f"Error with {filepath}: {e}")
                    try:
                        os.remove(filepath)
                        corrupted_count += 1
                    except:
                        pass
    
    print(f"\n✅ Results:")
    print(f"Valid images: {valid_count}")
    print(f"Corrupted (removed): {corrupted_count}")

if __name__ == "__main__":
    print("🧹 Cleaning corrupted images using OpenCV...")
    check_and_remove_corrupted_images("datasets/diseases")
    print("✅ Cleanup complete!")
