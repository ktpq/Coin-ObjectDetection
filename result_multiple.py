from ultralytics import YOLO
import os
from dotenv import load_dotenv
load_dotenv()
model_name = os.environ.get("MODEL_NAME")

# 1. โหลดโมเดลของคุณ
model = YOLO(f"{model_name}.pt") 

# 2. กำหนด Path ของ "โฟลเดอร์" ที่เก็บรูปภาพทั้งหมด

# folder_path = "test_images/thai_coins_images_test/1_1-9Kingbaht/" 
# folder_path = "test_images/thai_coins_images_test/3_2baht/" 
# folder_path = "test_images/thai_coins_images_test/3_5baht/" 
# folder_path = "test_images/thai_coins_images_test/4_10baht/" 
folder_path = "test_images/thai_coins_images_test/4_10baht/" 

print(f"🚀 กำลังเริ่มสแกนรูปภาพในโฟลเดอร์: {folder_path} ...\n")
print("-" * 40)

# กำหนดนามสกุลไฟล์ที่ต้องการให้อ่าน
valid_extensions = ('.jpg', '.jpeg', '.png')

# ตัวแปรสำหรับคำนวณค่าเฉลี่ย
total_confidence = 0.0
total_objects_detected = 0

# 3. วนลูปอ่านทุกไฟล์ในโฟลเดอร์
for filename in os.listdir(folder_path):
    if filename.lower().endswith(valid_extensions):
        image_path = os.path.join(folder_path, filename)
        
        # 4. สั่งทำนายผล (ใส่ verbose=False เพื่อไม่ให้ YOLO ปริ้น Log รกหน้าจอ)
        results = model.predict(image_path, verbose=False)
        
        # 5. ดึงข้อมูลกล่อง, เปอร์เซ็นต์ความมั่นใจ และชื่อคลาส
        boxes = results[0].boxes
        class_names_dict = results[0].names 
        
        detected_items = []
        
        # เช็คว่าเจอกล่องวัตถุในรูปไหม
        if len(boxes) > 0:
            # วนลูปดึงข้อมูลทีละวัตถุที่ตรวจเจอ
            for c, conf in zip(boxes.cls, boxes.conf):
                class_id = int(c)
                class_name = class_names_dict[class_id]
                
                # ดึงค่าความมั่นใจ (เช่น 0.9521)
                conf_value = conf.item()
                
                # บวกสะสมค่าเพื่อเอาไปหาค่าเฉลี่ยตอนจบ
                total_confidence += conf_value
                total_objects_detected += 1
                
                # แปลงค่า conf ให้เป็นเปอร์เซ็นต์เพื่อโชว์ทีละรูป (เช่น 95%)
                confidence_percent = int(conf_value * 100)
                
                # จัดรูปแบบข้อความ "ชื่อคลาส (XX%)"
                detected_items.append(f"{class_name} ({confidence_percent}%)")
                
            # ปริ้นชื่อไฟล์ และสิ่งที่เจอทั้งหมด
            print(f"📄 {filename} -> เจอ: {', '.join(detected_items)}")
        else:
            # กรณีสแกนแล้วไม่เจออะไรเลย
            print(f"📄 {filename} -> ❌ ไม่พบวัตถุ")

print("-" * 40)

# 6. สรุปผลความมั่นใจเฉลี่ยรวมด้านล่างสุด
if total_objects_detected > 0:
    # คำนวณเปอร์เซ็นต์เฉลี่ย
    average_confidence = (total_confidence / total_objects_detected) * 100
    print(f"📊 สรุปผล: ตรวจพบวัตถุทั้งหมด {total_objects_detected} ชิ้น")
    print(f"🎯 ความมั่นใจเฉลี่ยรวม (Average Confidence): {average_confidence:.2f}%")
else:
    print("📊 สรุปผล: ไม่พบวัตถุใดๆ ให้คำนวณเลย")

print("✅ สแกนเสร็จสิ้นทุกรูปแล้ว!")