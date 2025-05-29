import streamlit as st
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageFont
import requests
from io import BytesIO
import os

# โหลดฟอนต์สำหรับวาดตัวเลขแกน (ใช้ฟอนต์ DejaVuSans ที่มากับ PIL ถ้าไม่มีจะใช้ฟอนต์ดีฟอลต์)
def get_font(size=14):
    try:
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if not os.path.exists(font_path):
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

    origin = (margin, margin + h)

    # วาดแกน X
    draw.line([origin, (margin + w, margin + h)], fill=axis_color, width=2)
    # วาดแกน Y
    draw.line([origin, (margin, margin)], fill=axis_color, width=2)

    num_ticks = 5
    step_x = w / num_ticks
    step_y = h / num_ticks

    for i in range(num_ticks + 1):
        x = margin + int(i * step_x)
        y = margin + h
        draw.line([(x, y), (x, y + 5)], fill=axis_color, width=1)
        text = str(int(i * step_x))
        try:
            bbox = draw.textbbox((0, 0), text, font=font)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]
        except AttributeError:
            text_w, text_h = draw.textsize(text, font=font)
        draw.text((x - text_w // 2, y + 7), text, fill=axis_color, font=font)

    for i in range(num_ticks + 1):
        x = margin
        y = margin + h - int(i * step_y)
        draw.line([(x - 5, y), (x, y)], fill=axis_color, width=1)
        text = str(int(i * step_y))
        try:
            bbox = draw.textbbox((0, 0), text, font=font)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]
        except AttributeError:
            text_w, text_h = draw.textsize(text, font=font)
        draw.text((x - 10 - text_w, y - text_h // 2), text, fill=axis_color, font=font)

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
            # ปรับขนาดภาพย่อให้พอดีคอลัมน์
            max_width = 150
            ratio = max_width / img.width
            new_size = (max_width, int(img.height * ratio))
            img_thumb = img.resize(new_size, Image.LANCZOS)

            if st.image(img_thumb, caption=name, use_container_width=True, output_format="PNG"):
                pass
            if st.button(f"เลือก {name}", key=name):
                st.session_state.selected_name = name

        except Exception as e:
            st.error(f"โหลดภาพ {name} ไม่ได้")

# ฟังก์ชันใหม่เพื่อแปลงภาพเป็น clickable image (จำกัดด้วย Streamlit API ปัจจุบัน)
def image_clickable(name, img):
    # จริงๆ Streamlit ยังไม่รองรับกดที่รูปโดยตรง
    # เลยต้องใช้ปุ่มเลือก
    if st.button(f"เลือก {name}", key=f"btn_{name}"):
        st.session_state.selected_name = name
    st.image(img, caption=name, use_container_width=False)

if st.session_state.selected_name:
    selected_name = st.session_state.selected_name
    st.subheader(f"ภาพ: {selected_name}")

    # ฟิลเตอร์ต่าง ๆ
    convert_gray = st.checkbox("แปลงเป็นขาวดำ")
    apply_blur = st.checkbox("เบลอภาพ")
    contrast_factor = st.slider("ปรับคอนทราสต์", 0.5, 2.0, 1.0, 0.1)
    rotate_angle = st.slider("หมุนภาพ (องศา)", 0, 360, 0, 5)
    resize_factor = st.slider("ปรับขนาดภาพ (%)", 10, 200, 100, 5)

    full_url = image_data[selected_name].split("?")[0]
    try:
        response = requests.get(full_url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content)).convert("RGB")

        if convert_gray:
            img = img.convert("L").convert("RGB")
        if apply_blur:
            img = img.filter(ImageFilter.GaussianBlur(2))
        if contrast_factor != 1.0:
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(contrast_factor)
        if rotate_angle != 0:
            img = img.rotate(-rotate_angle, expand=True)
        if resize_factor != 100:
            new_w = int(img.width * resize_factor / 100)
            new_h = int(img.height * resize_factor / 100)
            img = img.resize((new_w, new_h), Image.LANCZOS)

        img_with_axes = add_axes_and_bg_rotated(img, bg_color=(240, 240, 240), axis_color=(0, 0, 0))
        st.image(img_with_axes, caption=f"{selected_name} (หลังปรับ)", use_container_width=True)

    except Exception as e:
        st.error(f"ไม่สามารถโหลดภาพแบบเต็มได้: {e}")
