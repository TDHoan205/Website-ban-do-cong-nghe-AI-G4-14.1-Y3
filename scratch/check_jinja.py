import os
from jinja2 import Environment, FileSystemLoader

def check_templates():
    env = Environment(loader=FileSystemLoader('.'))
    for root, dirs, files in os.walk('.'):
        if '.venv' in root or '.git' in root or 'node_modules' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                path = os.path.join(root, file)
                rel_path = os.path.relpath(path, '.')
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        source = f.read()
                    env.parse(source)
                    # print(f"OK: {rel_path}")
                except Exception as e:
                    line = getattr(e, 'lineno', 'unknown')
                    print(f"ERROR: {rel_path} (Line {line}) - {e}")

if __name__ == "__main__":
    check_templates()
