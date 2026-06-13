import cv2
from ultralytics import YOLO


model = YOLO("my-model.pt") 

image_path = "test_images/thai_coins_images_test/multiple-coin3.jpg" 

print(f"กำลังสแกนรูปภาพ: {image_path} ...")

results = model.predict(image_path, verbose=False)


boxes = results[0].boxes
class_names = results[0].names

print("\n--- ผลลัพธ์การสแกน ---")

if len(boxes) == 0:
    # กรณีที่สแกนแล้วรูปนั้นไม่มีอะไรคล้ายวัตถุเลย
    print("ไม่พบวัตถุใดๆ")
else:
    for c, conf in zip(boxes.cls, boxes.conf):
        confidence_percent = int(conf.item() * 100)
        class_name = class_names[int(c)]
        
        # เงื่อนไข: ถ้ามั่นใจมากกว่า 80%
        if confidence_percent >= 80:
            print(f"✅ เจอ: {class_name} (มั่นใจ {confidence_percent}%)")
        else:
            # ถ้าน้อยกว่าหรือเท่ากับ 80%
            print(f"❌ ไม่พบ (AI เห็นเป็น {class_name} แต่มั่นใจแค่ {confidence_percent}% เลยปัดตก)")




# 4. ดึงรูปภาพที่ AI วาดกล่องและใส่ % Confidence เรียบร้อยแล้วออกมา
annotated_img = results[0].plot()

# --- ✨ เพิ่มโค้ดย่อขนาดรูปลงไปตรงนี้ ✨ ---
# เช็คขนาดดั้งเดิมของรูปก่อน
h, w = annotated_img.shape[:2]

# กำหนดความสูงสูงสุดที่จอคุณรับไหว (เช่น 800 หรือ 720 พิกเซล)
max_height = 800 

# ถ้ารูปสูงกว่าที่กำหนดไว้ ให้คำนวณอัตราส่วนเพื่อย่อขนาด
if h > max_height:
    scale = max_height / h
    new_w = int(w * scale)
    new_h = int(h * scale)
    annotated_img = cv2.resize(annotated_img, (new_w, new_h))
# ------------------------------------

# 5. เปิดหน้าต่างโชว์รูปภาพ (คราวนี้พอดีจอแน่นอน)
cv2.imshow("YOLO Test Result", annotated_img)

print("🖼️ วาดรูปเสร็จแล้ว! (กดปุ่มใดๆ บนคีย์บอร์ดเพื่อปิดหน้าต่าง)")

# สั่งให้โปรแกรมหยุดรอจนกว่าคุณจะกดปุ่มบนคีย์บอร์ด ถึงจะปิดหน้าต่างลง
cv2.waitKey(0)
cv2.destroyAllWindows()