import gradio as gr
import requests
import threading
import time
import re
import sys
from io import StringIO
import contextlib

# Настройки Telegram бота
TELEGRAM_BOT_TOKEN = "7920656565:AAGkaRKpkXITOqMFQ-SUtgpL8f4ZBaV7Dss"  # ЗАМЕНИТЕ на реальный
TELEGRAM_CHAT_ID = "781959480"      # ЗАМЕНИТЕ на реальный

def send_telegram_message(message):
    """Отправка сообщения в Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        print(f"📤 Статус отправки: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Ошибка отправки: {e}")
        return False

def fake_rag(query):
    return f"Вы спросили: '{query}'. Хороший вопрос! RAG сервер не работает корректно. ✅"

# Глобальная переменная для хранения демо-интерфейса
demo_instance = None

def run_gradio_server():
    """Запускает Gradio сервер и возвращает публичную ссылку"""
    global demo_instance
    
    print("🔄 Создание Gradio интерфейса...")
    
    demo = gr.Interface(
        fn=fake_rag,
        inputs=gr.Textbox(
            lines=2, 
            placeholder="Введите ваш вопрос здесь...",
            label="Ваш вопрос"
        ),
        outputs=gr.Textbox(
            label="Ответ RAG системы",
            lines=4
        ),
        title="🤖 RAG Ассистент", 
        description="Сервер запущен и готов к работе!",
        examples=[
            "Что такое RAG?",
            "Как работает эта система?",
            "Расскажи о возможностях"
        ]
    )
    
    demo_instance = demo
    
    # Запускаем сервер с перехватом вывода
    print("🚀 Запуск сервера...")
    
    # Создаем буфер для перехвата вывода
    output_buffer = StringIO()
    
    with contextlib.redirect_stdout(output_buffer), contextlib.redirect_stderr(output_buffer):
        # Запускаем в отдельном потоке
        def launch_server():
            try:
                demo.launch(
                    server_name="0.0.0.0", 
                    server_port=7860, 
                    share=True,
                    show_error=True
                )
            except Exception as e:
                print(f"Ошибка запуска сервера: {e}")
        
        server_thread = threading.Thread(target=launch_server, daemon=True)
        server_thread.start()
        
        # Ждем и анализируем вывод для поиска публичной ссылки
        public_url = None
        for i in range(40):  # Ждем до 40 секунд
            time.sleep(1)
            output_text = output_buffer.getvalue()
            
            # Ищем публичную ссылку в выводе
            public_url_match = re.search(r'https://[a-f0-9]+\.gradio\.live', output_text)
            if public_url_match:
                public_url = public_url_match.group(0)
                print(f"✅ Найдена публичная ссылка: {public_url}")
                break
            
            # Также проверяем другие форматы ссылок
            if not public_url:
                public_url_match = re.search(r'Running on public URL: (https://[^\s]+)', output_text)
                if public_url_match:
                    public_url = public_url_match.group(1)
                    print(f"✅ Найдена публичная ссылка: {public_url}")
                    break
            
            print(f"⏳ Ожидание ссылки... ({i+1}/40)")
        
        return public_url

def main():
    print("=" * 60)
    print("🤖 ЗАПУСК RAG СЕРВЕРА")
    print("=" * 60)
    
    # Отправляем сообщение о начале запуска
    send_telegram_message("🔄 <b>Запуск RAG сервера...</b>\n⏳ Генерация публичной ссылки...")
    
    # Запускаем сервер и получаем публичную ссылку
    public_url = run_gradio_server()
# Отправляем результат в Telegram
    if public_url:
        message = f"🚀 <b>RAG сервер запущен и работает!</b>\n\n"
        message += f"🌐 <b>Публичная ссылка:</b>\n<code>{public_url}</code>\n\n"
        message += f"📍 <b>Локальная ссылка:</b>\nhttp://localhost:7860\n\n"
        message += f"⏰ <b>Ссылка действительна:</b> 72 часа\n"
        message += f"✅ <b>Статус:</b> Сервер активен и готов к запросам"
        
        if send_telegram_message(message):
            print(f"✅ Публичная ссылка отправлена в Telegram")
        else:
            print("❌ Не удалось отправить сообщение в Telegram")
    else:
        error_msg = "⚠️ <b>RAG сервер запущен локально</b>\n\n"
        error_msg += "📍 <b>Локальная ссылка:</b>\nhttp://localhost:7860\n\n"
        error_msg += "🌐 <b>Публичная ссылка:</b> Не сгенерирована\n\n"
        error_msg += "💡 <b>Примечание:</b> Сервер работает, но可能需要 проверить настройки сети"
        
        send_telegram_message(error_msg)
        print("⚠️ Публичная ссылка не найдена, но сервер запущен")
    
    print("\n" + "=" * 60)
    print("🎯 СЕРВЕР ЗАПУЩЕН И РАБОТАЕТ!")
    print("📍 Локальный адрес: http://localhost:7860")
    if public_url:
        print(f"🌐 Публичный адрес: {public_url}")
    print("⏹️  Для остановки нажмите Ctrl+C")
    print("=" * 60)
    
    # Бесконечный цикл чтобы сервер продолжал работать
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Остановка сервера...")
        if demo_instance and hasattr(demo_instance, 'server'):
            try:
                demo_instance.server.close()
                print("✅ Сервер остановлен")
            except:
                print("⚠️ Не удалось корректно остановить сервер")

if __name__ == "__main__":
    main()