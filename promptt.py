import streamlit as st
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageFont
import requests
from io import BytesIO

def add_axes_and_bg(image, bg_color=(230, 230, 230), axis_color=(0, 0, 0)):
    # สร้างภาพพื้นหลังใหญ่กว่าภาพจริง เพื่อเว้นที่แกน
    w, h = image.size
    margin = 40  # ขอบสำหรับแกน

    new_w = w + margin + 10
    new_h = h + margin + 10

    # สร้าง canvas ใหม่สี bg_color
    canvas = Image.new("RGB", (new_w, new_h), bg_color)
    # วางภาพจริงลง canvas
    canvas.paste(image, (margin, 0))

    draw = ImageDraw.Draw(canvas)

    # วาดแกน X (แนวนอน)
    draw.line([(margin, h), (new_w - 10, h)], fill=axis_color, width=2)
    # วาดแกน Y (แนวตั้ง)
    draw.line([(margin, 0), (margin, h + 10)], fill=axis_color, width=2)

    # วาดตัวเลขแกน X
    for x in range(0, w+1, max(1, w//5)):
        pos_x = margin + x
        draw.line([(pos_x, h), (pos_x, h+5)], fill=axis_color, width=1)
        draw.text((pos_x-5, h+7), str(x), fill=axis_color)

    # วาดตัวเลขแกน Y
    for y in range(0, h+1, max(1, h//5)):
        pos_y = y
        draw.line([(margin-5, pos_y), (margin, pos_y)], fill=axis_color, width=1)
        draw.text((margin-30, pos_y-7), str(h - y), fill=axis_color)

    return canvas

st.title("ภาพพร้อมแกน X, Y และพื้นหลัง")

image_url = "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg"

try:
    response = requests.get(image_url)
    response.raise_for_status()
    img = Image.open(BytesIO(response.content)).convert("RGB")

    # ใส่แกนและพื้นหลังสีเทาอ่อน
    img_with_axes = add_axes_and_bg(img, bg_color=(240, 240, 240), axis_color=(0, 0, 0))

    st.image(img_with_axes, caption="ภาพพร้อมแกน X, Y", use_container_width=True)

except Exception as e:
    st.error(f"โหลดภาพไม่ได้: {e}")
