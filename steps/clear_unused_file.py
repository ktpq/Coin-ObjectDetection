import os
import shutil

def cleanup_workspace():
    print("🧹 เริ่มกระบวนการทำความสะอาด Workspace...\n")

    # กำหนดเป้าหมายที่ต้องการลบ
    folders_to_delete = ['data', 'runs', 'cropped_coins', 'dataset', 'test_images_flat']
    
    # หมายเหตุ: ใส่ทั้ง data.yml และ data.yaml เผื่อไว้ในกรณีที่พิมพ์นามสกุลต่างกัน
    files_to_delete = ['data.yml', 'data.yaml', 'yolo11s.pt']

    # 1. จัดการลบโฟลเดอร์ (ใช้ shutil.rmtree เพื่อลบโฟลเดอร์ที่มีของข้างใน)
    for folder in folders_to_delete:
        if os.path.exists(folder):
            try:
                shutil.rmtree(folder)
                print(f"🗑️ ลบโฟลเดอร์: {folder}")
            except Exception as e:
                print(f"❌ ลบโฟลเดอร์ '{folder}' ไม่สำเร็จ: {e}")
        else:
            print(f"⏩ ข้าม: ไม่พบโฟลเดอร์ '{folder}'")

    # 2. จัดการลบไฟล์ (ใช้ os.remove สำหรับไฟล์เดี่ยว)
    for file in files_to_delete:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"🗑️ ลบไฟล์: {file}")
            except Exception as e:
                print(f"❌ ลบไฟล์ '{file}' ไม่สำเร็จ: {e}")
        else:
            print(f"⏩ ข้าม: ไม่พบไฟล์ '{file}'")

    print("\n✨ ทำความสะอาดเสร็จสิ้น! พื้นที่โปรเจกต์ของคุณกลับมาโล่งเหมือนใหม่แล้วครับ")

# สั่งให้ฟังก์ชันเริ่มทำงาน
if __name__ == '__main__':
    cleanup_workspace()