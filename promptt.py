import streamlit as st
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw
import requests
from io import BytesIO

def add_axes_and_bg(image, bg_color=(240, 240, 240), axis_color=(0, 0, 0)):
    w, h = image.size
    margin = 40  # ขอบสำหรับแกน

    new_w = w + margin + 10
    new_h = h + margin + 10

    canvas = Image.new("RGB", (new_w, new_h), bg_color)
    canvas.paste(image, (margin, 0))

    draw = ImageDraw.Draw(canvas)

    # แกน X
    draw.line([(margin, h), (new_w - 10, h)], fill=axis_color, width=2)
    # แกน Y
    draw.line([(margin, 0), (margin, h + 10)], fill=axis_color, width=2)

    # Tick mark และตัวเลขแกน X
    step_x = max(1, w // 5)
    for x in range(0, w + 1, step_x):
        pos_x = margin + x
        draw.line([(pos_x, h), (pos_x, h + 5)], fill=axis_color, width=1)
        draw.text((pos_x - 5, h + 7), str(x), fill=axis_color)

    # Tick mark และตัวเลขแกน Y
    step_y = max(1, h // 5)
    for y in range(0, h + 1, step_y):
        pos_y = y
        draw.line([(margin - 5, pos_y), (margin, pos_y)], fill=axis_color, width=1)
        draw.text((margin - 30, pos_y - 7), str(h - y), fill=axis_color)

    return canvas

st.title("เลือกรูปจากรายการพร้อมภาพย่อและฟิลเตอร์")

image_data = {
    "Bulldog": "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "brooch": "https://upload-os-bbs.hoyolab.com/upload/2023/02/07/5774947/8105b30243238bce2ef7c8a35934bd6f_9170432348253218955.png?x-oss-process=image%2Fresize%2Cs_300",
    "Kiana": "https://upload-os-bbs.hoyolab.com/upload/2023/02/07/5774947/713cbe914f7c32a3e4364e426105591c_8715800185506906620.png?x-oss-process=image%2Fresize%2Cs_300"
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
            st.image(img, caption=name, use_container_width=True)
            if st.button(f"เลือก {name}", key=name):
                st.session_state.selected_name = name
        except Exception as e:
            st.error(f"โหลดภาพ {name} ไม่ได้")

if st.session_state.selected_name:
    selected_name = st.session_state.selected_name
    st.subheader(f"ภาพ: {selected_name}")

    # ฟิลเตอร์ต่าง ๆ
    convert_gray = st.checkbox("แปลงเป็นขาวดำ")
    apply_blur = st.checkbox("เบลอภาพ")
    contrast_factor = st.slider("ปรับคอนทราสต์", 0.5, 2.0, 1.0, 0.1)
    rotate_angle = st.slider("หมุนภาพ (องศา)", 0, 360, 0, 5)

    full_url = image_data[selected_name].split("?")[0]
    try:
        response = requests.get(full_url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content)).convert("RGB")

        if convert_gray:
            img = img.convert("L").convert("RGB")  # แปลงกลับเป็น RGB เพื่อวาดแกนได้
        if apply_blur:
            img = img.filter(ImageFilter.GaussianBlur(2))
        if contrast_factor != 1.0:
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(contrast_factor)
        if rotate_angle != 0:
            img = img.rotate(-rotate_angle, expand=True)

        # เพิ่มแกน X, Y และพื้นหลังสีเทาอ่อน
        img_with_axes = add_axes_and_bg(img, bg_color=(240, 240, 240), axis_color=(0, 0, 0))

        st.image(img_with_axes, caption=f"{selected_name} (หลังปรับ)", use_container_width=True)

    except Exception as e:
        st.error(f"ไม่สามารถโหลดภาพแบบเต็มได้: {e}")
