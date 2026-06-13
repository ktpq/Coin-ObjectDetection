import cv2
import os

# กำหนด Path ไปที่โฟลเดอร์ที่เราเพิ่ง Auto-label เสร็จ
img_dir = "./custom_data/images"
lbl_dir = "./custom_data/labels"

print("🔍 กำลังเปิดโปรแกรมตรวจสอบ Label...")
print("👉 กดปุ่ม 'Spacebar' หรือปุ่มใดๆ เพื่อดูรูปถัดไป")
print("👉 กดปุ่ม 'q' เพื่อออกจากโปรแกรม")

# กำหนดขนาดช่องว่างรอบรูป (พิกเซล)
PADDING = 40 
# กำหนดความสูงสูงสุดของหน้าต่างที่แสดงผล
MAX_HEIGHT = 800 

# วนลูปอ่านรูปภาพทุกรูป
for filename in os.listdir(img_dir):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        img_path = os.path.join(img_dir, filename)
        
        # หาชื่อไฟล์ .txt ที่คู่กัน
        base_name = os.path.splitext(filename)[0]
        lbl_path = os.path.join(lbl_dir, f"{base_name}.txt")

        # อ่านรูปภาพและหาขนาด กว้าง x สูง ดั้งเดิม
        img = cv2.imread(img_path)
        if img is None:
            continue
            
        img_height, img_width, _ = img.shape

        # ✨ เสริมขอบดำรอบรูปภาพ (บน, ล่าง, ซ้าย, ขวา)
        img_padded = cv2.copyMakeBorder(
            img, PADDING, PADDING, PADDING, PADDING, 
            cv2.BORDER_CONSTANT, value=[0, 0, 0]
        )

        # ตรวจสอบว่ามีไฟล์ Label คู่กันไหม
        if os.path.exists(lbl_path):
            with open(lbl_path, 'r') as f:
                lines = f.readlines()
                
                # วนลูปวาดกรอบตามจำนวนบรรทัด (จำนวนเหรียญ) ในไฟล์ .txt
                for line in lines:
                    data = line.strip().split()
                    if len(data) == 5:
                        class_id = int(data[0])
                        x_center = float(data[1])
                        y_center = float(data[2])
                        box_width = float(data[3])
                        box_height = float(data[4])

                        # แปลงสัดส่วน 0.0-1.0 กลับมาเป็นพิกัด Pixel (บวก PADDING)
                        cx = int(x_center * img_width) + PADDING
                        cy = int(y_center * img_height) + PADDING
                        w = int(box_width * img_width)
                        h = int(box_height * img_height)

                        # หาจุดมุมซ้ายบนและขวาล่างเพื่อวาดสี่เหลี่ยม
                        x_min = int(cx - (w / 2))
                        y_min = int(cy - (h / 2))
                        x_max = int(cx + (w / 2))
                        y_max = int(cy + (h / 2))

                        # วาดกรอบสีเขียวหนา 4 px (เพิ่มความหนาเผื่อตอนโดนย่อรูป)
                        cv2.rectangle(img_padded, (x_min, y_min), (x_max, y_max), (0, 255, 0), 4)
                        
                        # แปะ Text รหัส Class ไว้บนกล่อง (ขยายฟอนต์ให้ใหญ่ขึ้นเผื่อโดนย่อ)
                        cv2.putText(img_padded, f"Class {class_id}", (x_min, y_min - 15), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)

        # --- ✨ โค้ดย่อขนาดรูปก่อนแสดงผล ✨ ---
        h, w = img_padded.shape[:2]
        if h > MAX_HEIGHT:
            scale = MAX_HEIGHT / h
            new_w = int(w * scale)
            new_h = int(h * scale)
            img_padded = cv2.resize(img_padded, (new_w, new_h))
        # ------------------------------------

        # โชว์รูปภาพที่เติมขอบและย่อขนาดแล้ว
        cv2.imshow("Check Auto-Label", img_padded)
        
        # รอรับคำสั่งคีย์บอร์ด
        key = cv2.waitKey(0) & 0xFF
        if key == ord('q'):  # ถ้ากด 'q' ให้เบรกออกจากลูป
            print("🛑 ปิดโปรแกรมตรวจสอบ")
            break

cv2.destroyAllWindows()