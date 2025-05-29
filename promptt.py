import streamlit as st
from PIL import Image
import requests
from io import BytesIO

st.title("เลือกรูปภาพจาก 3 ตัวเลือก")

image_data = {
    "Bulldog": "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "Brooch": "https://upload-os-bbs.hoyolab.com/upload/2023/02/07/5774947/8105b30243238bce2ef7c8a35934bd6f_9170432348253218955.png?x-oss-process=image%2Fresize%2Cs_300",
    "Kiana": "https://upload-os-bbs.hoyolab.com/upload/2023/02/07/5774947/713cbe914f7c32a3e4364e426105591c_8715800185506906620.png?x-oss-process=image%2Fresize%2Cs_300"
}

# กำหนดค่าเริ่มต้นใน session_state
if "selected_name" not in st.session_state:
    st.session_state.selected_name = None

cols = st.columns(len(image_data))

for i, (name, url) in enumerate(image_data.items()):
    with cols[i]:
        try:
            response = requests.get(url)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))
            st.image(img, caption=name, use_column_width=True)
            if st.button(f"เลือก {name}", key=f"btn_{name}"):
                st.session_state.selected_name = name
        except Exception as e:
            st.error(f"โหลดภาพ {name} ไม่ได้")

# แสดงภาพเต็มหลังเลือก
if st.session_state.selected_name:
    selected_name = st.session_state.selected_name
    st.subheader(f"ภาพที่เลือก: {selected_name}")
    full_url = image_data[selected_name].split("?")[0]
    try:
        response = requests.get(full_url)
        response.raise_for_status()
        full_img = Image.open(BytesIO(response.content))
        st.image(full_img, caption=selected_name, use_column_width=True)
    except Exception as e:
        st.error(f"ไม่สามารถโหลดภาพเต็มได้: {e}")
