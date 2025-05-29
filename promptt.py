import streamlit as st
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageFont
import requests
from io import BytesIO
import math
import os

# โหลดฟอนต์สำหรับวาดตัวเลขแกน (ใช้ฟอนต์ DejaVuSans ที่มากับ PIL ถ้าไม่มีจะใช้ฟอนต์ดีฟอลต์)
def get_font(size=14):
    try:
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if not os.path.exists(font_path):
            # ลองโหลดฟอนต์ PIL ในตัว
            return ImageFont.load_default()
        return ImageFont.truetype(font_path, size)
    except Exception:
        return ImageFont.load_default()

def add_axes_and_bg_rotated(image, bg_color=(240, 240, 240), axis_color=(0, 0, 0)):
    """
    วาดแกน X, Y และพื้นหลังสีเทาอ่อน โดยแกนจะหมุนตามภาพด้วย
    """
    w, h = image.size
    margin = 50  # ขอบเพิ่มมากขึ้นเพื่อวาดแกน

    new_w = w + margin + 10
    new_h = h + margin + 10

    canvas = Image.new("RGB", (new_w, new_h), bg_color)
    canvas.paste(image, (margin, margin))

    draw = ImageDraw.Draw(canvas)
    font = get_font(14)

    # จุดเริ่มต้นแกน (bottom-left corner ของภาพ)
    origin = (margin, margin + h)

    # วาดแกน X
    draw.line([origin, (margin + w, margin + h)], fill=axis_color, width=2)
    # วาดแกน Y
    draw.line([origin, (margin, margin)], fill=axis_color, width=2)

    # จำนวน tick marks
    num_ticks = 5

    # Tick marks แกน X
    step_x = w / num_ticks
    for i in range(num_ticks + 1):
        x = margin + int(i * step_x)
        y = margin + h
        draw.line([(x, y), (x, y + 5)], fill=axis_color, width=1)
        text = str(int(i * step_x))
        text_w, text_h = draw.textsize(text, font=font)
        draw.text((x - text_w // 2, y + 7), text, fill=axis_color, font=font)

    # Tick marks แกน Y
    step_y = h / num_ticks
    for i in range(num_ticks + 1):
        x = margin
        y = margin + h - int(i * step_y)
        draw.line([(x - 5, y), (x, y)], fill=axis_color, width=1)
        text = str(int(i * step_y))
        text_w, text_h = draw.textsize(text, font=font)
        draw.text((x - 10 - text_w, y - text_h // 2), text, fill=axis_color, font=font)

    return canvas


st.title("เลือกรูปจากรายการพร้อมภาพย่อและฟิลเตอร์")

image_data = {
    "Bulldog": "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "brooch": "https://upload-os-bbs.hoyolab.com/upload/2023/02/07/5774947/8105b30243238bce2ef7c8a35934bd6f_9170432348253218955.jpg",
    "Kiana": "https://upload-os-bbs.hoyolab.com/upload/2023/02/07/5774947/713cbe914f7c32a3e4364e426105591c_8715800185506906620.jpg"
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

        # วาดแกนและพื้นหลังที่ปรับให้เข้ากับภาพหมุน
        img_with_axes = add_axes_and_bg_rotated(img, bg_color=(240, 240, 240), axis_color=(0, 0, 0))

        st.image(img_with_axes, caption=f"{selected_name} (หลังปรับ)", use_container_width=True)

    except Exception as e:
        st.error(f"ไม่สามารถโหลดภาพแบบเต็มได้: {e}")
