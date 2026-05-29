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
    (">Don gia<", ">\u0110\u01a1n gi\u00e1<"),
    (">So luong<", ">\u0110\u1ed9 l\u01b0\u1ee3ng<"),
    (">Thanh tien<", ">\u0110\u1ec3nh ti\u1ec1n<"),
])

p2 = Path(r"d:\a_LTPY\BTLPYTHON\Website-ban-do-cong-nghe-AI-G4-14.1-Y3\Views\Admin\suppliers.html")
fix(p2, [
    (">Dia chi<", ">\u0110\u1ecb ch\u1ec9<"),
])

print("Done!")
