import streamlit as st
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageFont
import requests
from io import BytesIO
import os

def get_font(size=14):
    try:
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if not os.path.exists(font_path):
            return ImageFont.load_default()
        return ImageFont.truetype(font_path, size)
    except Exception:
        return ImageFont.load_default()

def add_axes_and_bg_rotated(image, bg_color=(240, 240, 240), axis_color=(0, 0, 0)):
    w, h = image.size
    margin = 50
    new_w = w + margin + 10
    new_h = h + margin + 10
    canvas = Image.new("RGB", (new_w, new_h), bg_color)
    canvas.paste(image, (margin, margin))
    draw = ImageDraw.Draw(canvas)
    font = get_font(14)
    origin = (margin, margin + h)
    draw.line([origin, (margin + w, margin + h)], fill=axis_color, width=2)
    draw.line([origin, (margin, margin)], fill=axis_color, width=2)
    num_ticks = 5
    step_x = w / num_ticks
    step_y = h / num_ticks
    for i in range(num_ticks + 1):
        x = margin + int(i * step_x)
        y = margin + h
        draw.line([(x, y), (x, y + 5)], fill=axis_color, width=1)
        text = str(int(i * step_x))
        text_w, text_h = draw.textsize(text, font=font)
        draw.text((x - text_w // 2, y + 7), text, fill=axis_color, font=font)
    for i in range(num_ticks + 1):
        x = margin
        y = margin + h - int(i * step_y)
        draw.line([(x - 5, y), (x, y)], fill=axis_color, width=1)
        text = str(int(i * step_y))
        text_w, text_h = draw.textsize(text, font=font)
        draw.text((x - 10 - text_w, y - text_h // 2), text, fill=axis_color, font=font)
    return canvas

# ------------------

st.title("เลือกรูปภาพโดยคลิกที่ภาพ พร้อมฟิลเตอร์")

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
            # แสดงภาพย่อ
            st.image(img_thumb, caption=name, use_container_width=True)
            # ปุ่มซ่อนใต้ภาพเพื่อเลือก
            if st.button(f"select_{name}", key=f"select_{name}"):
                st.session_state.selected_name = name
        except Exception as e:
            st.error(f"โหลดภาพ {name} ไม่ได้: {e}")

if st.session_state.selected_name:
    selected_name = st.session_state.selected_name
    st.subheader(f"ภาพที่เลือก: {selected_name}")

    # ฟิลเตอร์
    convert_gray = st.checkbox("แปลงเป็นขาวดำ")
    apply_blur = st.checkbox("เบลอภาพ")
    contrast_factor = st.slider("ปรับคอนทราสต์", 0.5, 2.0, 1.0, 0.1)
    rotate_angle = st.slider("หมุนภาพ (องศา)", 0, 360, 0, 5)
    resize_scale = st.slider("ปรับขนาดภาพ (สเกล)", 0.1, 2.0, 1.0, 0.1)

    full_url = image_data[selected_name].split("?")[0]

    try:
        response = requests.get(full_url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content)).convert("RGB")

        # ปรับขนาดภาพตามสเกลที่เลือก
        if resize_scale != 1.0:
            new_w = int(img.width * resize_scale)
            new_h = int(img.height * resize_scale)
            img = img.resize((new_w, new_h), Image.LANCZOS)

        if convert_gray:
            img = img.convert("L").convert("RGB")
        if apply_blur:
            img = img.filter(ImageFilter.GaussianBlur(2))
        if contrast_factor != 1.0:
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(contrast_factor)
        if rotate_angle != 0:
            img = img.rotate(-rotate_angle, expand=True)

        img_with_axes = add_axes_and_bg_rotated(img, bg_color=(240, 240, 240), axis_color=(0, 0, 0))

        st.image(img_with_axes, caption=f"{selected_name} (หลังปรับ)", use_container_width=True)

    except Exception as e:
        st.error(f"โหลดภาพไม่สำเร็จ: {e}")
