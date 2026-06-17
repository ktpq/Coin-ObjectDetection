import supervision as sv
from tqdm import tqdm  # เปลี่ยนมาใช้ tqdm แบบปกติสำหรับ Terminal
import os

# 1. ชี้เป้าไปที่ไฟล์วีดีโอของคุณโดยตรงเลย
VIDEO_PATH = "./videos/10bahtTail.mov"  # 👈 เปลี่ยนชื่อไฟล์ให้ตรงกับของคุณ
IMAGE_DIR_PATH = "./images/6_10bahtTail"
FRAME_STRIDE = 10

# สร้างโฟลเดอร์เก็บรูป (ถ้ายังไม่มีจะได้ไม่ Error)
os.makedirs(IMAGE_DIR_PATH, exist_ok=True)

print(f"🎬 กำลังเตรียมสับวีดีโอ: {VIDEO_PATH}")

# ดึงชื่อไฟล์วีดีโอมาตั้งเป็นชื่อรูป (เช่น my_coin_video-00001.png)
video_name = os.path.splitext(os.path.basename(VIDEO_PATH))[0]
image_name_pattern = video_name + "-{:05d}.png"

# ใช้ supervision นับจำนวนเฟรมทั้งหมดก่อน จะได้แสดงหลอดโหลด % ได้ถูกต้อง
video_info = sv.VideoInfo.from_video_path(video_path=VIDEO_PATH)
total_frames = video_info.total_frames // FRAME_STRIDE

print(f"📸 คาดว่าจะได้รูปภาพทั้งหมดประมาณ {total_frames} รูป...")

# 2. เริ่มกระบวนการดึงและเซฟรูปภาพ
with sv.ImageSink(target_dir_path=IMAGE_DIR_PATH, image_name_pattern=image_name_pattern) as sink:
    # สร้างตัวผลิตเฟรมภาพ
    frame_generator = sv.get_video_frames_generator(source_path=VIDEO_PATH, stride=FRAME_STRIDE)
    
    # ใช้ tqdm ครอบไว้เพื่อดูหลอดโหลดแบบ Real-time
    for image in tqdm(frame_generator, total=total_frames, desc="กำลังสกัดภาพ"):
        sink.save_image(image=image)

print(f"\n✅ เสร็จสมบูรณ์! เข้าไปดูรูปภาพได้ที่โฟลเดอร์: {IMAGE_DIR_PATH}")