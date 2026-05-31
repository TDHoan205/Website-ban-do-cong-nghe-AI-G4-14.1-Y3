path = r"d:\Website-ban-do-cong-nghe-AI-G4-14.1-Y3\Views\Home\index.html"
with open(path, "r", encoding="utf-8") as f:
    html = f.read()

footer_idx = html.find("</footer>")
if footer_idx != -1:
    print(html[footer_idx:footer_idx + 1000])
else:
    print("No </footer> found")
