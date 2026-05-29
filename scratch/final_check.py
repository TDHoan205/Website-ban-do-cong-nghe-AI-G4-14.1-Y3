# -*- coding: utf-8 -*-
"""Final comprehensive scan for ASCII-only Vietnamese text in all HTML templates."""
from pathlib import Path
import re

vn_phrase_re = re.compile(
    r'>'                                          # opening tag boundary
    r'('
    r'Cong nghe thong minh|Cong nghe thong minh hon|'
    r'Mien phi van chuyen|Mien phi van chuyen toan quoc|'
    r'San pham noi bat|San pham moi|San pham hot|San pham|giam gia|khuyen mai hom nay|'
    r'Gio hang|Gio hangg|Dang nhap|Dang ky|Dang xuat|'
    r'Trang chu|Trang chu|Trang chu|'
    r'Ho tro|Ho tro|Khuyen mai|Khuyen mai hom|'
    r'Chinh hang 100|Chinh hang|'
    r'Giao hang nhanh|Giao hang|'
    r'Doi tra 7 ngay|Doi tra|'
    r'Trai nghiem|Trai nghiem|'
    r'Mua sam ngay|Mua sam|'
    r'Xem san pham|Xem san|'
    r'Tu van|Tu van|'
    r'Tro ly|Tro ly AI|'
    r'Lien he|Lien he|'
    r'Quan ly|Quan ly Admin|'
    r'Thong tin ca nhan|Thong tin ca nhan|'
    r'Don hang|Don hang|'
    r'Ho tro 24|ho tro 24|'
    r'Moi nhat|Moi nhat|'
    r'Toan quoc|toan quoc|'
    r'Tat ca|Tat ca|'
    r'Chua co|Chua co|'
    r'Khong tim thay|Khong tim thay|'
    r'Khong co|Khong co|'
    r'Khong san|Khong san|'
    r'Tong cong|Tong cong|'
    r'Don gia|Don gia|'
    r'So luong|So luong|'
    r'Thanh tien|Thanh tien|'
    r'Ghi chu|Ghi chu|'
    r'Da xoa|Da xoa|'
    r'Da luu|Da luu|'
    r'Da cap nhat|Da cap nhat|'
    r'Dang xu ly|Dang xu ly|'
    r'Da nhan|Da nhan|'
    r'Dang giao|Dang giao|'
    r'Da giao|Da giao|'
    r'Da huy|Da huy|'
    r'Khach vang lai|Khach vang lai|'
    r'Loi ket noi|Loi ket noi|'
    r'Loi|Loi|Loi:'
    r')'
    r'<', re.IGNORECASE
)

# Check all HTML files in Views
views_dir = Path(r"d:\a_LTPY\BTLPYTHON\Website-ban-do-cong-nghe-AI-G4-14.1-Y3\Views")
html_files = list(views_dir.rglob("*.html"))

issues = []
for f in html_files:
    c = f.read_text(encoding='utf-8')
    for m in vn_phrase_re.finditer(c):
        text = m.group()
        # Filter out false positives: inside href/src/url attributes
        # Get surrounding context
        start = max(0, m.start() - 30)
        end = min(len(c), m.end() + 30)
        context = c[start:end]
        # Skip if inside href, src, action, url attributes
        skip = False
        for attr in ['href=', 'src=', 'action=', 'url(', 'placeholder=']:
            # Find the last occurrence of attr before this match
            last_attr = c.rfind(attr, start, m.start())
            if last_attr >= 0:
                between = c[last_attr:m.start()]
                if '"' not in between and "'" not in between:
                    skip = True
                    break
        if not skip:
            issues.append((f.name, text))

if issues:
    print(f"Found {len(issues)} potential issues:")
    for fn, text in issues[:20]:
        print(f"  {fn}: {text}")
else:
    print("No ASCII-only Vietnamese text found in visible content!")
    print(f"Scanned {len(html_files)} files.")
