<img width="924" height="698" alt="image" src="https://github.com/user-attachments/assets/8390bd10-ae9a-4540-8199-810933d73bad" /># Coin Object Detection

## รายละเอียดโปรเจกต์

วัตถุประสงค์หลักของโปรเจกต์นี้คือ:
- ต้องการนำไปใช้แยกเหรียญประเภทต่างๆ
- ต้องการให้การ train model เพื่อเเยกประเภทเหรียญ เป็นแบบ อัตโนมัติมากที่สุด
- เพื่อให้การ label รูปภาพก่อนการเทรนเป็นแบบอัตโนมัติ
---

## การติดตั้ง (Installation)

เปิด Command Line หรือ Terminal แล้ว clone โปรเจกต์ (Private Repository):

```bash
git clone https://github.com/ktpq/Coin-ObjectDetection.git
```

จากนั้นเข้าไปยังโฟลเดอร์ของโปรเจกต์ เเละ สร้าง Python virtual environment 
```bash
python -m venv .venv
```

ทำการ activate Python virtual environment
```bash
.venv\Scripts\activate.bat
```

ลง package ที่จำเป็นใน virtual environment ด้วยคำสั่งต่อไปนี้ (อาจใช้เวลานานถึง 30-40 นาที)
```bash
pip install --no-deps -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cu124
```

---

## วิธีการใช้งาน
หลังจากลง package เสร็จเรียบร้อย สามารถลองใช้งานได้ทันที โดยใช้คำสั่งด้านล่าง 
```bash
python result_single.py 
```
โดยไฟล์ result_single.py จะเป็นสคริปต์ไว้สำหรับเช็คผลลัพธ์การ classification ของ model โดยค่าเริ่มต้นจะเรียกใช้ตัว default model ที่เราเทรนไว้ให้เเล้ว (example-my-model.pt) 
แบ่งเป็นเหรียญ ดังนี้ **สามารถเปลี่ยน path ของรูปภาพเพื่อทดสอบการทำงานของ model ได้จากในโค้ดเลย !!!**
  - 1 baht
  - 5 baht
  - 10 baht

## เทรน Model ด้วยตัวเอง

1️⃣ เตรียมรูปภาพที่ต้องการจะนำมาเทรนใส่ใน folder "images" โดยมี format ของ folder ดังภาพ [classId]_[className]

<img width="387" height="92" alt="image" src="https://github.com/user-attachments/assets/5dcd5a7b-db07-4bda-b1c5-6efe4e27dfe1" />

2️⃣ รันคำสั่ง ด้านล่างเพื่อเทรน model (อาจใช้เวลานานถึง 1 ชั่วโมง ขึ้นอยู่กับจำนวนภาพ เเละ setting ที่เราตั้งไว้)

```bash
python run.py
```

3️⃣ ผลลัพธ์จะออกมาเป็น file model ชื่อ "my-model.pt" หลังจากนั้นสามารถไปเปลี่ยน MODEL_NAME ใน .env เป็น my-model เพื่อเรียกใช้งาน model ใน **result_single.py** ตามเดิมได้เลย

<img width="379" height="26" alt="image" src="https://github.com/user-attachments/assets/ed6c2421-d033-4921-aa85-48b9bcdf0417" />


---

## หลังจากกด train model เกิดอะไรขึ้นบ้าง ???

หลังจาก run **python run.py** ในไฟล์จะมีการเรียก ใช้ python script หลายๆตัว โดยจะอธิบายแบ่งเป็น 4 phases ดังภาพ

<img width="860" height="394" alt="image" src="https://github.com/user-attachments/assets/ee237a56-77a7-47d9-b158-390bb1e04649" />




### 1️⃣ **Phase 1** เตรียมข้อมูลก่อน Label

หลังจากเตรียมรูปใส่ในโฟลเดอร์ images เเล้วจัดตาม format ที่เคยบอกไว้ในขั้นตอนก่อนหน้าเรียบร้อยเเล้ว ในขั้นตอนนี้ Python Script จะเอาภาพในเเต่ละโฟลเดอร์มารวมไว้ที่เดียวพร้อม stamp ชื่อ class ไว้ที่ชื่อไฟล์ เพื่อเอาไปเข้ากระบวนการใน **Phase 2** ต่อไป

<img width="1515" height="561" alt="image" src="https://github.com/user-attachments/assets/ae5b5ffd-73e9-417a-9e9b-b3cc94fa633d" />


### 2️⃣ **Phase 2** Label รูปภาพ อัตโนมัติ
**Q:** เราจะ label รูปภาพอัตโนมัติยังไง ?

**Ans:** Grounding Dino + Python Script

**Grounding Dino** คือโมเดลปัญญาประดิษฐ์ประเภท **Computer Vision** ที่มีความสามารถในการตรวจจับวัตถุในภาพ 

<img width="674" height="449" alt="image" src="https://github.com/user-attachments/assets/fe7bed11-ae77-4f79-9ee6-7ed5ef0154e9" />

ถึง GD จะมีความสามารถในการตรวจจับและแยกประเภทวัตถุในภาพได้เก่งก็จริง **แต่**ไม่เก่งจนสามารถแยกประเภทของเหรียญแต่ละชนิดได้อย่างแม่นยำ

ในเคสนี้เราเลยใช้ GD ในการตรวจจับในภาพของเราว่ามีเหรียญอยู่ในภาพตรงไหนบ้าง แล้วให้ทำการ label ว่าเป็น coin เอาไว้เฉยๆ จากนั้นใช้ Python Script เพื่อเอา class ที่เรา stamp ไว้ที่ชื่อไฟล์มาทับ Label เดิม 

**หมายความว่า** **ถ้า**รูปที่เรานำมาเทรนเห็นเป็นเหรียญชัดเจน เเล้ว ใส่โฟลเดอร์เตรียมไว้อย่างถูกต้อง จะไม่มีทาง Label ผิดพลาดเลย

**ตัวอย่างรูปที่ Label เเล้วจากการใช้ Grounding Dino**

<img width="598" height="784" alt="image" src="https://github.com/user-attachments/assets/7695c26e-734f-4929-9f3e-d55f38d37dce" />
<img width="959" height="712" alt="image" src="https://github.com/user-attachments/assets/1499be40-d420-4ba3-9775-f93248bb3658" />
<img width="924" height="698" alt="image" src="https://github.com/user-attachments/assets/71912572-ae45-43e6-8a72-8f353e2ec678" />




### 3️⃣ **Phase 3** เตรียมข้อมูลก่อนเริ่มเทรน

ในขั้นตอนนี้จะ ทำการ format ข้อมูลที่ได้จาก phase ก่อนหน้า โดยจะแบ่งข้อมูลเป็น 2 set (train/validation) ตาม format ที่ตัว model ของ **Yolo** ต้องการ

### 4️⃣ **Phase 4** เทรน model

เริ่มเทรน model โดยจะมี Base Model เป็น **yolo11s.pt** ซึ่งมีคำสั่งเบื้องหลังในการเทรนดังภาพ จบขั้นตอนนี้เราจะได้ไฟล์ **my-model.pt** มาเพื่อใช้งาน

<img width="1514" height="212" alt="image" src="https://github.com/user-attachments/assets/4877405a-74bd-4f92-bbb9-a5588b53136e" />


**Parameters ที่สำคัญ**
- model = ตั้งค่า model เริ่มต้นก่อนที่จะเริ่มเทรน
- epochs = จำนวนรอบที่ ai จะเทรน รูปภาพทุกภาพ
- imgsz = ขนาดรูปภาพที่ ai จะย่อลงมา
- workers = จำนวน cpu threads
- device = สิ่งที่จะใช้ในการประมวลผล (0=gpu)

**parameters แต่ละตัวขึ้นอยู่กับความแรงของเครื่อง server ที่รัน script**

---
## หมายเหตุ
- **.env** ที่อยู่ใน git repository นี้ตั้งใจ commit ขึ้นมาเนื่องจากใช้เเค่เก็บตัวแปรที่สำคัญบางตัว ไม่ได้มีการเก็บ **Sensitive Data** เเต่อย่างใด





