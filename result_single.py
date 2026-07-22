import cv2
from ultralytics import YOLO


import os
from dotenv import load_dotenv
load_dotenv()
model_name = os.environ.get("MODEL_NAME")

model = YOLO(f"{model_name}.pt") 

image_path = "test_images/thai_coins_images_test/46.jpg"

print(f"กำลังสแกนรูปภาพ: {image_path} ...")

results = model.predict(
    image_path, 
    verbose=False,
    # conf=0.5,          # ตัดกล่องที่ความมั่นใจต่ำกว่า 50% ทิ้งไปก่อนเลยตั้งแต่แรก
    iou=0.45,          # เกณฑ์การซ้อนทับ (ถ้ากล่องซ้อนทับกันเกิน 45% จะเข้าข่ายโดนยุบรวม)
    agnostic_nms=True  # บังคับยุบรวมกล่องที่ซ้อนกัน (ข้าม Class) โดยเลือกอันที่ % สูงสุด
)

boxes = results[0].boxes
class_names = results[0].names

print("\n--- ผลลัพธ์การสแกน ---")

# --- ✨ เพิ่ม Dictionary สำหรับเก็บข้อมูลตรงนี้ ✨ ---
all_coins_dict = {}       # เก็บเหรียญทั้งหมดที่เจอ
confident_coins_dict = {} # เก็บเฉพาะเหรียญที่มั่นใจ >= 80%
# ----------------------------------------------

if len(boxes) == 0:
    # กรณีที่สแกนแล้วรูปนั้นไม่มีอะไรคล้ายวัตถุเลย
    print("ไม่พบวัตถุใดๆ")
else:
    for c, conf in zip(boxes.cls, boxes.conf):
        confidence_percent = int(conf.item() * 100)
        class_name = class_names[int(c)]
        
        # 1. บันทึกเหรียญทุกอันที่เจอลง dict ตัวแรก
        # ใช้ .get() เพื่อเช็คว่าถ้ายังไม่มีคลาสนี้ใน dict ให้ค่าเริ่มต้นเป็น 0 แล้วบวก 1
        all_coins_dict[class_name] = all_coins_dict.get(class_name, 0) + 1
        
        # เงื่อนไข: ถ้ามั่นใจมากกว่า 80%
        if confidence_percent >= 80:
            print(f"✅ เจอ: {class_name} (มั่นใจ {confidence_percent}%)")
            
            # 2. บันทึกเฉพาะเหรียญที่มั่นใจ >= 80 ลง dict ตัวที่สอง
            confident_coins_dict[class_name] = confident_coins_dict.get(class_name, 0) + 1
            
        else:
            # ถ้าน้อยกว่า 80%
            print(f"❌ ไม่พบ (AI เห็นเป็น {class_name} แต่มั่นใจแค่ {confidence_percent}% เลยปัดตก)")

# --- ✨ ปริ้นแสดงผลสรุป Dictionary ✨ ---
print("\n--- 📊 สรุปข้อมูล Dictionary ---")
print(f"🪙 เหรียญทั้งหมดที่เจอ (ทุกระดับความมั่นใจ): {all_coins_dict}")
print(f"🎯 เหรียญที่ผ่านเกณฑ์ (มั่นใจ >= 80%): {confident_coins_dict}")
# -----------------------------------

# 4. ดึงรูปภาพที่ AI วาดกล่องและใส่ % Confidence เรียบร้อยแล้วออกมา
annotated_img = results[0].plot()

# --- เช็คและย่อขนาดรูป ---
h, w = annotated_img.shape[:2]
max_height = 800 

if h > max_height:
    scale = max_height / h
    new_w = int(w * scale)
    new_h = int(h * scale)
    annotated_img = cv2.resize(annotated_img, (new_w, new_h))
# ------------------------------------

# 5. เปิดหน้าต่างโชว์รูปภาพ
cv2.imshow("YOLO Test Result", annotated_img)

print("\n🖼️ วาดรูปเสร็จแล้ว! (กดปุ่มใดๆ บนคีย์บอร์ดเพื่อปิดหน้าต่าง)")

# สั่งให้โปรแกรมหยุดรอจนกว่าจะกดปุ่ม
cv2.waitKey(0)
cv2.destroyAllWindows()

