from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__, static_folder="static")

API_URL = "https://api.together.xyz/v1/chat/completions"
API_KEY = "ТВОЙ_API_КЛЮЧ"

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    messages = data.get("messages", [])

    response = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "mistral",
            "messages": messages
        }
    )

    result = response.json()

    return jsonify({
        "answer": result["choices"][0]["message"]["content"]
    })

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
