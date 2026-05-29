# -*- coding: utf-8 -*-
from pathlib import Path

p = Path(r"d:\a_LTPY\BTLPYTHON\Website-ban-do-cong-nghe-AI-G4-14.1-Y3\Views\Admin\categories.html")
c = p.read_text(encoding='utf-8')
if "Mo ta danh muc san pham" in c:
    c = c.replace("Mo ta danh muc san pham", "M\u00f4 t\u1ea3 danh m\u1ee5c s\u1ea3n ph\u1ea9m")
    p.write_text(c, encoding='utf-8')
    print("Fixed categories.html")
print("Done!")
