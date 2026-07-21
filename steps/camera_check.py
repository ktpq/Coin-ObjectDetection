import cv2
from ultralytics import YOLO

# 1. โหลดโมเดลของคุณ
model = YOLO("water_level.pt") 

# 2. เปิดกล้อง Webcam (เลข 0 หมายถึงกล้องตัวแรกของเครื่อง)
# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

print("🎥 กำลังเปิดกล้อง... (กดปุ่ม 'q' บนคีย์บอร์ดเพื่อปิด)")

# 3. สร้างลูปเพื่อดึงภาพจากกล้องมาสแกนแบบต่อเนื่อง
while cap.isOpened():
    # อ่านภาพจากกล้องทีละเฟรม (success จะเป็น True ถ้าอ่านภาพสำเร็จ)
    success, frame = cap.read()
    
    if success:
        # 4. ส่งภาพเฟรมนั้นให้ YOLO ทำนาย 
        # (ใส่ conf=0.8 เพื่อกรองขยะออก และ verbose=False เพื่อไม่ให้ Log รันเต็มหน้าจอ)
        results = model.predict(frame, conf=0.8, verbose=False)
        
        # 5. ให้ YOLO วาดกรอบสี่เหลี่ยมลงบนภาพ
        annotated_frame = results[0].plot()
        
        # 6. โชว์ภาพที่วาดกรอบแล้วขึ้นบนหน้าต่าง
        cv2.imshow("Real-Time Coin Detection", annotated_frame)
        
        # 7. เช็กการกดคีย์บอร์ด (รอ 1 มิลลิวินาที) ถ้ากด 'q' ให้เบรกลูป
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("🛑 ปิดกล้องเรียบร้อยแล้ว")
            break
    else:
        # ถ้าดึงภาพจากกล้องไม่ได้ ให้หยุดการทำงาน
        print("❌ ไม่สามารถดึงภาพจากกล้องได้")
        break

# 8. คืนทรัพยากรกล้องและปิดหน้าต่างทั้งหมด
cap.release()
cv2.destroyAllWindows()