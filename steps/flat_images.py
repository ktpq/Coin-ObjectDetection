import os
import shutil

# 1. หาตำแหน่งของไฟล์สคริปต์นี้ก่อน (มันจะรู้ตัวว่าอยู่ในโฟลเดอร์ steps)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. ถอยขึ้นไป 1 ชั้น (..) แล้วเข้าไปหาโฟลเดอร์เป้าหมาย
SOURCE_DIR = os.path.join(CURRENT_DIR, "..", "test_images", "thai_coins_images")
FLAT_DIR = os.path.join(CURRENT_DIR, "..", "test_images_flat")

os.makedirs(FLAT_DIR, exist_ok=True)
print("🔄 กำลังรวมไฟล์และประทับตราชื่อ...")

for folder_name in os.listdir(SOURCE_DIR):
    folder_path = os.path.join(SOURCE_DIR, folder_name)
    
    # เช็คว่าเป็นโฟลเดอร์จริงๆ
    if os.path.isdir(folder_path):
        for file_name in os.listdir(folder_path):
            if file_name.lower().endswith(('.jpg', '.png', '.jpeg')):
                # สร้างชื่อใหม่: เช่น จาก 1_baht/pic01.jpg -> 1_baht___pic01.jpg
                new_name = f"{folder_name}___{file_name}"
                shutil.copy(
                    os.path.join(folder_path, file_name), 
                    os.path.join(FLAT_DIR, new_name)
                )

print(f"✅ เตรียมรูปภาพพร้อมส่งให้ DINO อยู่ในโฟลเดอร์: {FLAT_DIR}")