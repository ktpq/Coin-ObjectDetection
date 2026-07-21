# Coin Object Detection

## รายละเอียดโปรเจกต์

วัตถุประสงค์หลักของโปรเจกต์นี้คือ:
- ต้องการนำไปใช้แยกเหรียญประเภทต่างๆ
- ต้องการให้การ train model เพื่อเเยกประเภทเหรียญ เป็นแบบ อัตโนมัติมากที่สุด
- เพื่อให้การ label รูปภาพก่อนการเทรนเป็นแบบอัตโนมัติ
---

## ขั้นตอนการติดตั้งและการตั้งค่าระบบ

คำแนะนำด้านล่างนี้สำหรับขั้นตอนการเตรียมความพร้อมและการเรียกใช้งานโปรเจกต์บนเครื่องคอมพิวเตอร์ของคุณ

### 1️⃣ การติดตั้ง (Installation)

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
