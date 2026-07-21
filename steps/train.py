import subprocess

import sys

def run_cmd(command):
    print(f"\n🚀 กำลังรันคำสั่ง: {command}")
    # สั่งให้รันคำสั่ง และดึงข้อความจาก Terminal มาโชว์แบบ Real-time
    result = subprocess.run(command, shell=True, text=True)
    if result.returncode != 0:
        print(f"❌ เกิดข้อผิดพลาดตอนรัน: {command}")
        sys.exit(1) # หยุดการทำงานทั้งหมดถ้ามีบรรทัดไหนพัง


# รายการคำสั่งเรียงตามลำดับ (ลบของเก่าทิ้งหมดแล้ว)
# window_commands = [
#     # ?. สร้างโฟลเดอร์ (ถ้ามีอยู่แล้วก็ไม่เด้ง Error)
#     # "if not exist custom_data mkdir custom_data",

#     # ?. แตกไฟล์ zip ไปไว้ในโฟลเดอร์ custom_data
#     # "tar -xf data.zip -C custom_data",

#     # 1. สั่งรันไฟล์สคริปต์เพื่อแบ่งกองรูปภาพ (Train 90% / Val 10%)
#     # (ใช้ single quote ครอบสตริง เพื่อให้ใส่ double quote ข้างในได้)
#     # 'python train_val_split.py --datapath="custom_data" --train_pct=0.9',

#     # 2. สั่งรันไฟล์ตั้งค่า (ถ้ามีในโปรเจกต์)
#     # "python config_training.py",

#     # 3. เริ่มกระบวนการเทรน YOLO
#     "yolo detect train data=data.yaml model=yolo11s.pt epochs=60 imgsz=480 batch=8 workers=0 device=0",

#     # 4. ก๊อป model ออกมาที่ root dir
#     "copy runs\\detect\\train\\weights\\best.pt my-model.pt"
# ]

# รายการคำสั่งเรียงตามลำดับ
window_commands = [
    # ... (ส่วนของ Phase 1-3 ที่คุณคอมเมนต์ไว้) ...

    # 3. เริ่มกระบวนการเทรน YOLO (อัปเกรดความฉลาด + รีดพลัง GTX 1650)
    (
        "yolo detect train data=data.yaml model=yolo11s.pt "
        "epochs=300 patience=50 imgsz=480 batch=8 workers=0 device=0 "
    ),

    # 4. ก๊อป model ออกมาที่ root dir ให้พร้อมใช้งาน
    "copy runs\\detect\\train\\weights\\best.pt my-model.pt"
]

for cmd in window_commands:
    run_cmd(cmd)

print("\n✅ รันสคริปต์เสร็จสมบูรณ์ ทุกขั้นตอนผ่านฉลุย!")
