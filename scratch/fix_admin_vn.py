# -*- coding: utf-8 -*-
from pathlib import Path

def fix(path, old, new):
    c = path.read_text(encoding='utf-8')
    if old in c:
        c = c.replace(old, new)
        path.write_text(c, encoding='utf-8')
        print(f"Fixed {path.name}: '{old[:30]}' -> '{new[:30]}'")
    else:
        print(f"SKIP {path.name}: '{old[:30]}' not found")

# Fix Admin/chatbot.html - use Unicode escapes for safety
p1 = Path(r"d:\a_LTPY\BTLPYTHON\Website-ban-do-cong-nghe-AI-G4-14.1-Y3\Views\Admin\chatbot.html")
fix(p1,
    "Khong the ket noi chatbot",
    "Kh\u00F4ng th\u1EC3 k\u1EBFt n\u1ED1i chatbot")

# Fix Admin/suppliers.html
p2 = Path(r"d:\a_LTPY\BTLPYTHON\Website-ban-do-cong-nghe-AI-G4-14.1-Y3\Views\Admin\suppliers.html")
fix(p2,
    "Chua co nha cung cap nao",
    "Ch\u01B0a c\u00F3 nh\u00E0 cung c\u1EA5p n\u00E0o")

print("Done!")
