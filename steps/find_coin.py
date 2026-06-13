from autodistill.detection import CaptionOntology
from autodistill_grounding_dino import GroundingDINO
import torch
import os

print("🚀 เริ่มต้นสคริปต์ค้นหาเหรียญ...")

ontology = CaptionOntology({
    "coin": "coin"
})

# 1. ล็อก Path ให้เป๊ะ ไม่ให้โฟลเดอร์กระเด็นไปที่อื่น
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR_PATH = os.path.join(CURRENT_DIR, "..", "test_images_flat")
DATASET_DIR_PATH = os.path.join(CURRENT_DIR, "..", "dataset") # <--- แก้ตรงนี้แล้ว!

print(f"📂 กำลังดึงรูปจาก: {IMAGE_DIR_PATH}")
print(f"💾 จะบันทึก Dataset ไปที่: {DATASET_DIR_PATH}")

torch.use_deterministic_algorithms(False)

# 2. เรียกใช้ DINO
print("🤖 กำลังโหลดโมเดล Grounding DINO (ครั้งแรกอาจจะใช้เวลาโหลดไฟล์นิดนึง)...")
base_model = GroundingDINO(ontology=ontology)

# 3. สั่งรัน
print("🔍 เริ่มทำการ Auto-Label...")
dataset = base_model.label(
    input_folder=IMAGE_DIR_PATH,
    extension=".jpg",  # 🚨 เช็คให้ชัวร์ว่าไฟล์ใน test_images_flat เป็น .jpg
    output_folder=DATASET_DIR_PATH
)

print("✅ ตีกรอบเสร็จสมบูรณ์! ลองเช็คโฟลเดอร์ dataset ดูครับ")