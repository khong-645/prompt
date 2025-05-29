import streamlit as st
from PIL import Image
import requests
from io import BytesIO

st.title("เลือกรูปภาพจาก URL พร้อมปรับขนาด")

image_data = {
    "Bulldog": "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "Brooch": "https://upload-os-bbs.hoyolab.com/upload/2023/02/07/5774947/8105b30243238bce2ef7c8a35934bd6f_9170432348253218955.png",
    "Kiana": "https://upload-os-bbs.hoyolab.com/upload/2023/02/07/5774947/713cbe914f7c32a3e4364e426105591c_8715800185506906620.png"
}

# เลือกขนาดภาพเต็ม
width = st.slider("เลือกความกว้างภาพเต็ม (พิกเซล)", min_value=100, max_value=1000, value=400, step=50)

# โหลดภาพย่อและเก็บใน dict สำหรับแสดงใน radio
thumbs = {}
for name, url in image_data.items():
    try:
        response = requests.get(url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        img_thumb = img.copy()
        img_thumb.thumbnail((150, 150))
        thumbs[name] = img_thumb
    except Exception as e:
        st.error(f"โหลดภาพ {name} ไม่ได้: {e}")

# สร้างตัวเลือก radio โดยแสดงภาพย่อพร้อมชื่อ
def format_func(name):
    return name

selected_name = st.radio(
    "เลือกภาพโดยคลิกที่ภาพหรือชื่อ",
    options=list(image_data.keys()),
    format_func=format_func,
    key="selected_name",
    horizontal=True
)

# แสดงภาพย่อในแถวเดียวกันแบบคลิกเลือก
cols = st.columns(len(image_data))
for i, name in enumerate(image_data.keys()):
    with cols[i]:
        st.image(thumbs[name], caption=name, use_container_width=True)

# แสดงภาพเต็มของภาพที่เลือก
if selected_name:
    st.subheader(f"ภาพที่เลือก: {selected_name}")
    try:
        response = requests.get(image_data[selected_name])
        response.raise_for_status()
        full_img = Image.open(BytesIO(response.content))

        aspect_ratio = full_img.height / full_img.width
        new_width = width
        new_height = int(width * aspect_ratio)
        resized_img = full_img.resize((new_width, new_height))

        st.image(resized_img, caption=selected_name, use_container_width=False)
    except Exception as e:
        st.error(f"โหลดภาพเต็มไม่สำเร็จ: {e}")
