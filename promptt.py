import streamlit as st
from PIL import Image
import requests
from io import BytesIO

st.title("แสดงภาพจาก URL ที่เลือก")

# รายการ URL ของภาพ
image_urls = {
    "Bulldog": "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "แมวดำ": "https://upload.wikimedia.org/wikipedia/commons/0/0b/Cat_poster_1.jpg",
    "นกยูง": "https://upload.wikimedia.org/wikipedia/commons/b/b1/Peacock_Plumage.jpg"
}

# สร้างตัวเลือก dropdown
selected_image = st.selectbox("เลือกภาพที่ต้องการแสดง:", list(image_urls.keys()))

# ดึง URL จากตัวเลือก
image_url = image_urls[selected_image]

# แสดง URL และโหลดภาพ
st.write("แหล่งภาพ:", image_url)

try:
    response = requests.get(image_url)
    response.raise_for_status()
    img = Image.open(BytesIO(response.content))
    st.image(img, caption=selected_image, use_container_width=True)
except Exception as e:
    st.error(f"ไม่สามารถโหลดภาพได้: {e}")
