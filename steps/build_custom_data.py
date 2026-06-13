import os
import shutil
import glob
import json

# 1. ตั้งค่าโฟลเดอร์ต้นทาง (ใช้ dataset ของ DINO) และปลายทาง
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DINO_DATASET_DIR = os.path.join(CURRENT_DIR, "..", "dataset") 
OUTPUT_DIR = os.path.join(CURRENT_DIR, "..", "custom_data")

IMG_OUT_DIR = os.path.join(OUTPUT_DIR, "images")
LBL_OUT_DIR = os.path.join(OUTPUT_DIR, "labels")

os.makedirs(IMG_OUT_DIR, exist_ok=True)
os.makedirs(LBL_OUT_DIR, exist_ok=True)

# 2. ค้นหาไฟล์ทั้งหมดจากโฟลเดอร์ dataset ของ DINO (ทั้ง train และ valid)
image_files = []
for split in ['train', 'valid']:
    split_img_dir = os.path.join(DINO_DATASET_DIR, split, 'images')
    if os.path.exists(split_img_dir):
        image_files.extend(glob.glob(os.path.join(split_img_dir, "*.jpg")))

print(f"🔍 พบรูปภาพต้นฉบับทั้งหมด {len(image_files)} รูป")

# 3. แยกข้อมูลคลาสจากชื่อไฟล์
class_dict = {}
for img_path in image_files:
    filename = os.path.basename(img_path)
    if "___" in filename:
        prefix_full = filename.split("___")[0]
        raw_class = prefix_full.replace("train_", "").replace("valid_", "")
        
        if "_" in raw_class:
            prefix_num, actual_name = raw_class.split("_", 1)
            try:
                class_id = int(prefix_num) - 1
                class_dict[class_id] = actual_name
            except ValueError:
                continue

sorted_class_ids = sorted(class_dict.keys())

# 4. สร้างไฟล์ classes.txt และ notes.json
classes_txt_path = os.path.join(OUTPUT_DIR, "classes.txt")
with open(classes_txt_path, "w", encoding="utf-8") as f:
    for cid in range(max(sorted_class_ids) + 1 if sorted_class_ids else 0):
        name = class_dict.get(cid, f"unknown_{cid}")
        f.write(name + "\n")

notes_path = os.path.join(OUTPUT_DIR, "notes.json")
notes_data = {
    "categories": [{"id": cid, "name": class_dict[cid]} for cid in sorted_class_ids],
    "info": {"year": 2026, "version": "2.0 (Full Image)", "contributor": "Auto-Label"}
}
with open(notes_path, "w", encoding="utf-8") as f:
    json.dump(notes_data, f, ensure_ascii=False, indent=2)

print(f"📝 สร้างข้อมูลคลาสสำเร็จ! (พบ {len(class_dict)} คลาส)")
print("🚀 กำลังคัดลอกรูปเต็มและแก้ไข Label ID...")

# 5. คัดลอกภาพเต็มและอัปเดตไฟล์ Label
count = 0
for img_path in image_files:
    filename = os.path.basename(img_path)
    name, _ = os.path.splitext(filename)
    
    # หาโฟลเดอร์ labels ที่คู่กับรูปนี้
    parent_dir = os.path.dirname(os.path.dirname(img_path)) # ถอยกลับไปที่โฟลเดอร์ train หรือ valid
    dino_lbl_path = os.path.join(parent_dir, 'labels', name + '.txt')
    
    if "___" not in filename or not os.path.exists(dino_lbl_path):
        continue
        
    prefix_full = filename.split("___")[0]
    raw_class = prefix_full.replace("train_", "").replace("valid_", "")
    
    if "_" in raw_class:
        prefix_num, _ = raw_class.split("_", 1)
        try:
            target_class_id = int(prefix_num) - 1
        except ValueError:
            continue
            
        # คัดลอกรูปภาพเต็ม (ไม่ Crop)
        new_img_path = os.path.join(IMG_OUT_DIR, filename)
        shutil.copy(img_path, new_img_path)
        
        # อ่านไฟล์ Label เดิมของ DINO แล้วเปลี่ยนเฉพาะเลข Class ด้านหน้า
        new_label_path = os.path.join(LBL_OUT_DIR, name + ".txt")
        with open(dino_lbl_path, "r", encoding="utf-8") as f_in, \
             open(new_label_path, "w", encoding="utf-8") as f_out:
            
            for line in f_in.readlines():
                parts = line.strip().split()
                if len(parts) >= 5:
                    # เปลี่ยนเลขตัวแรก (ซึ่งเดิมคือ 0) เป็น target_class_id
                    parts[0] = str(target_class_id) 
                    # ประกอบร่างกลับเป็นข้อความเหมือนเดิม แล้วเขียนลงไฟล์ใหม่
                    f_out.write(" ".join(parts) + "\n")
        
        count += 1

print(f"🎉 เสร็จสมบูรณ์! จัดเตรียมรูปภาพและ Label ทั้งหมด {count} ไฟล์พร้อมเทรนแล้ว!")