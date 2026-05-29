# -*- coding: utf-8 -*-
from pathlib import Path

def fix_file(path, replacements):
    content = path.read_text(encoding='utf-8')
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            print(f"  OK: {old[:50]!r}")
        else:
            print(f"  SKIP: {old[:50]!r} (not found)")
    path.write_text(content, encoding='utf-8')
    print(f"  Written: {len(content)} chars")

base = Path(r"d:\a_LTPY\BTLPYTHON\Website-ban-do-cong-nghe-AI-G4-14.1-Y3\Views\Shared\base.html")
print("=== base.html ===")
fix_file(base, [
    ('<strong><i class="fas fa-truck"></i> Mien phi van chuyen</strong> toan quoc cho don tu 500.000d',
     '<strong><i class="fas fa-truck"></i> Mi\u1ec5n ph\u00ed v\u1eadn chuy\u1ec3n</strong> to\u00e0n qu\u1ed1c cho \u0111\u01a1n t\u1eeb 500.000\u0111'),
    ('<a href="/Products/"><i class="fas fa-bolt"></i> Khuyen mai hom nay</a>',
     '<a href="/Products/"><i class="fas fa-bolt"></i> Khuy\u1ebfn m\u00e3i h\u00f4m nay</a>'),
    ('<div class="header-logo-sub">Cong nghe thong minh</div>',
     '<div class="header-logo-sub">C\u00f4ng ngh\u1ec7 th\u00f4ng minh</div>'),
    ('placeholder="Tim kiem san pham..."',
     'placeholder="T\u00ecm ki\u1ebfm s\u1ea3n ph\u1ea9m..."'),
    ('<div class="header-act-label">Gio hang</div>',
     '<div class="header-act-label">Gi\u1ecf h\u00e0ng</div>'),
    ('<div class="header-act-label">Dang nhap</div>',
     '<div class="header-act-label">\u0110\u0103ng nh\u1eadp</div>'),
    ('<i class="fas fa-user"></i> Thong tin ca nhan</a>',
     '<i class="fas fa-user"></i> Th\u00f4ng tin c\u00e1 nh\u00e2n</a>'),
    ('<i class="fas fa-shopping-bag"></i> Don hang</a>',
     '<i class="fas fa-shopping-bag"></i> \u0110\u01a1n h\u00e0ng</a>'),
    ('<i class="fas fa-cog"></i> Quan ly Admin</a>',
     '<i class="fas fa-cog"></i> Qu\u1ea3n l\u00fd Admin</a>'),
    ('<i class="fas fa-sign-out-alt"></i> Dang xuat</a>',
     '<i class="fas fa-sign-out-alt"></i> \u0110\u0103ng xu\u1ea5t</a>'),
    ('<span>Danh muc</span>',
     '<span>Danh m\u1ee5c</span>'),
    ('<i class="fas fa-home"></i> Trang chu</a>',
     '<i class="fas fa-home"></i> Trang ch\u1ee7</a>'),
    ('<a href="/Products/">San pham</a>',
     '<a href="/Products/">S\u1ea3n ph\u1ea9m</a>'),
    ('<a href="/Cart/">Gio hang</a>',
     '<a href="/Cart/">Gi\u1ecf h\u00e0ng</a>'),
    ('<i class="fas fa-robot"></i> AI Tu van</a>',
     '<i class="fas fa-robot"></i> AI T\u01b0 v\u1ea5n</a>'),
    ('<i class="fas fa-bolt"></i> Moi nhat</a>',
     '<i class="fas fa-bolt"></i> M\u1edbi nh\u1ea5t</a>'),
    ('<i class="fas fa-fire"></i> Hot</a>',
     '<i class="fas fa-fire"></i> Hot</a>'),
    ('<i class="fas fa-headset"></i> Ho tro: 1800.6601</div>',
     '<i class="fas fa-headset"></i> H\u1ed7 tr\u1ee3: 1800.6601</div>'),
])

foot = Path(r"d:\a_LTPY\BTLPYTHON\Website-ban-do-cong-nghe-AI-G4-14.1-Y3\Views\partials\footer.html")
print("\n=== footer.html ===")
fix_file(foot, [
    ('Cua hang cong nghe hang dau Viet Nam voi tro ly AI thong minh',
     'C\u1eeda h\u00e0ng c\u00f4ng ngh\u1ec7 h\u00e0ng \u0111\u1ea7u Vi\u1ec7t Nam v\u1edbi tr\u1ee3 l\u00fd AI th\u00f4ng minh'),
    ('<h4 class="footer-col-title">Mua hang</h4>',
     '<h4 class="footer-col-title">Mua h\u00e0ng</h4>'),
    ('<h4 class="footer-col-title">Ho tro</h4>',
     '<h4 class="footer-col-title">H\u1ed7 tr\u1ee3</h4>'),
    ('<h4 class="footer-col-title">Lien he</h4>',
     '<h4 class="footer-col-title">Li\u00ean h\u1ec7</h4>'),
    ('<i class="fas fa-chevron-right"></i> San pham</a>',
     '<i class="fas fa-chevron-right"></i> S\u1ea3n ph\u1ea9m</a>'),
    ('<i class="fas fa-chevron-right"></i> San pham moi',
     '<i class="fas fa-chevron-right"></i> S\u1ea3n ph\u1ea9m m\u1edbi'),
    ('<i class="fas fa-chevron-right"></i> San pham hot',
     '<i class="fas fa-chevron-right"></i> S\u1ea3n ph\u1ea9m hot'),
    ('<i class="fas fa-chevron-right"></i> Dien thoai',
     '<i class="fas fa-chevron-right"></i> \u0110i\u1ec7n tho\u1ea1i'),
    ('<i class="fas fa-chevron-right"></i> Laptop</a>',
     '<i class="fas fa-chevron-right"></i> Laptop</a>'),
    ('<i class="fas fa-chevron-right"></i> Huong dan mua hang',
     '<i class="fas fa-chevron-right"></i> H\u01b0\u1edbng d\u1eabn mua h\u00e0ng'),
    ('<i class="fas fa-chevron-right"></i> Chinh sach doi tra',
     '<i class="fas fa-chevron-right"></i> Ch\u00ednh s\u00e1ch \u0111\u1ed5i tr\u1ea3'),
    ('<i class="fas fa-chevron-right"></i> Chinh sach bao hanh',
     '<i class="fas fa-chevron-right"></i> Ch\u00ednh s\u00e1ch b\u1ea3o h\u00e0nh'),
    ('<i class="fas fa-chevron-right"></i> Tro ly AI',
     '<i class="fas fa-chevron-right"></i> Tr\u1ee3 l\u00fd AI'),
    ('<i class="fas fa-chevron-right"></i> Lien he</a>',
     '<i class="fas fa-chevron-right"></i> Li\u00ean h\u1ec7</a>'),
    ('Ha Noi, Viet Nam', 'H\u00e0 N\u1ed9i, Vi\u1ec7t Nam'),
    ('Thu 2 - CN: 8:00 - 22:00', 'Th\u1ee9 2 - CN: 8:00 - 22:00'),
    ('Tat ca quyen duoc bao luu.', 'T\u1ea5t c\u1ea3 quy\u1ec1n \u0111\u01b0\u1ee3c b\u1ea3o l\u01b0u.'),
])

chat = Path(r"d:\a_LTPY\BTLPYTHON\Website-ban-do-cong-nghe-AI-G4-14.1-Y3\Views\partials\chatbot.html")
print("\n=== chatbot.html ===")
fix_file(chat, [
    ('<h6>Tro ly AI Tech Store</h6>',
     '<h6>Tr\u1ee3 l\u00fd AI Tech Store</h6>'),
    ('San sang ho tro', 'S\u1eb5n s\u00e0ng h\u1ed7 tr\u1ee3'),
    ('Xin chao! Toi la', 'Xin ch\u00e0o! T\u00f4i l\u00e0'),
    ('Tro ly AI</strong> cua Tech Store', 'Tr\u1ee3 l\u00fd AI</strong> c\u1ee7a Tech Store'),
    ('Toi co the giup ban', 'T\u00f4i c\u00f3 th\u1ec3 gi\u00fap b\u1ea1n'),
    ('Tim va tu van san pham cong nghe', 'T\u00ecm v\u00e0 t\u01b0 v\u1ea5n s\u1ea3n ph\u1ea9m c\u00f4ng ngh\u1ec7'),
    ('So sanh gia', 'So s\u00e1nh gi\u00e1'),
    ('thong so ky thuat', 'th\u00f4ng s\u1ed1 k\u1ef9 thu\u1eadt'),
    ('Tra cuu don hang', 'Tra c\u1ee9u \u0111\u01a1n h\u00e0ng'),
    ('khuyen mai', 'khuy\u1ebfn m\u00e3i'),
    ('Ban can ho tro gi', 'B\u1ea1n c\u1ea7n h\u1ed7 tr\u1ee3 g\u00ec'),
    ("cbSend('San pham noi bat?')", "cbSend('\u1ea2n ph\u1ea9m n\u1ed5i b\u1eadt?')"),
    ("cbSend('Co khuyen mai gi?')", "cbSend('C\u00f3 khuy\u1ebfn m\u00e3i g\u00ec?')"),
    ("cbSend('Tu van laptop')", "cbSend('T\u01b0 v\u1ea5n laptop')"),
    ('placeholder="Nhap tin nhan..."', 'placeholder="Nh\u1eadp tin nh\u1eafn..."'),
])

print("\nAll done!")
