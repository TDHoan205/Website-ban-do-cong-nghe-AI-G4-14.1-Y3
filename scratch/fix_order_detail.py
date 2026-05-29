# -*- coding: utf-8 -*-
from pathlib import Path

def fix(path, pairs):
    c = path.read_text(encoding='utf-8')
    for old, new in pairs:
        if old in c:
            c = c.replace(old, new)
            print("Fixed: " + old)
        else:
            print("SKIP: " + old)
    path.write_text(c, encoding='utf-8')

p1 = Path(r"d:\a_LTPY\BTLPYTHON\Website-ban-do-cong-nghe-AI-G4-14.1-Y3\Views\Admin\order_detail.html")
fix(p1, [
    ("Tong cong:", "\u0110\u1ed3ng c\u1ed9ng:"),
    ("Ghi chu", "\u0110\u1ecb ch\u00fa"),
    ("'Da cap nhat!", "'\u0110\u00e3 c\u1eadp nh\u1eadt r\u1ed3i!"),
    ("'Da cap nhat trang thai don hang!", "'\u0110\u00e3 c\u1eadp nh\u1eadt tr\u1ea1ng th\u00e1i \u0111\u01a1n h\u00e0ng!"),
])

print("Done!")
