@echo off
chcp 65001 >nul
echo ================================================
echo   TechShop Admin - Cai dat va Chay
echo ================================================
echo.

REM Di chuyen vao thu muc project
cd /d "%~dp0"

echo [1/5] Kiem tra Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo LOI: Khong tim thay Python. Vui long cai Python 3.9+
    pause
    exit /b 1
)

echo [2/5] Cai dat thu vien...
pip install Django>=4.2 django-crispy-forms django-filter pyodbc >nul 2>&1
if errorlevel 1 (
    echo LOI: Khong the cai dat thu vien.
    pause
    exit /b 1
)
echo   Da cai dat xong!

echo [3/5] Tao Migration...
python manage.py makemigrations >nul 2>&1
echo   Da tao migrations!

echo [4/5] Chay Migration...
python manage.py migrate
echo   Da chay migrate!

echo [5/5] Tao tai khoan Admin...
python manage.py shell -c "from apps.users.models import Account; Account.objects.filter(username='admin').exists() or Account.objects.create_superuser('admin', 'admin123', email='admin@techshop.vn')"
echo   Tai khoan admin da tao!

echo.
echo ================================================
echo   Hoan tat! Chay server...
echo ================================================
echo.
echo Truy cap: http://127.0.0.1:8000/accounts/login/
echo Tai khoan: admin
echo Mat khau:  admin123
echo.
echo Nhan phim bat ky de chay server...
pause >nul

python manage.py runserver
