# -*- coding: utf-8 -*-
from pathlib import Path

p = Path(r"d:\a_LTPY\BTLPYTHON\Website-ban-do-cong-nghe-AI-G4-14.1-Y3\Views\Admin\chatbot.html")
c = p.read_text(encoding='utf-8')
if "Da nhan duoc tin nhan" in c:
    c = c.replace("Da nhan duoc tin nhan", "\u0110\u00e3 nh\u1eadn \u0111\u01b0\u1ee3c tin nh\u1eafn")
    p.write_text(c, encoding='utf-8')
    print("Fixed chatbot.html")
print("Done!")
