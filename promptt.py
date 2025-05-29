def add_axes_and_bg_rotated(image, rotate_angle=0, bg_color=(240, 240, 240), axis_color=(0, 0, 0)):
    import math
    w, h = image.size
    margin = 70

    new_w = w + margin * 2
    new_h = h + margin * 2

    canvas = Image.new("RGB", (new_w, new_h), bg_color)
    canvas.paste(image, (margin, margin))

    draw = ImageDraw.Draw(canvas)
    font = get_font(14)

    origin = (margin, margin + h)
    theta = math.radians(-rotate_angle)  # หมุนแกนไปทางซ้ายตามภาพหมุน

    length_x = w
    length_y = h

    end_x = (origin[0] + length_x * math.cos(theta),
             origin[1] + length_x * math.sin(theta))
    end_y = (origin[0] - length_y * math.sin(theta),
             origin[1] + length_y * math.cos(theta))

    # วาดแกน X, Y
    draw.line([origin, end_x], fill=axis_color, width=2)
    draw.line([origin, end_y], fill=axis_color, width=2)

    num_ticks = 5
    for i in range(num_ticks + 1):
        t = i / num_ticks
        tx = origin[0] + length_x * t * math.cos(theta)
        ty = origin[1] + length_x * t * math.sin(theta)
        tick_dx = 5 * math.sin(theta)
        tick_dy = -5 * math.cos(theta)
        draw.line([(tx, ty), (tx + tick_dx, ty + tick_dy)], fill=axis_color, width=1)
        text = str(int(length_x * t))
        try:
            bbox = draw.textbbox((0, 0), text, font=font)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]
        except AttributeError:
            text_w, text_h = draw.textsize(text, font=font)
        draw.text((tx + 2 * tick_dx - text_w // 2, ty + 2 * tick_dy - text_h // 2), text, fill=axis_color, font=font)

    for i in range(num_ticks + 1):
        t = i / num_ticks
        tx = origin[0] - length_y * t * math.sin(theta)
        ty = origin[1] + length_y * t * math.cos(theta)
        tick_dx = -5 * math.cos(theta)
        tick_dy = -5 * math.sin(theta)
        draw.line([(tx, ty), (tx + tick_dx, ty + tick_dy)], fill=axis_color, width=1)
        text = str(int(length_y * t))
        try:
            bbox = draw.textbbox((0, 0), text, font=font)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]
        except AttributeError:
            text_w, text_h = draw.textsize(text, font=font)
        draw.text((tx + 2 * tick_dx - text_w, ty + 2 * tick_dy - text_h // 2), text, fill=axis_color, font=font)

    label_offset = 20
    label_x_pos = (end_x[0] + label_offset * math.cos(theta),
                   end_x[1] + label_offset * math.sin(theta))
    label_y_pos = (end_y[0] - label_offset * math.sin(theta),
                   end_y[1] + label_offset * math.cos(theta))
    draw.text(label_x_pos, "X", fill=axis_color, font=font)
    draw.text(label_y_pos, "Y", fill=axis_color, font=font)

    return canvas


# ส่วนเรียกใช้ใน Streamlit
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
        
        st.write(f"ภาพต้นฉบับขนาด: {img.size}")
        if rotate_angle != 0:
            img = img.rotate(-rotate_angle, expand=True)
            st.write(f"ภาพหมุนขนาด: {img.size}")

        img_with_axes = add_axes_and_bg_rotated(img, rotate_angle, bg_color=(240, 240, 240), axis_color=(0, 0, 0))
        st.write(f"ภาพพร้อมแกนขนาด: {img_with_axes.size}")

        st.image(img_with_axes, caption=f"{selected_name} (หลังปรับ)", use_container_width=True)

    except Exception as e:
        st.error(f"ไม่สามารถโหลดภาพแบบเต็มได้: {e}")
