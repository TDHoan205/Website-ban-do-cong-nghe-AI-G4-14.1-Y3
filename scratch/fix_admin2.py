# -*- coding: utf-8 -*-
from pathlib import Path

p1 = Path(r"d:\a_LTPY\BTLPYTHON\Website-ban-do-cong-nghe-AI-G4-14.1-Y3\Views\Admin\chatbot.html")
c1 = p1.read_text(encoding='utf-8')
if "Khong the ket noi" in c1:
    c1 = c1.replace("Khong the ket noi", "Kh\u00F4ng th\u1EC3 k\u1EBFt n\u1ED1i")
    p1.write_text(c1, encoding='utf-8')
    print("OK chatbot")

p2 = Path(r"d:\a_LTPY\BTLPYTHON\Website-ban-do-cong-nghe-AI-G4-14.1-Y3\Views\Admin\suppliers.html")
c2 = p2.read_text(encoding='utf-8')
if "Chua co nha cung cap nao" in c2:
    c2 = c2.replace("Chua co nha cung cap nao", "Ch\u01B0a c\u00F3 nh\u00E0 cung c\u1EA5p n\u00E0o")
    p2.write_text(c2, encoding='utf-8')
    print("OK suppliers")
print("Done!")
