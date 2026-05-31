path = r"d:\Website-ban-do-cong-nghe-AI-G4-14.1-Y3\Views\Home\index.html"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "danh mục sản phẩm" in line.lower() or "categories" in line.lower():
        print(f"Line {i+1}: {line.strip()}")
