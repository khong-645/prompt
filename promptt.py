import streamlit as st
from PIL import Image, ImageFilter, ImageEnhance
import requests
from io import BytesIO

st.title("เลือกรูปจากรายการพร้อมภาพย่อและฟิลเตอร์")

# รายการภาพ
image_data = {
    "Bulldog": "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "brooch": "https://upload-os-bbs.hoyolab.com/upload/2023/02/07/5774947/8105b30243238bce2ef7c8a35934bd6f_9170432348253218955.png?x-oss-process=image%2Fresize%2Cs_300",
    "Kiana": "https://upload-os-bbs.hoyolab.com/upload/2023/02/07/5774947/713cbe914f7c32a3e4364e426105591c_8715800185506906620.png?x-oss-process=image%2Fresize%2Cs_300"
}

# แสดงภาพย่อพร้อมปุ่มเลือก
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

# ถ้ามีการเลือกภาพ
if selected_name:
    st.subheader(f"ภาพ: {selected_name}")

    # ตัวเลือกฟิลเตอร์
    convert_gray = st.checkbox("แปลงเป็นขาวดำ")
    apply_blur = st.checkbox("เบลอภาพ")
    contrast_factor = st.slider("ปรับคอนทราสต์", 0.5, 2.0, 1.0, 0.1)
    rotate_angle = st.slider("หมุนภาพ (องศา)", 0, 360, 0, 5)

    # โหลดภาพต้นฉบับ (ไม่ย่อ)
    full_url = image_data[selected_name].split("?")[0]
    try:
        response = requests.get(full_url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))

        # แปลงภาพตามฟิลเตอร์
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
