import streamlit as st
from PIL import Image
import requests
from io import BytesIO

st.title("เลือกรูปภาพจาก URL พร้อมปรับขนาด")

# รายการภาพ (ชื่อ + URL)
image_data = {
    "Bulldog": "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "Brooch": "https://upload-os-bbs.hoyolab.com/upload/2023/02/07/5774947/8105b30243238bce2ef7c8a35934bd6f_9170432348253218955.png",
    "Kiana": "https://upload-os-bbs.hoyolab.com/upload/2023/02/07/5774947/713cbe914f7c32a3e4364e426105591c_8715800185506906620.png"
}

# เลือกขนาดภาพที่จะแสดง (พิกเซล กว้าง x สูง)
width = st.slider("เลือกความกว้างภาพเต็ม (พิกเซล)", min_value=100, max_value=1000, value=400, step=50)

# แสดงภาพย่อพร้อมปุ่มเลือก
cols = st.columns(len(image_data))

for i, (name, url) in enumerate(image_data.items()):
    with cols[i]:
        try:
            response = requests.get(url)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))

            # แสดงภาพย่อ ขนาดกว้าง 150 px (ปรับขนาดภาพย่อ)
            img_thumb = img.copy()
            img_thumb.thumbnail((150, 150))
            st.image(img_thumb, caption=name, use_container_width=True)

            if st.button(f"เลือก {name}", key=name):
                st.session_state.selected_name = name
                st.session_state.selected_url = url
        except Exception as e:
            st.error(f"โหลดภาพ {name} ไม่ได้: {e}")

# ถ้ามีภาพถูกเลือกให้แสดงภาพเต็มตามขนาดที่เลือก
if "selected_name" in st.session_state and st.session_state.selected_name:
    st.subheader(f"ภาพที่เลือก: {st.session_state.selected_name}")
    try:
        response = requests.get(st.session_state.selected_url)
        response.raise_for_status()
        full_img = Image.open(BytesIO(response.content))

        # ปรับขนาดภาพเต็มตามความกว้างที่เลือก โดยรักษาอัตราส่วนเดิม
        aspect_ratio = full_img.height / full_img.width
        new_width = width
        new_height = int(width * aspect_ratio)
        resized_img = full_img.resize((new_width, new_height))

        st.image(resized_img, caption=st.session_state.selected_name, use_container_width=False)
    except Exception as e:
        st.error(f"โหลดภาพเต็มไม่สำเร็จ: {e}")
