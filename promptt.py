import streamlit as st
from PIL import Image
import requests
from io import BytesIO

st.title("เลือกรูปภาพโดยกดที่ภาพ")

image_data = {
    "Bulldog": "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "Brooch": "https://upload-os-bbs.hoyolab.com/upload/2023/02/07/5774947/8105b30243238bce2ef7c8a35934bd6f_9170432348253218955.png",
    "Kiana": "https://upload-os-bbs.hoyolab.com/upload/2023/02/07/5774947/713cbe914f7c32a3e4364e426105591c_8715800185506906620.png"
}

if "selected_name" not in st.session_state:
    st.session_state.selected_name = None

cols = st.columns(len(image_data))

for i, (name, url) in enumerate(image_data.items()):
    with cols[i]:
        try:
            response = requests.get(url)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))
            img_thumb = img.copy()
            img_thumb.thumbnail((150, 150))
            st.image(img_thumb, caption=name, use_container_width=True)
            if st.button(f"เลือก {name}", key=name):
                st.session_state.selected_name = name
        except Exception as e:
            st.error(f"โหลดภาพ {name} ไม่ได้: {e}")

if st.session_state.selected_name:
    st.write(f"คุณเลือก: {st.session_state.selected_name}")
    url = image_data[st.session_state.selected_name]
    try:
        response = requests.get(url)
        response.raise_for_status()
        img_full = Image.open(BytesIO(response.content))
        st.image(img_full, caption=st.session_state.selected_name, use_container_width=True)
    except Exception as e:
        st.error(f"โหลดภาพเต็มไม่สำเร็จ: {e}")
