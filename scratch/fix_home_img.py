import re

for filepath, new_pattern in [
    ("Views/Home/index.html", 'src="{{ product.first_image_url }}"'),
    ("Views/Products/index.html", None),  # already uses first_image_url
]:
    pass

# Fix Home/index.html - replace the two img src blocks
with open("Views/Home/index.html", "r", encoding="utf-8") as f:
    content = f.read()

old_pattern = r"src=\"\{% set imgs = product\.product_images\|selectattr\('is_primary'\)\|list %\}.*?product\.product_images %\}%}\s*\{% else %\}/static/images/no-image\.png\{% endif %\}\""
new_src = 'src="{{ product.first_image_url }}"'

count = 0
content_new, n = re.subn(old_pattern, new_src, content, flags=re.DOTALL)
if n > 0:
    print(f"Home/index.html: replaced {n} occurrence(s)")
    count += n
else:
    print("Home/index.html: pattern NOT found, trying alternative...")

# Alternative: simple string replace
alt_old = 'src="{% set imgs = product.product_images|selectattr(\'is_primary\')|list %}\n                        {% if imgs and imgs[0].image_url %}{{ imgs[0].image_url }}{% elif product.image_url %}{{ product.image_url }}{% elif product.product_images %}{{ product.product_images[0].image_url }}{% else %}/static/images/no-image.png{% endif %}"'
if alt_old in content_new:
    content_new = content_new.replace(alt_old, 'src="{{ product.first_image_url }}"')
    print("Home/index.html: replaced using alternative string")

with open("Views/Home/index.html", "w", encoding="utf-8") as f:
    f.write(content_new)

print("Done")
