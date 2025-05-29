import math
from PIL import ImageDraw

def add_axes_and_bg_rotated(image, rotate_angle_deg, bg_color=(240, 240, 240), axis_color=(0, 0, 0)):
    w, h = image.size
    margin = 70  # เพิ่มขอบให้กว้างขึ้นเพื่อรองรับแกนหมุน

    new_w = w + margin * 2
    new_h = h + margin * 2

    canvas = Image.new("RGB", (new_w, new_h), bg_color)
    canvas.paste(image, (margin, margin))

    draw = ImageDraw.Draw(canvas)
    font = get_font(14)

    # Origin จุดฐานแกน (bottom-left ของภาพบน canvas)
    origin = (margin, margin + h)

    # แปลงองศาเป็นเรเดียน (สำหรับคำนวณ sin cos)
    theta = math.radians(-rotate_angle_deg)  # หมุนไปทางซ้ายตามการหมุนภาพ

    # ความยาวแกน X และ Y (ใช้ขนาดภาพ)
    length_x = w
    length_y = h

    # คำนวณจุดปลายแกน X และ Y หมุนตามมุม
    end_x = (origin[0] + length_x * math.cos(theta),
             origin[1] + length_x * math.sin(theta))
    end_y = (origin[0] - length_y * math.sin(theta),
             origin[1] + length_y * math.cos(theta))

    # วาดแกน X, Y
    draw.line([origin, end_x], fill=axis_color, width=2)
    draw.line([origin, end_y], fill=axis_color, width=2)

    # วาด tick marks บนแกน X
    num_ticks = 5
    for i in range(num_ticks + 1):
        t = i / num_ticks
        # ตำแหน่ง tick บนแกน X (linear interpolation)
        tx = origin[0] + length_x * t * math.cos(theta)
        ty = origin[1] + length_x * t * math.sin(theta)

        # แนวขวาง tick mark (ตั้งฉากแกน X)
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

        # วางข้อความห่างจาก tick mark เล็กน้อย
        text_pos = (tx + 2 * tick_dx - text_w // 2, ty + 2 * tick_dy - text_h // 2)
        draw.text(text_pos, text, fill=axis_color, font=font)

    # วาด tick marks บนแกน Y
    for i in range(num_ticks + 1):
        t = i / num_ticks
        # ตำแหน่ง tick บนแกน Y
        tx = origin[0] - length_y * t * math.sin(theta)
        ty = origin[1] + length_y * t * math.cos(theta)

        # แนวขวาง tick mark (ตั้งฉากแกน Y)
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

        # วางข้อความห่างจาก tick mark เล็กน้อย
        text_pos = (tx + 2 * tick_dx - text_w, ty + 2 * tick_dy - text_h // 2)
        draw.text(text_pos, text, fill=axis_color, font=font)

    # วาด label แกน X, Y
    label_offset = 20
    # Label X
    label_x_pos = (end_x[0] + label_offset * math.cos(theta),
                   end_x[1] + label_offset * math.sin(theta))
    draw.text(label_x_pos, "X", fill=axis_color, font=font)
    # Label Y
    label_y_pos = (end_y[0] - label_offset * math.sin(theta),
                   end_y[1] + label_offset * math.cos(theta))
    draw.text(label_y_pos, "Y", fill=axis_color, font=font)

    return canvas
