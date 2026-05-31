"""
Fix all admin pages to match dashboard.html topbar structure exactly.
"""
import os, re

ADMIN_VIEWS = os.path.join(os.path.dirname(__file__), "Views", "Admin")
PAGES = [
    "products.html", "orders.html", "accounts.html", "categories.html",
    "suppliers.html", "faqs.html", "chatbot.html", "chats.html",
    "order_detail.html", "statistics.html", "product_edit.html"
]

# Fix: update product table images in products.html to use first_image_url
def fix_products_images(content):
    old_img = "{% set admin_imgs = product.product_images|selectattr('is_primary')|list %}"
    new_img = "{{ product.first_image_url }}"
    count = content.count(old_img)
    if count > 0:
        content = content.replace(old_img, "")
        content = content.replace(
            "{% if admin_imgs and admin_imgs[0].image_url %}\n              <img src=\"{{ admin_imgs[0].image_url }}\"",
            "<img src=\"{{ product.first_image_url }}\""
        )
        content = content.replace(
            "{% elif product.image_url %}\n              <img src=\"{{ product.image_url }}\"",
            ""
        )
        content = content.replace(
            "{% else %}\n              <div class=\"product-img d-flex align-items-center justify-content-center\"><i class=\"fas fa-image text-muted\"></i></div>\n            {% endif %}",
            ""
        )
        print(f"  Replaced {count}x in products.html")
    return content

for page in PAGES:
    path = os.path.join(ADMIN_VIEWS, page)
    if not os.path.exists(path):
        print(f"SKIP: {page} not found")
        continue

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    if page == "products.html":
        content = fix_products_images(content)

    # Add admin-logo CSS after first style rule
    css_add = ".admin-logo-text{line-height:1.2;}.admin-logo-badge{font-size:0.6rem;background:#ffd700;color:#0f172a;padding:1px 6px;border-radius:4px;font-weight:700;}"
    if ".admin-logo-badge" not in content:
        # Find first } in style and add after
        idx = content.find(">*{")
        if idx >= 0:
            end = content.find("}", idx)
            if end >= 0:
                content = content[:end+1] + "\n      " + css_add + content[end+1:]
                print(f"  Added CSS to {page}")

    # Replace topbar-right
    tr_pattern = r'(<div class="topbar-right">)([\s\S]*?)(<a href="/Auth/Logout"[^>]*>.*?</a>\s*</div>\s*</div>)'
    new_tr = r'''\1
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
      \3'''

    new_content = re.sub(tr_pattern, new_tr, content, count=1)
    if new_content != content:
        content = new_content
        print(f"  Replaced topbar-right in {page}")

    if content != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  WROTE: {page}")
    else:
        print(f"  NOCHG: {page}")

print("Done!")
