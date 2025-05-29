# ... โค้ดส่วนบนเหมือนเดิม ...

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

# ส่วน image_data
image_data = {
    "Bulldog": "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "brooch": "https://upload-os-bbs.hoyolab.com/upload/2023/02/07/5774947/8105b30243238bce2ef7c8a35934bd6f_9170432348253218955.png?x-oss-process=image%2Fresize%2Cs_300",
    "Kiana": "https://upload-os-bbs.hoyolab.com/upload/2023/02/07/5774947/713cbe914f7c32a3e4364e426105591c_8715800185506906620.png?x-oss-process=image%2Fresize%2Cs_300"
}

# ... โค้ดส่วนที่เหลือเหมือนเดิม ...
