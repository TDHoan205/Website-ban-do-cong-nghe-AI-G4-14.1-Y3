"""
Convert standalone HTML templates to extend Shared/base.html.
Run: python scratch/convert_to_extends.py
"""
import re
import os
from pathlib import Path

VIEWS_DIR = Path(__file__).parent.parent / "Views"


def convert_to_extends(filepath: Path) -> bool:
    """Convert a standalone HTML template to extend base.html."""
    content = filepath.read_text(encoding="utf-8")

    # Skip if already extends
    if "{% extends" in content or '{%extends' in content:
        return False

    # Skip base.html itself
    if filepath.name == "base.html":
        return False

    # Must have doctype to be standalone
    if "<!doctype html>" not in content.lower():
        return False

    # Extract page-specific <style> blocks
    style_blocks = re.findall(r'<style[^>]*>(.*?)</style>', content, re.DOTALL)

    # Extract body content (everything between <body> and </body>)
    body_match = re.search(r'<body[^>]*>(.*)</body>', content, re.DOTALL)
    if not body_match:
        return False
    body_content = body_match.group(1).strip()

    # Remove page-specific style blocks from body content
    for style_tag in re.finditer(r'<style[^>]*>.*?</style>', body_content, re.DOTALL):
        body_content = body_content.replace(style_tag.group(0), "")

    # Remove duplicate navbar/footer from body (base.html provides them)
    # Remove nav bars that look like the main site nav
    nav_patterns = [
        r'<nav[^>]*class="[^"]*navbar[^"]*"[^>]*>.*?</nav>',
        r'<div class="top-bar[^"]*"[^>]*>.*?</div>\s*<header[^>]*>.*?</header>\s*<nav[^>]*class="[^"]*nav-bar[^"]*"[^>]*>.*?</nav>',
    ]
    for pattern in nav_patterns:
        body_content = re.sub(pattern, "", body_content, flags=re.DOTALL | re.IGNORECASE)

    # Remove footer that looks like the main site footer
    footer_patterns = [
        r'<footer[^>]*class="[^"]*main-footer[^"]*"[^>]*>.*?</footer>',
        r'<footer[^>]*class="[^"]*bg-dark[^"]*"[^>]*>.*?</footer>',
    ]
    for pattern in footer_patterns:
        body_content = re.sub(pattern, "", body_content, flags=re.DOTALL | re.IGNORECASE)

    # Remove duplicate global scripts (base.html provides them)
    scripts_to_remove = [
        r'<script[^>]*src=["\']https://cdn\.jsdelivr\.net/npm/bootstrap@5\.3\.2/dist/js/bootstrap\.bundle\.min\.js["\'][^>]*></script>',
        r'<script[^>]*src=["\']/static/js/main\.js[^"\']*["\'][^>]*></script>',
        r'<script[^>]*src=["\']https://cdn\.jsdelivr\.net/npm/bootstrap@5\.3\.2/dist/js/bootstrap\.bundle\.min\.js["\'][^>]*>\s*</script>',
    ]
    for pattern in scripts_to_remove:
        body_content = re.sub(pattern, "", body_content, flags=re.DOTALL)

    # Remove toast container (base.html provides it)
    body_content = re.sub(r'<div id=["\']toast-container["\'][^>]*>.*?</div>', "", body_content, flags=re.DOTALL)

    # Remove duplicate chatbot (base.html provides it via include)
    body_content = re.sub(
        r'<!--\s*CHATBOX[\s\S]*?<!--\s*END CHATBOX[\s\S]*?-->',
        "",
        body_content,
        flags=re.IGNORECASE,
    )
    # Also remove standalone chatbot HTML elements
    body_content = re.sub(
        r'<button[^>]*class=["\']chatbox-toggle["\'][^>]*>.*?</button>',
        "",
        body_content,
        flags=re.DOTALL,
    )
    body_content = re.sub(
        r'<div[^>]*class=["\']chatbox-popup["\'][^>]*>.*?</div>',
        "",
        body_content,
        flags=re.DOTALL,
    )

    body_content = body_content.strip()

    # Build new file content
    new_lines = ["{% extends \"Shared/base.html\" %}", ""]

    if style_blocks:
        new_lines.append("{% block extra_head %}")
        for style in style_blocks:
            style_clean = style.strip()
            if style_clean:
                new_lines.append(f"<style>{style_clean}</style>")
        new_lines.append("{% endblock %}")
        new_lines.append("")

    new_lines.append("{% block content %}")
    new_lines.append("")
    new_lines.append(body_content)
    new_lines.append("")
    new_lines.append("{% endblock %}")

    new_content = "\n".join(new_lines)

    # Write back
    filepath.write_text(new_content, encoding="utf-8")
    return True


def main():
    standalone = [
        VIEWS_DIR / "Products/index.html",
        VIEWS_DIR / "Products/detail.html",
        VIEWS_DIR / "Cart/index.html",
        VIEWS_DIR / "Auth/Login.html",
        VIEWS_DIR / "Auth/Register.html",
        VIEWS_DIR / "Auth/Profile.html",
        VIEWS_DIR / "Auth/ForgotPassword.html",
        VIEWS_DIR / "Auth/AdminLogin.html",
        VIEWS_DIR / "Chat/index.html",
        VIEWS_DIR / "Checkout/checkout.html",
        VIEWS_DIR / "Checkout/success.html",
        VIEWS_DIR / "Checkout/cancel.html",
        VIEWS_DIR / "Checkout/expired.html",
        VIEWS_DIR / "Admin/dashboard.html",
        VIEWS_DIR / "Admin/products.html",
        VIEWS_DIR / "Admin/product_edit.html",
        VIEWS_DIR / "Admin/categories.html",
        VIEWS_DIR / "Admin/orders.html",
        VIEWS_DIR / "Admin/order_detail.html",
        VIEWS_DIR / "Admin/accounts.html",
        VIEWS_DIR / "Admin/faqs.html",
        VIEWS_DIR / "Admin/chats.html",
        VIEWS_DIR / "Admin/chatbot.html",
        VIEWS_DIR / "Admin/statistics.html",
        VIEWS_DIR / "Admin/suppliers.html",
        VIEWS_DIR / "Shared/error.html",
    ]

    converted = []
    skipped = []
    errors = []

    for path in standalone:
        if not path.exists():
            skipped.append(f"{path.name} (not found)")
            continue
        try:
            if convert_to_extends(path):
                converted.append(path.name)
            else:
                skipped.append(f"{path.name} (already extends or not standalone)")
        except Exception as e:
            errors.append(f"{path.name}: {e}")

    print(f"Converted: {len(converted)}")
    for n in converted:
        print(f"  + {n}")
    if skipped:
        print(f"\nSkipped: {len(skipped)}")
        for n in skipped:
            print(f"  - {n}")
    if errors:
        print(f"\nErrors: {len(errors)}")
        for n in errors:
            print(f"  ! {n}")


if __name__ == "__main__":
    main()
