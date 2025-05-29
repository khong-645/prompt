import streamlit as st
from PIL import Image
import requests
from io import BytesIO

# ตั้งชื่อแอป
st.title("แสดงภาพจาก URL")

# URL ของภาพ
image_url = "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg"

# แสดง URL ให้ผู้ใช้เห็น
st.write("แหล่งภาพ:", image_url)

# ดาวน์โหลดและแสดงภาพ
try:
    response = requests.get(image_url)
    response.raise_for_status()  # ตรวจสอบว่าโหลดสำเร็จ
    img = Image.open(BytesIO(response.content))
    st.image(img, caption="ภาพจาก Wikipedia", use_column_width=True)
except Exception as e:
    st.error(f"ไม่สามารถโหลดภาพได้: {e}")
