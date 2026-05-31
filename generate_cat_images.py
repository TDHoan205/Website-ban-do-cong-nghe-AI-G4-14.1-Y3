"""Generate category placeholder images"""
from PIL import Image, ImageDraw, ImageFont
import os

OUTPUT_DIR = r"d:\Website-ban-do-cong-nghe-AI-G4-14.1-Y3\wwwroot\images"

def create_cat_image(filename, color1, color2, icon_char, width=400, height=300):
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    for y in range(height):
        ratio = y / height
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Draw rounded rect
    draw.rounded_rectangle([15, 15, width-15, height-15], radius=20, outline=(255,255,255,100), width=2)
    
    # Phone icon shape
    cx, cy = width//2, height//2
    draw.rounded_rectangle([cx-25, cy-40, cx+25, cy+40], radius=8, fill=(255,255,255,200))
    draw.ellipse([cx-4, cy+28, cx+4, cy+36], fill=(255,255,255,200))
    
    img.save(filename, "PNG")
    print(f"Created: {filename}")

# Categories
cats = [
    ("cat_phone.png", (66, 133, 244), (103, 58, 183)),
    ("cat_laptop.png", (52, 168, 83), (30, 100, 200)),
    ("cat_tablet.png", (234, 67, 53), (255, 112, 67)),
    ("cat_accessories.png", (255, 150, 50), (200, 100, 200)),
]

for fname, c1, c2 in cats:
    create_cat_image(os.path.join(OUTPUT_DIR, fname), c1, c2, "📱")

print("Done!")
