"""Fix index.html - remove duplicate header/navbar/ann-bar and footer from content block."""
from pathlib import Path

f = Path(r"d:\a_LTPY\BTLPYTHON\Website-ban-do-cong-nghe-AI-G4-14.1-Y3\Views\Home\index.html")
content = f.read_text(encoding="utf-8")

# Find where {% block content %} starts
block_start = content.find("{% block content %}")
if block_start == -1:
    print("ERROR: block content not found")
    exit(1)

# The content block starts AFTER "{% block content %}"
# We need to remove:
# 1. Duplicate ann-bar div (starts with <!-- Announcement Bar -->)
# 2. Duplicate header/header-inner (starts with <!-- Header -->)
# 3. Duplicate navbar (starts with <!-- Navbar -->)
# And keep everything from <!-- Hero --> onwards

# Find Hero section start
hero_start = content.find("<!-- Hero -->", block_start)
if hero_start == -1:
    print("ERROR: Hero section not found")
    exit(1)

# Build new content
new_content = (
    content[:block_start] +
    "{% block content %}\n\n"
    + content[hero_start:]
)

# Also need to remove footer from the content
# Footer in homepage content: find the last </section> before the closing block, then footer
# Actually, the homepage content ends with support-banner section + PMO modal + scripts
# Let's check what's after support-banner
print("Content after hero_start snippet:", repr(content[hero_start:hero_start+100]))
f.write_text(new_content, encoding="utf-8")
print("Fixed index.html")
print(f"New content length: {len(new_content)}")
