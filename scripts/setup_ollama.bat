@echo off
chcp 65001 >nul
echo.
echo ================================================
echo    OLLAMA SETUP - AI Chatbot cho TechStore
echo ================================================
echo.

:: Kiểm tra Ollama đã cài chưa
where ollama >nul 2>&1
if %errorlevel%==0 (
    echo [OK] Ollama đã được cài đặt!
    echo.
    ollama --version
    echo.
    goto :check_models
)

:: Ollama chưa cài - hỏi người dùng
echo [INFO] Ollama chưa được cài đặt.
echo.
echo Ban co muon tai Ollama khong?
echo.
echo   1. Co, tai Ollama (Khuyen nghi - Hoan toan FREE!)
echo   2. Khong, chi kiem tra model
echo.
set /p choice="Lua chon cua ban (1/2): "

if /i "%choice%"=="1" goto :download_ollama

:check_models
echo.
echo ================================================
echo    Kiem tra Models da cai
echo ================================================
echo.
ollama list
echo.

:model_menu
echo.
echo ================================================
echo    Chon thao tac:
echo ================================================
echo.
echo   1. Cai model llama3.2 (2GB) - Khuyen nghi!
echo   2. Cai model qwen2.5:3b (2GB)
echo   3. Cai model deepseek-r1:1.5b (1.5GB)
echo   4. Cai tat ca model tren
echo   5. Kiem tra Ollama server
echo   6. Thoat
echo.
set /p model_choice="Lua chon cua ban (1-6): "

if "%model_choice%"=="1" goto :pull_llama
if /i "%model_choice%"=="2" goto :pull_qwen
if /i "%model_choice%"=="3" goto :pull_deepseek
if /i "%model_choice%"=="4" goto :pull_all
if /i "%model_choice%"=="5" goto :check_server
if /i "%model_choice%"=="6" goto :end

echo Lua chon khong hop le!
goto :model_menu

:pull_llama
echo.
echo Dang tai model llama3.2...
echo.
ollama pull llama3.2
echo.
echo [OK] Da tai xong model llama3.2!
goto :model_menu

:pull_qwen
echo.
echo Dang tai model qwen2.5:3b...
echo.
ollama pull qwen2.5:3b
echo.
echo [OK] Da tai xong model qwen2.5:3b!
goto :model_menu

:pull_deepseek
echo.
echo Dang tai model deepseek-r1:1.5b...
echo.
ollama pull deepseek-r1:1.5b
echo.
echo [OK] Da tai xong model deepseek-r1:1.5b!
goto :model_menu

:pull_all
echo.
echo Dang tai tat ca model...
echo.
echo [1/3] Tai llama3.2...
ollama pull llama3.2
echo.
echo [2/3] Tai qwen2.5:3b...
ollama pull qwen2.5:3b
echo.
echo [3/3] Tai deepseek-r1:1.5b...
ollama pull deepseek-r1:1.5b
echo.
echo [OK] Da tai xong tat ca model!
goto :model_menu

:check_server
echo.
echo Kiem tra Ollama server...
echo.
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel%==0 (
    echo [OK] Ollama server dang chay tai http://localhost:11434
    echo.
    echo Models available:
    curl -s http://localhost:11434/api/tags | findstr /i "name"
) else (
    echo [WARN] Ollama server chua chay!
    echo.
    echo De khoi dong Ollama server, chay:
    echo   ollama serve
    echo.
    echo Hoac khoi dong app Ollama tu Start Menu.
)
goto :model_menu

:download_ollama
echo.
echo ================================================
echo    Tai Ollama...
echo ================================================
echo.
echo Vui long tai Ollama tu: https://ollama.com/download
echo.
echo Sau khi tai xong, chay lai script nay!
echo.
echo Nhan phim bat ky de mo trinh duyet...
start https://ollama.com/download
pause >nul
goto :end

:end
echo.
echo ================================================
echo    Hoan tat!
echo ================================================
echo.
echo De su dung Ollama:
echo.
echo   1. Khoi dong Ollama server:
echo      ollama serve
echo.
echo   2. Hoac chay app Ollama tu Start Menu
echo.
echo De kiem tra server:
echo   curl http://localhost:11434/api/tags
echo.
echo De chat thu:
echo   ollama run llama3.2
echo.
echo ================================================
echo.
pause
