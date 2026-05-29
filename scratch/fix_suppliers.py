# -*- coding: utf-8 -*-
from pathlib import Path

def fix(path, pairs):
    c = path.read_text(encoding='utf-8')
    for old, new in pairs:
        if old in c:
            c = c.replace(old, new)
            print("Fixed: " + old)
    path.write_text(c, encoding='utf-8')

# Fix Admin/suppliers.html
p = Path(r"d:\a_LTPY\BTLPYTHON\Website-ban-do-cong-nghe-AI-G4-14.1-Y3\Views\Admin\suppliers.html")
fix(p, [
    (">So dien thoai<", ">\u0110i\u1ec7n tho\u1ea1i<"),
    (">Nguoi lien he<", ">Ng\u01b0\u1eddi li\u00ean h\u1ec7<"),
    ("placeholder=\"Dia chi day du\"", "placeholder=\"\u0110\u1ecb ch\u1ec9 \u0111\u1ea7y \u0111\u1ee7\""),
])

print("Done!")
