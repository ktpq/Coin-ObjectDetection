import cv2
import os
import glob

# 1. ตั้งค่าโฟลเดอร์ (ถ้ารันไฟล์นี้จากในโฟลเดอร์ steps)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(CURRENT_DIR, "..", "dataset") 
OUTPUT_DIR = os.path.join(CURRENT_DIR, "..", "cropped_coins")

os.makedirs(OUTPUT_DIR, exist_ok=True)
print(f"🚀 กำลังเริ่มตัดภาพจาก Dataset: {DATASET_DIR}")

count = 0
# 2. วนลูปเข้าไปดึงรูปจากทั้งโฟลเดอร์ train และ valid
for split in ['train', 'valid']:
    img_dir = os.path.join(DATASET_DIR, split, 'images')
    lbl_dir = os.path.join(DATASET_DIR, split, 'labels')
    
    # ดึงไฟล์รูปทั้งหมด
    image_files = glob.glob(os.path.join(img_dir, '*.jpg')) + glob.glob(os.path.join(img_dir, '*.png'))
    
    for img_path in image_files:
        filename = os.path.basename(img_path)
        name, _ = os.path.splitext(filename)
        lbl_path = os.path.join(lbl_dir, name + '.txt')
        
        # ถ้าไม่มีไฟล์ txt Label ให้ข้ามไป
        if not os.path.exists(lbl_path): 
            continue
            
        img = cv2.imread(img_path)
        if img is None: continue
        h, w, _ = img.shape
        
        with open(lbl_path, 'r') as f:
            lines = f.readlines()
            
        # 3. เริ่มกระบวนการตัดรูปตามพิกัด YOLO
        for idx, line in enumerate(lines):
            parts = line.strip().split()
            if len(parts) < 5: continue
            
            # แปลงสัดส่วนพิกัด YOLO กลับมาเป็นขนาด Pixel จริงของรูป
            _, x_c, y_c, bw, bh = map(float, parts[:5])
            x1 = int((x_c - bw / 2) * w)
            y1 = int((y_c - bh / 2) * h)
            x2 = int((x_c + bw / 2) * w)
            y2 = int((y_c + bh / 2) * h)
            
            # ป้องกันกรณี AI หากรอบทะลุขอบภาพ
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(w, x2), min(h, y2)
            
            # ✂️ สั่งตัดภาพ
            crop_img = img[y1:y2, x1:x2]
            if crop_img.shape[0] == 0 or crop_img.shape[1] == 0: continue
            
            # บันทึกภาพที่ตัดแล้วลงโฟลเดอร์
            # ตัวอย่างชื่อไฟล์: train_001_1_Baht_thailand_crop0.jpg
            crop_name = f"{split}_{name}_crop{idx}.jpg"
            cv2.imwrite(os.path.join(OUTPUT_DIR, crop_name), crop_img)
            count += 1

print(f"✅ เสร็จสิ้น! ตัดรูปเหรียญเน้นๆ ออกมาได้ทั้งหมด {count} รูป")
print(f"📁 เข้าไปดูรูปได้ที่โฟลเดอร์: {OUTPUT_DIR}")