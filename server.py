from flask import Flask, request, jsonify
import requests

app = Flask(__name__, static_folder="static")

OLLAMA_URL = "http://localhost:11434/api/generate"

def ask_ollama(prompt):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            }
        )
        return response.json().get("response", "Ошибка ответа")
    except Exception as e:
        return f"Ошибка Ollama: {e}"

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json

    messages = data.get("messages", [])
    mode = data.get("mode", "mini")

    # собираем весь диалог в один промпт
    prompt = ""
    for m in messages:
        if m["role"] == "user":
            prompt += f"User: {m['content']}\n"
        else:
            prompt += f"AI: {m['content']}\n"

    prompt += "AI:"

    if mode == "mini":
        prompt = "Отвечай коротко.\n\n" + prompt
    elif mode == "1.1":
        prompt = "Отвечай подробно и с объяснением.\n\n" + prompt

    answer = ask_ollama(prompt)

    return jsonify({
        "answer": answer
    })

if __name__ == "__main__":
    app.run(port=5000, debug=True)