import re

def fix_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern 1: category_id
    pattern1 = r'\{%\s+if\s+category_id\s+\|\s+string=""\s+="cat\.category_id"\s+\|\s+string\s+%\}(selected)\{%\s+endif\s+%\}'
    content = re.sub(pattern1, r'{% if category_id|string == cat.category_id|string %}selected{% endif %}', content, flags=re.MULTILINE)
    
    # Pattern 2: sort_by (generic)
    # This matches the broken multi-line if blocks
    pattern2 = r'\{%\s+if\s+sort_by=""\s+="([^"]+)"\s+%\}(selected)\{%\s+endif\s+%\}'
    content = re.sub(pattern2, r'{% if sort_by == "\1" %}selected{% endif %}', content, flags=re.MULTILINE)

    # Pattern 3: another variation of broken category_id (just in case)
    pattern3 = r'\{%\s+if\s+category_id\s+\|\s+string\s+==\s+cat\.category_id\s+\|\s+string\s+%\}(selected)\{%\s+endif\s+%\}'
    # This one might be OK, but let's make sure it's consistent

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed {path}")

def fix_all():
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.html'):
                fix_file(os.path.join(root, file))

if __name__ == "__main__":
    import os
    fix_all()
