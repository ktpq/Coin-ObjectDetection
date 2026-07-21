import subprocess
import sys
import time  # ✨ เพิ่มไลบรารีสำหรับจับเวลา

def run_cmd(command):
    print(f"\n🚀 กำลังรันคำสั่ง: {command}")
    # สั่งให้รันคำสั่ง และดึงข้อความจาก Terminal มาโชว์แบบ Real-time
    result = subprocess.run(command, shell=True, text=True)
    if result.returncode != 0:
        print(f"❌ เกิดข้อผิดพลาดตอนรัน: {command}")
        sys.exit(1) # หยุดการทำงานทั้งหมดถ้ามีบรรทัดไหนพัง

# รายการคำสั่งเรียงตามลำดับ (ลบของเก่าทิ้งหมดแล้ว)
window_commands = [
    'python steps\\clear_model.py',

    # # phase1
    'python steps\\flat_images.py',

    # # phase2
    'python steps\\find_coin.py',
    'python steps\\build_custom_data.py',

    # -------------------

    # phase3
    'python steps\\train_val_split.py --datapath="custom_data" --train_pct=0.9',
    "python steps\\config_training.py",

    # phase4
    'python steps\\train.py',

    'python steps\\clear_unused_file.py',
]

# ⏱️ เริ่มจับเวลาตรงนี้!
start_time = time.time()

for cmd in window_commands:
    run_cmd(cmd)

# ⏱️ สิ้นสุดการรัน หยุดจับเวลา
end_time = time.time()

# คำนวณระยะเวลา
total_seconds = int(end_time - start_time)
hours, remainder = divmod(total_seconds, 3600)
minutes, seconds = divmod(remainder, 60)

print("\n✅ รันสคริปต์เสร็จสมบูรณ์ ทุกขั้นตอนผ่านฉลุย!")

# โชว์เวลาที่ใช้ไปแบบสวยๆ
if hours > 0:
    print(f"⏱️ ใช้เวลาไปทั้งหมด: {hours} ชั่วโมง {minutes} นาที {seconds} วินาที")
elif minutes > 0:
    print(f"⏱️ ใช้เวลาไปทั้งหมด: {minutes} นาที {seconds} วินาที")
else:
    print(f"⏱️ ใช้เวลาไปทั้งหมด: {seconds} วินาที")