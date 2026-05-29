# -*- coding: utf-8 -*-
from pathlib import Path

def fix(path, pairs):
    c = path.read_text(encoding='utf-8')
    changed = False
    for old, new in pairs:
        if old in c:
            c = c.replace(old, new)
            changed = True
    if changed:
        path.write_text(c, encoding='utf-8')
        return True
    return False

p3 = Path(r"d:\a_LTPY\BTLPYTHON\Website-ban-do-cong-nghe-AI-G4-14.1-Y3\Views\Admin\orders.html")
fixes3 = [
    ("alert('L\u1ed7i: ' + d.error)", "alert('\u0110\u1ed5: ' + d.error)"),
    ("alert('L\u1ed7i k\u1ebft n\u1ed1i!')", "alert('\u0110\u1ed5 k\u1ebft n\u1ed1i!')"),
]
if fix(p3, fixes3):
    print("orders done")

p4 = Path(r"d:\a_LTPY\BTLPYTHON\Website-ban-do-cong-nghe-AI-G4-14.1-Y3\Views\Admin\order_detail.html")
fixes4 = [
    ("Khach vang lai", "Kh\u00e1ch v\u00e3ng lai"),
    ("alert('Loi: ' + data.error)", "alert('\u0110\u1ed5: ' + data.error)"),
    ("alert('Loi ket noi!')", "alert('\u0110\u1ed5 k\u1ebft n\u1ed1i!')"),
]
if fix(p4, fixes4):
    print("order_detail done")

print("Done!")
