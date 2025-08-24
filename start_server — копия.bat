@echo off
chcp 65001 > nul
cd /d "D:\fanuc_rag"

echo 🚀 Сервер запущен. Ожидание изменений...
echo 📍 Для перезагрузки сделайте: git push на ПК разработчика

:main_loop
call rag_venv\Scripts\activate.bat

# Ждем изменения в GitHub
git fetch origin
git status -uno | findstr "behind" > nul
if not errorlevel 1 (
    echo 🔄 Обновление обнаружено! Перезагрузка...
    git pull origin main
    pip install -r requirements.txt
    taskkill /f /im python.exe > nul 2>&1
    timeout /t 2 /nobreak > nul
    python app.py
)

timeout /t 10 /nobreak > nul
goto main_loop
