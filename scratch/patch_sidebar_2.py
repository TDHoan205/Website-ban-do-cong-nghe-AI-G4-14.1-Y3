import os
import glob
import re

views_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Views", "Admin"))
files = glob.glob(os.path.join(views_dir, "*.html"))

for filepath in files:
    filename = os.path.basename(filepath)
    if filename in ["chats.html", "dashboard.html"]:
        continue
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    original = content
    
    # We want to insert the AI chatbot and Chat history links before the Xem website link in the sidebar
    pattern = r'(<a href="/".*?>\s*<i class="fas fa-globe"></i> Xem website\s*</a>)'
    replacement = r'<a href="/Chat/" target="_blank" class="sidebar-link"><i class="fas fa-robot"></i> AI Chatbot</a>\n    <a href="/Admin/Chats" class="sidebar-link"><i class="fas fa-comments"></i> Lịch sử Chat</a>\n    \1'
    
    content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Patched {filename}")
    else:
        print(f"Could not find pattern in {filename}")
