
import cv2

import os
from dotenv import load_dotenv
load_dotenv()
images_path = os.environ.get("IMAGES_PATH")

# 1. หาตำแหน่งของไฟล์สคริปต์นี้ก่อน (มันจะรู้ตัวว่าอยู่ในโฟลเดอร์ steps)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. ถอยขึ้นไป 1 ชั้น (..) แล้วเข้าไปหาโฟลเดอร์เป้าหมาย (เปลี่ยนเป็น images2 แล้ว)
SOURCE_DIR = os.path.join(CURRENT_DIR, "..", f"{images_path}")
FLAT_DIR = os.path.join(CURRENT_DIR, "..", "test_images_flat")

os.makedirs(FLAT_DIR, exist_ok=True)
print("🔄 กำลังรวมไฟล์และแปลงทุกรูปให้เป็น .jpg...")

for folder_name in os.listdir(SOURCE_DIR):
    folder_path = os.path.join(SOURCE_DIR, folder_name)
    
    # เช็คว่าเป็นโฟลเดอร์จริงๆ
    if os.path.isdir(folder_path):
        for file_name in os.listdir(folder_path):
            if file_name.lower().endswith(('.jpg', '.png', '.jpeg')):
                # ตัดนามสกุลเดิมออก และบังคับให้ใส่ .jpg
                base_name = os.path.splitext(file_name)[0]
                new_name = f"{folder_name}___{base_name}.png"
                
                src_path = os.path.join(folder_path, file_name)
                dst_path = os.path.join(FLAT_DIR, new_name)
                
                # ใช้ cv2 อ่านและเซฟเป็น jpg เสมอ
                img = cv2.imread(src_path)
                if img is not None:
                    cv2.imwrite(dst_path, img)

print(f"✅ เตรียมรูปภาพพร้อมส่งให้ DINO อยู่ในโฟลเดอร์: {FLAT_DIR}")