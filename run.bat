@echo off
chcp 65001 >NUL
echo [Tech Store] Starting server with UTF-8 mode...
set PYTHONIOENCODING=utf-8
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
