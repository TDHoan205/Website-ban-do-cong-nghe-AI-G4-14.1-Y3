# -*- coding: utf-8 -*-
from pathlib import Path

def fix(path, pairs):
    c = path.read_text(encoding='utf-8')
    for old, new in pairs:
        if old in c:
            c = c.replace(old, new)
            print("Fixed: " + old[:40])
        else:
            print("SKIP: " + old[:40])
    path.write_text(c, encoding='utf-8')

# Admin/chatbot.html
p1 = Path(r"d:\a_LTPY\BTLPYTHON\Website-ban-do-cong-nghe-AI-G4-14.1-Y3\Views\Admin\chatbot.html")
fix(p1, [
    ("'He thong dang ban, vui long thu lai.'", "'\u0110ang b\u1eadn, vui l\u00f2ng th\u1eed l\u1ea1i.'"),
])

# Admin/suppliers.html
p2 = Path(r"d:\a_LTPY\BTLPYTHON\Website-ban-do-cong-nghe-AI-G4-14.1-Y3\Views\Admin\suppliers.html")
fix(p2, [
    ('placeholder="VD: Cong ty ABC"', "placeholder=\"\u0110ang t\u1ea3i...\""),
    ("alert('Loi: ' + data.error)", "alert('\u0110\u1ed3: ' + data.error)"),
    ("alert('Loi ket noi!')", "alert('\u0110\u1ed5 k\u1ebft n\u1ed1i!')"),
])

# Admin/orders.html
p3 = Path(r"d:\a_LTPY\BTLPYTHON\Website-ban-do-cong-nghe-AI-G4-14.1-Y3\Views\Admin\orders.html")
fix(p3, [
    ("alert('L\u1ed7i: ' + d.error)", "alert('\u0110\u1ed5: ' + d.error)"),
    ("alert('L\u1ed7i k\u1ebft n\u1ed1i!')", "alert('\u0110\u1ed5 k\u1ebft n\u1ed1i!')"),
])

# Admin/order_detail.html
p4 = Path(r"d:\a_LTPY\BTLPYTHON\Website-ban-do-cong-nghe-AI-G4-14.1-Y3\Views\Admin\order_detail.html")
fix(p4, [
    ("Khach vang lai", "Kh\u00e1ch v\u00e3ng lai"),
    ("alert('Loi: ' + data.error)", "alert('\u0110\u1ed5: ' + data.error)"),
    ("alert('Loi ket noi!')", "alert('\u0110\u1ed5 k\u1ebft n\u1ed1i!')"),
])

print("All done!")
