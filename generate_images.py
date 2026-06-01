"""
Generate product placeholder images using Pillow
"""
from PIL import Image, ImageDraw, ImageFont
import os
import random

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wwwroot", "images", "products")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Color palette for product categories
CATEGORY_COLORS = {
    "Điện thoại": [(66, 133, 244), (52, 168, 83), (234, 67, 53), (103, 58, 183), (255, 112, 67)],
    "Laptop": [(0, 100, 200), (30, 30, 40), (100, 100, 110), (70, 130, 180), (25, 25, 35)],
    "Tablet": [(100, 100, 120), (180, 180, 200), (200, 200, 210), (60, 60, 80), (80, 80, 100)],
    "Phụ kiện": [(255, 150, 50), (200, 100, 200), (100, 200, 150), (200, 200, 100), (150, 100, 200)],
}

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def wrap_text(text, font, max_width):
    words = text.split()
    lines, line = [], ""
    for word in words:
        test = (line + " " + word).strip()
        if font.getlength(test) <= max_width:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines

def create_product_image(filename, product_name, category_hint, width=400, height=400):
    # Pick gradient colors based on category
    colors = CATEGORY_COLORS.get(category_hint, [(66, 133, 244), (103, 58, 183)])
    c1 = random.choice(colors)
    c2 = tuple(max(0, min(255, c1[i] // 2 + 50)) for i in range(3))
    c3 = tuple(max(0, min(255, c1[i] // 3)) for i in range(3))

    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)

    # Gradient background
    for y in range(height):
        ratio = y / height
        r = int(c1[0] * (1 - ratio) + c2[0] * ratio)
        g = int(c1[1] * (1 - ratio) + c2[1] * ratio)
        b = int(c1[2] * (1 - ratio) + c2[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Rounded rectangle outline
    rect_padding = 12
    draw.rounded_rectangle(
        [rect_padding, rect_padding, width - rect_padding, height - rect_padding],
        radius=28,
        outline=c1,
        width=3
    )

    # Icon based on category
    icon_size = 100
    icon_x, icon_y = width // 2 - icon_size // 2, height // 3 - icon_size // 2

    if "iPhone" in product_name or "Điện thoại" in product_name or "Phone" in product_name or "Samsung" in product_name or "Galaxy" in product_name or "Xiaomi" in product_name or "Oppo" in product_name:
        icon_char = "📱"
        icon_bg = (255, 255, 255)
    elif "MacBook" in product_name or "Laptop" in product_name or "Dell" in product_name or "ASUS" in product_name or "HP" in product_name or "Lenovo" in product_name:
        icon_char = "💻"
        icon_bg = (255, 255, 255)
    elif "iPad" in product_name or "Tablet" in product_name or "Samsung Tab" in product_name:
        icon_char = "📲"
        icon_bg = (255, 255, 255)
    elif "AirPods" in product_name or "Tai nghe" in product_name or "Headphone" in product_name or "Loa" in product_name or "Loa" in product_name or "Apple Watch" in product_name or "Watch" in product_name:
        icon_char = "🎧"
        icon_bg = (255, 255, 255)
    elif "Ốp lưng" in product_name or "Case" in product_name or "Bàn phím" in product_name or "Keyboard" in product_name or "Chuột" in product_name or "Mouse" in product_name or "Cáp" in product_name or "Sạc" in product_name or "Hub" in product_name:
        icon_char = "🔌"
        icon_bg = (255, 255, 255)
    elif "Samsung Watch" in product_name or "Watch" in product_name or "Đồng hồ" in product_name:
        icon_char = "⌚"
        icon_bg = (255, 255, 255)
    else:
        icon_char = "📦"
        icon_bg = (255, 255, 255)

    # Draw icon background circle
    cx, cy = width // 2, height // 3
    circle_r = 60
    draw.ellipse([cx - circle_r, cy - circle_r, cx + circle_r, cy + circle_r], fill=(255, 255, 255, 180))

    # Try to draw icon char
    try:
        icon_font_size = 48
        try:
            icon_font = ImageFont.truetype("seguiemj.ttf", icon_font_size)
        except:
            try:
                icon_font = ImageFont.truetype("C:/Windows/Fonts/seguiemj.ttf", icon_font_size)
            except:
                icon_font = ImageFont.load_default()
    except:
        icon_font = ImageFont.load_default()

    # Simple phone icon using shapes
    draw.rounded_rectangle([cx - 22, cy - 36, cx + 22, cy + 36], radius=6, fill=c1, outline="white", width=2)

    # Product name text
    text_max_w = width - 60
    try:
        name_font_size = 22
        try:
            name_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", name_font_size)
        except:
            name_font = ImageFont.load_default()
    except:
        name_font = ImageFont.load_default()

    lines = wrap_text(product_name, name_font, text_max_w)
    line_h = int(name_font.size * 1.3)
    total_text_h = len(lines) * line_h
    text_start_y = height // 2 + 20

    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=name_font)
        text_w = bbox[2] - bbox[0]
        x = (width - text_w) // 2
        y = text_start_y + i * line_h
        draw.text((x, y), line, font=name_font, fill=(255, 255, 255))

    # Price tag
    try:
        price_font_size = 16
        try:
            price_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", price_font_size)
        except:
            price_font = ImageFont.load_default()
    except:
        price_font = ImageFont.load_default()

    price_text = "Tech Store AI"
    bbox = draw.textbbox((0, 0), price_text, font=price_font)
    price_w = bbox[2] - bbox[0]
    draw.text(((width - price_w) // 2, height - 50), price_text, font=price_font, fill=(255, 255, 255, 180))

    img.save(filename, "PNG")
    print(f"Created: {filename}")

# Products to generate
products = [
    # Điện thoại
    ("iphone-15-pro-max.png", "iPhone 15 Pro Max", "Điện thoại"),
    ("iphone-15-pro.png", "iPhone 15 Pro", "Điện thoại"),
    ("iphone-15.png", "iPhone 15", "Điện thoại"),
    ("iphone-14-pro-max.png", "iPhone 14 Pro Max", "Điện thoại"),
    ("iphone-14.png", "iPhone 14", "Điện thoại"),
    ("iphone-se.png", "iPhone SE", "Điện thoại"),
    ("samsung-s24-ultra.png", "Samsung Galaxy S24 Ultra", "Điện thoại"),
    ("samsung-s24-plus.png", "Samsung Galaxy S24+", "Điện thoại"),
    ("samsung-s24.png", "Samsung Galaxy S24", "Điện thoại"),
    ("samsung-z-fold5.png", "Samsung Galaxy Z Fold5", "Điện thoại"),
    ("samsung-z-flip5.png", "Samsung Galaxy Z Flip5", "Điện thoại"),
    ("xiaomi-14-ultra.png", "Xiaomi 14 Ultra", "Điện thoại"),
    ("xiaomi-14.png", "Xiaomi 14", "Điện thoại"),
    ("oppo-find-x7.png", "OPPO Find X7 Ultra", "Điện thoại"),
    ("vivo-x100-pro.png", "Vivo X100 Pro", "Điện thoại"),
    # Laptop
    ("macbook-pro-14-m3.png", "MacBook Pro 14 M3", "Laptop"),
    ("macbook-pro-16-m3.png", "MacBook Pro 16 M3 Max", "Laptop"),
    ("macbook-air-15-m3.png", "MacBook Air 15 M3", "Laptop"),
    ("macbook-air-13-m3.png", "MacBook Air 13 M3", "Laptop"),
    ("dell-xps-15.png", "Dell XPS 15 9530", "Laptop"),
    ("dell-xps-13.png", "Dell XPS 13 Plus", "Laptop"),
    ("dell-g15.png", "Dell G15 Gaming", "Laptop"),
    ("asus-rog-zephyrus.png", "ASUS ROG Zephyrus G14", "Laptop"),
    ("asus-zenbook.png", "ASUS ZenBook 14", "Laptop"),
    ("asus-vivobook.png", "ASUS VivoBook 15", "Laptop"),
    ("hp-spectre.png", "HP Spectre x360", "Laptop"),
    ("hp-pavilion.png", "HP Pavilion 15", "Laptop"),
    ("lenovo-thinkpad-x1.png", "Lenovo ThinkPad X1 Carbon", "Laptop"),
    ("lenovo-yoga.png", "Lenovo Yoga 9i", "Laptop"),
    ("msi-stealth.png", "MSI Stealth 16", "Laptop"),
    # Tablet
    ("ipad-pro-13.png", "iPad Pro 13 inch M4", "Tablet"),
    ("ipad-pro-11.png", "iPad Pro 11 inch M4", "Tablet"),
    ("ipad-air.png", "iPad Air 11 inch M2", "Tablet"),
    ("ipad-10.png", "iPad 10.9 inch", "Tablet"),
    ("ipad-mini.png", "iPad mini", "Tablet"),
    ("samsung-tab-s9-ultra.png", "Samsung Galaxy Tab S9 Ultra", "Tablet"),
    ("samsung-tab-s9.png", "Samsung Galaxy Tab S9", "Tablet"),
    ("samsung-tab-s9-fe.png", "Samsung Galaxy Tab S9 FE", "Tablet"),
    ("xiaomi-pad-6.png", "Xiaomi Pad 6", "Tablet"),
    # Phụ kiện
    ("airpods-pro-2.png", "AirPods Pro 2", "Phụ kiện"),
    ("airpods-3.png", "AirPods 3", "Phụ kiện"),
    ("airpods-2.png", "AirPods 2", "Phụ kiện"),
    ("airpods-max.png", "AirPods Max", "Phụ kiện"),
    ("apple-watch-ultra-2.png", "Apple Watch Ultra 2", "Phụ kiện"),
    ("apple-watch-series-9.png", "Apple Watch Series 9", "Phụ kiện"),
    ("apple-watch-se.png", "Apple Watch SE", "Phụ kiện"),
    ("samsung-watch-6.png", "Samsung Galaxy Watch 6", "Phụ kiện"),
    ("samsung-watch-6-classic.png", "Samsung Galaxy Watch 6 Classic", "Phụ kiện"),
    ("galaxy-buds-2-pro.png", "Samsung Galaxy Buds 2 Pro", "Phụ kiện"),
    ("galaxy-buds-fe.png", "Samsung Galaxy Buds FE", "Phụ kiện"),
    ("oppo-enco-x3.png", "OPPO Enco X3", "Phụ kiện"),
    ("oppo-watch.png", "OPPO Watch 4 Pro", "Phụ kiện"),
    ("sac-magsafe.png", "Sạc MagSafe Apple", "Phụ kiện"),
    ("sac-20w-apple.png", "Sạc Apple 20W USB-C", "Phụ kiện"),
    ("sac-samsung-45w.png", "Sạc Samsung 45W", "Phụ kiện"),
    ("op-lung-iphone-15-pro.png", "Ốp lưng iPhone 15 Pro", "Phụ kiện"),
    ("op-lung-iphone-15.png", "Ốp lưng iPhone 15", "Phụ kiện"),
    ("kinh-mac-mini.png", "Kính Mac mini", "Phụ kiện"),
    ("ban-phim-apple.png", "Bàn phím Apple Magic", "Phụ kiện"),
    ("chuot-apple.png", "Chuột Apple Magic Mouse", "Phụ kiện"),
    ("sac-du-phong.png", "Sạc dự phòng 20000mAh", "Phụ kiện"),
    ("cap-usbc.png", "Cáp USB-C Lightning", "Phụ kiện"),
    ("hub-usbc.png", "Hub USB-C 7 in 1", "Phụ kiện"),
    ("loa-jbl.png", "Loa JBL Flip 6", "Phụ kiện"),
    ("loa-sonos.png", "Loa Sonos Roam", "Phụ kiện"),
]

for filename, name, category in products:
    create_product_image(os.path.join(OUTPUT_DIR, filename), name, category)

print(f"\nTotal: {len(products)} images created in {OUTPUT_DIR}")
