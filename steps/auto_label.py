import os
import shutil
import random
import string
import json

def generate_full_dataset(source_dir="test_images/thai_coins_images", output_dir="custom_data"):
    print("🚀 เริ่มกระบวนการสร้าง Dataset...")

    # 1. เตรียมโฟลเดอร์ปลายทาง
    img_dir = os.path.join(output_dir, "images")
    lbl_dir = os.path.join(output_dir, "labels")
    
    # ล้างโฟลเดอร์เก่า (ถ้ามี) และสร้างใหม่ เพื่อป้องกันไฟล์เก่าตกค้าง
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(img_dir, exist_ok=True)
    os.makedirs(lbl_dir, exist_ok=True)

    # ตัวแปรสำหรับเก็บข้อมูลไปทำไฟล์ txt และ json
    class_names = []
    categories = []
    
    # ดึงรายชื่อโฟลเดอร์ย่อย และเรียงลำดับตามตัวอักษร/ตัวเลข (เช่น 1_Bishop, 2_King...)
    if not os.path.exists(source_dir):
        print(f"❌ ไม่พบโฟลเดอร์ต้นทาง: {source_dir}")
        return

    subfolders = sorted([f for f in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, f))])
    
    valid_extensions = ('.jpg', '.jpeg', '.png')

    # 2. วนลูปตามโฟลเดอร์ย่อย (Class)
    for class_id, folder_name in enumerate(subfolders):
        # ดึงชื่อคลาสจากหลังเครื่องหมาย _ (เช่น "1_Bishop" -> "Bishop")
        class_name = folder_name.split('_')[1] if '_' in folder_name else folder_name
        class_names.append(class_name)
        
        # เก็บข้อมูลสำหรับ notes.json
        categories.append({
            "id": class_id,
            "name": class_name
        })
        
        folder_path = os.path.join(source_dir, folder_name)
        
        # 3. วนลูปอ่านไฟล์รูปภาพในแต่ละโฟลเดอร์
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(valid_extensions):
                # สุ่มตัวอักษร+ตัวเลข 10 ตัว
                random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
                
                # สร้างชื่อไฟล์ใหม่: [random10]-ชื่อไฟล์เดิม
                new_filename = f"{random_str}-{filename}"
                
                # แยกชื่อไฟล์กับนามสกุล เพื่อเอาไปสร้างไฟล์ .txt
                base_name, _ = os.path.splitext(new_filename)
                
                new_img_path = os.path.join(img_dir, new_filename)
                new_lbl_path = os.path.join(lbl_dir, f"{base_name}.txt")
                
                # คัดลอกรูปภาพ
                shutil.copy(os.path.join(folder_path, filename), new_img_path)
                
                # สร้างไฟล์ Label (คลุมทั้งภาพ: x_center y_center width height)
                with open(new_lbl_path, 'w', encoding='utf-8') as f:
                    f.write(f"{class_id} 0.5 0.5 1.0 1.0\n")
                    
        print(f"✅ จัดการคลาส: {class_name} (ID: {class_id}) เสร็จเรียบร้อย")

    # 4. สร้างไฟล์ classes.txt
    classes_file = os.path.join(output_dir, "classes.txt")
    with open(classes_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(class_names))
    print("✅ สร้างไฟล์ classes.txt สำเร็จ")

    # 5. สร้างไฟล์ notes.json
    notes_file = os.path.join(output_dir, "notes.json")
    notes_data = {
        "categories": categories,
        "info": {
            "year": 2026,
            "version": "1.0",
            "contributor": "Label Studio"
        }
    }
    with open(notes_file, 'w', encoding='utf-8') as f:
        json.dump(notes_data, f, indent=2, ensure_ascii=False)
    print("✅ สร้างไฟล์ notes.json สำเร็จ")

    print(f"\n🎉 เสร็จสิ้น! ข้อมูลทั้งหมดถูกเตรียมไว้ที่โฟลเดอร์ '{output_dir}' พร้อมเทรนแล้วครับ")

# สั่งให้สคริปต์เริ่มทำงาน
if __name__ == "__main__":
    generate_full_dataset()

# import os
# import shutil
# import random
# import string
# import json
# import cv2
# import numpy as np

# def generate_full_dataset(source_dir="test_images/thai_coins_images", output_dir="custom_data"):
#     print("🚀 เริ่มกระบวนการสร้าง Dataset ด้วย OpenCV (ฉบับอัปเกรดความแม่นยำ)...")

#     img_dir = os.path.join(output_dir, "images")
#     lbl_dir = os.path.join(output_dir, "labels")
    
#     if os.path.exists(output_dir):
#         shutil.rmtree(output_dir)
#     os.makedirs(img_dir, exist_ok=True)
#     os.makedirs(lbl_dir, exist_ok=True)

#     class_names = []
#     categories = []
    
#     if not os.path.exists(source_dir):
#         print(f"❌ ไม่พบโฟลเดอร์ต้นทาง: {source_dir}")
#         return

#     subfolders = sorted([f for f in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, f))])
#     valid_extensions = ('.jpg', '.jpeg', '.png')

#     for class_id, folder_name in enumerate(subfolders):
#         class_name = folder_name.split('_')[1] if '_' in folder_name else folder_name
#         class_names.append(class_name)
#         categories.append({"id": class_id, "name": class_name})
        
#         folder_path = os.path.join(source_dir, folder_name)
        
#         for filename in os.listdir(folder_path):
#             if filename.lower().endswith(valid_extensions):
#                 original_img_path = os.path.join(folder_path, filename)
                
#                 random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
#                 new_filename = f"{random_str}-{filename}"
#                 base_name, _ = os.path.splitext(new_filename)
                
#                 new_img_path = os.path.join(img_dir, new_filename)
#                 new_lbl_path = os.path.join(lbl_dir, f"{base_name}.txt")
                
#                 shutil.copy(original_img_path, new_img_path)
                
#                 # ====================================================
#                 # 🌟 ส่วนที่อัปเกรด: คัดกรองเหรียญให้แม่นยำขึ้น
#                 # ====================================================
#                 img = cv2.imread(original_img_path)
#                 img_height, img_width, _ = img.shape
                
#                 gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#                 # ใช้ GaussianBlur ช่วยลด Noise รอยขีดข่วนบนพื้นผิวได้ดีกว่า
#                 blurred = cv2.GaussianBlur(gray, (11, 11), 0)
                
#                 # ตั้งค่าระยะห่างขั้นต่ำแบบยืดหยุ่น (10% ของความกว้างภาพ)
#                 dynamic_min_dist = max(img_width // 10, 50)

#                 circles = cv2.HoughCircles(
#                     blurred, 
#                     cv2.HOUGH_GRADIENT, 
#                     dp=1.2, 
#                     minDist=dynamic_min_dist, # บังคับไม่ให้วงกลมอยู่ติดกันเกินไป
#                     param1=50,        
#                     param2=60,        # 👈 โหดขึ้น! (เดิม 30) ต้องเป็นวงกลมชัดๆ ถึงจะยอมรับ
#                     minRadius=20,     
#                     maxRadius=img_width // 2 
#                 )
                
#                 final_circles = []
                
#                 if circles is not None:
#                     circles = np.round(circles[0, :]).astype("int")
                    
#                     # 🌟 ระบบกรองวงกลมที่ซ้อนทับกัน (Overlap Filter)
#                     for (x, y, r) in circles:
#                         overlap = False
#                         for (fx, fy, fr) in final_circles:
#                             # คำนวณระยะห่างระหว่างจุดศูนย์กลางของวงกลม 2 วง
#                             dist = np.sqrt((x - fx)**2 + (y - fy)**2)
#                             # ถ้าระยะห่างน้อยกว่ารัศมี แปลว่ามันคือเหรียญเดียวกันที่จับซ้อนกัน
#                             if dist < max(r, fr):
#                                 overlap = True
#                                 break
                        
#                         # ถ้าไม่ซ้อนทับกับใครเลย ค่อยเก็บเข้าลิสต์ของจริง
#                         if not overlap:
#                             final_circles.append((x, y, r))

#                 # เขียนพิกัดลงไฟล์ Label
#                 with open(new_lbl_path, 'w', encoding='utf-8') as f:
#                     for (cx, cy, r) in final_circles:
#                         r = int(r * 1.05) # เผื่อขอบแค่ 5% พอ (เดิม 10% อาจจะกว้างไป)
                        
#                         x_center = cx / img_width
#                         y_center = cy / img_height
#                         box_width = (2 * r) / img_width
#                         box_height = (2 * r) / img_height
                        
#                         x_center = max(0.0, min(1.0, x_center))
#                         y_center = max(0.0, min(1.0, y_center))
#                         box_width = max(0.0, min(1.0, box_width))
#                         box_height = max(0.0, min(1.0, box_height))
                        
#                         f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {box_width:.6f} {box_height:.6f}\n")

#         print(f"✅ จัดการคลาส: {class_name} (ID: {class_id}) เสร็จเรียบร้อย")

#     classes_file = os.path.join(output_dir, "classes.txt")
#     with open(classes_file, 'w', encoding='utf-8') as f:
#         f.write('\n'.join(class_names))

#     notes_file = os.path.join(output_dir, "notes.json")
#     notes_data = {"categories": categories, "info": {"year": 2026, "version": "2.0"}}
#     with open(notes_file, 'w', encoding='utf-8') as f:
#         json.dump(notes_data, f, indent=2, ensure_ascii=False)

#     print(f"\n🎉 เสร็จสิ้น! ข้อมูลถูกเตรียมพร้อมแล้วครับ")

# if __name__ == "__main__":
#     generate_full_dataset()