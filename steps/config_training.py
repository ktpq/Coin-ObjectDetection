import yaml
import os

def create_data_yaml(path_to_classes_txt, path_to_data_yaml):

    # 1. อ่านไฟล์ classes.txt เพื่อเอาชื่อคลาส
    if not os.path.exists(path_to_classes_txt):
        print(f'classes.txt file not found! Please create a classes.txt labelmap and move it to {path_to_classes_txt}')
        return
        
    with open(path_to_classes_txt, 'r') as f:
        classes = []
        for line in f.readlines():
            if len(line.strip()) == 0: continue
            classes.append(line.strip())
    number_of_classes = len(classes)

    # 2. สร้างโครงสร้างข้อมูล (Data dictionary)
    # ใช้ os.path.abspath เพื่อแปลงเป็น Path เต็มของโฟลเดอร์ ป้องกันปัญหา YOLO หาไฟล์บน Windows ไม่เจอ
    dataset_path = os.path.abspath('data')

    data = {
        'path': dataset_path,
        'train': 'train/images',
        'val': 'validation/images',
        'nc': number_of_classes,
        'names': classes
    }

    # 3. เขียนข้อมูลลงไฟล์ YAML
    with open(path_to_data_yaml, 'w') as f:
        yaml.dump(data, f, sort_keys=False)
    print(f'Created config file at {path_to_data_yaml}')

    return

# กำหนดเส้นทางไฟล์สำหรับบนเครื่อง Windows (อ้างอิงจากโฟลเดอร์ปัจจุบัน)
path_to_classes_txt = 'custom_data/classes.txt'
path_to_data_yaml = 'data.yaml'

# สั่งรันฟังก์ชัน
create_data_yaml(path_to_classes_txt, path_to_data_yaml)

# แสดงผลลัพธ์ในไฟล์ (แทนการใช้คำสั่ง !cat)
print('\nFile contents:\n')
if os.path.exists(path_to_data_yaml):
    with open(path_to_data_yaml, 'r') as f:
        print(f.read())