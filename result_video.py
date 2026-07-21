import cv2
from ultralytics import YOLO

# 1. โหลดโมเดล
model = YOLO("water_level.pt") 

# 2. กำหนด Path ของวิดีโอ (ถ้าใส่เลข 0 จะเป็นการเปิดกล้อง Webcam)
video_path = "dataset/test/images/test-video.mp4" 
cap = cv2.VideoCapture(video_path)

print(f"🎬 กำลังเปิดวิดีโอ: {video_path} ...")
print("👉 กดปุ่ม 'q' เพื่อหยุดและปิดหน้าต่างวิดีโอ")

# ตรวจสอบว่าเปิดวิดีโอสำเร็จไหม
if not cap.isOpened():
    print("❌ ไม่สามารถเปิดไฟล์วิดีโอได้ กรุณาเช็ค Path อีกครั้ง")
    exit()

# 3. สร้างลูปเพื่ออ่านวิดีโอทีละเฟรม
while cap.isOpened():
    # ret จะเป็น True ถ้าอ่านภาพสำเร็จ, frame คือรูปภาพ 1 ช็อต
    ret, frame = cap.read()
    
    if not ret:
        print("✅ วิดีโอจบแล้ว หรือไม่สามารถอ่านเฟรมต่อไปได้")
        break

    # 4. สั่งให้ YOLO สแกน "รูปภาพทีละเฟรม"
    # ✨ แนะนำให้ใส่ stream=True เพื่อให้ระบบคืนค่ากลับมาเป็น Generator (ช่วยประหยัด RAM เครื่องได้มหาศาลตอนรันวิดีโอ)
    results = model.predict(
        source=frame, 
        stream=True,        
        verbose=False,
        iou=0.45,
        agnostic_nms=True
    )

    # วนลูปอ่านผลลัพธ์ (เนื่องจากใช้ stream=True เลยต้องวนลูปผลลัพธ์)
    for result in results:
        boxes = result.boxes
        class_names = result.names

        # รีเซ็ต Dictionary ใหม่ทุกๆ เฟรม เพื่อดูว่า "วินาทีนี้" เจออะไรบ้าง
        current_frame_dict = {} 
        
        if len(boxes) > 0:
            for c, conf in zip(boxes.cls, boxes.conf):
                confidence_percent = int(conf.item() * 100)
                class_name = class_names[int(c)]
                
                # เก็บเฉพาะวัตถุที่มั่นใจ >= 80% (ปรับลอจิกให้กระชับขึ้นสำหรับรันแบบเรียลไทม์)
                if confidence_percent >= 80:
                    current_frame_dict[class_name] = current_frame_dict.get(class_name, 0) + 1

        # 5. วาดกล่อง Bounding Box ลงบนเฟรมนั้นๆ
        annotated_frame = result.plot()

        # แปะ Text สรุปจำนวนที่เจอมุมซ้ายบนของวิดีโอ (ออปชันเสริม)
        y_offset = 40
        cv2.putText(annotated_frame, f"Detected (>=80%):", (20, y_offset), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        for name, count in current_frame_dict.items():
            y_offset += 35
            cv2.putText(annotated_frame, f"- {name}: {count}", (20, y_offset), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # --- เช็คและย่อขนาดวิดีโอก่อนแสดงผล (กันล้นจอ) ---
        h, w = annotated_frame.shape[:2]
        max_height = 800 
        if h > max_height:
            scale = max_height / h
            new_w = int(w * scale)
            new_h = int(h * scale)
            annotated_frame = cv2.resize(annotated_frame, (new_w, new_h))
        # ------------------------------------

        # 6. แสดงผลวิดีโอ
        cv2.imshow("YOLO Real-time Detection", annotated_frame)

    # 7. หน่วงเวลาและรอรับคำสั่งคีย์บอร์ด
    # cv2.waitKey(1) หมายถึง โชว์รูปค้างไว้ 1 มิลลิวินาที (ทำให้ภาพเล่นต่อเนื่องเป็นวิดีโอ)
    # ถ้ากดตัว 'q' ให้เบรกออกจากลูปทันที
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("🛑 ผู้ใช้กดหยุดวิดีโอ")
        break

# 8. คืนทรัพยากรให้ระบบ (เคลียร์ Memory)
cap.release()
cv2.destroyAllWindows()
print("👋 ปิดโปรแกรมเรียบร้อยครับ")