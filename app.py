import gradio as gr
#заглушка. Возвращает запрос.
def fake_rag(query):
	return f" you ask:'{query}'. Хороший вопрос, но RAG сервер еще не создан."
# Веб-интерфейс
demo = gr.Interface(
	fn=fake_rag,
	inputs=gr.Textbox(lines=2, placeholder="Введите ваш вопрос здесь..."),
	outputs="text",
	title="RAG Ассистент",
	description="Тест веб-сервера без RAG."
)

# Запуск сервера
if __name__ =="__main__":
	demo.launch(server_name="0.0.0.0", server_port=7860, share=True)