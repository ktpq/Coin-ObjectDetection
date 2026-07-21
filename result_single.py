import cv2
from ultralytics import YOLO

model = YOLO("my-model.pt") 

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

# import cv2
# import numpy as np
# from ultralytics import YOLO

# # 1. โหลดโมเดลเตรียมไว้ (จะใช้แค่ตอน Setup เท่านั้น)
# model = YOLO("my-model.pt")

# # --- Database เสมือน ---
# DB_FIXED_BOX = None
# DB_RATIO = 0
# DB_TOP_METERS = 0.0
# DB_OLD_BOTTOM_Y = 0 # เพิ่มตัวแปรเก็บเส้นระดับก้นคลองเดิมไว้โชว์เปรียบเทียบ
# # -------------------------

# def step1_setup_camera(image_path, top_val_str, bottom_val_str):
#     """ รูปที่ 1: รัน AI แค่ครั้งแรกเพื่อตีกรอบและจำค่า Ratio """
#     global DB_FIXED_BOX, DB_RATIO, DB_TOP_METERS, DB_OLD_BOTTOM_Y
#     print(f"\n[Step 1: Setup] กำลังใช้ AI สแกนภาพต้นฉบับ ({image_path})...")

#     results = model.predict(image_path, verbose=False, iou=0.45, agnostic_nms=True)
#     boxes = results[0].boxes

#     if len(boxes) == 0:
#         print("Setup ล้มเหลว: มองไม่เห็นเสาวัดน้ำ")
#         return False

#     # ดึงพิกัด
#     x_min, y_min, x_max, y_max = map(int, boxes.xyxy[0])
    
#     top_meters = float(top_val_str.replace("m", ""))
#     bottom_meters = float(bottom_val_str.replace("m", ""))

#     pixel_height = y_max - y_min
#     real_height = top_meters - bottom_meters

#     if pixel_height > 0:
#         DB_FIXED_BOX = (x_min, y_min, x_max, y_max)
#         DB_RATIO = real_height / pixel_height
#         DB_TOP_METERS = top_meters
#         DB_OLD_BOTTOM_Y = y_max

#         print(f"Setup สำเร็จ! บันทึก Ratio: 1 px = {DB_RATIO:.6f} เมตร")
#         return True
#     return False

# def step2_read_water_level(image_path):
#     """ รูปที่ 2: ใช้ OpenCV สแกนหาระดับน้ำที่สูงขึ้นในกรอบเดิม """
#     global DB_FIXED_BOX, DB_RATIO, DB_TOP_METERS, DB_OLD_BOTTOM_Y

#     if DB_FIXED_BOX is None:
#         print("เออร์เรอร์: ยังไม่ได้ทำ Step 1 (Setup)")
#         return

#     print(f"\n[Step 2: Real-time] กำลังประมวลผลรูปน้ำขึ้น ({image_path})...")
#     img = cv2.imread(image_path)
#     if img is None:
#         print("หารูปภาพไม่เจอครับ เช็คชื่อไฟล์อีกที")
#         return

#     x_min, y_min, x_max, y_max = DB_FIXED_BOX

#     # 1. ตัดภาพเฉพาะในกรอบ Fixed ROI (เสาวัดน้ำ)
#     cropped_pole = img[y_min:y_max, x_min:x_max]

#     # --- OpenCV Logic: สแกนหารอยต่อผิวน้ำ ---
#     # แปลงเป็นภาพขาวดำ และหาเส้นขอบ (Edge Detection)
#     gray = cv2.cvtColor(cropped_pole, cv2.COLOR_BGR2GRAY)
#     edges = cv2.Canny(gray, 50, 150)
    
#     # นับจำนวนพิกเซลที่เป็น "เส้นขอบ" ในแต่ละแนวนอน (Row)
#     row_sums = np.sum(edges, axis=1)

#     # สแกนจากล่าง (น้ำ) ขึ้นบน (ยอดเสา) หาแถวแรกที่มีเส้นตารางสเกล
#     waterline_local = cropped_pole.shape[0] - 1
#     for y in range(cropped_pole.shape[0] - 1, -1, -1):
#         if row_sums[y] > (255 * 5): # ถ้าเจอพิกเซลเส้นขอบติดกันเกิน 5 พิกเซล แปลว่าเจอเสาแล้ว
#             waterline_local = y
#             break
            
#     # แปลงพิกัด Y กลับไปเป็นพิกัดของรูปใหญ่
#     waterline_global = y_min + waterline_local
#     # ------------------------------------------

#     # 2. คำนวณระดับน้ำใหม่
#     pixels_from_top = waterline_global - y_min 
#     meters_from_top = pixels_from_top * DB_RATIO 
#     current_water_level = DB_TOP_METERS - meters_from_top 

#     # 3. วาดผลลัพธ์ลงบนภาพ
#     # กรอบ Fixed ROI (สีเขียว)
#     cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
    
#     # เส้น Baseline เดิม (สีแดงเข้ม เส้นประ/บาง) เพื่อให้เห็นว่าน้ำขึ้นมาจากไหน
#     cv2.line(img, (x_min, DB_OLD_BOTTOM_Y), (x_max, DB_OLD_BOTTOM_Y), (0, 0, 150), 2)
#     cv2.putText(img, "Old Baseline (1.10 m)", (x_max + 10, DB_OLD_BOTTOM_Y), 
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 150), 1)

#     # เส้นระดับน้ำปัจจุบัน (สีฟ้าสว่าง เส้นหนา)
#     cv2.line(img, (x_min, waterline_global), (x_max, waterline_global), (255, 255, 0), 3)
#     cv2.putText(img, f"New Level: {current_water_level:.2f} m", (x_max + 10, waterline_global), 
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

#     # ย่อรูปและแสดงผล
#     h, w = img.shape[:2]
#     if h > 800:
#         scale = 800 / h
#         img = cv2.resize(img, (int(w * scale), int(h * scale)))

#     cv2.imshow("Water Level Calculation", img)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

# # ==========================================
# # ลำดับการรันโปรแกรม (เทส 2 รูปต่อเนื่อง)
# # ==========================================
# image_ref = "dataset/test/images/test.jpg"   # รูปที่ 1: น้ำปกติ
# image_new = "dataset/test/images/test-2.jpg" # รูปที่ 2: น้ำขึ้นสูงแล้ว

# # 1. ส่งรูปน้ำปกติไปให้ AI จำพิกัดและสร้างสมการ
# is_setup_success = step1_setup_camera(image_ref, "2.00m", "1.12m")

# # 2. ส่งรูปน้ำสูงไปให้ OpenCV สแกนหาระดับน้ำปัจจุบัน
# if is_setup_success:
#     step2_read_water_level(image_new)