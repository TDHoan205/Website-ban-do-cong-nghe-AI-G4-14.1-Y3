"""
Fix Vietnamese accents in admin pages topbar-right.
"""
import os, re

BASE = r"d:\Website-ban-do-cong-nghe-AI-G4-14.1-Y3"
ADMIN = os.path.join(BASE, "Views", "Admin")

PAGES = [
    "products.html", "orders.html", "accounts.html", "categories.html",
    "suppliers.html", "faqs.html", "chatbot.html", "chats.html",
    "order_detail.html", "statistics.html", "product_edit.html"
]

# Replace non-accented text with proper Vietnamese
REPLACEMENTS = [
    ("Xem website", "Xem website"),
    ("Quan tri vien", "Quản trị viên"),
    ("Tai khoan cua toi", "Tài khoản của tôi"),
    ("Dang xuat", "Đăng xuất"),
]

for page in PAGES:
    fpath = os.path.join(ADMIN, page)
    if not os.path.exists(fpath):
        continue
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    original = content

    for old, new in REPLACEMENTS:
        if old != new and old in content:
            content = content.replace(old, new)
            print(f"[{page}] '{old}' -> '{new}'")

    if content != original:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[{page}] WROTE")

print("Done!")
