"""
Fix all admin pages: replace topbar-right with exact dashboard version.
"""
import os, re

BASE = r"d:\Website-ban-do-cong-nghe-AI-G4-14.1-Y3"
ADMIN = os.path.join(BASE, "Views", "Admin")

PAGES = [
    "products.html", "orders.html", "accounts.html", "categories.html",
    "suppliers.html", "faqs.html", "chatbot.html", "chats.html",
    "order_detail.html", "statistics.html", "product_edit.html"
]

DASHBOARD_RIGHT = """      <div class="topbar-right">
        <a href="/" target="_blank" class="topbar-btn btn-gold">
          <i class="fas fa-external-link-alt"></i> Xem website
        </a>
        <div class="topbar-user">
          <div class="user-avatar"><i class="fas fa-user-shield"></i></div>
          <div class="user-info">
            <div class="user-name">{{ admin.username }}</div>
            <div class="user-role">Quan tri vien</div>
          </div>
        </div>
        <a href="/Auth/Profile" class="topbar-btn btn-gold" title="Tai khoan cua toi">
          <i class="fas fa-user-circle"></i> Tai khoan cua toi
        </a>
        <a href="/Auth/Logout" class="topbar-btn btn-red">
          <i class="fas fa-sign-out-alt"></i> Dang xuat
        </a>
      </div>
    </div>"""

NEW_CSS = ".admin-logo-text{line-height:1.2;}\n      .admin-logo-badge{font-size:0.6rem;background:#ffd700;color:#0f172a;padding:1px 6px;border-radius:4px;font-weight:700;}"

for page in PAGES:
    fpath = os.path.join(ADMIN, page)
    if not os.path.exists(fpath):
        print(f"SKIP: {page} not found at {fpath}")
        continue
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    original = content

    # 1. Add CSS if not present
    if ".admin-logo-badge" not in content:
        m = re.search(r'<style>([^<]*{[^}]*})', content)
        if m:
            old_css = m.group(1)
            new_css = old_css + "\n      " + NEW_CSS
            content = content.replace(old_css, new_css, 1)
            print(f"[{page}] CSS added")
        else:
            print(f"[{page}] could not find style rule")

    # 2. Replace topbar-right block - find the whole topbar-right from open to closing </div> of topbar
    # Pattern: <div class="topbar-right"> ... until <a href="/Auth/Logout" ... </a> </div> </div>
    tr_pat = r'<div class="topbar-right">[\s\S]*?<a href="/Auth/Logout"[^>]*>[\s\S]*?</a>\s*</div>\s*</div>'
    m = re.search(tr_pat, content)
    if m:
        old_right = m.group(0)
        content = content.replace(old_right, DASHBOARD_RIGHT, 1)
        print(f"[{page}] topbar-right replaced")
    else:
        print(f"[{page}] topbar-right pattern not found")

    if content != original:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[{page}] WROTE")
    else:
        print(f"[{page}] no change")

print("Done!")
