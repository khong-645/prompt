import streamlit as st
from PIL import Image, ImageFilter, ImageEnhance
import requests
from io import BytesIO

# ใส่ CSS แบบฝังเพื่อจัด layout และเพิ่มพื้นหลัง
st.markdown(
    """
    <style>
    /* ตั้งพื้นหลังแบบไล่ระดับสี */
    .main {
        background: linear-gradient(135deg, #89f7fe 0%, #66a6ff 100%);
        padding: 20px;
        border-radius: 12px;
    }
    /* จัด container ตัวเลือกให้เรียงเป็นแถวและความสูงเท่ากัน */
    .filter-container {
        display: flex;
        gap: 20px;
        align-items: center;  /* ความสูงเท่ากัน */
        margin-bottom: 20px;
        flex-wrap: wrap;
    }
    /* ขนาดเล็กและจัดแนวกลางสำหรับแต่ละ control */
    .filter-item {
        flex: 1;
        min-width: 150px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ครอบ div main
st.markdown('<div class="main">', unsafe_allow_html=True)

st.title("เลือกรูปจากรายการพร้อมภาพย่อและฟิลเตอร์")

image_data = {
    "Bulldog": "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "brooch": "https://upload-os-bbs.hoyolab.com/upload/2023/02/07/5774947/8105b30243238bce2ef7c8a35934bd6f_9170432348253218955.png?x-oss-process=image%2Fresize%2Cs_300",
    "Kiana": "https://upload-os-bbs.hoyolab.com/upload/2023/02/07/5774947/713cbe914f7c32a3e4364e426105591c_8715800185506906620.png?x-oss-process=image%2Fresize%2Cs_300"
}

st.subheader("เลือกรูปที่ต้องการดูแบบเต็ม:")
cols = st.columns(len(image_data))
selected_name = None

for i, (name, url) in enumerate(image_data.items()):
    with cols[i]:
        try:
            response = requests.get(url)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))
            st.image(img, caption=name, use_container_width=True)
            if st.button(f"เลือก {name}", key=name):
                selected_name = name
        except Exception as e:
            st.error(f"โหลดภาพ {name} ไม่ได้")

if selected_name:
    st.subheader(f"ภาพ: {selected_name}")

    # ใช้ container div สำหรับจัดแท็บตัวเลือกเป็นแถวเดียวกัน
    st.markdown('<div class="filter-container">', unsafe_allow_html=True)
    
    # แต่ละตัวเลือกอยู่ใน div ของตัวเองเพื่อจัด CSS
    st.markdown('<div class="filter-item">', unsafe_allow_html=True)
    convert_gray = st.checkbox("แปลงเป็นขาวดำ")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="filter-item">', unsafe_allow_html=True)
    apply_blur = st.checkbox("เบลอภาพ")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="filter-item">', unsafe_allow_html=True)
    contrast_factor = st.slider("ปรับคอนทราสต์", 0.5, 2.0, 1.0, 0.1)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="filter-item">', unsafe_allow_html=True)
    rotate_angle = st.slider("หมุนภาพ (องศา)", 0, 360, 0, 5)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # ปิด filter-container

    # โหลดภาพเต็มและแปลงตามตัวเลือก
    full_url = image_data[selected_name].split("?")[0]
    try:
        response = requests.get(full_url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))

        if convert_gray:
            img = img.convert("L")
        if apply_blur:
            img = img.filter(ImageFilter.GaussianBlur(2))
        if contrast_factor != 1.0:
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(contrast_factor)
        if rotate_angle != 0:
            img = img.rotate(-rotate_angle, expand=True)

        st.image(img, caption=f"{selected_name} (หลังปรับ)", use_container_width=True)

    except Exception as e:
        st.error(f"ไม่สามารถโหลดภาพแบบเต็มได้: {e}")

st.markdown('</div>', unsafe_allow_html=True)  # ปิด main div
