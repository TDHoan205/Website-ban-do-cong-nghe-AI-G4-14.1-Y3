# -*- coding: utf-8 -*-
from pathlib import Path
import re

files = [
    Path(r"d:\a_LTPY\BTLPYTHON\Website-ban-do-cong-nghe-AI-G4-14.1-Y3\Views\Admin\categories.html"),
    Path(r"d:\a_LTPY\BTLPYTHON\Website-ban-do-cong-nghe-AI-G4-14.1-Y3\Views\Admin\accounts.html"),
    Path(r"d:\a_LTPY\BTLPYTHON\Website-ban-do-cong-nghe-AI-G4-14.1-Y3\Views\Admin\product_edit.html"),
    Path(r"d:\a_LTPY\BTLPYTHON\Website-ban-do-cong-nghe-AI-G4-14.1-Y3\Views\Admin\products.html"),
    Path(r"d:\a_LTPY\BTLPYTHON\Website-ban-do-cong-nghe-AI-G4-14.1-Y3\Views\Admin\order_detail.html"),
    Path(r"d:\a_LTPY\BTLPYTHON\Website-ban-do-cong-nghe-AI-G4-14.1-Y3\Views\Admin\suppliers.html"),
    Path(r"d:\a_LTPY\BTLPYTHON\Website-ban-do-cong-nghe-AI-G4-14.1-Y3\Views\Admin\faqs.html"),
]

bad_count = 0
for p in files:
    c = p.read_text(encoding='utf-8')
    for m in re.finditer(r"alert\('([^']+)'\)", c):
        text = m.group(1)
        has_vn = any(ord(ch) > 127 for ch in text)
        if not has_vn and len(text) > 2:
            print(f"BAD: {p.name} -> {text}")
            bad_count += 1
    for m2 in re.finditer(r'addMsg\("([^"]+)"', c):
        text = m2.group(1)
        has_vn = any(ord(ch) > 127 for ch in text)
        if not has_vn and len(text) > 2:
            print(f"BAD addMsg: {p.name} -> {text}")
            bad_count += 1

if bad_count == 0:
    print("All alert/addMsg strings have proper Vietnamese!")
