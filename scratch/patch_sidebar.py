import os
import glob

views_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Views", "Admin"))
files = glob.glob(os.path.join(views_dir, "*.html"))

target_str1 = """          <a href="/Chat/" target="_blank" class="sidebar-link">
            <i class="fas fa-robot"></i> AI Chatbot
          </a>
          <a href="/" class="sidebar-link">
            <i class="fas fa-globe"></i> Xem website
          </a>"""

target_str2 = """<a href="/Chat/" target="_blank" class="sidebar-link"><i class="fas fa-robot"></i> AI Chatbot</a>
          <a href="/" class="sidebar-link"><i class="fas fa-globe"></i> Xem website</a>"""

replace_str1 = """          <a href="/Chat/" target="_blank" class="sidebar-link">
            <i class="fas fa-robot"></i> AI Chatbot
          </a>
          <a href="/Admin/Chats" class="sidebar-link">
            <i class="fas fa-comments"></i> Lịch sử Chat
          </a>
          <a href="/" class="sidebar-link">
            <i class="fas fa-globe"></i> Xem website
          </a>"""

replace_str2 = """<a href="/Chat/" target="_blank" class="sidebar-link"><i class="fas fa-robot"></i> AI Chatbot</a>
          <a href="/Admin/Chats" class="sidebar-link"><i class="fas fa-comments"></i> Lịch sử Chat</a>
          <a href="/" class="sidebar-link"><i class="fas fa-globe"></i> Xem website</a>"""


for filepath in files:
    if os.path.basename(filepath) == "chats.html":
        continue
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    original = content
    content = content.replace(target_str1, replace_str1)
    content = content.replace(target_str2, replace_str2)
    
    # Just in case indentation varies, fallback regex:
    import re
    if content == original:
        pattern = r'(<a href="/Chat/".*?>\s*<i class="fas fa-robot"></i> AI Chatbot\s*</a>)\s*(<a href="/".*?>\s*<i class="fas fa-globe"></i> Xem website\s*</a>)'
        replacement = r'\1\n          <a href="/Admin/Chats" class="sidebar-link"><i class="fas fa-comments"></i> Lịch sử Chat</a>\n          \2'
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Patched {os.path.basename(filepath)}")
    else:
        print(f"Could not find pattern in {os.path.basename(filepath)}")
