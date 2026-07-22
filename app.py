import streamlit as st
from ultralytics import YOLO
from PIL import Image
import numpy as np
import cv2
import os
from dotenv import load_dotenv
load_dotenv()
model_name = os.environ.get("MODEL_NAME")

# ─── Page Config ───
st.set_page_config(
    page_title="🪙 Thai Coin Counter",
    page_icon="🪙",
    layout="wide"
)

# ─── Custom CSS ───
st.markdown("""
<style>
    /* พื้นหลังหลัก */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    }

    /* หัวข้อใหญ่ */
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #f7971e, #ffd200);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        text-align: center;
        color: #aaa;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    /* กล่องสรุป */
    .summary-box {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(10px);
    }
    .coin-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.06);
        font-size: 1.1rem;
    }
    .coin-row:last-child { border-bottom: none; }
    .coin-name { color: #ddd; }
    .coin-count { 
        color: #ffd200; 
        font-weight: 700; 
        font-size: 1.2rem;
    }

    /* มูลค่ารวม */
    .total-box {
        background: linear-gradient(135deg, #f7971e, #ffd200);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        margin-top: 1rem;
    }
    .total-label {
        font-size: 1rem;
        color: #333;
        font-weight: 600;
    }
    .total-value {
        font-size: 3rem;
        font-weight: 900;
        color: #1a1a2e;
        line-height: 1.2;
    }

    /* กล่อง metric */
    .metric-card {
        background: rgba(255,255,255,0.07);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
    }
    .metric-number {
        font-size: 2.2rem;
        font-weight: 800;
        color: #ffd200;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #999;
        margin-top: 0.2rem;
    }

    /* ซ่อน Streamlit default */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ─── Header ───
st.markdown('<div class="main-title">🪙 Thai Coin Counter</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">อัปโหลดรูปภาพเหรียญไทย แล้ว AI จะนับให้อัตโนมัติ</div>', unsafe_allow_html=True)

# ─── Load Model (cached) ───
@st.cache_resource
def load_model():
    model_path = os.path.join(os.path.dirname(__file__), f"{model_name}.pt")
    return YOLO(model_path)

model = load_model()

# ─── มูลค่าเหรียญแต่ละประเภท ───
COIN_VALUES = {
    "1baht": 1,
    "5baht": 5,
    "10baht": 10,
}

COIN_DISPLAY_NAMES = {
    "1baht": "🥉 เหรียญ 1 บาท",
    "5baht": "🥈 เหรียญ 5 บาท",
    "10baht": "🥇 เหรียญ 10 บาท",
}

# ─── Sidebar Settings ───
with st.sidebar:
    st.markdown("### ⚙️ ตั้งค่าการตรวจจับ")
    confidence_threshold = st.slider(
        "🎯 Confidence ขั้นต่ำ (%)", 
        min_value=10, max_value=100, value=25, step=5,
        help="เหรียญที่ AI มั่นใจน้อยกว่าค่านี้จะถูกตัดออก (YOLO ค่าเริ่มต้น = 25%)"
    )
    
    iou_threshold = st.slider(
        "📦 IoU Threshold",
        min_value=0.1, max_value=1.0, value=0.45, step=0.05,
        help="ถ้ากล่อง 2 อันซ้อนทับกันเกินค่านี้ จะถูกยุบรวมเป็นอันเดียว"
    )

    use_agnostic_nms = st.checkbox(
        "🔀 Agnostic NMS", value=True,
        help="ยุบกล่องซ้อนทับข้าม Class (เลือกอันที่ % สูงสุด)"
    )

    st.markdown("---")
    st.markdown("### 📖 วิธีใช้")
    st.markdown("""
    1. อัปโหลดรูปเหรียญ (jpg/png)
    2. AI จะตีกรอบเหรียญให้อัตโนมัติ
    3. ดูผลสรุปจำนวน + มูลค่ารวมด้านขวา
    """)

# ─── Upload Image ───
uploaded_file = st.file_uploader(
    "📤 อัปโหลดรูปภาพเหรียญ",
    type=["jpg", "jpeg", "png"],
    help="รองรับไฟล์ .jpg, .jpeg, .png"
)

if uploaded_file is not None:
    # อ่านภาพ
    image = Image.open(uploaded_file)
    img_array = np.array(image)

    # รัน YOLO
    with st.spinner("🔍 AI กำลังตรวจจับเหรียญ..."):
        results = model.predict(
            img_array, 
            verbose=False,
            conf=confidence_threshold / 100,
            iou=iou_threshold,
            agnostic_nms=use_agnostic_nms,
        )

    boxes = results[0].boxes
    class_names_dict = results[0].names

    # นับเหรียญ
    coin_counts = {}
    confidences = []

    if len(boxes) > 0:
        for c, conf in zip(boxes.cls, boxes.conf):
            class_name = class_names_dict[int(c)]
            conf_val = conf.item()
            confidences.append(conf_val)
            coin_counts[class_name] = coin_counts.get(class_name, 0) + 1

    # วาดกล่องลงบนรูป (plot() คืน RGB ตาม input จาก PIL อยู่แล้ว)
    annotated_img_rgb = results[0].plot()

    # ─── Layout: ภาพ (ซ้าย) + สรุป (ขวา) ───
    col_img, col_summary = st.columns([3, 1.5])

    with col_img:
        st.image(annotated_img_rgb, caption="📸 ผลการตรวจจับ", use_container_width=True)

    with col_summary:
        total_coins = sum(coin_counts.values())
        total_value = sum(COIN_VALUES.get(name, 0) * count for name, count in coin_counts.items())
        avg_conf = (sum(confidences) / len(confidences) * 100) if confidences else 0

        # Metric cards
        m1, m2 = st.columns(2)
        with m1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-number">{total_coins}</div>
                <div class="metric-label">เหรียญที่พบ</div>
            </div>
            """, unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-number">{avg_conf:.0f}%</div>
                <div class="metric-label">ความมั่นใจเฉลี่ย</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # รายละเอียดเหรียญ
        if coin_counts:
            st.markdown('<div class="summary-box">', unsafe_allow_html=True)
            st.markdown("#### 🪙 รายละเอียดเหรียญ")
            
            for class_name in sorted(coin_counts.keys(), key=lambda x: COIN_VALUES.get(x, 0)):
                count = coin_counts[class_name]
                display_name = COIN_DISPLAY_NAMES.get(class_name, class_name)
                value = COIN_VALUES.get(class_name, 0) * count
                st.markdown(f"""
                <div class="coin-row">
                    <span class="coin-name">{display_name}</span>
                    <span class="coin-count">{count} เหรียญ = {value} บาท</span>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

            # มูลค่ารวม
            st.markdown(f"""
            <div class="total-box">
                <div class="total-label">💰 มูลค่ารวม</div>
                <div class="total-value">{total_value} บาท</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("❌ ไม่พบเหรียญในภาพ ลองปรับค่า Confidence ลงหรืออัปโหลดภาพอื่น")

else:
    # ─── ยังไม่อัปโหลด: โชว์ตัวอย่าง ───
    st.markdown("---")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-number">📤</div>
            <div class="metric-label">อัปโหลดรูปภาพ</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-number">🔍</div>
            <div class="metric-label">AI ตรวจจับเหรียญ</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-number">💰</div>
            <div class="metric-label">สรุปมูลค่ารวม</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("👆 กดปุ่ม **Browse files** ด้านบนเพื่ออัปโหลดรูปภาพเหรียญ แล้ว AI จะนับให้อัตโนมัติครับ!")
