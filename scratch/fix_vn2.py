# -*- coding: utf-8 -*-
"""Fix all Vietnamese text in HTML template files using Python file I/O."""
from pathlib import Path
import re

def do_fixes(path, fixes):
    raw = path.read_bytes()
    text = raw.decode('utf-8')
    original = text
    for pattern, replacement in fixes:
        if pattern in text:
            text = text.replace(pattern, replacement)
            print(f"  FIXED: {pattern[:60]!r}")
        else:
            print(f"  SKIP:  {pattern[:60]!r}")
    if text != original:
        path.write_text(text, encoding='utf-8')
        print(f"  Written: {len(text)} chars")
    else:
        print("  Nothing changed")

def r(s):
    """Raw string helper."""
    return s

# ============================================================
# FOOTER.HTML
# ============================================================
footer = Path(r"d:\a_LTPY\BTLPYTHON\Website-ban-do-cong-nghe-AI-G4-14.1-Y3\Views\partials\footer.html")
print("=== footer.html ===")
do_fixes(footer, [
    # Desc
    ("Cua hang cong nghe hang dau Viet Nam voi tro ly AI thong minh, giup ban tim kiem va chon lua san pham phu hop nhat.",
     "C\u1eeda h\u00e0ng c\u00f4ng ngh\u1ec7 h\u00e0ng \u0111\u1ea7u Vi\u1ec7t Nam v\u1edbi tr\u1ee3 l\u00fd AI th\u00f4ng minh, gi\u00fap b\u1ea1n t\u00ecm ki\u1ebfm v\u00e0 ch\u1ecdn l\u1ef1a s\u1ea3n ph\u1ea9m ph\u00f9 h\u1ee3p nh\u1ea5t."),
    # Col titles
    (">Mua hang<", ">Mua h\u00e0ng<"),
    (">Ho tro<", ">H\u1ed7 tr\u1ee3<"),
    (">Lien he<", ">Li\u00ean h\u1ec7<"),
    # Links - san pham variants
    (">San pham<", ">S\u1ea3n ph\u1ea9m<"),
    (">San pham moi<", ">S\u1ea3n ph\u1ea9m m\u1edbi<"),
    (">San pham hot<", ">S\u1ea3n ph\u1ea9m hot<"),
    (">Dien thoai<", ">\u0110i\u1ec7n tho\u1ea1i<"),
    (">Huong dan mua hang<", ">H\u01b0\u1edbng d\u1eabn mua h\u00e0ng<"),
    (">Chinh sach doi tra<", ">Ch\u00ednh s\u00e1ch \u0111\u1ed5i tr\u1ea3<"),
    (">Chinh sach bao hanh<", ">Ch\u00ednh s\u00e1ch b\u1ea3o h\u00e0nh<"),
    (">Tro ly AI<", ">Tr\u1ee3 l\u00fd AI<"),
    (">Lien he<", ">Li\u00ean h\u1ec7<"),
    # Contact
    (">Ha Noi, Viet Nam<", ">H\u00e0 N\u1ed9i, Vi\u1ec7t Nam<"),
    (">Thu 2 - CN: 8:00 - 22:00<", ">Th\u1ee9 2 - CN: 8:00 - 22:00<"),
    # Copyright
    ("Tat ca quyen duoc bao luu.", "T\u1ea5t c\u1ea3 quy\u1ec1n \u0111\u01b0\u1ee3c b\u1ea3o l\u01b0u."),
])

# ============================================================
# BASE.HTML
# ============================================================
base = Path(r"d:\a_LTPY\BTLPYTHON\Website-ban-do-cong-nghe-AI-G4-14.1-Y3\Views\Shared\base.html")
print("\n=== base.html ===")
do_fixes(base, [
    # Ann bar
    (">Mien phi van chuyen<", ">Mi\u1ec5n ph\u00ed v\u1eadn chuy\u1ec3n<"),
    ("toan quoc cho don tu 500.000d", "to\u00e0n qu\u1ed1c cho \u0111\u01a1n t\u1eeb 500.000\u0111"),
    (">Khuyen mai hom nay<", ">Khuy\u1ebfn m\u00e3i h\u00f4m nay<"),
    # Logo
    (">Cong nghe thong minh<", ">C\u00f4ng ngh\u1ec7 th\u00f4ng minh<"),
    # Search
    ("Tim kiem san pham", "T\u00ecm ki\u1ebfm s\u1ea3n ph\u1ea9m"),
    # Header actions
    (">Gio hang<", ">Gi\u1ecf h\u00e0ng<"),
    (">Dang nhap<", ">\u0110\u0103ng nh\u1eadp<"),
    # User dropdown
    (">Thong tin ca nhan<", ">Th\u00f4ng tin c\u00e1 nh\u00e2n<"),
    (">Don hang<", ">\u0110\u01a1n h\u00e0ng<"),
    (">Quan ly Admin<", ">Qu\u1ea3n l\u00fd Admin<"),
    (">Dang xuat<", ">\u0110\u0103ng xu\u1ea5t<"),
    # Navbar
    (">Danh muc<", ">Danh m\u1ee5c<"),
    (">Trang chu<", ">Trang ch\u1ee7<"),
    (">San pham<", ">S\u1ea3n ph\u1ea9m<"),
    (">AI Tu van<", ">AI T\u01b0 v\u1ea5n<"),
    (">Moi nhat<", ">M\u1edbi nh\u1ea5t<"),
    (">Ho tro:", ">H\u1ed7 tr\u1ee3:"),
])

# ============================================================
# CHATBOT.HTML
# ============================================================
chatbot = Path(r"d:\a_LTPY\BTLPYTHON\Website-ban-do-cong-nghe-AI-G4-14.1-Y3\Views\partials\chatbot.html")
print("\n=== chatbot.html ===")
do_fixes(chatbot, [
    (">Tro ly AI Tech Store<", ">Tr\u1ee3 l\u00fd AI Tech Store<"),
    (">San sang ho tro<", ">S\u1eb5n s\u00e0ng h\u1ed7 tr\u1ee3<"),
    (">Xin chao!<", ">Xin ch\u00e0o!<"),
    (">Toi la <", ">T\u00f4i l\u00e0 <"),
    (">cua Tech Store<", ">c\u1ee7a Tech Store<"),
    (">Toi co the giup ban:<", ">T\u00f4i c\u00f3 th\u1ec3 gi\u00fap b\u1ea1n:<"),
    (">Tim va tu van san pham cong nghe<", ">T\u00ecm v\u00e0 t\u01b0 v\u1ea5n s\u1ea3n ph\u1ea9m c\u00f4ng ngh\u1ec7<"),
    (">So sanh gia<", ">So s\u00e1nh gi\u00e1<"),
    (">thong so ky thuat<", ">th\u00f4ng s\u1ed1 k\u1ef9 thu\u1eadt<"),
    (">Tra cuu don hang<", ">Tra c\u1ee9u \u0111\u01a1n h\u00e0ng<"),
    (">khuyen mai<", ">khuy\u1ebfn m\u00e3i<"),
    (">Ban can ho tro gi?<", ">B\u1ea1n c\u1ea7n h\u1ed7 tr\u1ee3 g\u00ec?<"),
    (">San pham noi bat?<", ">S\u1ea3n ph\u1ea9m n\u1ed5i b\u1eadt?<"),
    (">Co khuyen mai gi?<", ">C\u00f3 khuy\u1ebfn m\u00e3i g\u00ec?<"),
    (">Tu van laptop<", ">T\u01b0 v\u1ea5n laptop<"),
    ('placeholder="Nhap tin nhan..."', 'placeholder="Nh\u1eadp tin nh\u1eafn..."'),
    # JS button labels
    ("'San pham noi bat?'", "'\u1ea2n ph\u1ea9m n\u1ed5i b\u1eadt?'"),
    ("'Co khuyen mai gi?'", "'\u00d3 khuy\u1ebfn m\u00e3i g\u00ec?'"),
    ("'Tu van laptop'", "'\u1ee8 v\u1ea5n laptop'"),
    # Loading
    (">Dang tai...<", ">Đang tải...<"),
])

print("\nDone!")
