import streamlit as st
from PIL import Image
import requests
from io import BytesIO

st.title("แสดงภาพจาก URL ที่เลือก")

# รายการ URL ของภาพ
image_urls = {
    "Bulldog": "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "brooch": "https://upload-os-bbs.hoyolab.com/upload/2023/02/07/5774947/8105b30243238bce2ef7c8a35934bd6f_9170432348253218955.png?x-oss-process=image%2Fresize%2Cs_1000%2Fauto-orient%2C0%2Finterlace%2C1%2Fformat%2Cwebp%2Fquality%2Cq_70.jpg",
    "Kiana": "https://upload-os-bbs.hoyolab.com/upload/2023/02/07/5774947/713cbe914f7c32a3e4364e426105591c_8715800185506906620.png?x-oss-process=image%2Fresize%2Cs_1000%2Fauto-orient%2C0%2Finterlace%2C1%2Fformat%2Cwebp%2Fquality%2Cq_70.jpg"
}

# สร้างตัวเลือก dropdown
selected_image = st.selectbox("เลือกภาพที่ต้องการแสดง:", list(image_urls.keys()))

# ดึง URL จากตัวเลือก
image_url = image_urls[selected_image]

# แสดง URL
st.write("แหล่งภาพ:", image_url)

# ตัวเลือกแปลงเป็นขาวดำ
convert_gray = st.checkbox("แปลงเป็นภาพขาวดำ")

# ปุ่มกดเพื่อแสดงภาพ
if st.button("แสดงภาพ"):
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        
        # แปลงเป็น grayscale ถ้าเลือก
        if convert_gray:
            img = img.convert("L")
        
        st.image(img, caption=selected_image, use_container_width=True)
    except Exception as e:
        st.error(f"ไม่สามารถโหลดภาพได้: {e}")
