@echo off
chcp 65001 > nul
cd /d "D:\fanuc_rag"
echo Отправка изменений на GitHub...
echo.

call rag_venv\Scripts\activate.bat

echo Текущий статус:
git status

echo.
set /p commit_msg="Введите описание изменений: "

echo.
echo Добавляем файлы...
git add .

echo Фиксируем изменения...
git commit -m "%commit_msg%"

echo Отправляем на GitHub...
git push origin main

echo.
echo Изменения успешно отправлены!
